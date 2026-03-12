"""
BETO_STATE extractor — best-effort extraction from BETO artifacts.

Rules:
- Never raises. All functions return empty values on failure.
- All failures are logged to `warnings` list passed by caller.
- Regex patterns derived from real artifact samples (cycles/*/), not templates.
- Two format variants handled where observed in real cycles.
"""

from __future__ import annotations
import re
import json
from pathlib import Path

from .schema import BETOState, NodoBETO, OQ


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _section_content(content: str, section_num: int) -> str:
    """
    Extrae el contenido de la sección N de un BETO_CORE.
    Formato real: '## N. TITLE' o '## SECCIÓN N' o '## N. TITLE\n'
    Retorna texto hasta la siguiente sección numerada o fin de documento.
    """
    # Patron flexible: ## seguido de N. o SECCIÓN N
    pattern = re.compile(
        rf"^##\s+(?:SECCIÓN\s+)?{section_num}[.\s]",
        re.MULTILINE | re.IGNORECASE,
    )
    m = pattern.search(content)
    if not m:
        return ""

    start = m.end()
    # Buscar siguiente ## con número
    next_sec = re.search(r"^##\s+(?:SECCIÓN\s+)?\d+[.\s]", content[start:], re.MULTILINE | re.IGNORECASE)
    end = start + next_sec.start() if next_sec else len(content)
    return content[start:end].strip()


def _extract_bullet_list(text: str) -> list[str]:
    """
    Extrae items de listas markdown: '- text', '* text', '• text'.
    Retorna lista de strings limpios.
    """
    items = []
    for line in text.split("\n"):
        m = re.match(r"^[-*•]\s+(.+)", line.strip())
        if m:
            items.append(m.group(1).strip())
    return items


def _extract_checked_items(text: str) -> list[str]:
    """Extrae items con ✅ o checkbox marcado."""
    items = []
    for line in text.split("\n"):
        if "✅" in line or "[x]" in line.lower():
            clean = re.sub(r"✅|\[x\]", "", line, flags=re.IGNORECASE).strip("- |").strip()
            if clean:
                items.append(clean)
    return items


# ---------------------------------------------------------------------------
# BETO_CORE_DRAFT extractor
# ---------------------------------------------------------------------------

def _unwrap_beto_core_content(content: str) -> str:
    """
    Algunos BETO_CORE_DRAFT se generan envueltos en JSON (formato Paso 0/1):
      BEGIN_JSON { ... "beto_core_updated": "# BETO CORE CONTEXT\n..." } END_JSON
    Esta función extrae el markdown real del campo beto_core_updated si existe.
    Retorna el contenido original si no tiene ese wrapper.
    """
    if not content.strip().startswith("BEGIN_JSON"):
        return content
    try:
        json_str = re.search(r"BEGIN_JSON\s*([\s\S]+?)\s*END_JSON", content)
        if not json_str:
            return content
        data = json.loads(json_str.group(1))
        core_md = data.get("beto_core_updated", "")
        if core_md:
            return core_md
    except Exception:
        pass
    return content


def extract_from_beto_core_draft(content: str, warnings: list[str]) -> dict:
    """
    Extrae: system_intent, system_boundaries, stable_decisions, oqs.
    Formato real observado: secciones '## N. TITLE'.
    Maneja también el formato BEGIN_JSON/END_JSON (Paso 0/1).
    """
    content = _unwrap_beto_core_content(content)
    result = {
        "system_name": "",
        "system_intent": "",
        "system_boundaries_in": [],
        "system_boundaries_out": [],
        "stable_decisions": [],
        "oqs_abiertas": [],
        "oqs_cerradas": [],
    }

    # System name: primera línea del header o título del documento
    m = re.search(r"^#\s+.+?[—–-]\s*(.+)$", content, re.MULTILINE)
    if m:
        result["system_name"] = m.group(1).strip()
    else:
        m = re.search(r"Sistema[:\s]+(.+)", content[:500])
        if m:
            result["system_name"] = m.group(1).strip()[:80]

    # Sección 1 — SYSTEM INTENT
    sec1 = _section_content(content, 1)
    if sec1:
        result["system_intent"] = sec1[:600]
    else:
        warnings.append("BETO_CORE_DRAFT: no se extrajo SYSTEM INTENT (sección 1)")

    # Sección 2 — SYSTEM BOUNDARIES
    sec2 = _section_content(content, 2)
    if sec2:
        # Separar In scope / Out of scope
        in_m = re.search(r"(?:In scope|Dentro del alcance|In-Scope)[:\s]*\n([\s\S]+?)(?:Out|Fuera|\Z)", sec2, re.IGNORECASE)
        out_m = re.search(r"(?:Out of scope|Fuera del alcance|Out-of-Scope)[:\s]*\n([\s\S]+?)(?:\Z|##)", sec2, re.IGNORECASE)

        if in_m:
            result["system_boundaries_in"] = _extract_bullet_list(in_m.group(1))
            # También captura líneas con ✅
            if not result["system_boundaries_in"]:
                result["system_boundaries_in"] = _extract_checked_items(in_m.group(1))
        if out_m:
            result["system_boundaries_out"] = _extract_bullet_list(out_m.group(1))
            if not result["system_boundaries_out"]:
                result["system_boundaries_out"] = _extract_checked_items(out_m.group(1))

        if not result["system_boundaries_in"] and not result["system_boundaries_out"]:
            warnings.append("BETO_CORE_DRAFT: boundaries extraídos como texto libre (formato no estándar)")
    else:
        warnings.append("BETO_CORE_DRAFT: no se extrajo SYSTEM BOUNDARIES (sección 2)")

    # Sección 8 — STABLE TECHNICAL DECISIONS
    sec8 = _section_content(content, 8)
    if sec8:
        decisions = []
        for line in sec8.split("\n"):
            # Formato: '- **Decisión** (Confirmed): texto'
            m = re.match(r"^-\s+\*\*(.+?)\*\*.*?:\s*(.+)", line.strip())
            if m:
                decisions.append(f"{m.group(1)}: {m.group(2).strip()}")
            elif re.match(r"^-\s+.{10,}", line.strip()):
                decisions.append(line.strip()[2:])
        result["stable_decisions"] = decisions[:15]  # tope razonable
    else:
        warnings.append("BETO_CORE_DRAFT: no se extrajo STABLE TECHNICAL DECISIONS (sección 8)")

    # OQs — tres fuentes:
    # Fuente A: cuerpo del documento "> **OQ-N**: texto"
    oqs_body: dict[str, str] = {}
    for m in re.finditer(r">\s*\*\*(OQ-[\w\-]+)\*\*\s*[:\-]\s*(.+?)(?:\n|$)", content):
        oqs_body[m.group(1)] = m.group(2).strip()

    # Fuente B: sección 9/10 "- OQ-N (topic): CLOSED/OPEN — mode. text" (formato compacto)
    oqs_sec9: dict[str, dict] = {}
    sec9 = _section_content(content, 9) or _section_content(content, 10)
    if sec9:
        for m in re.finditer(
            r"-\s+(OQ-[\w\-]+)\s*(?:\([^)]*\))?:\s*(CLOSED|OPEN|CERRADA|ABIERTA)\s*[—–-]?\s*([\w_]*)\.?\s*(.*)",
            sec9, re.IGNORECASE
        ):
            oqs_sec9[m.group(1)] = {
                "estado": m.group(2).upper(),
                "modo": m.group(3),
                "resolucion": m.group(4).strip(),
            }

        # Fuente C: sección 9 formato detallado "- **OQ-N**: texto\n  status: OPEN/CLOSED"
        # Captura OQs que Fuente B no detectó (status en línea separada)
        for m in re.finditer(
            r"-\s+\*\*(OQ-[\w\-]+)\*\*\s*[:\-]\s*([^\n]+)",
            sec9
        ):
            oq_id = m.group(1)
            if oq_id not in oqs_sec9:
                texto = m.group(2).strip()
                # Buscar status en las líneas siguientes (hasta 8 líneas)
                after = sec9[m.end():]
                estado_m = re.search(r"status:\s*(OPEN|CLOSED|CERRADA|ABIERTA)", after[:300], re.IGNORECASE)
                estado = estado_m.group(1).upper() if estado_m else "OPEN"
                res_m = re.search(r"resolution:\s*(.+)", after[:300])
                resolucion = res_m.group(1).strip() if res_m and res_m.group(1).strip() else ""
                oqs_sec9[oq_id] = {"estado": estado, "modo": "", "resolucion": resolucion}
                if oq_id not in oqs_body:
                    oqs_body[oq_id] = texto

    # Consolidar: cerradas si aparecen en sec9 como CLOSED
    all_oq_ids = set(oqs_body.keys()) | set(oqs_sec9.keys())
    for oq_id in sorted(all_oq_ids):
        texto = oqs_body.get(oq_id, "")
        sec9_data = oqs_sec9.get(oq_id, {})
        estado = sec9_data.get("estado", "OPEN")

        if "CLOSED" in estado or "CERRADA" in estado:
            result["oqs_cerradas"].append(OQ(
                id=oq_id,
                texto=texto,
                modo_cierre=sec9_data.get("modo", ""),
                resolucion=sec9_data.get("resolucion", ""),
            ))
        else:
            result["oqs_abiertas"].append(OQ(id=oq_id, texto=texto))

    return result


# ---------------------------------------------------------------------------
# BETO_SYSTEM_GRAPH extractor
# ---------------------------------------------------------------------------

def extract_from_beto_system_graph(content: str, warnings: list[str]) -> dict:
    """
    Extrae: system_name, nodos (id, tipo, beto_core).
    Formato real: 'System name: X' y bloques con '- Node ID: / Node type: / Associated BETO_CORE target:'
    """
    result = {
        "system_name": "",
        "nodos": [],
    }

    # System name
    m = re.search(r"System name:\s*(.+)", content)
    if m:
        result["system_name"] = m.group(1).strip()
    else:
        warnings.append("BETO_SYSTEM_GRAPH: no se encontró 'System name:'")

    # Nodos — formato observado:
    # '- Node ID:          X'
    # '  Node type:        Y'
    # '  Associated BETO_CORE target: Z'
    # También puede aparecer sin guión al inicio (formato alternativo)
    node_blocks = re.split(r"(?=(?:^|\n)\s*-?\s*Node ID:)", content)
    for block in node_blocks:
        id_m = re.search(r"Node ID:\s*(.+)", block)
        tipo_m = re.search(r"Node type:\s*(.+)", block)
        core_m = re.search(r"Associated BETO_CORE target:\s*(\S+)", block)

        if not id_m:
            continue

        node_id = id_m.group(1).strip()
        node_tipo = tipo_m.group(1).strip() if tipo_m else "UNKNOWN"
        node_core_raw = core_m.group(1).strip() if core_m else ""

        # Limpiar el beto_core: quitar paréntesis y sufijos como (not_generated_yet)
        node_core = re.sub(r"\s*\([^)]*\)", "", node_core_raw).strip()
        if node_core and not node_core.endswith(".md"):
            node_core += ".md"
        # Si el target es not_generated_yet u otro placeholder, dejarlo vacío
        if node_core.lower().startswith("not_generated"):
            node_core = ""

        # Filtrar nodos INTERNAL y SHARED CONCERN (no tienen BETO_CORE propio)
        if node_tipo.upper() in ("INTERNAL", "SHARED_CONCERN", "SHARED CONCERN", "UNKNOWN"):
            continue

        result["nodos"].append(NodoBETO(
            id=node_id,
            tipo=node_tipo.upper(),
            beto_core=node_core,
        ))

    # Deduplicar por node_id — el grafo a veces declara el mismo nodo en tabla y en lista
    seen_ids: set[str] = set()
    deduped = []
    for n in result["nodos"]:
        if n.id not in seen_ids:
            seen_ids.add(n.id)
            deduped.append(n)
    result["nodos"] = deduped

    if not result["nodos"]:
        warnings.append("BETO_SYSTEM_GRAPH: no se extrajeron nodos")

    return result


# ---------------------------------------------------------------------------
# CIERRE_ASISTIDO extractor
# ---------------------------------------------------------------------------

def extract_from_cierre_asistido(content: str, warnings: list[str]) -> dict:
    """
    Extrae OQs cerradas con su modo y resolución.
    Fuente primaria: tabla resumen | OQ-id | ... | ✅ CERRADA |
    Fuente secundaria: secciones detalle '### OQ-N — topic'
    """
    result: dict[str, OQ] = {}

    # Tabla resumen: | OQ-id | BETO_CORE | topic | status | ✅ |
    for m in re.finditer(
        r"\|\s*(OQ-[\w\-]+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*(✅[^|]*)\|",
        content
    ):
        oq_id = m.group(1).strip()
        topic = m.group(3).strip()
        result[oq_id] = OQ(id=oq_id, texto=topic, modo_cierre="BETO_ASSISTED", resolucion="")

    # Secciones detalle: '### OQ-N — topic' seguido de resolución
    for m in re.finditer(
        r"###\s+(OQ-[\w\-]+)\s*[—–-]\s*([^\n]+)\n([\s\S]+?)(?=###\s+OQ-|##\s+|\Z)",
        content
    ):
        oq_id = m.group(1).strip()
        topic = m.group(2).strip()
        body = m.group(3)

        # Extraer modo de cierre del cuerpo
        modo_m = re.search(r"\*\*(BETO_ASSISTED|HUMAN|OPERATOR)[_\s]?\w*\*\*", body, re.IGNORECASE)
        modo = modo_m.group(1).upper() if modo_m else "BETO_ASSISTED"

        # Extraer resolución: primera línea no vacía después del header
        res_lines = [l.strip() for l in body.split("\n") if l.strip() and not l.strip().startswith("#")]
        resolucion = res_lines[0][:150] if res_lines else ""

        if oq_id in result:
            result[oq_id].modo_cierre = modo
            result[oq_id].resolucion = resolucion
        else:
            result[oq_id] = OQ(id=oq_id, texto=topic, modo_cierre=modo, resolucion=resolucion)

    if not result:
        warnings.append("CIERRE_ASISTIDO: no se extrajeron OQs cerradas")

    return {"oqs_cerradas_cierre": list(result.values())}


# ---------------------------------------------------------------------------
# State JSON extractor (Gestor de Ciclo)
# ---------------------------------------------------------------------------

def extract_from_state_json(json_content: str, warnings: list[str]) -> dict:
    """
    Extrae decisiones de gate y gaps activos desde el JSON del Gestor de Ciclo.
    """
    result = {
        "decisiones_gate": [],
        "gaps_activos": [],
    }

    try:
        state = json.loads(json_content)
    except json.JSONDecodeError as e:
        warnings.append(f"state.json: error de parseo — {e}")
        return result

    result["decisiones_gate"] = state.get("decisiones_gate", [])
    result["gaps_activos"] = [
        g for g in state.get("beto_gaps", [])
        if g.get("estado", "").upper() == "PENDIENTE"
    ]

    return result


# ---------------------------------------------------------------------------
# Nodo intent extractor (para enriquecer nodos con intent de sus BETO_COREs)
# ---------------------------------------------------------------------------

def extract_node_intent(core_content: str) -> str:
    """
    Extrae el SYSTEM INTENT de un BETO_CORE hijo (máx 200 chars).
    Best-effort — retorna "" si no encuentra.
    """
    sec1 = _section_content(core_content, 1)
    if sec1:
        # Primera línea no vacía del cuerpo
        for line in sec1.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                return line[:200]
    return ""

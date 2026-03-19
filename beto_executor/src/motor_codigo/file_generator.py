"""
BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.CODE_GENERATION
BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.FILE_GENERATOR
BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.CONTEXT_PER_FILE
BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE
BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.CONTEXT_PER_FILE
"""

from openai import OpenAI

from .plan_builder import EntradaPlan
from .trace_verifier import extraer_ids_autorizados_de_registry


def _split_by_top_comma(s: str) -> list[str]:
    """Split string by comma, respecting parentheses/brackets depth."""
    parts, depth, buf = [], 0, []
    for ch in s:
        if ch in "([{":
            depth += 1
            buf.append(ch)
        elif ch in ")]}":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            if p := "".join(buf).strip():
                parts.append(p)
            buf = []
        else:
            buf.append(ch)
    if p := "".join(buf).strip():
        parts.append(p)
    return parts


def _build_stubs_from_symbols(stub_symbols: str) -> list[str]:
    """
    Parse stub_symbols and emit Python stub lines.

    Handles patterns separated by ";":
      funcs: f1(args), f2(args)
      class X: m1(args), m2(args)
      @dataclass class X: field1, field2
      class X(Exception)
    """
    import re

    lines = []
    for section in [s.strip() for s in stub_symbols.split(";") if s.strip()]:
        if section.startswith("import:"):
            # Cross-module import contract — emitted as a real Python import statement
            imp = section[7:].strip()
            if imp:
                lines.append(imp)
                lines.append("")
        elif section.startswith("funcs:"):
            fn_str = section[6:].strip()
            for raw in _split_by_top_comma(fn_str):
                sig = raw.strip()
                if not sig:
                    continue
                # If descriptive text (contains "—"), extract the signature before it
                # and stop processing further items in this comma-split (rest is prose)
                is_descriptive = "\u2014" in sig
                if is_descriptive:
                    sig = sig.split("\u2014")[0].strip()
                if not sig:
                    break
                if "(" not in sig:
                    sig = sig + "()"
                lines += [f"def {sig}:", "    pass", ""]
                if is_descriptive:
                    break
        elif re.search(r"(?:^|\s)class\s", section):
            # Use regex to find standalone "class" (not inside @dataclass)
            m = re.search(r"(?:^|(?<=\s))class\s", section)
            class_pos = m.start() if m else 0
            prefix = section[:class_pos].strip()  # e.g. "@dataclass"
            rest = section[class_pos:].strip()
            colon_idx = rest.find(":")
            if colon_idx == -1:
                # class X(Base) with no methods listed
                if prefix:
                    lines.append(prefix)
                lines += [f"{rest}:", "    pass", ""]
            else:
                class_decl = rest[:colon_idx].strip()
                members_str = rest[colon_idx + 1:].strip()
                if prefix:
                    lines.append(prefix)
                lines.append(f"{class_decl}:")
                if members_str:
                    for raw in _split_by_top_comma(members_str):
                        m2 = raw.strip()
                        if not m2:
                            continue
                        if "(" in m2:
                            lines += [f"    def {m2}:", "        pass", ""]
                        else:
                            # dataclass field — emit as comment hint
                            lines.append(f"    # field: {m2}")
                    lines.append("")
                else:
                    lines += ["    pass", ""]
    return lines


def _strip_code_fences(text: str) -> str:
    """Elimina markdown code fences que el LLM puede incluir.

    Robusto ante texto explicativo posterior al bloque de código:
    si el output empieza con una fence, extrae solo hasta el primer cierre.
    """
    text = text.strip()
    if not text.startswith("```"):
        return text
    # Saltar la primera línea (```python o similar)
    first_newline = text.index("\n") if "\n" in text else len(text)
    content_start = first_newline + 1
    # Truncar en el primer cierre de fence — descarta texto explicativo posterior
    close_pos = text.find("\n```", content_start)
    if close_pos != -1:
        return text[content_start:close_pos].strip()
    return text[content_start:].strip()


SYSTEM_PROMPT_IMPLEMENTACION = """
Eres un motor de generación de código Python.
Recibirás un SCAFFOLD que es un stub Python con la estructura del módulo ya declarada.

Tu tarea es implementar el módulo COMPLETO: rellena los cuerpos de clases y funciones.

REGLAS DURAS — SE VERIFICAN AUTOMÁTICAMENTE DESPUÉS:

BETO-TRACE — FORMATO Y DISTRIBUCIÓN:
- El scaffold ya tiene las anotaciones `BETO-TRACE: ID` en el docstring del MÓDULO.
- Conserva EXACTAMENTE esas líneas en el docstring del módulo del output.
- El formato es `BETO-TRACE: ID` — NO `#ID: ID`, NO `# BETO-TRACE: ID`.
- Las anotaciones BETO-TRACE van SOLO dentro de docstrings (triple comillas).
  NUNCA como líneas de código sueltas fuera de un docstring.
- En docstrings de CLASES y MÉTODOS: NO copies los IDs del módulo.
  Si quieres anotar una clase o método, usa SOLO 0-2 IDs directamente relevantes.
  La mayoría de clases y métodos no necesitan anotación propia.

ESTRUCTURA — NO MODIFICAR:
- Conserva los nombres de clases y funciones exactamente como aparecen en el scaffold.
- Conserva las firmas de métodos (parámetros y tipos) exactamente como están.
- Añade imports necesarios al inicio del archivo.
- Implementa la lógica real de cada función/método.

LO QUE NO DEBES HACER:
- No renombrar clases ni funciones del scaffold.
- No añadir BETO-TRACE IDs que no estén en el scaffold.
- No copiar los comentarios `# stub:` o `# NODO:` del scaffold al output.
- No incluir texto explicativo, markdown ni bloques de código después del módulo.

Genera SOLO el contenido del archivo Python. Sin explicaciones. Sin markdown.
"""


def _seleccionar_ids_para_archivo(nombre_archivo: str, all_ids: set, max_ids: int = 12) -> list[str]:
    """
    Selecciona los IDs más relevantes del TRACE_REGISTRY para un archivo específico.
    Estrategia: tokens del nombre del archivo → match parcial contra la parte ELEMENTO del ID.
    Complementa con IDs de INTENT (SEC1) si hay pocos matches. Cap: max_ids.
    """
    import re

    # Tokens del nombre del archivo (sin extensión, sin path)
    base = re.sub(r"\.\w+$", "", nombre_archivo.split("/")[-1])
    tokens = [t.upper() for t in re.split(r"[_\-]", base) if len(t) > 2]

    scored: list[tuple[int, str]] = []
    for id_ in all_ids:
        parts = id_.split(".")
        elemento = parts[-1] if len(parts) >= 4 else ""
        seccion = parts[1] if len(parts) >= 2 else ""

        score = 0
        # Tokens del archivo que aparecen en el ELEMENTO o SECCIÓN del ID
        for tok in tokens:
            if tok in elemento or tok in seccion:
                score += 2
        # Bonus: IDs de INTENT (SEC1) — siempre útiles
        if "SEC1" in id_:
            score += 1
        # Bonus: IDs de MODEL/PHASE (SEC6, SEC7) — más específicos
        if "SEC6" in id_ or "SEC7" in id_:
            score += 1

        scored.append((score, id_))

    # Ordenar: mayor score primero, luego alfabético
    scored.sort(key=lambda x: (-x[0], x[1]))

    # Tomar los mejores max_ids, pero siempre incluir al menos 1 INTENT si hay
    selected = [id_ for _, id_ in scored[:max_ids]]
    if not any("SEC1" in id_ for id_ in selected):
        intent_ids = [id_ for _, id_ in scored if "SEC1" in id_]
        if intent_ids:
            selected = intent_ids[:2] + selected[:max_ids - 2]

    return sorted(selected)


class FileGenerator:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.FILE_GENERATOR
    BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE

    Genera un archivo de código en dos etapas:
    1. Sistema construye scaffold con BETO-TRACE desde el TRACE_REGISTRY (sin LLM)
    2. Motor de código implementa el módulo completo a partir del scaffold
    """

    def __init__(self, code_client: OpenAI, code_model: str):
        # BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE
        # BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.CODE_MODEL_CONFIGURABLE
        self.code_client = code_client
        self.code_model = code_model

    def generar(
        self,
        entrada: EntradaPlan,
        idea_raw: str,
        beto_core_contenido: str,
        trace_registry_contenido: str,
    ) -> tuple[str, str]:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.CONTEXT_PER_FILE
        BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.CONTEXT_PER_FILE

        Genera el archivo en dos pasos.
        Retorna (scaffold, codigo_final).
        """
        scaffold = self._build_scaffold_from_manifest(entrada, trace_registry_contenido)
        codigo_final = self._implementar_scaffold(
            entrada, scaffold, idea_raw, beto_core_contenido, trace_registry_contenido
        )
        return scaffold, codigo_final

    def _build_scaffold_from_manifest(
        self,
        entrada: EntradaPlan,
        trace_registry_contenido: str,
    ) -> str:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.FILE_GENERATOR

        Construye el scaffold como un stub Python real:
        - Docstring de módulo con los primary_ids en formato BETO-TRACE: correcto
        - Comentario con stub_symbols para guiar la estructura al LLM
        - El LLM implementa los cuerpos conservando los BETO-TRACE del docstring
        """
        ids = entrada.primary_ids if entrada.primary_ids else _seleccionar_ids_para_archivo(
            entrada.nombre_archivo,
            extraer_ids_autorizados_de_registry(trace_registry_contenido),
        )

        lines = ['"""']
        for trace_id in ids:
            lines.append(f"BETO-TRACE: {trace_id}")
        lines.append('"""')
        lines.append("")

        if entrada.stub_symbols:
            stub_lines = _build_stubs_from_symbols(entrada.stub_symbols)
            lines.extend(stub_lines)
        else:
            lines.append(f"# NODO: {entrada.nodo}")
            lines.append("# IMPLEMENT: conservar BETO-TRACE del docstring; implementar lógica real.")
            lines.append("")
            lines.append("pass  # IMPLEMENT")

        return "\n".join(lines)

    def _implementar_scaffold(
        self,
        entrada: EntradaPlan,
        scaffold: str,
        idea_raw: str,
        beto_core_contenido: str,
        trace_registry_contenido: str,
    ) -> str:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.FILE_GENERATOR

        Motor de código genera la implementación completa del módulo
        a partir del scaffold con BETO-TRACE y el contexto del BETO_CORE.
        """
        prompt = (
            f"=== CONTEXTO (referencia — no copiar al output) ===\n\n"
            f"IDEA_RAW:\n{idea_raw}\n\n"
            f"BETO_CORE ({entrada.beto_core_origen}):\n{beto_core_contenido}\n\n"
            f"=== SCAFFOLD A IMPLEMENTAR ===\n\n"
            f"Archivo: {entrada.nombre_archivo}\n\n"
            f"{scaffold}\n\n"
            f"=== INSTRUCCIÓN ===\n\n"
            f"Implementa el módulo Python completo '{entrada.nombre_archivo}'.\n"
            f"- Conserva EXACTAMENTE todas las líneas `BETO-TRACE: X` del docstring del MÓDULO.\n"
            f"- Formato obligatorio: `BETO-TRACE: X` (no `#ID: X`).\n"
            f"- Los BETO-TRACE van SOLO en docstrings. NUNCA como código suelto.\n"
            f"- NO copies los BETO-TRACE del módulo a los docstrings de clases ni métodos.\n"
            f"- Conserva nombres de clases y firmas de métodos del scaffold.\n"
            f"- NO copies los comentarios `# NODO:`, `# stub:`, `# IMPLEMENT:`, `# field:` al output.\n"
            f"- Genera SOLO código Python. Sin explicaciones. Sin markdown."
        )

        # BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE
        response = self.code_client.chat.completions.create(
            model=self.code_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_IMPLEMENTACION},
                {"role": "user", "content": prompt},
            ],
            max_tokens=8192,
        )
        return _strip_code_fences(response.choices[0].message.content)

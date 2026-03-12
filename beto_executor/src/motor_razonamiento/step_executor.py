"""
BETO-TRACE: BETO_MOTOR_RAZ.SEC4.UNIT.PASO_EJECUCION
BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.STEP_SEQUENCER
BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE
BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.MODELS_CONFIGURABLE
"""

from pathlib import Path

from openai import OpenAI

from .artifact_writer import ArtifactWriter, ARTEFACTOS_POR_PASO, obtener_artefactos_paso
from .context_builder import construir_contexto

# BETO-TRACE: BETO_MOTOR_RAZ.SEC4.FIELD.PASO_ID
PROMPTS_POR_PASO: dict[int, str] = {
    0: (
        "Eres un evaluador BETO Framework v4.2. Evalúa la IDEA_RAW recibida "
        "y produce el artefacto PASO_0_EVALUACION.md con la decisión de elegibilidad "
        "(GO / GO_WITH_WARNINGS / NO_GO) y los warnings si aplica. "
        "Sigue estrictamente el formato del BETO Framework."
    ),
    1: (
        "Eres un arquitecto BETO Framework v4.2. A partir de la IDEA_RAW y la "
        "evaluación de elegibilidad, genera el BETO_CORE_DRAFT.md (Secciones 1-10). "
        "Declara todas las Open Questions (OQs) necesarias. Estado final: DRAFT. "
        "OBLIGATORIO — Sección 4 (CORE UNIT OF PROCESSING): si el sistema lee, "
        "parsea o consume artefactos con formato conocido (Markdown estructurado, "
        "JSON con schema definido, CSV, u otros formatos con estructura fija), "
        "documenta en Sección 4 el schema exacto de esos artefactos: nombres de "
        "campos, patrones estructurales y formato esperado. "
        "Usa únicamente información presente en el contexto o en la IDEA_RAW. "
        "Si el schema es desconocido o no está declarado, abre una OQ en Sección 9."
    ),
    2: (
        "Eres un entrevistador BETO Framework v4.2. Usando el BETO_CORE_DRAFT.md, "
        "genera el BETO_CORE_INTERVIEW_COMPLETED.md respondiendo las 12 secciones "
        "de la entrevista estructural. Responde basándote únicamente en la información disponible. "
        "OBLIGATORIO: SECCIÓN 12 — PASE DE CONSISTENCIA (P12.1 a P12.5) debe estar presente y "
        "completamente respondida. No puede omitirse aunque no elicite información nueva. "
        "Un artefacto sin SECCIÓN 12 está incompleto y es inválido."
    ),
    3: (
        "Eres un clasificador BETO Framework v4.2. Usando la entrevista completada, "
        "genera el STRUCTURAL_CLASSIFICATION_REGISTRY.md identificando y clasificando "
        "todos los candidatos a nodos (PARALLEL / SUBBETO). Aplica el test de independencia semántica."
    ),
    4: (
        "Eres un arquitecto de grafos BETO Framework v4.2. Usando la entrevista y el "
        "registro de clasificación, genera el BETO_SYSTEM_GRAPH.md con todos los nodos, "
        "aristas y validaciones topológicas. Estado final: VALIDATED. "
        "OBLIGATORIO: el artefacto debe incluir la Sección 14 — FINAL VALIDATION STATUS "
        "con exactamente estas líneas: 'Graph status: VALIDATED' y "
        "'Ready to generate BETO_CORE children: YES'. Sin estas líneas el artefacto está incompleto."
    ),
    5: (
        "Eres un arquitecto BETO Framework v4.2. Usando el BETO_SYSTEM_GRAPH y el BETO_CORE_DRAFT, "
        "genera el BETO_CORE hijo indicado con las 10 secciones completas. "
        "Estado final: en proceso (OQs abiertas permitidas). "
        "Genera ÚNICAMENTE el artefacto solicitado. Sin explicaciones adicionales."
    ),
    6: (
        "Eres un asistente de cierre BETO Framework v4.2. Usando todos los BETO_COREs "
        "hijos, genera el CIERRE_ASISTIDO.md cerrando todas las OQs con el modo BETO_ASSISTED "
        "donde sea derivable del SYSTEM INTENT. Actualiza todos los BETO_COREs a SUCCESS_CLOSED."
    ),
    7: (
        "Eres un generador de fases BETO Framework v4.2. Usando los BETO_COREs disponibles, "
        "genera el documento de fase indicado según el PHASE_TEMPLATE con 8 secciones: "
        "PURPOSE, INPUT CONTRACT, OUTPUT CONTRACT, PHASE RULES, VALIDATIONS, "
        "EDGE CASES, PROCESS STEPS, HANDOFF TO NEXT PHASE. "
        "Genera ÚNICAMENTE el artefacto solicitado. Sin explicaciones adicionales."
    ),
    8: (
        "Eres un generador de manifests BETO Framework v4.2. Usando el BETO_CORE correspondiente, "
        "genera el artefacto indicado: si es MANIFEST, produce el inventario completo de artefactos "
        "del nodo; si es TRACE_REGISTRY, produce el catálogo de IDs de trazabilidad autorizados "
        "con patrón SISTEMA.SEC<N>.<TIPO>.<ELEMENTO> donde SISTEMA es el nombre del nodo en mayúsculas. "
        "Genera ÚNICAMENTE el artefacto solicitado. Sin explicaciones adicionales."
    ),
    9: (
        "Eres un generador de manifests BETO Framework v4.2. Usando el BETO_SYSTEM_GRAPH "
        "y todos los MANIFESTs individuales, genera el MANIFEST_PROYECTO.md con el inventario "
        "completo del proyecto, el plan de materialización ordenado por dependencias, y el "
        "estado final del ciclo de especificación. "
        "OBLIGATORIO: en SECCIÓN 8 (Orden de Construcción), además de los BETO_COREs, "
        "lista explícitamente los archivos Python a materializar para cada nodo, "
        "usando formato backtick: `directorio/archivo.py`. "
        "Ejemplo: `evaluador_consistencia/evaluador_consistencia.py`. "
        "Sin esta lista de archivos Python el Motor de Código no puede materializar el sistema correcto."
    ),
}


class StepExecutor:
    """
    BETO-TRACE: BETO_MOTOR_RAZ.SEC4.UNIT.PASO_EJECUCION
    BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE

    Ejecuta un paso BETO via LLM OpenAI-compatible.
    """

    def __init__(
        self,
        client: OpenAI,
        model: str,
        artifact_writer: ArtifactWriter,
        templates_dir: Path | None = None,
    ):
        # BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE
        # BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.MODELS_CONFIGURABLE
        self.client = client
        self.model = model
        self.artifact_writer = artifact_writer
        self.templates_dir = templates_dir

    def ejecutar_paso(self, paso: int, idea_raw: str) -> list[str]:
        """
        BETO-TRACE: BETO_MOTOR_RAZ.SEC4.UNIT.PASO_EJECUCION
        BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.CONTEXT_PER_STEP

        Ejecuta el paso dado via LLM y escribe los artefactos generados.
        Para pasos con múltiples artefactos, hace una llamada LLM por artefacto.
        Retorna la lista de nombres de artefactos escritos.
        """
        system_prompt = PROMPTS_POR_PASO.get(paso)
        if system_prompt is None:
            raise ValueError(f"Paso {paso} no tiene prompt declarado.")

        nombres_artefactos = obtener_artefactos_paso(paso, self.artifact_writer.cycle_dir)
        escritos = []

        if len(nombres_artefactos) == 1:
            nombre = nombres_artefactos[0]
            if paso == 2:
                # Paso 2 — generación en dos llamadas para garantizar SECCIÓN 12
                contenido = self._ejecutar_paso2_split(idea_raw, system_prompt)
            elif paso == 4:
                # Paso 4 — generación en dos llamadas para garantizar SECCIÓN 14
                contenido = self._ejecutar_paso4_split(idea_raw, system_prompt)
            else:
                mensajes_usuario = construir_contexto(
                    paso, idea_raw, self.artifact_writer.cycle_dir, self.templates_dir
                )
                messages = [{"role": "system", "content": system_prompt}] + mensajes_usuario
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=16384,
                )
                contenido = response.choices[0].message.content
            self.artifact_writer.escribir(nombre, contenido)
            escritos.append(nombre)
        else:
            # Paso multi-artefacto — una llamada LLM por artefacto
            for nombre in nombres_artefactos:
                print(f"    [Paso {paso}] Generando {nombre}...")
                mensajes_usuario = construir_contexto(
                    paso, idea_raw, self.artifact_writer.cycle_dir, self.templates_dir
                )
                # Agregar instrucción específica para este artefacto
                mensajes_usuario = mensajes_usuario + [
                    {
                        "role": "user",
                        "content": f"Genera ÚNICAMENTE el artefacto: {nombre}",
                    }
                ]
                messages = [{"role": "system", "content": system_prompt}] + mensajes_usuario
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=16384,
                )
                contenido = response.choices[0].message.content
                self.artifact_writer.escribir(nombre, contenido)
                escritos.append(nombre)

        return escritos

    def _ejecutar_paso2_split(self, idea_raw: str, system_prompt: str) -> str:
        """
        BETO-TRACE: BETO_MOTOR_RAZ.SEC4.UNIT.PASO_EJECUCION

        Genera BETO_CORE_INTERVIEW_COMPLETED.md en dos llamadas para garantizar
        que SECCIÓN 12 (Pase de Consistencia) siempre se genere completa.

        Llamada 1: SECCIÓN 1-11
        Llamada 2: SECCIÓN 12 usando SECCIÓN 1-11 como contexto
        """
        mensajes_usuario = construir_contexto(
            2, idea_raw, self.artifact_writer.cycle_dir, self.templates_dir
        )

        # — Llamada 1: SECCIÓN 1 a 11 —
        messages_1 = (
            [{"role": "system", "content": system_prompt}]
            + mensajes_usuario
            + [{"role": "user", "content": (
                "Genera el BETO_CORE_INTERVIEW_COMPLETED.md con las SECCIONES 1 a 11. "
                "Detente exactamente al cerrar SECCIÓN 11. "
                "NO generes SECCIÓN 12 todavía."
            )}]
        )
        response_1 = self.client.chat.completions.create(
            model=self.model,
            messages=messages_1,
            max_tokens=16384,
        )
        contenido_s1_s11 = response_1.choices[0].message.content

        # — Llamada 2: SECCIÓN 12 —
        messages_2 = (
            [{"role": "system", "content": system_prompt}]
            + mensajes_usuario
            + [
                {"role": "assistant", "content": contenido_s1_s11},
                {"role": "user", "content": (
                    "Ahora genera ÚNICAMENTE la SECCIÓN 12 — PASE DE CONSISTENCIA "
                    "con los checks P12.1, P12.2, P12.3, P12.4 y P12.5 completos, "
                    "verificando la coherencia interna de las secciones anteriores. "
                    "Incluye el cierre de consistencia final."
                )},
            ]
        )
        response_2 = self.client.chat.completions.create(
            model=self.model,
            messages=messages_2,
            max_tokens=4096,
        )
        contenido_s12 = response_2.choices[0].message.content

        return contenido_s1_s11 + "\n\n" + contenido_s12

    def _ejecutar_paso4_split(self, idea_raw: str, system_prompt: str) -> str:
        """
        BETO-TRACE: BETO_MOTOR_RAZ.SEC4.UNIT.PASO_EJECUCION

        Genera BETO_SYSTEM_GRAPH.md en dos llamadas para garantizar que
        la Sección 14 — FINAL VALIDATION STATUS siempre se genere completa.

        Llamada 1: Secciones 1-13 (nodos, aristas, topología, changelog)
        Llamada 2: Sección 14 usando Secciones 1-13 como contexto
        """
        mensajes_usuario = construir_contexto(
            4, idea_raw, self.artifact_writer.cycle_dir, self.templates_dir
        )

        # — Llamada 1: Secciones 1 a 13 —
        messages_1 = (
            [{"role": "system", "content": system_prompt}]
            + mensajes_usuario
            + [{"role": "user", "content": (
                "Genera el BETO_SYSTEM_GRAPH.md completo con las Secciones 1 a 13 "
                "(METADATA, PURPOSE, SOURCE OF AUTHORITY, NODE TYPES, EDGE TYPES, "
                "ROOT NODE, NODE REGISTRY, EDGE REGISTRY, CLASSIFICATION TRACE, "
                "TOPOLOGY CONSTRAINTS, EXPANSION ORDER, DERIVATION CONTRACT, CHANGELOG). "
                "Detente exactamente al cerrar la Sección 13. "
                "NO generes la Sección 14 todavía."
            )}]
        )
        response_1 = self.client.chat.completions.create(
            model=self.model,
            messages=messages_1,
            max_tokens=16384,
        )
        contenido_s1_s13 = response_1.choices[0].message.content

        # — Llamada 2: Sección 14 —
        # Verificar que no esté ya presente (por si el LLM la incluyó igual)
        if "Graph status: VALIDATED" in contenido_s1_s13 and "Ready to generate BETO_CORE children" in contenido_s1_s13:
            return contenido_s1_s13

        messages_2 = (
            [{"role": "system", "content": system_prompt}]
            + mensajes_usuario
            + [
                {"role": "assistant", "content": contenido_s1_s13},
                {"role": "user", "content": (
                    "Ahora genera ÚNICAMENTE la Sección 14 — FINAL VALIDATION STATUS. "
                    "Debe contener exactamente: "
                    "'Graph status: VALIDATED' y 'Ready to generate BETO_CORE children: YES'. "
                    "Declara los blocking issues (none si no hay). "
                    "Cierra con '## END OF DOCUMENT'."
                )},
            ]
        )
        response_2 = self.client.chat.completions.create(
            model=self.model,
            messages=messages_2,
            max_tokens=512,
        )
        contenido_s14 = response_2.choices[0].message.content

        return contenido_s1_s13 + "\n\n" + contenido_s14


def _separar_artefactos(contenido: str, nombres: list[str]) -> dict[str, str]:
    """
    BETO-TRACE: BETO_MOTOR_RAZ.SEC4.UNIT.PASO_EJECUCION
    Separa el contenido del LLM en artefactos individuales.
    Busca marcadores del tipo '=== ARCHIVO: nombre.md ===' en el output.
    Si no encuentra marcadores, asigna todo al primer artefacto.
    """
    import re
    result = {}
    bloques = re.split(r"===\s*ARCHIVO:\s*([^\s=]+)\s*===", contenido)

    if len(bloques) > 1:
        # Tiene marcadores — iterar de dos en dos (nombre, contenido)
        for i in range(1, len(bloques) - 1, 2):
            nombre_encontrado = bloques[i].strip()
            texto = bloques[i + 1].strip()
            # Buscar el nombre declarado más parecido
            match = next((n for n in nombres if n == nombre_encontrado), None)
            if match:
                result[match] = texto
    else:
        # Sin marcadores — asignar al primero si solo hay uno, o repartir
        if nombres:
            result[nombres[0]] = contenido

    # Asegurar que todos los nombres esperados estén en result
    for n in nombres:
        if n not in result:
            result[n] = f"# {n}\n\n[BETO_GAP: contenido no generado por el LLM]\n"

    return result

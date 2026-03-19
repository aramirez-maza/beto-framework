# FRAMEWORK BETO — Documentación Oficial
**Versión 4.2 — 2026-03-07**

---

## Índice

1. [Presentación](#1-presentación)
2. [El Problema que BETO Resuelve](#2-el-problema-que-beto-resuelve)
3. [Conceptos Fundamentales](#3-conceptos-fundamentales)
4. [El Proceso BETO — Los 11 Pasos](#4-el-proceso-beto--los-11-pasos)
5. [Inventario de Artefactos del Framework](#5-inventario-de-artefactos-del-framework)
6. [Dev Assistant — Primera Materialización](#6-dev-assistant--primera-materialización)
7. [Inventario Completo de Componentes](#7-inventario-completo-de-componentes)
8. [Los Cinco Tipos de Tarea](#8-los-cinco-tipos-de-tarea)
9. [Artefactos por Ejecución](#9-artefactos-por-ejecución)
10. [Integración LLM](#10-integración-llm)
11. [Instalación y Configuración](#11-instalación-y-configuración)
12. [Errores Comunes y Soluciones](#12-errores-comunes-y-soluciones)
13. [Referencia Rápida](#13-referencia-rápida)

---

## 1. Presentación

El **Framework BETO** es un protocolo de gobernanza epistémica para la especificación y materialización de software asistida por modelos de lenguaje.

No es un framework de documentación. No es un protocolo de generación de código. Es un sistema de compensación que contrarresta la tendencia estructural de los LLMs a completar silenciosamente lo que no fue declarado — inventando campos, asumiendo comportamientos, colapsando ambigüedades sin registrarlas.

**Definición central:**

> BETO formaliza el desconocimiento de una IA.

En lugar de confiar en que el modelo complete los huecos de manera coherente, BETO los nombra, los registra y los bloquea hasta que el operador los resuelva explícitamente. Los estados epistémicos funcionan como semáforos de ejecución: lo que no está declarado no puede ejecutarse.

El resultado es software que puede trazarse desde cada línea de código hasta la decisión de diseño que la autorizó.

---

## 2. El Problema que BETO Resuelve

Cuando se le pide a un LLM que diseñe o construya un sistema, el modelo completa los vacíos de especificación de forma silenciosa. Inventa campos de datos porque "parecen razonables". Asume arquitecturas porque "es lo habitual". Genera código que funciona para el caso promedio pero que no fue declarado por el operador.

Este comportamiento no es un error del modelo. Es su función principal: completar. El problema es que en contextos de ingeniería de software, esa completitud silenciosa produce:

- **Especificaciones infladas**: el sistema hace cosas que nadie declaró.
- **Contratos frágiles**: los campos entre componentes no tienen origen trazable.
- **Deuda epistémica**: nadie sabe qué fue decidido y qué fue inventado.
- **Fallo en revisión**: no hay forma de auditar lo que no tiene origen.

BETO resuelve esto imponiendo tres reglas formales sobre el ejecutor:

1. **Solo puede existir lo que fue declarado.** Si algo no está en el BETO_CORE aprobado, no existe.
2. **Lo no declarado se registra, no se infiere.** Los huecos se convierten en Open Questions bloqueantes.
3. **La inferencia está autorizada únicamente en la frontera controlada** (Pasos 0 y 1). Después del cierre del BETO_CORE_DRAFT, la inferencia está prohibida.

---

## 3. Conceptos Fundamentales

### 3.1 Estados Epistémicos

Cada elemento del sistema tiene exactamente uno de estos tres estados:

| Estado | Significado | Efecto sobre ejecución |
|---|---|---|
| `DECLARED` | Fue explícitamente definido por el operador | Habilita ejecución |
| `NOT_STATED` | No fue declarado ni puede inferirse | Bloquea ejecución — se registra como Open Question |
| `INFERRED` | Derivado de contexto por el ejecutor | Autorizado solo en Pasos 0 y 1. Prohibido después del cierre del BETO_CORE_DRAFT |

El estado `INFERRED` no es permanente: debe convertirse en `DECLARED` mediante confirmación del operador, o en `NOT_STATED` si el operador lo rechaza.

### 3.2 Tipos de Nodo Estructural

El Framework BETO reconoce tres tipos de nodos en el árbol de un sistema:

**BETO raíz (ROOT)**
- Único por sistema.
- Se genera directamente desde la IDEA_RAW elegible.
- Define el SYSTEM INTENT global, las fronteras, invariantes, arquitectura conceptual y mapa de capacidades.
- Es el tronco. Todo lo demás deriva de él.

**SubBETO (SUBBETO)**
- Se crea para cerrar una ambigüedad estructural del BETO padre.
- Nace por ambigüedad, no por tamaño.
- Representa descomposición vertical del diseño.
- Puede ser recursivo.
- No puede existir si el padre ya lo especifica completamente.

**BETO Paralelo (PARALLEL)**
- Representa una capacidad funcional autónoma del sistema.
- Nace por independencia funcional, no por ambigüedad.
- Tiene propósito, inputs y outputs propios.
- Puede desarrollarse con contexto propio suficiente.
- No depende de la lógica interna de otros BETO_PARALELOS.

### 3.3 BETO_GAP

Un `BETO_GAP` es un intento de operación fuera de los límites autorizados. Hay dos severidades:

- **BETO_GAP [REGISTRADO]**: Gap detectado dentro del flujo normal. Se registra y bloquea localmente.
- **BETO_GAP [ESCALADO]**: Intento de escritura fuera del scope autorizado o violación de invariante crítica. Genera parada inmediata y reporte obligatorio al operador.

### 3.4 BETO_SYSTEM_GRAPH

Artefacto estructural intermedio obligatorio entre el Paso 3 y el Paso 5. Su función es:

- Congelar los nodos y relaciones autorizados antes de generar los BETO_CORE hijos.
- Servir como base formal para los documentos de fase, manifests individuales y MANIFEST_PROYECTO.
- Impedir que aparezcan nodos o relaciones no autorizadas en pasos posteriores.

El BETO_SYSTEM_GRAPH **no redefine el SYSTEM INTENT**. **No reemplaza al BETO_CORE**. **No introduce capacidades nuevas**. Su autoridad es exclusivamente topológica.

El MANIFEST_PROYECTO deriva exclusivamente del BETO_SYSTEM_GRAPH validado.

### 3.5 Tipos de Arista Estructural

| Tipo | Significado |
|---|---|
| `FUNCTIONAL_BRANCH` | El hijo nació por capacidad funcional autónoma (ROOT → PARALLEL) |
| `STRUCTURAL_REFINEMENT` | El hijo nació para cerrar ambigüedad estructural del padre (ROOT → SUBBETO) |
| `DECLARED_DEPENDENCY` | El hijo usa el contrato de otro nodo como entrada declarada |

### 3.6 Invariante de Iniciativa Controlada

El ejecutor **no puede tomar iniciativa** más allá de la expansión controlada autorizada en los Pasos 0 y 1. Una vez cerrado el BETO_CORE_DRAFT y aprobado por el operador, toda inferencia está prohibida. El ejecutor solo puede:

- Ejecutar lo que está DECLARED.
- Registrar lo que está NOT_STATED.
- Escalar lo que viola los límites.

### 3.7 Node Extension Registration

Mecanismo formal para mantener la trazabilidad BETO cuando un sistema materializado recibe extensiones post-materialización.

**Condición de activación:** La extensión usa o necesita anotaciones BETO-TRACE en el código. Si no hay anotaciones, no hay obligación de registro formal.

**Qué hace:** Actualiza exclusivamente los artefactos del nodo afectado:
- El `TRACE_REGISTRY` del nodo recibe los nuevos IDs con prefijo `[EXT-POST-MAT]`
- El `MANIFEST` del nodo registra la extensión con fecha y origen

**Qué no hace:** No reabre el ciclo BETO. No reinicia los Pasos 0–10. No redefine contratos existentes de forma retroactiva.

**Resultado:** Las extensiones post-materialización quedan bajo autoridad epistémica BETO — con trazabilidad completa entre código, TRACE_ID, nodo y ciclo operativo que originó la extensión.

---

## 4. El Proceso BETO — Los 11 Pasos

El proceso BETO va del Paso 0 al Paso 11. El orden es obligatorio. No se puede saltar ni reordenar ningún paso.

El ciclo tiene dos cierres distintos: **cierre de construcción** (Pasos 0–10) y **cierre operacional** (Paso 11). Sin el Paso 11, el sistema está construido pero el ciclo BETO no está cerrado.

---

### Paso 0 — Elegibilidad Semántica de IDEA_RAW

**Propósito:** Determinar si la IDEA_RAW puede ingresar legítimamente al universo BETO.

Se evalúan dos condiciones simultáneamente:
- **Condición 1 — Intención de creación:** La IDEA_RAW expresa voluntad de crear, transformar, resolver, estructurar, producir o materializar algo.
- **Condición 2 — Coherencia semántica mínima:** Contiene suficiente núcleo conceptual para identificar un objeto reconocible, una dirección funcional, una transformación o un problema a resolver, sin expansión arbitraria.

**Salidas autorizadas:**

| Resultado | Significado |
|---|---|
| `GO` | Elegible. Continuar al Paso 1. |
| `GO_WITH_WARNINGS` | Elegible con debilidades semánticas. Se preservan como warnings desde el arranque. |
| `NO_GO` | No elegible. Parada obligatoria. No se genera nada. |

**Regla clave:** La vaguedad no es causal de rechazo. El vacío semántico sí lo es.

---

### Paso 1 — Generar BETO_CORE Raíz (Borrador)

**Propósito:** Producir el primer BETO_CORE a partir de la IDEA_RAW elegible.

Se usa el PROMPT_CANONICO_DE_ELICITACION como marco de expansión controlada, el BETO_CORE_INTERVIEW como guía de preguntas estructurales, y el BETO_CORE_TEMPLATE como estructura obligatoria de salida.

En este paso está **permitido**: Open Questions, elementos `NOT_STATED`, warnings preservados desde el Paso 0.

Está **prohibido**: crear múltiples BETO raíz, inventar capacidades no expresadas en la IDEA_RAW, cerrar silenciosamente ambigüedades.

El resultado es el `BETO_CORE_DRAFT.md` — un borrador que debe ser revisado y aprobado por el operador antes de continuar.

---

### Paso 2 — Entrevista Estructural del Sistema (BETO_CORE_INTERVIEW)

**Propósito:** Cerrar las Open Questions del BETO_CORE_DRAFT mediante preguntas estructuradas al operador.

Se usa el BETO_CORE_INTERVIEW.md como marco. La entrevista tiene 12 secciones que cubren: modelo de datos, tipos de operación, invariantes del sistema, restricciones de scope, mecanismos de ejecución, y detección de candidatos a BETO_PARALELO (P6.3).

Cada pregunta produce exactamente una de estas respuestas:
- Respuesta del operador → se registra como DECLARED.
- Silencio / "no lo sé" → se mantiene NOT_STATED.

---

### Paso 3 — Clasificación Estructural (STRUCTURAL_CLASSIFICATION_REGISTRY)

**Propósito:** Clasificar los candidatos identificados durante la entrevista como SUBBETO o PARALLEL.

Se aplica el test de independencia semántica a cada candidato:
1. ¿Puede especificarse con contratos externos solamente?
2. ¿Requiere conocimiento interno de otro componente?
3. ¿Puede darse a un equipo independiente con propósito + inputs + outputs?

El resultado es el STRUCTURAL_CLASSIFICATION_REGISTRY con la clasificación formal de cada candidato y el orden recomendado de expansión.

---

### Paso 4 — Generación y Validación del BETO_SYSTEM_GRAPH

**Propósito:** Congelar la topología del sistema antes de expandir los hijos.

Se genera el BETO_SYSTEM_GRAPH usando el BETO_SYSTEM_GRAPH_TEMPLATE. Debe alcanzar estado `VALIDATED` antes de continuar. El operador aprueba la topología. Una vez validado, no puede modificarse retroactivamente.

---

### Paso 5 — Generación de BETO_CORE Hijos

**Propósito:** Generar los BETO_CORE de los nodos hijos (PARALLEL y SUBBETO) según la topología congelada en el Paso 4.

El orden de generación respeta las dependencias declaradas en el BETO_SYSTEM_GRAPH. Los SUBBETO que definen contratos base se generan primero; los PARALLEL que dependen de esos contratos se generan después.

---

### Paso 6 — Modo Asistido de Cierre

**Propósito:** Cerrar todos los BETO_CORE (raíz e hijos) hasta que todos tengan estado `SUCCESS_CLOSED`.

Se revisan las Open Questions pendientes, se resuelven con el operador, y se actualiza cada BETO_CORE. Un BETO_CORE solo puede cerrarse cuando todas sus secciones están en estado `DECLARED` o tienen una decisión explícita de mantener `NOT_STATED` como límite aceptado del sistema.

---

### Paso 7 — Generación de Documentos de Fase (PHASE_TEMPLATE)

**Propósito:** Documentar las fases internas de cada BETO_CORE usando el PHASE_TEMPLATE.

Cada fase describe: propósito, inputs, outputs, restricciones, y decisiones de diseño. Los documentos de fase son la referencia operativa para la materialización.

---

### Paso 8 — TRACE_REGISTRY + MANIFEST Individual por BETO_CORE

**Propósito:** Generar el registro de trazabilidad y el manifest de estado para cada nodo.

**TRACE_REGISTRY:** Lista todos los IDs de trazabilidad autorizados para ese BETO_CORE en formato:
```
BETO_<NOMBRE>.SEC<N>.<TIPO>.<ELEMENTO>
```

Los tipos autorizados son: `FIELD`, `PHASE`, `CONCEPT`, `CONSTRAINT`, `DECISION`, `OUTPUT`, `TRACE_FIELD`, `INPUT`, `SCOPE`.

**MANIFEST_BETO:** Documenta el estado, dependencias, evidencias y artefactos de cada nodo. Solo puede estar en estado `COMPLETE` cuando el BETO_CORE está `SUCCESS_CLOSED`.

---

### Paso 9 — MANIFEST_PROYECTO

**Propósito:** Generar el manifest del proyecto completo.

Deriva exclusivamente del BETO_SYSTEM_GRAPH validado. Incluye: topología completa, matriz de dependencias, orden de construcción, y matriz de trazabilidad global. Es el artefacto de referencia para auditoría del sistema completo.

---

### Paso 10 — Materialización

**Propósito:** Producir el código fuente del sistema con anotaciones BETO-TRACE.

Cada archivo materializado incluye comentarios `# BETO-TRACE: <ID>` que trazan cada elemento significativo al TRACE_REGISTRY del BETO_CORE correspondiente. La materialización solo puede proceder sobre elementos con estado `DECLARED`. Todo elemento materializado debe tener un ID de trazabilidad autorizado.

---

### Paso 11 — Aprendizaje Operacional (Snapshot de Cierre)

**Propósito:** Cerrar el ciclo completo BETO capturando lo que el sistema enseñó en operación y retroalimentando al framework.

**Cuándo se activa:** Una vez, después del primer ciclo de operación real del sistema materializado. No automático — el operador decide el momento de corte.

**Proceso:** Dos preguntas, no más:
1. ¿Qué encontramos en operación que la entrevista o el PROMPT_CANONICO no preguntaron y que cambiaría el diseño si lo preguntasen? → Esos gaps son **interceptables** → van a `FRAMEWORK_FEEDBACK.md`
2. ¿Qué aprendió este sistema específico que no es generalizable pero que vale preservar? → Esos gaps son **operacionales** → van a `OPERATIONAL_LESSONS.md`

**Tipos de gap:**

| Tipo | Definición | Destino |
|---|---|---|
| Interceptable | Una pregunta correcta en la entrevista lo hubiera capturado antes de construir | `FRAMEWORK_FEEDBACK.md` → insumo para evolución del framework |
| Operacional | Solo emerge con el sistema real en uso | `OPERATIONAL_LESSONS.md` → memoria del proyecto |

**Condición de cierre:** El operador firma ambos artefactos. Una vez cerrados, no se reabren. Si aparecen nuevas lecciones, eso abre un nuevo ciclo BETO — no extiende el Paso 11 anterior.

**Regla anti-loop:** El Paso 11 se ejecuta exactamente una vez por ciclo de operación. Es un snapshot formal, no un proceso continuo.

**Salida:**
- `FRAMEWORK_FEEDBACK.md` — cerrado por el operador (usa FRAMEWORK_FEEDBACK_TEMPLATE.md)
- `OPERATIONAL_LESSONS.md` — cerrado por el operador (usa OPERATIONAL_LESSONS_TEMPLATE.md)

---

## 5. Inventario de Artefactos del Framework

El Framework BETO v4.2 se compone de los siguientes archivos de template y protocolo:

| Archivo | Tipo | Paso | Propósito |
|---|---|---|---|
| `BETO_INSTRUCTIVO.md` | Meta-instrucción | — | Protocolo completo de ejecución (Pasos 0–11 + REGLAS) |
| `PROMPT_CANONICO_DE_ELICITACION.md` | Prompt | 0–1 | Marco de elicitación controlada (Modos A y B, salida JSON) |
| `BETO_CORE_INTERVIEW.md` | Template | 2 | Entrevista estructural — 12 secciones + P6.3 para PARALLEL |
| `BETO_CORE_TEMPLATE.md` | Template | 1–6 | Estructura del BETO_CORE — 10 secciones + BETO_GAP LOG |
| `BETO_SYSTEM_GRAPH_TEMPLATE.md` | Template | 4 | Topología formal del sistema — 14 secciones |
| `PHASE_TEMPLATE.md` | Template | 7 | Documentos de fase por BETO_CORE — 8 secciones |
| `MANIFEST_BETO_TEMPLATE.md` | Template | 8 | Manifest individual por nodo |
| `MANIFEST_PROYECTO_TEMPLATE.md` | Template | 9 | Manifest de proyecto completo — 13 secciones |
| `FRAMEWORK_FEEDBACK_TEMPLATE.md` | Template | 11 | Gaps interceptables con propuestas concretas al framework |
| `OPERATIONAL_LESSONS_TEMPLATE.md` | Template | 11 | Memoria operacional específica del proyecto |

**Regla de uso:** Todos los templates son obligatorios en su paso correspondiente. Los templates del Paso 11 se usan después del primer ciclo de operación real, no durante la construcción.

---

## 6. Dev Assistant — Primera Materialización

### 6.1 Descripción del Sistema

El **Dev Assistant** es el primer sistema construido íntegramente bajo el Framework BETO v4.2.

Es un asistente de desarrollo de software que analiza la estructura de un proyecto en el sistema de archivos local y aplica tareas de desarrollo sobre sus archivos utilizando un modelo de lenguaje local. El operador describe la tarea en lenguaje natural; el sistema determina qué archivos tocar, crea un respaldo, invoca al modelo, escribe el resultado y persiste un reporte.

Opera completamente offline. No requiere APIs externas.

**SYSTEM INTENT (del BETO_CORE_DRAFT aprobado):**
> A system that comprehends the structure of a software project and operates directly on its real files and components to assist in its creation, modification, organization, maintenance, and evolution.

### 6.2 Topología de Nodos BETO

El sistema fue especificado en 6 nodos BETO formalizados bajo el proceso completo (Pasos 0–10):

```
BETO_DEV_ASSISTANT (ROOT)
├── BETO_PROJECT_COMPREHENSION (SUBBETO) ─── STRUCTURAL_REFINEMENT
├── BETO_TASK_STRUCTURE (SUBBETO) ────────── STRUCTURAL_REFINEMENT
├── BETO_SCOPE_RESOLUTION (SUBBETO) ─────── STRUCTURAL_REFINEMENT
├── BETO_PROJECT_ANALYZER (PARALLEL) ─────── FUNCTIONAL_BRANCH
│     └── DECLARED_DEPENDENCY → BETO_PROJECT_COMPREHENSION
└── BETO_TASK_EXECUTOR (PARALLEL) ────────── FUNCTIONAL_BRANCH
      ├── DECLARED_DEPENDENCY → BETO_PROJECT_COMPREHENSION
      ├── DECLARED_DEPENDENCY → BETO_TASK_STRUCTURE
      └── DECLARED_DEPENDENCY → BETO_SCOPE_RESOLUTION
```

| Nodo | Tipo | Propósito |
|---|---|---|
| `BETO_DEV_ASSISTANT` | ROOT | SYSTEM INTENT, fronteras, invariantes y contratos globales |
| `BETO_PROJECT_COMPREHENSION` | SUBBETO | Define el contrato del modelo de comprensión (campos, tipos, estructura) |
| `BETO_TASK_STRUCTURE` | SUBBETO | Define qué es una tarea ejecutable y sus 5 tipos |
| `BETO_SCOPE_RESOLUTION` | SUBBETO | Define cómo se determina el scope operativo |
| `BETO_PROJECT_ANALYZER` | PARALLEL | Implementa la comprensión del proyecto (lee filesystem, produce el modelo) |
| `BETO_TASK_EXECUTOR` | PARALLEL | Ejecuta tareas sobre archivos usando los contratos de los 3 SubBETOs |

**Orden de construcción:**
- Fase 1 (paralela): `BETO_PROJECT_COMPREHENSION`, `BETO_TASK_STRUCTURE`
- Fase 2: `BETO_SCOPE_RESOLUTION` (requiere contratos de Fase 1)
- Fase 3 (paralela): `BETO_PROJECT_ANALYZER`, `BETO_TASK_EXECUTOR` (requieren contratos de Fase 1 y 2)

### 6.3 Ciclo de Operación

```
FASE 1 — Comprensión del Proyecto
  Traversal → Analysis → Assembly → ComprehensionModel

FASE 2 — Ejecución de Tarea
  Parse → Build → Validate → StructuredTask
       ↓
  Hint Resolution → Dependency Expansion → Boundary Definition → ResolvedScope
       ↓
  Precheck → State Preservation → Task Execution → Report Generation → ExecutionReport
```

### 6.4 Invariantes de Sistema

1. El sistema no opera sobre archivos sin comprenderlos primero.
2. Toda escritura está acotada al `scope.boundary` — ningún archivo fuera del scope puede ser modificado.
3. El estado previo se preserva obligatoriamente antes de cualquier escritura.
4. El reporte de ejecución se genera siempre — independientemente del resultado (éxito o fallo).
5. No hay ejecución silenciosa: todo gap se registra y escala.

---

## 7. Inventario Completo de Componentes

### 7.1 Árbol de Archivos

```
src/
├── pyproject.toml
└── dev_assistant/
    ├── __init__.py
    ├── main.py
    ├── cli.py
    ├── models/
    │   ├── __init__.py
    │   ├── comprehension.py
    │   ├── task.py
    │   ├── scope.py
    │   └── report.py
    ├── project_analyzer/
    │   ├── __init__.py
    │   ├── traversal.py
    │   ├── analysis.py
    │   └── assembly.py
    ├── task_structure/
    │   ├── __init__.py
    │   ├── parse.py
    │   ├── build.py
    │   └── validate.py
    ├── scope_resolution/
    │   ├── __init__.py
    │   ├── hints.py
    │   ├── expansion.py
    │   └── boundary.py
    ├── task_executor/
    │   ├── __init__.py
    │   ├── precheck.py
    │   ├── preservation.py
    │   ├── execution.py
    │   ├── report.py
    │   ├── evaluation.py          ← Fase 5 (extensión local)
    │   ├── restore.py             ← Restore por EXEC-ID (extensión local)
    │   └── test_runner.py         ← Fase 6 (extensión local)
    └── llm/
        ├── __init__.py
        ├── config.py
        ├── prompts.py
        ├── parser.py
        └── engine.py
```

---

### 7.2 Modelos de Datos (`models/`)

Origen BETO: SubBETOs `BETO_PROJECT_COMPREHENSION`, `BETO_TASK_STRUCTURE`, `BETO_SCOPE_RESOLUTION`, `BETO_TASK_EXECUTOR`.

#### `comprehension.py` — Contrato del modelo de comprensión

Producido por `BETO_PROJECT_ANALYZER`. Consumido por `BETO_SCOPE_RESOLUTION` y `BETO_TASK_EXECUTOR`.

| Clase | Campo | Tipo | Descripción |
|---|---|---|---|
| `FileEntry` | `absolute_path` | str | Ruta absoluta del archivo |
| | `relative_path` | str | Ruta relativa desde project_root |
| | `language` | str | Lenguaje detectado |
| | `role` | str | `source` / `config` / `test` / `data` / `docs` / `unknown` |
| | `size_bytes` | int | Tamaño en bytes |
| `ModuleEntry` | `name` | str | Nombre del módulo |
| | `files` | list[str] | Archivos que componen el módulo |
| `DependencyEdge` | `from_file` | str | Archivo origen de la dependencia |
| | `to_file` | str | Archivo destino de la dependencia |
| | `import_ref` | str | Referencia de importación original |
| `ComprehensionModel` | `snapshot_id` | str | ID único del snapshot (ej: `SNAP-3A1B2C`) |
| | `project_root` | str | Ruta raíz del proyecto analizado |
| | `timestamp` | str | ISO 8601 UTC |
| | `directory_tree` | dict | Árbol de directorios |
| | `file_inventory` | list[FileEntry] | Inventario completo de archivos |
| | `module_map` | list[ModuleEntry] | Mapa de módulos detectados |
| | `dependency_graph` | list[DependencyEdge] | Grafo de dependencias (aristas) |
| | `entry_points` | list[str] | Puntos de entrada detectados |
| | `languages_detected` | list[str] | Lenguajes presentes en el proyecto |
| | `files_read` | list[str] | Archivos leídos durante el análisis |

#### `task.py` — Contrato de tarea estructurada

| Elemento | Descripción |
|---|---|
| `TaskType` (enum) | `GENERATE` / `MODIFY` / `CORRECT` / `REORGANIZE` / `INTEGRATE` |
| `StructuredTask.task_id` | ID único de la tarea (ej: `TASK-AB3F4C`) |
| `StructuredTask.task_type` | TaskType asignado |
| `StructuredTask.task_description` | Descripción original del operador |
| `StructuredTask.scope_hint` | Hint extraído de la descripción (puede ser None) |
| `StructuredTask.validation_status` | `VALID` / `INVALID` |
| `StructuredTask.validation_errors` | Lista de errores si INVALID |

#### `scope.py` — Contrato de scope resuelto

| Campo | Descripción |
|---|---|
| `ResolvedScope.scope_id` | ID único del scope (ej: `SCOPE-65A2B3`) |
| `ResolvedScope.primary_files` | Archivos objetivo de la operación |
| `ResolvedScope.context_files` | Archivos de contexto (dependencias 1 nivel) |
| `ResolvedScope.boundary` | Set de todos los paths autorizados para escritura |

#### `report.py` — Contrato del reporte de ejecución

| Elemento | Descripción |
|---|---|
| `STATUS_SUCCESS` | `"SUCCESS"` — todos los archivos procesados correctamente |
| `STATUS_PARTIAL` | `"PARTIAL"` — algunos procesados, otros fallaron |
| `STATUS_FAILED` | `"FAILED"` — sin escrituras realizadas |
| `FileModifiedEntry.absolute_path` | Ruta del archivo modificado |
| `FileModifiedEntry.change_summary` | Descripción del cambio aplicado |
| `FileModifiedEntry.prior_state_ref` | Ruta del backup previo |
| `ExecutionReport.execution_id` | ID único de la ejecución (ej: `EXEC-3A1B2C4D`) |
| `ExecutionReport.task_ref` | ID de la tarea ejecutada |
| `ExecutionReport.scope_ref` | ID del scope utilizado |
| `ExecutionReport.comprehension_model_ref` | snapshot_id del modelo usado |
| `ExecutionReport.timestamp` | ISO 8601 UTC |
| `ExecutionReport.files_modified` | list[FileModifiedEntry] |
| `ExecutionReport.files_created` | list[str] — rutas de archivos nuevos |
| `ExecutionReport.status` | STATUS_SUCCESS / PARTIAL / FAILED |
| `ExecutionReport.error_description` | Detalle del error si FAILED |

---

También en `models/` (extensiones post-materialización — Node Extension Registration 2026-03-07):
- `evaluation.py` — `EvaluationResult` dataclass (contrato de salida de la Fase 5)
- `restore_report.py` — `RestoreReport` dataclass (contrato de salida de `restore_execution`)
- `test_report.py` — `TestReport` dataclass (contrato de salida de la Fase 6)

#### `restore_report.py` — Contrato del reporte de restore

| Campo | Tipo | Descripción |
|---|---|---|
| `original_execution_id` | str | ID de la ejecución que se está revirtiendo |
| `restore_timestamp` | str | ISO 8601 UTC del momento del restore |
| `files_restored` | list[str] | Rutas absolutas de archivos restaurados desde backup |
| `files_deleted` | list[str] | Rutas absolutas de archivos creados que fueron eliminados |
| `model_refreshed` | bool | `True` si el ComprehensionModel fue reconstruido tras el restore |
| `status` | str | `SUCCESS` / `PARTIAL` / `FAILED` |
| `notes` | str | Descripción del resultado o errores encontrados |

#### `test_report.py` — Contrato del reporte de tests (Fase 6)

| Campo | Tipo | Descripción |
|---|---|---|
| `execution_id` | str | ID de la ejecución evaluada |
| `test_command` | str | Comando ejecutado (o `"(none)"` si no se detectó) |
| `result` | str | `PASS` / `FAIL` / `TIMEOUT` / `NO_TEST_COMMAND` / `ERROR` |
| `exit_code` | int \| None | Código de salida del proceso |
| `stderr_excerpt` | str | Primeros/últimos chars del stderr, truncado a 2000 chars |
| `duration_seconds` | float | Tiempo de ejecución del proceso |
| `timestamp` | str | ISO 8601 UTC |
| `security_note` | str | Nota explícita sobre el boundary de ejecución de comandos |

### 7.3 Project Analyzer (`project_analyzer/`)

Origen BETO: `BETO_PROJECT_ANALYZER` (PARALLEL). Implementa la Fase 1 del ciclo.

#### `traversal.py` — Fase 1: Traversal del Árbol

| Función | Descripción |
|---|---|
| `traverse_project(project_root)` | Recorre el filesystem ignorando paths excluidos. Produce `file_inventory`, `directory_tree`, `files_read`. |

**Paths ignorados automáticamente:** `.git`, `.venv`, `venv`, `env`, `node_modules`, `__pycache__`, `.tox`, `dist`, `build`, `*.egg-info`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `.DS_Store`, `.idea`, `.vscode`

**Lenguajes reconocidos:** Python, JavaScript, TypeScript, Go, Java, Rust, Ruby, C#, C, C++, Kotlin, PHP, Swift, Bash/Shell

**Roles detectados:** `source` (código fuente), `config` (configuración), `test` (pruebas), `data` (datos), `docs` (documentación), `unknown`

**Respeta `.gitignore`:** Si existe en project_root, sus reglas se aplican durante el traversal.

#### `analysis.py` — Fase 2: Análisis de Contenido

| Función | Descripción |
|---|---|
| `analyze_files(file_inventory)` | Lee cada archivo y extrae señales estructurales: imports, exports, puntos de entrada. Produce `structure_signals` por archivo. |

Detección de imports por lenguaje mediante expresiones regulares. Detección de entry points: `if __name__ == "__main__"` (Python), exports default (JS/TS).

#### `assembly.py` — Fase 3: Ensamblaje del Modelo

| Función | Descripción |
|---|---|
| `assemble_model(...)` | Combina el árbol, el inventario y las señales para producir el `ComprehensionModel` final. Construye `module_map` (directorios como módulos), `dependency_graph` (aristas entre archivos), lista de `entry_points`. |

---

### 7.4 Task Structure (`task_structure/`)

Origen BETO: `BETO_TASK_STRUCTURE` (SUBBETO). Implementa la Fase 2a del ciclo.

#### `parse.py` — Fase 1: Clasificación de Declaración

| Función | Descripción |
|---|---|
| `parse_declaration(raw_declaration)` | Clasifica la declaración en uno de los 5 tipos de tarea y extrae el scope_hint. |

**Mecanismo de clasificación:** scoring por keywords. El tipo con mayor score gana. Si dos tipos empatan en score: `NOT_STATED` — ambigüedad bloqueante.

**Keywords por tipo:**

| Tipo | Keywords |
|---|---|
| `CORRECT` | fix, correct, repair, resolve, debug, broken, bug, error, issue, problem, crash, fail |
| `REORGANIZE` | move, rename, reorganize, restructure, relocate, reorder, rearrange, split |
| `INTEGRATE` | integrate, connect, wire, plug, hook, add to existing, link, bridge, extend existing |
| `GENERATE` | create, generate, add new, new file, new module, new class, scaffold, write, build, implement |
| `MODIFY` | change, modify, update, edit, alter, adjust, replace, rewrite, refactor, improve, enhance |

**Extracción de scope_hint:** Se intentan tres patrones en orden — rutas entre comillas, patrón `in|at|from|to|file|module <path>`, nombre de archivo con extensión conocida.

**Caso especial REORGANIZE:** El scope_hint es el destino (no existe aún). `resolve_hint` lo ignora y usa keyword matching sobre la descripción en su lugar.

#### `build.py` — Fase 2: Construcción de la Tarea

| Función | Descripción |
|---|---|
| `build_task(raw_declaration, task_type, scope_hint)` | Genera un `StructuredTask` con UUID como `task_id`. |

#### `validate.py` — Fase 3: Validación

| Función | Descripción |
|---|---|
| `validate_task(task)` | Valida campos obligatorios y restricciones por tipo. Devuelve la tarea con `validation_status = VALID` o `INVALID`. |

---

### 7.5 Scope Resolution (`scope_resolution/`)

Origen BETO: `BETO_SCOPE_RESOLUTION` (SUBBETO). Implementa la Fase 2b del ciclo.

#### `hints.py` — Fase 1: Resolución de Hint

| Función | Descripción |
|---|---|
| `resolve_hint(task, model)` | Resuelve el scope_hint contra el inventario del ComprehensionModel. |

**Proceso de resolución:**
1. Si la tarea es REORGANIZE: ignora el scope_hint (es destino) y usa keyword matching.
2. Si hay scope_hint: intenta match exacto de path, luego match de nombre de módulo.
3. Si el scope_hint no coincide con ningún archivo: `NOT_STATED` — bloqueante.
4. Si no hay scope_hint: keyword matching sobre task_description, fallback a todos los archivos fuente.

#### `expansion.py` — Fase 2: Expansión de Dependencias

| Función | Descripción |
|---|---|
| `expand_dependencies(primary_candidates, model)` | Expande 1 nivel: archivos que el primario importa (outgoing) + archivos que importan al primario (incoming). |
| `expand_mentioned_files(task_description, primary_candidates, model)` | Para INTEGRATE: extrae filenames mencionados en la descripción y agrega los que existen en el proyecto como contexto adicional. Resuelve el gap de módulos a integrar que aún no tienen arista en el grafo. |

#### `boundary.py` — Fase 3: Definición del Boundary

| Función | Descripción |
|---|---|
| `define_boundary(primary_candidates, context_files, task, model)` | `boundary = primary_files ∪ context_files`. Verifica que todos estén dentro de project_root. Produce el `ResolvedScope`. |

Todo intento de escritura fuera del boundary durante la ejecución genera `BETO_GAP [ESCALADO]`.

---

### 7.6 Task Executor (`task_executor/`)

Origen BETO: `BETO_TASK_EXECUTOR` (PARALLEL). Implementa la Fase 2c del ciclo.

#### `precheck.py` — Fase 1: Verificación Previa

| Función | Descripción |
|---|---|
| `precheck(model, task, scope)` | Valida los 3 inputs de ejecución (modelo, tarea, scope). Genera el `execution_id`. Devuelve lista de fallos si algún input es inválido. |

#### `preservation.py` — Fase 2: Preservación de Estado

| Función | Descripción |
|---|---|
| `preserve_state(scope, model, execution_id)` | Copia todos los archivos del scope a `.beto_state/{execution_id}/` antes de cualquier escritura. Invariante: si la preservación falla para algún archivo, la ejecución se aborta. |

Esta fase es obligatoria e incondicional. No hay escritura sin backup previo.

#### `execution.py` — Fase 3: Ejecución de la Tarea

Despacha al handler correspondiente según `task.task_type`. Todos los handlers aplican el check de boundary antes de escribir.

| Handler | Tipo | Descripción |
|---|---|---|
| `_execute_generate` | LLM | Deriva el nombre del archivo de la descripción. Verifica que el path destino esté dentro de project_root. Si el archivo ya existe, lo trata como MODIFY. |
| `_execute_modify` | LLM | Lee el archivo primario, envía al LLM con contexto, escribe el resultado. |
| `_execute_correct` | LLM | Como MODIFY pero el prompt incluye el issue y pide una explicación de fix en una línea. |
| `_execute_reorganize` | Autónomo | Extrae origen y destino con regex. Busca el origen en el inventario. Mueve con `shutil.move`. No usa LLM. |
| `_execute_integrate` | LLM | Como MODIFY con el contexto más fuerte — los context_files se etiquetan como "REFERENCE CONTRACTS" con instrucción explícita de usar sus nombres de campo, métodos e imports. |

**Fallback cuando el gateway no está disponible:**

| Tipo | Comportamiento fallback |
|---|---|
| GENERATE | Escribe un stub con `raise NotImplementedError` |
| MODIFY | Agrega marcador `# --- MODIFICATION ---` al final del archivo |
| CORRECT | Limpia whitespace y agrega `# --- CORRECTION NOTE ---` |
| INTEGRATE | Agrega marcador `# --- INTEGRATION ---` al final del archivo |
| REORGANIZE | No afectado — no usa LLM |

#### `report.py` — Fase 4: Generación del Reporte

| Función | Descripción |
|---|---|
| `generate_report(...)` | Construye el `ExecutionReport` y lo persiste como JSON en `<project_root>/.beto_reports/{execution_id}.json`. Obligatorio independientemente del resultado de la ejecución. |

#### `evaluation.py` — Fase 5: Evaluación del Output (extensión local)

Extensión declarada del producto. No modifica contratos existentes. Produce su propio artefacto de salida separado del `ExecutionReport`.

**Propósito:** Distinguir formalmente entre *escritura correcta* (el archivo fue escrito) y *resolución correcta* (el cambio satisface la intención declarada).

**Condiciones de halt / NOT_EVALUABLE:**
- Ejecución con status FAILED
- Sin archivos modificados ni creados
- Backup no disponible para comparación

**Criterios de evaluación por tipo:**

| Tipo | Checks realizados |
|---|---|
| CORRECT | Contenido cambió · Token de defecto ausente en código (heurístico, solo si hay señal explícita en la tarea) · Integridad estructural del archivo |
| MODIFY | Contenido cambió · Keywords de la tarea presentes en el resultado |
| GENERATE | Archivo existe · No está vacío · Contiene estructura programática compatible con el lenguaje detectado |
| REORGANIZE | Origen removido · Destino existe · Integridad de contenido (comparación byte a byte con backup) |
| INTEGRATE | Contenido cambió · Import del módulo integrado presente · Llamadas a la API declarada presentes |

**Estados de evaluación:**

| Estado | Significado |
|---|---|
| `RESOLVED` | Todos los checks pasan — el cambio satisface la intención declarada |
| `UNCERTAIN` | El archivo cambió y pasa checks básicos, pero no puede confirmarse resolución completa |
| `UNRESOLVED` | Uno o más checks críticos fallan — el cambio probablemente no resolvió lo solicitado |
| `NOT_EVALUABLE` | Información insuficiente para evaluar |

**Output contract — `EvaluationResult`:**

| Campo | Descripción |
|---|---|
| `execution_id` | ID de la ejecución evaluada |
| `task_ref` | ID de la tarea |
| `task_type` | Tipo de tarea evaluada |
| `evaluation_status` | RESOLVED / UNCERTAIN / UNRESOLVED / NOT_EVALUABLE |
| `checks_performed` | Lista de checks ejecutados |
| `checks_passed` | Lista de checks que pasaron |
| `checks_failed` | Lista de checks que fallaron |
| `evaluation_notes` | Resumen legible del resultado |
| `promotion_signal` | `True` si la complejidad justifica futura promoción a nodo BETO |

**Artefacto persistido:** `<project_root>/.beto_reports/<EXEC-ID>_eval.json`

**Nota de evolución:** Si los criterios de evaluación crecen en complejidad diferenciada por tipo, o si la evaluación demuestra valor reutilizable en otros sistemas materializados bajo BETO, se considerará su promoción a nodo BETO independiente (SUBBETO o PARALLEL).

#### `restore.py` — Restore por EXEC-ID (extensión local)

Extensión declarada del producto. Permite revertir el proyecto al estado previo a una ejecución dada, usando los backups creados por la Fase 2 (State Preservation).

**Función principal:**

| Función | Descripción |
|---|---|
| `restore_execution(execution_id, project_root)` | Lee `<project_root>/.beto_reports/<EXEC-ID>.json`. Restaura cada archivo en `files_modified` copiando desde `prior_state_ref`. Elimina cada archivo en `files_created`. Persiste `<EXEC-ID>_restore.json`. |

**Flujo de restore:**
1. Lee el reporte de ejecución en `.beto_reports/<EXEC-ID>.json`
2. Para cada entrada en `files_modified`: crea directorios padre si es necesario, copia el backup (`prior_state_ref`) sobre la ruta original
3. Para cada entrada en `files_created`: elimina el archivo si existe. Si ya no existe, se omite silenciosamente — operación no bloqueante
4. Persiste `<EXEC-ID>_restore.json` como evidencia

**Estados de RestoreReport:**

| Estado | Significado |
|---|---|
| `SUCCESS` | Todos los archivos restaurados y/o eliminados correctamente |
| `PARTIAL` | Algunos archivos restaurados, otros fallaron (backups no encontrados) |
| `FAILED` | No se pudo restaurar nada — reporte no encontrado o ilegible |

**Artefacto persistido:** `<project_root>/.beto_reports/<EXEC-ID>_restore.json`

#### `test_runner.py` — Fase 6: Validación Funcional (extensión local)

Extensión declarada del producto. Ejecuta el suite de tests del proyecto después de cada ejecución exitosa para comprobar que el sistema sigue funcionando. No es un gate — no activa restore automáticamente.

**SECURITY BOUNDARY:** Esta fase ejecuta un comando descubierto de archivos del propio proyecto. Se asume confianza del operador en el proyecto cargado — la misma confianza que ya implica cargar y modificar su código fuente.

**Función principal:**

| Función | Descripción |
|---|---|
| `run_tests(execution_id, project_root, timeout)` | Detecta el comando de tests, lo ejecuta con subprocess, captura resultado y stderr. Persiste `<EXEC-ID>_test.json`. |

**Detección del comando de tests (orden de prioridad):**

| Prioridad | Indicador | Comando resultante |
|---|---|---|
| 1 | `pyproject.toml` con sección pytest | `python3 -m pytest` |
| 2 | `setup.cfg` con `[tool:pytest]` o `[pytest]` | `python3 -m pytest` |
| 3 | `package.json` con `scripts.test` definido | `npm test` |
| 4 | `go.mod` presente | `go test ./...` |
| 5 | `Makefile` con target `test:` | `make test` |
| 6 | Archivos `test_*.py` en el proyecto | `python3 -m pytest` |
| — | Ninguno encontrado | `NO_TEST_COMMAND` (no bloqueante) |

**Nota sobre Python:** Se usa `python3 -m pytest` en lugar de `pytest` para no depender de que el ejecutable esté en el PATH del sistema. Funciona con el intérprete activo en el entorno del operador.

**Estados de resultado:**

| Estado | Significado |
|---|---|
| `PASS` | Exit code 0 — todos los tests pasaron |
| `FAIL` | Exit code distinto de 0 — al menos un test falló |
| `TIMEOUT` | El proceso excedió el timeout configurado |
| `NO_TEST_COMMAND` | No se detectó ningún comando de tests en el proyecto |
| `ERROR` | El proceso no pudo iniciarse (error de subprocess) |

**Artefacto persistido:** `<project_root>/.beto_reports/<EXEC-ID>_test.json`

---

### 7.7 Integración LLM (`llm/`)

Módulo aditivo — no modifica contratos existentes. Se comunica con el gateway LiteLLM en formato Anthropic `/v1/messages`. Sin dependencias externas — solo stdlib (`urllib`, `json`).

#### `config.py` — Configuración del Gateway

```python
@dataclass
class GatewayConfig:
    base_url: str = "http://127.0.0.1:8000"
    model: str = "qwen-coder"
    api_key: str = "local"
    timeout: int = 120
    max_tokens_generate: int = 2048
    max_tokens_modify: int = 2048
    max_tokens_correct: int = 2048
    max_tokens_integrate: int = 2048
```

#### `prompts.py` — Constructores de Prompt

| Función | Descripción |
|---|---|
| `build_generate_prompt(...)` | Prompt para crear un archivo nuevo |
| `build_modify_prompt(...)` | Archivo primario etiquetado como "FILE TO MODIFY" + contexto como "REFERENCE CONTRACTS" |
| `build_correct_prompt(...)` | Como MODIFY + instrucción de una línea de explicación del fix |
| `build_integrate_prompt(...)` | Etiquetado más fuerte: "REFERENCE CONTRACTS — IMPORTANT: use these to get correct field names, method names, and imports" |

**Principio de diseño:** Los context_files siempre se etiquetan como "REFERENCE CONTRACTS" para forzar al modelo a usar los nombres de campo correctos (encontrado en gateway test 4: sin este label, el modelo usa `str(task)` en lugar de `task.task_id`).

#### `parser.py` — Parser de Respuestas LLM

| Función | Descripción |
|---|---|
| `extract_code(response)` | Extrae el primer bloque de código fenced (` ```...``` `). Fallback: si la respuesta no tiene estructura de prosa y contiene `def`/`class`, la trata como código directo. |
| `extract_fix_explanation(response)` | Para CORRECT: extrae la primera línea no-code como explicación del fix. |

#### `engine.py` — Motor LLM

| Método | Descripción |
|---|---|
| `_call(prompt, max_tokens)` | POST al gateway. Retorna `content[0].text` o `None` en caso de fallo. Maneja `URLError`, `KeyError`, `JSONDecodeError`. |
| `_read_context_files(paths)` | Lee archivos de contexto del disco. Omite silenciosamente los ilegibles. |
| `generate(...)` | Construye prompt, llama al gateway, extrae código. |
| `modify(...)` | Ídem para MODIFY. |
| `correct(...)` | Retorna `(corrected_content, fix_explanation)`. |
| `integrate(...)` | Incluye context_files como reference contracts completos. |

---

### 7.8 Orquestación

#### `main.py` — Orquestador Principal

| Función | Descripción |
|---|---|
| `run_project_analysis(project_root)` | Ejecuta las 3 fases del Project Analyzer. Retorna `(ComprehensionModel, error)`. |
| `run_task_pipeline(raw_declaration, model)` | Ejecuta el pipeline completo: Task Structure → Scope Resolution → Task Executor. Retorna `ExecutionReport` o `None` si se bloqueó antes de ejecutar. |
| `main()` | Loop de CLI interactivo. Detecta si el input es un path (activa Fase 1), el comando `restore <EXEC-ID>` o una declaración de tarea (activa Fase 2). |

**Auto-refresh del ComprehensionModel:** Después de cada ejecución exitosa que modifica o crea archivos (`report.files_modified` o `report.files_created`), el sistema re-ejecuta automáticamente `run_project_analysis()` y actualiza `state["model"]`. Esto mantiene el modelo de comprensión sincronizado con el estado real del filesystem sin requerir un comando `reload` explícito.

**Fase 6:** Después de la Fase 5, si el status de la ejecución no es FAILED, se invoca `run_tests()` para ejecutar el suite de tests del proyecto. El resultado se muestra en consola y se persiste como artefacto. No es un gate — no bloquea ni revierte la ejecución.

**Comando restore:** Al recibir `restore <EXEC-ID>`, invoca `restore_execution()`, y si el restore tuvo éxito total o parcial, re-ejecuta `run_project_analysis()` para reflejar el estado restaurado en el modelo.

#### `cli.py` — Helpers de Presentación

| Función | Descripción |
|---|---|
| `print_banner()` | Banner de inicio |
| `print_model_summary(model)` | Resumen del ComprehensionModel cargado |
| `print_scope_summary(scope)` | Muestra primary_files y context_files del scope resuelto |
| `print_report_summary(report, path)` | Resumen del resultado de ejecución |
| `print_evaluation_summary(eval_result)` | Resumen del resultado de la Fase 5 (estado, checks, notas) |
| `print_test_summary(test_report)` | Resumen de la Fase 6: icono de resultado, comando, duración, extracto de stderr en caso de fallo |
| `print_restore_summary(restore_report)` | Resumen del restore: archivos restaurados, eliminados, estado |
| `is_path_like(text)` | Heurística para detectar si el input del usuario es una ruta |

---

### 7.9 Artefactos BETO del Proyecto

Generados durante el proceso completo (Pasos 0–10):

```
outputs/dev_assistant/
├── BETO_CORE_DRAFT.md                     ← Paso 1 — ROOT (SUCCESS_CLOSED)
├── BETO_CORE_INTERVIEW_COMPLETED.md       ← Paso 2 — Entrevista completa
├── STRUCTURAL_CLASSIFICATION_REGISTRY.md  ← Paso 3 — Clasificación formal
├── BETO_SYSTEM_GRAPH.md                   ← Paso 4 — Topología (VALIDATED)
├── BETO_CORE_PROJECT_COMPREHENSION.md     ← Paso 5 (SUCCESS_CLOSED)
├── BETO_CORE_TASK_STRUCTURE.md            ← Paso 5 (SUCCESS_CLOSED)
├── BETO_CORE_SCOPE_RESOLUTION.md          ← Paso 5 (SUCCESS_CLOSED)
├── BETO_CORE_PROJECT_ANALYZER.md          ← Paso 5 (SUCCESS_CLOSED)
├── BETO_CORE_TASK_EXECUTOR.md             ← Paso 5 (SUCCESS_CLOSED)
├── MANIFEST_PROYECTO.md                   ← Paso 9
├── FRAMEWORK_FEEDBACK.md                  ← Paso 11 — Gaps interceptables (CERRADO)
├── OPERATIONAL_LESSONS.md                 ← Paso 11 — Memoria operacional (CERRADO)
├── phases/                                ← Paso 7 — documentos de fase
└── manifests/                             ← Paso 8 — TRACE_REGISTRY + MANIFEST por nodo
    ├── TRACE_REGISTRY_DEV_ASSISTANT.md          (39 IDs — 3 vía Node Extension Registration)
    ├── TRACE_REGISTRY_PROJECT_COMPREHENSION.md  (37 IDs)
    ├── TRACE_REGISTRY_TASK_STRUCTURE.md         (35 IDs)
    ├── TRACE_REGISTRY_SCOPE_RESOLUTION.md       (33 IDs)
    ├── TRACE_REGISTRY_PROJECT_ANALYZER.md       (31 IDs)
    ├── TRACE_REGISTRY_TASK_EXECUTOR.md          (61 IDs — 10 vía Node Extension Registration)
    ├── MANIFEST_DEV_ASSISTANT.md
    ├── MANIFEST_PROJECT_COMPREHENSION.md
    ├── MANIFEST_TASK_STRUCTURE.md
    ├── MANIFEST_SCOPE_RESOLUTION.md
    ├── MANIFEST_PROJECT_ANALYZER.md
    └── MANIFEST_TASK_EXECUTOR.md
```

**Total de IDs de trazabilidad autorizados:** 236 (distribuidos en los 6 TRACE_REGISTRY — incluye 13 IDs añadidos vía Node Extension Registration 2026-03-07).

**Estado del ciclo BETO:** CERRADO — construcción (Pasos 0–10), aprendizaje operacional (Paso 11) y Node Extension Registration completados.

---

## 8. Los Cinco Tipos de Tarea

### 8.1 CORRECT — Corregir un error

**Cuándo usarlo:** Hay un bug identificado, un error de runtime, una inconsistencia en el código.

**Keywords de activación:** `fix`, `correct`, `repair`, `resolve`, `debug`, `bug`, `error`, `issue`, `crash`

**Lo que hace:** Lee el archivo objetivo, envía el contenido más la descripción del problema al LLM, escribe la versión corregida. El LLM incluye una línea de explicación del fix.

**Ejemplos:**
```
fix the NameError in calculator.py — variable resut should be result
correct the off-by-one error in parser.py when processing the last token
debug the authentication middleware in auth.py
```

---

### 8.2 MODIFY — Modificar comportamiento existente

**Cuándo usarlo:** El código funciona pero su comportamiento debe cambiar.

**Keywords de activación:** `modify`, `change`, `update`, `edit`, `alter`, `adjust`, `replace`, `rewrite`, `refactor`, `improve`, `enhance`

**Lo que hace:** Lee el archivo objetivo, envía el contenido más la instrucción de cambio al LLM, escribe el resultado.

**Ejemplos:**
```
modify config.py to load settings from environment variables using os.getenv
update the logging in server.py to use JSON format
refactor the database connection in db.py to use a connection pool
```

---

### 8.3 GENERATE — Crear un archivo nuevo

**Cuándo usarlo:** Hay que crear un módulo, clase o función que no existe.

**Keywords de activación:** `create`, `generate`, `add new`, `new file`, `new module`, `scaffold`, `write`, `build`, `implement`

**Lo que hace:** Deriva el nombre del archivo de las palabras clave de la descripción (stop words removidas). Verifica que el destino esté dentro de project_root. Si el archivo ya existe, lo trata como MODIFY.

**Nota:** El nombre del archivo resultante se deriva automáticamente de la descripción. Para mayor control sobre el nombre, incluirlo explícitamente en la tarea (pero sin extensión .py para evitar que sea capturado como scope_hint).

**Ejemplos:**
```
create a new module text_cleaner with functions for whitespace normalization
generate a utility file with slug generation and string truncation functions
write a new cache module for in-memory storage
```

---

### 8.4 REORGANIZE — Mover o renombrar archivos

**Cuándo usarlo:** Hay que mover, renombrar o relocalizar archivos dentro del proyecto.

**Keywords de activación:** `move`, `rename`, `reorganize`, `relocate`, `restructure`

**Lo que hace:** Extrae origen y destino mediante regex. Busca el archivo origen en el inventario del ComprehensionModel. Ejecuta `shutil.move`. **No usa LLM** — operación completamente autónoma.

**Formato obligatorio:** `move <origen> to <destino>`

**Restricción:** El destino debe estar dentro de project_root. Mover archivos fuera genera `BETO_GAP [ESCALADO]`.

**Ejemplos:**
```
move helpers.py to utils/helpers.py
rename old_utils.py to utils/helpers.py
move the auth module to core/auth
```

---

### 8.5 INTEGRATE — Incorporar una capacidad en un archivo existente

**Cuándo usarlo:** Hay que conectar un módulo o capacidad existente dentro de otro archivo.

**Keywords de activación:** `integrate`, `connect`, `wire`, `plug`, `hook`, `link`, `bridge`, `extend existing`

**Lo que hace:** Identifica el archivo objetivo (primary) y el módulo a integrar. Lee ambos archivos. Envía al LLM con el módulo a integrar etiquetado explícitamente como "REFERENCE CONTRACT" para que use los nombres de campo y métodos correctos.

**Importante:** Mencionar el nombre del archivo del módulo a integrar en la descripción (ej: `cache.py`) para que el sistema lo incluya automáticamente en el contexto.

**Ejemplos:**
```
integrate the cache module into processor.py so that fetch_record results are cached using Cache.get and Cache.set
connect the rate limiter middleware to server.py
wire the email validator from validators.py into the registration handler in auth.py
```

---

## 9. Artefactos por Ejecución

Cada ejecución — exitosa o fallida — produce tres artefactos dentro del directorio del proyecto:

### 9.1 Backup de Estado Previo

**Ubicación:** `<project_root>/.beto_state/<EXEC-ID>/`

Contiene copias de los archivos primarios **antes de cualquier modificación**. Se crea en la Fase 2 (State Preservation), antes de que se llame al LLM. Si la ejecución falla o el resultado es incorrecto, es posible restaurar manualmente desde este directorio.

### 9.2 Archivos Modificados o Creados

Los archivos primarios son sobreescritos con el contenido generado por el LLM. Los archivos creados por GENERATE aparecen en el directorio objetivo. El original solo está disponible en `.beto_state/`.

### 9.3 Reporte JSON

**Ubicación:** `<project_root>/.beto_reports/<EXEC-ID>.json`

```json
{
  "execution_id": "EXEC-3A1B2C4D5E6F7G8H",
  "task_ref": "TASK-ABCD1234",
  "scope_ref": "SCOPE-XY5678",
  "comprehension_model_ref": "SNAP-FF9D9C",
  "timestamp": "2026-03-07T14:32:10+00:00",
  "status": "SUCCESS",
  "files_modified": [
    {
      "absolute_path": "/home/user/myapp/calculator.py",
      "change_summary": "Corrected via LLM (qwen-coder): Fix the NameError...",
      "prior_state_ref": "/home/user/myapp/.beto_state/EXEC-.../calculator.py"
    }
  ],
  "files_created": [],
  "error_description": null
}
```

| Status | Significado |
|---|---|
| `SUCCESS` | Todos los archivos objetivo fueron procesados y escritos |
| `PARTIAL` | Algunos archivos procesados, otros fallaron |
| `FAILED` | Sin escrituras realizadas — ver `error_description` |

### 9.4 Reporte de Evaluación (JSON) — Fase 5

Se guarda en:
```
<raíz_proyecto>/.beto_reports/<EXEC-ID>_eval.json
```

Ejemplo de contenido:
```json
{
  "execution_id": "EXEC-353BDD0AD28D45B0",
  "task_ref": "TASK-AB4E9707D60D",
  "task_type": "CORRECT",
  "evaluation_status": "RESOLVED",
  "checks_performed": ["content_changed", "defect_token_absent(resut)", "structural_integrity"],
  "checks_passed":    ["content_changed", "defect_token_absent(resut)", "structural_integrity"],
  "checks_failed": [],
  "evaluation_notes": "All checks passed.",
  "promotion_signal": false,
  "timestamp": "2026-03-07T18:45:23+00:00"
}
```

**Interpretación del campo `promotion_signal`:** `true` indica que la complejidad de la evaluación en este tipo de tarea justificaría en el futuro considerar la promoción de esta fase a un nodo BETO independiente.

### 9.5 Reporte de Restore (JSON)

Se genera al ejecutar el comando `restore <EXEC-ID>`. Se guarda en:
```
<raíz_proyecto>/.beto_reports/<EXEC-ID>_restore.json
```

Ejemplo de contenido:
```json
{
  "original_execution_id": "EXEC-353BDD0AD28D45B0",
  "restore_timestamp": "2026-03-07T19:12:04+00:00",
  "files_restored": [
    "/home/usuario/miaplicacion/calculator.py"
  ],
  "files_deleted": [],
  "model_refreshed": true,
  "status": "SUCCESS",
  "notes": "All files restored successfully."
}
```

| Campo | Descripción |
|---|---|
| `files_restored` | Archivos recuperados desde backup (`prior_state_ref`) |
| `files_deleted` | Archivos creados durante la ejecución que fueron eliminados |
| `model_refreshed` | Si el ComprehensionModel fue reconstruido después del restore |
| `status` | `SUCCESS` / `PARTIAL` / `FAILED` |

### 9.6 Reporte de Tests (JSON) — Fase 6

Se genera automáticamente después de cada ejecución no-FAILED. Se guarda en:
```
<raíz_proyecto>/.beto_reports/<EXEC-ID>_test.json
```

Ejemplo de contenido — PASS:
```json
{
  "execution_id": "EXEC-353BDD0AD28D45B0",
  "test_command": "python3 -m pytest",
  "result": "PASS",
  "exit_code": 0,
  "stderr_excerpt": "",
  "duration_seconds": 3.42,
  "timestamp": "2026-03-07T19:20:11+00:00",
  "security_note": "This phase executes a command discovered from project files..."
}
```

Ejemplo de contenido — FAIL:
```json
{
  "execution_id": "EXEC-7F3C1A9B2D4E5F6G",
  "test_command": "python3 -m pytest",
  "result": "FAIL",
  "exit_code": 1,
  "stderr_excerpt": "FAILED tests/test_calculator.py::test_add - AssertionError: assert 3 == 4\n...",
  "duration_seconds": 2.18,
  "timestamp": "2026-03-07T19:21:05+00:00",
  "security_note": "This phase executes a command discovered from project files..."
}
```

| Campo `result` | Significado |
|---|---|
| `PASS` | Exit code 0 — suite de tests completa sin fallos |
| `FAIL` | Exit code distinto de 0 — ver `stderr_excerpt` para detalles |
| `TIMEOUT` | El proceso excedió el timeout (default: 60s) |
| `NO_TEST_COMMAND` | No se detectó suite de tests en el proyecto |
| `ERROR` | El proceso no pudo iniciarse |

**No es un gate:** Un resultado FAIL no activa restore ni bloquea el flujo. Es una señal para el operador.

---

## 10. Integración LLM

### 10.1 Gateway Requerido

El sistema se comunica con un gateway LiteLLM local usando el formato Anthropic `/v1/messages`. El gateway actúa como proxy entre el sistema y el modelo de inferencia local.

**Configuración validada en producción:**
- **Gateway:** LiteLLM en `http://127.0.0.1:8000`
- **Backend:** vLLM en `http://127.0.0.1:8001`
- **Modelo:** Qwen2.5-Coder-14B-Instruct-AWQ (14B parámetros, cuantizado AWQ)
- **Contexto:** 32K tokens
- **Inferencia:** 100% local, sin conexión a internet

### 10.2 Verificación del Gateway

```bash
# Verificar que el gateway está activo
curl -s -o /dev/null -w "%{http_code}" \
  -H "x-api-key: local" \
  http://127.0.0.1:8000/v1/models
# Respuesta esperada: 200 o 401

# Test funcional completo
curl -X POST http://127.0.0.1:8000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: local" \
  -d '{"model":"qwen-coder","messages":[{"role":"user","content":"Say: OK"}],"max_tokens":10}'
```

### 10.3 Comportamiento sin Gateway

Si el gateway no está disponible, el sistema no falla. Escribe un fallback estructural en el archivo objetivo y reporta el resultado como SUCCESS con la nota `"gateway unavailable"` en el change_summary. El operador puede aplicar el cambio real manualmente o re-ejecutar la tarea cuando el gateway vuelva.

---

## 11. Instalación y Configuración

### 11.1 Requisitos

| Requisito | Versión mínima |
|---|---|
| Python | 3.10 |
| Sistema operativo | Linux, macOS, Windows (WSL2 soportado) |
| Gateway LLM | LiteLLM o compatible en `localhost:8000` |
| Modelo | Cualquier modelo de código expuesto via gateway |

### 11.2 Instalación

```bash
# 1. Ir al directorio fuente
cd path/to/dev_assistant/src

# 2. Crear entorno virtual
python3 -m venv .venv

# 3. Activar
source .venv/bin/activate          # Linux / macOS / WSL2
# .venv\Scripts\activate.bat       # Windows CMD
# .venv\Scripts\Activate.ps1       # Windows PowerShell

# 4. Instalar
pip install --upgrade pip setuptools
pip install -e .

# 5. Verificar
dev-assistant --help
```

### 11.3 Iniciar el Asistente

```bash
# Sin proyecto inicial
dev-assistant

# Con proyecto inicial
dev-assistant /ruta/al/proyecto
```

### 11.4 Comandos Disponibles

| Comando | Efecto |
|---|---|
| `/ruta/al/proyecto` | Analizar un directorio de proyecto |
| `restore <EXEC-ID>` | Restaurar el estado del proyecto antes de una ejecución dada |
| `status` | Resumen del proyecto cargado actualmente |
| `reload` | Re-analizar el proyecto actual (incorpora archivos nuevos) |
| `help` | Mostrar texto de ayuda |
| `quit` / `exit` / `q` | Salir |
| Cualquier otro texto | Tratado como declaración de tarea |

**Nota sobre auto-refresh:** Después de cada tarea que modifica o crea archivos, el ComprehensionModel se actualiza automáticamente. El comando `reload` es útil para incorporar cambios hechos externamente (fuera del asistente) o después de un restore manual.

### 11.5 Cambiar la Configuración del Gateway

Editar `src/dev_assistant/llm/config.py`:

```python
@dataclass
class GatewayConfig:
    base_url: str = "http://127.0.0.1:8000"   # Puerto del gateway
    model: str = "qwen-coder"                   # Alias del modelo en LiteLLM
    api_key: str = "local"                      # API key (usar "local" para setups locales)
    timeout: int = 120                          # Segundos antes de fallback
    max_tokens_generate: int = 2048             # Para tareas GENERATE
    max_tokens_modify: int = 2048               # Para tareas MODIFY
    max_tokens_correct: int = 2048              # Para tareas CORRECT
    max_tokens_integrate: int = 2048            # Para tareas INTEGRATE
```

---

## 12. Errores Comunes y Soluciones

### "NOT_STATED: cannot classify declaration into any of the five task types"

**Causa:** La declaración no contiene ninguna keyword reconocida.

**Solución:** Usar una de las keywords de activación del tipo de tarea deseado.

```
# Incorrecto — sin keyword
> revisar database.py

# Correcto
> fix the connection leak in database.py
```

---

### "NOT_STATED: declaration is ambiguous between task types"

**Causa:** Dos tipos de tarea obtuvieron el mismo score de keywords.

**Solución:** Ser más específico. Eliminar keywords del tipo no deseado.

```
# Ambiguo — "fix" (CORRECT) y "refactor" (MODIFY) empatan
> fix and refactor the parser

# Claro
> refactor parser.py to split the tokenizer into a separate method
```

---

### "NOT_STATED: scope_hint does not match any file or module"

**Causa:** El archivo mencionado en la declaración no existe en el proyecto.

**Solución:** Usar `status` para ver el inventario y corregir el nombre del archivo.

---

### "MODIFY target not found" / "CORRECT target not found"

**Causa:** El archivo fue eliminado después de cargar el proyecto.

**Solución:** Ejecutar `reload` para reconstruir el modelo, luego reintentar.

---

### "BETO_GAP [ESCALADO]: target outside project_root"

**Causa:** La tarea intentaría escribir fuera del directorio del proyecto.

**Solución:** Asegurarse de que el destino esté dentro del proyecto. Las rutas absolutas fuera del project_root no están permitidas.

---

### "REORGANIZE: cannot extract source → destination"

**Causa:** El parser de REORGANIZE no pudo identificar origen y destino.

**Solución:** Usar el formato explícito: `move <origen> to <destino>`

---

### El LLM escribe el contenido incorrecto en INTEGRATE

**Causa más común:** El módulo a integrar (`cache.py`, por ejemplo) no fue mencionado por nombre en la descripción y por tanto no llegó como contexto al LLM.

**Solución:** Mencionar el nombre exacto del archivo del módulo a integrar en la descripción de la tarea.

```
# Podría fallar — sin nombre de archivo del módulo
> integrate the cache into processor.py

# Correcto — nombre de archivo explícito
> integrate the cache module into processor.py using Cache.get and Cache.set
```

---

## 13. Referencia Rápida

```bash
# Instalación
cd src
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip setuptools && pip install -e .

# Iniciar
dev-assistant /ruta/al/proyecto

# Tipos de tarea con ejemplos
fix the NameError in calculator.py
modify config.py to load settings from environment variables
create a new text_cleaner module
move helpers.py to utils/helpers.py
integrate cache.py into processor.py using Cache.get and Cache.set

# Restaurar estado antes de una ejecución
restore EXEC-3A1B2C4D5E6F7G8H

# Artefactos generados por ejecución
<proyecto>/.beto_state/<EXEC-ID>/               ← backup previo a la modificación
<proyecto>/.beto_reports/<EXEC-ID>.json         ← reporte de ejecución
<proyecto>/.beto_reports/<EXEC-ID>_eval.json    ← evaluación del output (Fase 5)
<proyecto>/.beto_reports/<EXEC-ID>_test.json    ← resultado de tests (Fase 6)
<proyecto>/.beto_reports/<EXEC-ID>_restore.json ← reporte de restore (si aplica)
```

---

## 14. BETO v4.3 — Operational Semantic Closure (OSC)

### 14.1 El Problema que Resuelve

BETO v4.2 garantiza separación entre DECLARED, NOT_STATED e INFERRED. Detecta lo no declarado y lo bloquea. Sin embargo, una OQ puede:

- estar respondida
- estar alineada con el SYSTEM INTENT
- no violar BETO

y aun así ser inútil para implementación real porque contiene respuestas blandas como "alta confianza", "usar estándar", "cuando sea necesario", "según contexto".

BETO v4.3 añade control sobre la **calidad operativa** de lo declarado.

### 14.2 Nuevos Estados

| Estado | Significado |
|--------|-------------|
| `DECLARED_RAW` | Respuesta existe pero no es operativamente suficiente |
| `DECLARED_EXECUTABLE` | Respuesta es implementable sin inferencias relevantes |
| `DECLARED_WITH_LIMITS` | Respuesta es usable con ambigüedad controlada y aceptada |

### 14.3 Tipología de OQs (obligatoria)

Toda OQ debe clasificarse con exactamente uno de estos tipos:

| Tipo | Aplica a |
|------|---------|
| `OQ_CONFIG` | Parámetros de configuración, umbrales, límites |
| `OQ_POLICY` | Reglas de negocio, criterios de decisión, prioridades |
| `OQ_EXECUTION` | Flujo, secuencias, triggers, orquestación |
| `OQ_EXCEPTION` | Manejo de errores, fallback, casos de borde |
| `OQ_DATA_SEMANTICS` | Significado de campos, formatos, convenciones |
| `OQ_INTERFACE` | Contratos de E/S, APIs, formatos de intercambio |
| `OQ_OBSERVABILITY` | Logging, métricas, trazas, monitoreo |

**Regla:** OQ_POLICY, OQ_EXECUTION, OQ_EXCEPTION, OQ_DATA_SEMANTICS no pueden cerrarse con texto libre simple.

### 14.4 EXECUTION_READINESS_CHECK

Validador obligatorio para OQs críticas. Evalúa 8 campos:

| Campo | Pregunta |
|-------|---------|
| `alcance` | ¿Sobre qué aplica exactamente? |
| `trigger` | ¿Cuándo aplica? ¿Qué lo activa? |
| `input` | ¿Qué datos o condiciones recibe? |
| `output` | ¿Qué produce o decide? |
| `constraint` | ¿Qué restricciones duras aplican? |
| `fallback` | ¿Qué ocurre si no se puede aplicar? |
| `exception` | ¿Qué casos de excepción existen? |
| `trazabilidad` | ¿Hay ID de trazabilidad asignable? |

Resultados posibles:

| Resultado | Promoción |
|-----------|-----------|
| `PASS_EXECUTABLE` | → `DECLARED_EXECUTABLE` |
| `PASS_WITH_LIMITS` | → `DECLARED_WITH_LIMITS` |
| `FAIL_EXECUTIONAL_GAP` | → `DECLARED_RAW` + `BETO_GAP_EXECUTIONAL` |

### 14.5 Gate G-2B — Operational Readiness Gate

Subgate del Paso 6. No es un gate humano — es el resultado del EXECUTION_READINESS_CHECK.

**Pregunta:** ¿Las declaraciones críticas son ejecutables sin inferencias relevantes?

| Resultado | Condición |
|-----------|-----------|
| `APPROVED_EXECUTABLE` | Todas las OQs críticas en DECLARED_EXECUTABLE |
| `APPROVED_WITH_LIMITS` | Alguna en DECLARED_WITH_LIMITS, ninguna en DECLARED_RAW |
| `BLOCKED_BY_EXECUTIONAL_GAPS` | Una o más OQs críticas en DECLARED_RAW |

En **BETO_PARALELO**: G-2B se evalúa por unidad — no bloquea globalmente.

### 14.6 CIERRE_ASISTIDO_OPERATIVO

El Paso 6 se actualiza de CIERRE_ASISTIDO a CIERRE_ASISTIDO_OPERATIVO.

Artefactos generados:
- `CIERRE_ASISTIDO_OPERATIVO.md` — artefacto principal con estados finales por OQ
- `EXECUTION_INTENT_MAP.md` — mapa consolidado de ejecutabilidad
- `EXECUTIONAL_GAP_REGISTRY.md` — registro de gaps execucionales (si hay)

### 14.7 Política Anti-Perfeccionismo

- No buscar completitud absoluta — buscar ejecutabilidad suficiente
- Ambigüedad tolerable → `DECLARED_WITH_LIMITS` (no falla)
- `max_operational_requestions = 2` por OQ crítica
- Después de 2 repreguntas sin mejora: `DECLARED_RAW` permanente

### 14.8 Templates Nuevos

| Template | Propósito |
|----------|-----------|
| `OQ_RESPONSE_EXECUTABLE.md` | EXECUTION_READINESS_CHECK para una OQ individual |
| `EXECUTION_INTENT_MAP.md` | Mapa consolidado de ejecutabilidad del sistema |
| `CONFLICT_RESOLUTION_TABLE.md` | Resolución de conflictos operativos |
| `AMBIGUITY_RESIDUE_REPORT.md` | Registro formal de ambigüedad residual aceptada |
| `EXECUTIONAL_GAP_REGISTRY.md` | Registro centralizado de BETO_GAP_EXECUTIONAL |

### 14.9 Compatibilidad

BETO v4.3 es **completamente aditivo**:
- El núcleo v4.2 no cambia
- Los estados DECLARED, NOT_STATED, INFERRED no cambian
- Los gates G-1, G-2, G-3, G-4 no cambian
- Los ciclos v4.2 existentes son compatibles sin modificación
- Los campos OSC en BETOState tienen defaults seguros (backward-compatible)

---

*Framework BETO v4.3 — Alberto Ramírez — 2026*

---

## 15. BETO v4.4 — Execution Efficiency and Routing Layer

### 15.1 Introducción

BETO v4.4 introduce una capa de routing interno y eficiencia de ejecución que optimiza cómo ejecuta BETO sin alterar qué significa BETO. El núcleo semántico, las reglas de no invención, la trazabilidad y la compatibilidad con BETO v4.3 y OSC se preservan completamente.

El problema que resuelve: BETO, por su riqueza estructural y el crecimiento de artefactos, tiende a operar con demasiado contexto por llamada al modelo. V4.4 introduce contexto mínimo autorizado por subproblema mediante un sistema de routing determinista.

Adicionalmente, v4.4 absorbe las tareas simples dentro del executor unificado, eliminando la necesidad de mantener una pieza externa separada.

### 15.2 Sistema de routing interno

El **EXECUTION_ROUTER** evalúa cada subproblema mediante una función de complejidad:

```
complexity_score =
  w1*num_outputs + w2*num_entities + w3*num_dependencies +
  w4*ambiguity_level + w5*need_for_graph + w6*oq_critical_count +
  w7*cross_module_scope + w8*lifecycle_scope
```

Pesos por defecto (v4.4): w1=1, w2=1, w3=1, w4=2, w5=3, w6=2, w7=2, w8=2

| Score | Ruta | Uso |
|-------|------|-----|
| 0–5 | BETO_LIGHT_PATH | Tareas simples, salida puntual |
| 6–12 | BETO_PARTIAL_PATH | Tareas medianas o localizadas |
| 13+ | BETO_FULL_PATH | Sistemas completos, arquitectura nueva |

### 15.3 Contexto estratificado (3 capas)

| Capa | Nombre | Contenido |
|------|--------|-----------|
| A | STABLE_CORE_CONTEXT | Instructivo, reglas nucleares, templates invariantes (prefix-cacheable) |
| B | CYCLE_CONTEXT | BETO_CORE activo, paso actual, OQs activas, estado de routing |
| C | LOCAL_EXECUTION_CONTEXT | Archivo, template, phase, OQ — específico del subproblema |

Regla: toda llamada incluye solo A + B mínimo + C. No se envía contexto global completo si el subproblema puede resolverse localmente.

### 15.4 Snapshots persistentes

Almacenados en `.beto/snapshots/`. Se invalidan cuando cambian sus fuentes de autoridad.

- CYCLE_CONTEXT_SNAPSHOT — estado del ciclo en un momento
- ACTIVE_OQ_SET — OQs relevantes para el tramo actual
- LOCAL_EXECUTION_CONTEXT — contexto puntual del subproblema
- MATERIALIZATION_SCOPE — qué materializar en el tramo

### 15.5 PROJECT_INDEX

Archivo JSON persistente en `.beto/project_index.json`. Schema en `framework/PROJECT_INDEX_SCHEMA.json`. Permite localizar artefactos sin exploración global. Es fuente operativa de localización, NO autoridad semántica.

### 15.6 MODEL_CALL_PLAN y EXECUTION_PERFORMANCE_LOG

Todo llamada al modelo está gobernada por MODEL_CALL_PLAN (incluye contexto, snapshots, cache eligibility, fallback, trace). Logueada en EXECUTION_PERFORMANCE_LOG para auditoría de eficiencia.

### 15.7 Subejecutores (10)

eligibility_executor, interview_executor, closure_executor, osc_executor, materialization_executor, verification_executor, beto_light_executor, beto_partial_executor, beto_full_executor, route_promotion_evaluator. Todos bajo el orquestador unificado — no pueden llamarse entre sí sin pasar por él.

### 15.8 Nuevos templates (11)

EXECUTION_ROUTER.md, ROUTING_DECISION_RECORD.md, ROUTE_PROMOTION_RECORD.md, EXECUTION_MODE_POLICY.md, CYCLE_CONTEXT_SNAPSHOT.md, ACTIVE_OQ_SET.md, LOCAL_EXECUTION_CONTEXT.md, MATERIALIZATION_SCOPE.md, MODEL_CALL_PLAN.md, PROJECT_INDEX_SCHEMA.json, EXECUTION_PERFORMANCE_LOG.md

### 15.9 Compatibilidad

BETO v4.4 es completamente aditivo. El núcleo v4.2, la capa OSC v4.3 y todos los gates no cambian. Los ciclos v4.3 existentes son compatibles sin modificación. Todos los campos nuevos tienen safe defaults.

---

## 16. BETO v4.5 — Capa de Persistencia SQLite

### 16.1 Propósito

BETO v4.5 cierra la migración de persistencia que v4.4 dejó pendiente. El Executor opera ahora con SQLite como única fuente de verdad para todo el estado de ciclo en runtime. Los archivos JSON que funcionaban como base de datos implícita han sido convertidos en proyecciones derivadas: se generan cuando hace falta, no se leen durante la ejecución.

El protocolo BETO, los 11 pasos, los gates, los estados epistémicos y todos los artefactos formales no cambian. v4.5 es una migración de la capa de almacenamiento interno del Executor — no del protocolo.

---

### 16.2 El problema que resuelve

La persistencia basada en archivos JSON presentaba tres limitaciones estructurales:

**Sin garantías transaccionales.** Un fallo a mitad de un paso podía dejar `BETO_STATE.json`, los registros de routing y los snapshots en estados mutuamente inconsistentes. La detección requería `parity_check.py`, que actúa después del daño.

**Sin capa de consulta.** Acceder al historial de OQs, decisions de gate o routing entre ciclos requería parsear archivos. No había forma eficiente de consultar qué OQs críticas seguían abiertas o cuántas decisiones de gate había tomado el operador en un ciclo.

**Reconstrucción de estado frágil.** `BETOStateWriter` leía `BETO_STATE.json` al inicio de cada paso para no perder trabajo previo. Si el archivo estaba corrupto o ausente, el estado se perdía. El conteo de snapshots se reseteaba entre reinicios de proceso.

---

### 16.3 Capa de persistencia transversal (`persistence/`)

La capa vive en `beto_executor/src/persistence/` — separada del `execution_router/` porque almacena más que routing: ciclos, snapshots, OQs, gates, artefactos y llamadas al modelo.

```
persistence/
├── schema.py                   ← DDL, init_db(), migraciones por columna
├── connection.py               ← get_connection(beto_dir)
├── queries.py                  ← capa de lectura
├── writers/
│   ├── cycle_writer.py         ← CycleWriter: ensure_project, write_cycle, update_*
│   ├── routing_writer.py       ← RoutingWriter: decisiones y promociones
│   ├── snapshot_writer.py      ← SnapshotDBWriter: write, invalidate
│   ├── oq_writer.py            ← OQWriter: sync_from_dicts, sync_from_beto_state
│   ├── gate_writer.py          ← GateWriter: write
│   └── artifact_writer.py      ← ArtifactDBWriter: write (upsert)
├── readers/
│   └── state_reader.py         ← build_state_payload(beto_dir, cycle_id)
└── migrate/
    └── legacy_json_backfill.py ← migrate_project(beto_dir)
```

**Diseño de conexión:** `get_connection(beto_dir)` abre una conexión nueva por operación con WAL mode y foreign keys habilitados. No hay conexión compartida entre writers — compatible con el modelo de ejecución single-process de BETO sin requerir gestión de estado de conexión.

**Schema:** 11 tablas — `projects`, `cycles`, `routing_decisions`, `route_promotions`, `snapshots`, `open_questions`, `beto_gaps`, `gate_decisions`, `artifacts`, `model_calls`, `schema_version`. `init_db()` es idempotente: safe to call en cada inicio de ciclo.

---

### 16.4 Ensamblador canónico: `build_state_payload()`

```python
from persistence.readers.state_reader import build_state_payload
payload = build_state_payload(beto_dir, cycle_id)
```

Devuelve el estado canónico del ciclo construido desde SQLite. Incluye:

- Campos Phase 2: `cycle_id`, `project_id`, `route_mode`, `system_intent`, `system_boundaries`, `stable_decisions`, `open_questions`, `resolved_questions`, `routing`, `artifacts`, `gates`, `metadata`
- Aliases legacy para compatibilidad: `ciclo_id`, `paso_actual`, `oqs_abiertas`, `oqs_cerradas`
- `metadata.rendered_from = "sqlite"` — siempre

`BETO_STATE.json` es el resultado de escribir este payload al disco, complementado con campos extraídos de markdown (`nodos`, campos OSC) que aún no tienen columnas SQLite propias.

---

### 16.5 Modo SQLite-only en `BETOStateWriter`

**Carga de estado inicial (`_load_or_create`):**
Lee desde tablas `cycles` y `open_questions`. Si la base de datos no existe, retorna un `BETOState` vacío. Si el ciclo no está registrado, retorna un `BETOState` vacío. Los nodos y campos OSC se re-extraen de artefactos markdown en cada paso.

**Auto-creación de base de datos:**
Si `beto.db` no existe al momento de `update()`, se crea automáticamente con `init_db()`. No hay configuración manual requerida.

**Política de render (sin fallback):**
```
init_db() si ausente
→ _push_to_db(state, paso)      ← no-fatal: warning en stderr si falla
→ _do_phase4_render(state)      ← raise inmediato si falla — sin fallback
```

En v4.4 existía un sistema de fallback con `fallback_reason = DB_NOT_FOUND | PHASE2_RENDER_FAILED` y un modo strict configurable via `BETO_STRICT_PHASE2`. Ambos fueron eliminados en v4.5: el sistema siempre falla explícitamente si el render falla.

**Gates desde SQLite (`_load_gates_from_db`):**
Reemplaza `_update_from_state_json()` que leía el Gestor de Ciclo JSON (`{ciclo_id}.json`). Las decisiones de gate se cargan desde la tabla `gate_decisions` y se convierten al formato legacy `decisiones_gate`.

---

### 16.6 Hookup de GateWriter en el motor

Cada vez que `GatesOperador.procesar_gate()` devuelve una decisión, el motor persiste el resultado en SQLite:

```python
resultado = self.gates.procesar_gate(self.ciclo_id, señal)
# → GateWriter.write(beto_dir, cycle_id, gate_id, decision, paso)
```

La decisión del operador ("aprobado" / "rechazado") se normaliza a "APPROVED" / "REJECTED" antes de persistir. La operación es no-fatal — un fallo de escritura emite un warning y no bloquea la ejecución.

---

### 16.7 Routing y snapshots: backend único

**Routing decisions y promotions:**
`ExecutionRouter._persist_decision()` y `_persist_promotion()` escriben exclusivamente a SQLite. Los directorios `.beto/routing/decisions/` y `.beto/routing/promotions/` ya no se crean ni escriben en runtime.

**Snapshots:**
`SnapshotWriter` (en `execution_router/`) ya no escribe archivos. Su rol es generar IDs únicos y cargar contadores desde la tabla `snapshots` al inicializar — garantizando que IDs no se reusen en ciclos reanudados. La escritura a DB la ejecuta `SnapshotDBWriter` (en `persistence/writers/`).

**ProjectIndexExporter:**
`ProjectIndexWriter` fue renombrado a `ProjectIndexExporter`. El método principal es `export()`. Tanto `write()` como `ProjectIndexWriter` se preservan como aliases de compatibilidad — el código existente no requiere cambios.

---

### 16.8 Backfill de proyectos legacy

Para proyectos ejecutados bajo v4.3/v4.4 que tienen sus datos en JSON:

```python
from persistence.migrate.legacy_json_backfill import migrate_project
report = migrate_project(Path(".beto"))
print(report.summary())
```

`migrate_project(beto_dir)` escanea la estructura estándar:

| Fuente | Destino |
|---|---|
| `{cycle_dir}/BETO_STATE.json` | tablas `cycles`, `open_questions`, `gate_decisions` |
| `.beto/routing/decisions/*.json` | tabla `routing_decisions` |
| `.beto/routing/promotions/*.json` | tabla `route_promotions` |
| `.beto/snapshots/*.json` | tabla `snapshots` |
| `.beto/project_index.json` | tabla `artifacts` |

La operación es idempotente (`INSERT OR IGNORE` en todas las escrituras) y no destructiva (no modifica ni elimina los archivos JSON fuente). El `BackfillReport` devuelto incluye conteos por tabla y warnings sobre datos no encontrados.

---

### 16.9 Herramienta de auditoría: `parity_check`

`persistence/parity_check.py` es ahora una herramienta de auditoría manual, no un mecanismo de runtime. Su semántica en v4.5:

- Registros presentes en JSON pero ausentes de DB → divergencia reportada (indica un write a DB que se perdió)
- Registros presentes solo en DB → estado correcto en v4.5, no reportado

Se puede invocar sobre cualquier ciclo para verificar que un backfill fue completo o que no quedan archivos JSON legacy sin importar.

---

### 16.10 Compatibilidad y migración

| Elemento | Estado |
|---|---|
| `BETO_STATE.json` | Compatible — sigue existiendo como proyección renderizada |
| `ProjectIndexWriter` | Compatible — alias a `ProjectIndexExporter` |
| `write()` en project_index | Compatible — alias a `export()` |
| Ciclos v4.3/v4.4 | Migrables con `migrate_project()` — operación segura e idempotente |
| Nuevas dependencias | Ninguna — sqlite3 stdlib |
| Protocolo BETO | Sin cambios |

---

*Framework BETO v4.5 — Alberto Ramírez — 2026*

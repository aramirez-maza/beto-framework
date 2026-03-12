# BETO_SYSTEM_GRAPH.md
## BETO Framework v4.2 — Grafo del Sistema
### Arquitecto: BETO Framework v4.2 Graph Architect
### Input: BETO_CORE_INTERVIEW_COMPLETED.md + STRUCTURAL_CLASSIFICATION_REGISTRY.md
### Estado: VALIDATED | Versión: 1.0.0 | Fecha: 2025-01-31

---

## PREÁMBULO DEL ARQUITECTO

Este documento constituye el grafo canónico del sistema BETO v2. Toda decisión estructural está trazable a la entrevista completada o al registro de clasificación. Las resoluciones de OQs de la entrevista son verdad inmutable en este grafo; no se reabren. Los nodos PARALLEL son las unidades de entrega autónoma. Los SUBBETO son sub-nodos con diseño propio pero entrega dependiente de su padre. Los INTERNAL son componentes de implementación sin nodo propio. Los SHARED CONCERN son restricciones transversales que todo nodo debe respetar.

**Convención de identificadores**:
- Nodos PARALLEL: `P-NN`
- Sub-nodos SUBBETO: `P-NN.M`
- Shared Concerns: `SC-NN`
- Aristas: `E-NNN`

---

## PARTE I: INVENTARIO DE NODOS

### I.1 Nodos PARALLEL (Unidades de Entrega Autónoma)

| ID | Nombre Canónico | Módulo Principal | TIS | Origen Clasificación |
|----|-----------------|-----------------|-----|---------------------|
| `P-01` | Presentation Layer | `beto/static/` | 3/3 | C-01 → PARALLEL |
| `P-02` | API Layer | `beto/api/` | 3/3 | C-02 → PARALLEL |
| `P-03` | Orchestrator | `beto/orchestrator/pipeline_engine.py` | 3/3 | C-03 → PARALLEL |
| `P-04` | Event Bus | `beto/events/` | 3/3 | C-04 → PARALLEL |
| `P-05` | Plugin Layer | `beto/plugins/` | 3/3 | C-05 → PARALLEL |
| `P-06` | Persistence Layer | `beto/persistence/` | 3/3 | C-06 → PARALLEL |
| `P-07` | Gate Manager | `beto/orchestrator/gate_manager.py` | 3/3 | C-10 → PARALLEL |

**Total nodos PARALLEL: 7**

---

### I.2 Sub-nodos SUBBETO

| ID | Nombre Canónico | Nodo Padre | Módulo | TIS | Origen Clasificación |
|----|-----------------|-----------|--------|-----|---------------------|
| `P-01.1` | SSE Client | `P-01` | `beto/static/js/sse-client.js` | 3/3 | C-21 → SUBBETO(P-01) |
| `P-01.2` | API Client | `P-01` | `beto/static/js/api-client.js` | 3/3 | C-22 → SUBBETO(P-01) |
| `P-01.3` | Gate Panel UI | `P-01` | `beto/static/js/app.js` (sección gate) | 2/3 | C-23 → SUBBETO(P-01) |
| `P-03.1` | Project Manager | `P-03` | `beto/orchestrator/project_manager.py` | 2/3 | C-07 → SUBBETO(P-03) |
| `P-03.2` | Stage Execution Engine | `P-03` | `beto/orchestrator/pipeline_engine.py` (métodos run_stage) | 2/3 | C-09 → SUBBETO(P-03) |
| `P-05.1` | LLM Plugin Interface (ABCs) | `P-05` | `beto/plugins/base.py` | 2/3 | C-11 → SUBBETO(P-05) |
| `P-05.2` | OpenAI Adapter | `P-05` | `beto/plugins/adapters/openai_adapter.py` | 3/3* | C-12 → SUBBETO(P-05) |
| `P-05.3` | Ollama Adapter | `P-05` | `beto/plugins/adapters/ollama_adapter.py` | 3/3* | C-13 → SUBBETO(P-05) |
| `P-05.4` | LM Studio Adapter | `P-05` | `beto/plugins/adapters/lmstudio_adapter.py` | 2/3 | C-14 → SUBBETO(P-05) |
| `P-06.1` | JSON Store (atomic_write) | `P-06` | `beto/persistence/json_store.py` | 3/3* | C-24 → SUBBETO(P-06) |

*TIS 3/3 con decisión de SUBBETO por razonamiento de granularidad documentado en registro de clasificación.

**Total sub-nodos SUBBETO: 10**

---

### I.3 Componentes INTERNAL (No elevados a nodo)

| ID Origen | Nombre | Absorbido por | Justificación |
|-----------|--------|--------------|---------------|
| C-08 | Run Manager | `P-03` + `P-06` | Lógica de ejecución en P-03; estado persistido en P-06 |
| C-15 | Reasoning Engine ABC | `P-05.1` | Extensión de jerarquía de contratos, no componente operativo |
| C-16 | Code Engine ABC | `P-05.1` | Extensión de jerarquía de contratos, no componente operativo |
| C-17 | Pipeline State Machine | `P-03` | Lógica interna del Pipeline Engine |
| C-18 | Gate State Machine | `P-07` | Lógica interna del Gate Manager |
| C-20 | GUI Static Server | `P-02` | Configuración de FastAPI (`app.mount`), no componente independiente |
| C-25 | Crash Recovery / Reconciliation | `P-03.1` | Operación de startup de Project Manager |
| C-26 | Plugin Roles Store | `P-06` + `P-05` | Artefacto de datos; lectura en P-06, interpretación en P-05 |

---

### I.4 Shared Concerns (Restricciones Transversales)

| ID | Nombre | Nodos Afectados | Descripción |
|----|--------|----------------|-------------|
| `SC-01` | Atomic Write | `P-06`, `P-03`, `P-07` | Todo JSON se escribe vía `atomic_write()` (OQ-003 resuelto). Nunca escritura directa. |
| `SC-02` | Structured Logging | Todos los nodos | Logs estructurados (JSON) en cada operación relevante. Auditoría de decisiones del operador. |
| `SC-03` | Async-first Contract | `P-03`, `P-04`, `P-05`, `P-07` | Todo código en runtime asyncio. Plugins sync → wrapper automático en PluginRegistry (OQ-002 resuelto). |
| `SC-04` | Domain Types | `P-02`, `P-03`, `P-05`, `P-06`, `P-07` | `PipelineContext`, enumeraciones de estado, schemas Pydantic son tipos compartidos definidos en `beto/persistence/models.py` y `beto/api/schemas.py`. |
| `SC-05` | No Code Execution | Todos los nodos | BETO v2 no ejecuta código generado. El output de stages `code_generation` es texto. (OQ-001 resuelto). |

---

## PARTE II: ESPECIFICACIÓN DE NODOS PARALLEL

### P-01 — Presentation Layer

```
┌─────────────────────────────────────────────────────────────────┐
│  NODO: P-01 Presentation Layer                                  │
│  ─────────────────────────────────────────────────────────────  │
│  Módulo:      beto/static/                                      │
│  Tipo:        PARALLEL                                          │
│  Entregable:  index.html + css/style.css + js/{app,sse,api}.js  │
│  Propósito:   GUI web sin frameworks JS para operación del      │
│               sistema. Única interfaz de interacción humana.    │
│                                                                 │
│  RESPONSABILIDADES PROPIAS:                                     │
│  • Renderizar estado de proyectos y runs en tiempo real         │
│  • Mostrar y gestionar Gate Panel para decisiones del operador  │
│  • Permitir hot-swap de plugins desde GUI                       │
│  • Conectar a SSE stream (primario) con fallback a polling      │
│  • Enviar decisiones de gate via REST                           │
│                                                                 │
│  ANTI-RESPONSABILIDADES:                                        │
│  • NO ejecuta lógica de negocio                                 │
│  • NO mantiene estado persistente (solo estado de UI en memoria)│
│  • NO usa frameworks JS (React, Vue, Angular)                   │
│  • NO renderiza código ejecutable (SC-05)                       │
│                                                                 │
│  SUB-NODOS:                                                     │
│  • P-01.1  SSE Client (sse-client.js)                          │
│  • P-01.2  API Client (api-client.js)                          │
│  • P-01.3  Gate Panel UI (sección en app.js)                   │
│                                                                 │
│  CONTRATOS DE ENTRADA:                                          │
│  • HTTP GET  /api/projects, /api/runs/*, /api/gates/pending     │
│  • SSE GET   /api/events, /api/events/{project_id}              │
│                                                                 │
│  CONTRATOS DE SALIDA:                                           │
│  • HTTP POST /api/projects/{id}/runs                            │
│  • HTTP POST /api/gates/{id}/decide                             │
│  • HTTP PUT  /api/plugins/roles/{role}                          │
│  • HTTP POST /api/runs/{id}/cancel                              │
│                                                                 │
│  DEPENDENCIAS DE NODO (consume API de):                         │
│  • P-02 (API Layer) — todos los contratos HTTP/SSE              │
│                                                                 │
│  SHARED CONCERNS APLICABLES:                                    │
│  • SC-05 (No Code Execution)                                    │
└─────────────────────────────────────────────────────────────────┘
```

**Sub-nodo P-01.1 — SSE Client**

```
Archivo:    beto/static/js/sse-client.js
Propósito:  Gestionar conexión SSE con fallback automático a polling.
Contrato:   connect(onEvent: Function) → void
            disconnect() → void
Comportamiento:
  1. Intentar EventSource('/api/events')
  2. En error tras 3 fallos → degradar a polling cada 2000ms
  3. En polling → fetch('/api/runs/active') → emitir evento tipo 'poll_update'
Configuración: pollingIntervalMs (default: 2000, OBJ-03: latencia ≤ 2s)
```

**Sub-nodo P-01.2 — API Client**

```
Archivo:    beto/static/js/api-client.js
Propósito:  Wrapper fetch() tipado para todos los endpoints REST.
Contrato:   Expone métodos async por recurso:
              projects.list(), projects.create(), projects.startRun()
              gates.getPending(), gates.decide(id, decision)
              plugins.getRoles(), plugins.swapRole(role, pluginId)
              runs.getActive(), runs.cancel(id)
```

**Sub-nodo P-01.3 — Gate Panel UI**

```
Archivo:    beto/static/js/app.js (sección GatePanel)
Propósito:  Componente UI de aprobación de gates.
Comportamiento:
  • Escucha evento SSE 'gate_created' → muestra panel modal/overlay
  • Muestra: prompt_to_operator, output del stage, tipo de gate
  • Opciones: [Aprobar] [Rechazar*] [Aprobar con modificaciones*]
    * requieren campo 'notes' (textarea, obligatorio en rechazo)
  • Para MODIFIED: muestra editor (textarea monospace) por campo editable
    según tipo de stage (OQ-005 resuelto):
      reasoning     → output.reasoning_text, output.conclusions
      code_gen      → output.code, output.language, output.explanation
      code_review   → output.review_notes, output.approved, output.suggestions
      custom        → output.content
  • Submit → api-client.gates.decide(id, {decision, notes, modified_output})
  • Escucha evento SSE 'gate_resolved' → cierra panel
```

---

### P-02 — API Layer

```
┌─────────────────────────────────────────────────────────────────┐
│  NODO: P-02 API Layer                                           │
│  ─────────────────────────────────────────────────────────────  │
│  Módulo:      beto/api/ + beto/main.py                          │
│  Tipo:        PARALLEL                                          │
│  Entregable:  FastAPI app con todos los routers + schemas        │
│  Propósito:   Traducción HTTP↔Dominio. Punto de entrada único   │
│               para GUI y contratos REST/SSE.                    │
│                                                                 │
│  RESPONSABILIDADES PROPIAS:                                     │
│  • Definir y registrar todos los endpoints REST (Sección 3.1)   │
│  • Validación de request/response vía schemas Pydantic          │
│  • Montar StaticFiles para servir P-01                          │
│  • Registrar endpoint SSE (/api/events) que consume P-04        │
│  • Traducir errores de dominio a HTTP status codes              │
│  • NO contiene lógica de negocio (delega a P-03, P-05, P-07)   │
│                                                                 │
│  ANTI-RESPONSABILIDADES:                                        │
│  • NO ejecuta pipelines                                         │
│  • NO gestiona plugins directamente                             │
│  • NO escribe JSON directamente (delega a P-06)                 │
│                                                                 │
│  ARCHIVOS:                                                      │
│  • beto/main.py            — FastAPI app factory, mounts        │
│  • beto/api/schemas.py     — Todos los modelos Pydantic         │
│  • beto/api/routes/        — Un router por recurso:             │
│      projects.py, runs.py, gates.py, plugins.py, events.py      │
│                                                                 │
│  CONTRATOS DE ENTRADA (desde P-01):                             │
│  • Ver Sección 3.1 de la entrevista (tabla completa de endpoints)│
│                                                                 │
│  CONTRATOS DE SALIDA (llama a):                                 │
│  • P-03.1 ProjectManager: create_project, start_run, cancel_run │
│  • P-04 EventBus:         subscribe() para SSE fan-out          │
│  • P-05 PluginRegistry:   list_plugins, assign_role, health     │
│  • P-06 Persistence:      read para GET endpoints               │
│  • P-07 GateManager:      get_pending_gates, process_decision   │
│                                                                 │
│  SCHEMAS PYDANTIC CRÍTICOS (del INTERNAL C-20 absorbido):       │
│  • GateDecision (con validador MODIFIED→modified_output)        │
│  • RunCreate (initial_input + pipeline_config_override)         │
│  • PluginRoleUpdate                                             │
│  • ProjectCreate, ProjectUpdate                                 │
│  • RunSummary, RunDetail, ProjectSummary                        │
│                                                                 │
│  SHARED CONCERNS APLICABLES:                                    │
│  • SC-03 (Async-first: todos los handlers son async def)        │
│  • SC-04 (Domain Types: importa de persistence/models.py)       │
└─────────────────────────────────────────────────────────────────┘
```

---

### P-03 — Orchestrator

```
┌─────────────────────────────────────────────────────────────────┐
│  NODO: P-03 Orchestrator                                        │
│  ─────────────────────────────────────────────────────────────  │
│  Módulo:      beto/orchestrator/                                │
│  Tipo:        PARALLEL                                          │
│  Entregable:  pipeline_engine.py + project_manager.py           │
│  Propósito:   Motor de ejecución de pipelines. Coordina stages, │
│               plugins, gates y proyectos concurrentes.          │
│                                                                 │
│  RESPONSABILIDADES PROPIAS:                                     │
│  • Ejecutar stages del pipeline en orden según PipelineConfig   │
│  • Gestionar asyncio.Tasks por run (concurrencia multi-proyecto)│
│  • Resolver plugins en late-binding (OQ-006 resuelto)           │
│  • Gestionar retries de stage con feedback del operador (OQ-008)│
│  • Acumular PipelineContext entre stages                        │
│  • Ejecutar crash recovery en startup (OQ-003 aplicado)         │
│  • Emitir eventos al EventBus en cada transición de estado      │
│                                                                 │
│  ANTI-RESPONSABILIDADES:                                        │
│  • NO gestiona el gate en sí (delega a P-07)                   │
│  • NO invoca LLM directamente (delega a P-05)                   │
│  • NO persiste directamente (delega a P-06)                     │
│  • NO sirve HTTP (delega a P-02)                                │
│                                                                 │
│  SUB-NODOS:                                                     │
│  • P-03.1  Project Manager (project_manager.py)                 │
│  • P-03.2  Stage Execution Engine (métodos run_stage en engine) │
│                                                                 │
│  CONTRATOS DE ENTRADA (llamado por P-02):                       │
│  • start_run(project_id, initial_input) → Run                   │
│  • cancel_run(run_id) → Run                                     │
│  • get_active_runs() → List[RunSummary]                         │
│                                                                 │
│  CONTRATOS DE SALIDA (llama a):                                 │
│  • P-04 EventBus.publish(event) en cada transición              │
│  • P-05 PluginRegistry.get_for_role(role) → LLMPlugin           │
│  • P-06 Persistence.atomic_write / read (vía json_store)        │
│  • P-07 GateManager.create_gate / wait_for_decision             │
│                                                                 │
│  INTERNAL ABSORBIDOS:                                           │
│  • C-08 Run Manager → lógica de estado en pipeline_engine.py   │
│  • C-17 Pipeline State Machine → implementación interna         │
│  • C-25 Crash Recovery → P-03.1.reconcile() en startup          │
│                                                                 │
│  CONFIGURACIÓN RELEVANTE (config.yaml):                         │
│  • pipeline.max_stage_retries: 3 (OQ-008 resuelto)             │
│  • pipeline.gate_timeout_hours: null (OQ-009 resuelto)          │
│  • pipeline.gate_timeout_action: "cancel_run"                   │
│                                                                 │
│  SHARED CONCERNS APLICABLES:                                    │
│  • SC-01 (Atomic Write — via P-06)                              │
│  • SC-02 (Structured Logging en cada transición de estado)      │
│  • SC-03 (Async-first: todo código es async)                    │
│  • SC-04 (Domain Types: PipelineContext, RunStatus, etc.)       │
└─────────────────────────────────────────────────────────────────┘
```

**Sub-nodo P-03.1 — Project Manager**

```
Archivo:    beto/orchestrator/project_manager.py
Propósito:  Coordinar ciclo de vida de proyectos y runs concurrentes.
Responsabilidades:
  • Crear/archivar proyectos (CRUD en P-06)
  • Lanzar asyncio.Task por cada run iniciado
  • Mantener registro de Tasks activos: Dict[run_id, asyncio.Task]
  • Cancelar Task de run (cancel_run → task.cancel())
  • Ejecutar reconcile() en startup (crash recovery):
      - Runs RUNNING → marcar FAILED ("servidor_reiniciado")
      - Runs WAITING_GATE → mantener, gate sigue en P-07
  • Supervisar que no supere límite de concurrencia (≥3 proyectos, OBJ-04)
```

**Sub-nodo P-03.2 — Stage Execution Engine**

```
Archivo:    beto/orchestrator/pipeline_engine.py (métodos run_stage)
Propósito:  Ejecutar un stage individual del pipeline.
Contrato:   run_stage(stage_config, context, registry) → StageExecution
Comportamiento:
  1. Resolver plugin: registry.get_for_role(stage_config.plugin_role)
     → Late binding: resuelto en CADA llamada, no al inicio del run (OQ-006)
  2. Construir LLMRequest desde PipelineContext + prompt_template
  3. Invocar plugin.complete() o especialización según stage_type
  4. Emitir stage_progress vía EventBus (tokens parciales si streaming)
  5. En error: lanzar StageRetryException con contador
     → Retry añade "[RETRY - Feedback]: {rejection_notes}" al prompt
     → Max retries: config.pipeline.max_stage_retries (default: 3)
  6. Retornar StageExecution poblado (incluye tokens_used)
Nota: No invoca gates. El gate cycle es responsabilidad del pipeline_engine
      principal que llama a run_stage.
```

---

### P-04 — Event Bus

```
┌─────────────────────────────────────────────────────────────────┐
│  NODO: P-04 Event Bus                                           │
│  ─────────────────────────────────────────────────────────────  │
│  Módulo:      beto/events/                                      │
│  Tipo:        PARALLEL                                          │
│  Entregable:  bus.py (asyncio.Queue) + broadcaster.py (SSE)     │
│  Propósito:   Desacoplar productores de eventos (P-03, P-07,    │
│               P-05) de consumidores (P-02 SSE endpoint, P-06).  │
│                                                                 │
│  RESPONSABILIDADES PROPIAS:                                     │
│  • Recibir eventos tipados de cualquier nodo productor          │
│  • Fan-out a múltiples suscriptores (≥1 conexión SSE por cliente)│
│  • Filtrar eventos por project_id si suscriptor lo solicita     │
│  • Serializar eventos a formato SSE (`data: {json}\n\n`)        │
│  • Gestionar desconexión de suscriptores sin afectar productores│
│                                                                 │
│  ANTI-RESPONSABILIDADES:                                        │
│  • NO persiste eventos (log estructurado vía SC-02, no bus)     │
│  • NO transforma semántica de eventos                           │
│  • NO tiene conocimiento del dominio de negocio                 │
│                                                                 │
│  CONTRATOS:                                                     │
│  • publish(event: BETOEvent) → None  [llamado por P-03, P-07, P-05]│
│  • subscribe(project_id: Optional[str]) → AsyncIterator[BETOEvent]│
│    [llamado por P-02 en endpoint GET /api/events]               │
│                                                                 │
│  TIPO BETOEvent (SC-04):                                        │
│  {                                                              │
│    event_type: str,     # Ver tabla Sección 3.3 entrevista      │
│    project_id: str,                                             │
│    run_id: Optional[str],                                       │
│    stage_id: Optional[str],                                     │
│    timestamp: str,      # ISO 8601                              │
│    payload: dict        # Específico por event_type             │
│  }                                                              │
│                                                                 │
│  IMPLEMENTACIÓN:                                                │
│  • bus.py: asyncio.Queue central + lista de suscriptores        │
│  • broadcaster.py: tarea asyncio que lee Queue y fan-out        │
│    a cada suscriptor activo via asyncio.Queue por suscriptor    │
│                                                                 │
│  SHARED CONCERNS APLICABLES:                                    │
│  • SC-03 (Async-first: toda la API es async)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

### P-05 — Plugin Layer

```
┌─────────────────────────────────────────────────────────────────┐
│  NODO: P-05 Plugin Layer                                        │
│  ─────────────────────────────────────────────────────────────  │
│  Módulo:      beto/plugins/                                     │
│  Tipo:        PARALLEL                                          │
│  Entregable:  base.py + registry.py + adapters/                 │
│  Propósito:   Sistema de plugins LLM intercambiables.           │
│               Descubrimiento, registro, hot-swap y health.      │
│                                                                 │
│  RESPONSABILIDADES PROPIAS:                                     │
│  • Definir contratos ABC: LLMPlugin, ReasoningEngine, CodeEngine│
│  • Descubrir plugins (built-in → naming → entry_points) (OQ-007)│
│  • Registrar e inicializar plugins con config                   │
│  • Gestionar asignaciones role → plugin_id                      │
│  • Hot-swap: validar → health check → asignar → persistir →    │
│               emitir evento SSE 'plugin_swapped' (OQ-006)       │
│  • Wrapper sync→async automático para plugins no-nativos (OQ-002)│
│  • Health check individual y colectivo                          │
│  • Leer/escribir plugin_roles.json (via P-06, SC-01)           │
│                                                                 │
│  ANTI-RESPONSABILIDADES:                                        │
│  • NO ejecuta pipelines                                         │
│  • NO gestiona gates                                            │
│  • NO persiste outputs de LLM (los devuelve a P-03)            │
│                                                                 │
│  SUB-NODOS:                                                     │
│  • P-05.1  LLM Plugin Interface (ABCs en base.py)              │
│  • P-05.2  OpenAI Adapter                                       │
│  • P-05.3  Ollama Adapter                                       │
│  • P-05.4  LM Studio Adapter                                    │
│                                                                 │
│  CONTRATOS DE ENTRADA (llamado por P-02, P-03):                 │
│  • get_for_role(role: str) → LLMPlugin                          │
│  • assign_role(role: str, plugin_id: str) → None               │
│  • list_plugins() → List[PluginInfo]                            │
│  • health_check(plugin_id: str) → {healthy: bool, latency_ms}  │
│  • health_check_all() → dict[str, bool]                         │
│                                                                 │
│  CONTRATOS DE SALIDA:                                           │
│  • P-04 EventBus.publish('plugin_swapped', 'plugin_health')     │
│  • P-06 Persistence.read/write(plugin_roles.json)               │
│                                                                 │
│  DISCOVERY (OQ-007 resuelto, orden de precedencia):             │
│  1. Built-in: beto/plugins/adapters/*.py — siempre cargados     │
│  2. Naming convention: beto_plugin_*.py en plugins.search_paths │
│     Expone: MODULE_PLUGIN | get_plugin() | clase *Plugin        │
│  3. Entry points: grupo 'beto.plugins' (si instalado como pkg)  │
│                                                                 │
│  HOT-SWAP SEQUENCE (OQ-006 resuelto):                           │
│  1. health_check(new_plugin_id) → si falla: rechazar swap       │
│  2. _role_assignments[role] = new_plugin_id                     │
│  3. atomic_write(plugin_roles.json) via P-06                    │
│  4. EventBus.publish('plugin_swapped')                          │
│  5. Próximo get_for_role() retorna nuevo plugin                  │
│     (no interrumpe LLM calls en vuelo)                          │
│                                                                 │
│  SHARED CONCERNS APLICABLES:                                    │
│  • SC-01 (Atomic Write para plugin_roles.json)                  │
│  • SC-02 (Structured Logging de swaps y health checks)          │
│  • SC-03 (Async-first; wrapper sync→async en register())        │
│  • SC-04 (Domain Types: LLMRequest, LLMResponse, TokenUsage)    │
└─────────────────────────────────────────────────────────────────┘
```

**Sub-nodo P-05.1 — LLM Plugin Interface (ABCs)**

```
Archivo:    beto/plugins/base.py
Propósito:  Contratos puros para todos los plugins LLM del sistema.
Contenido:
  • Dataclasses: LLMMessage, LLMRequest, LLMResponse, TokenUsage
  • ABC LLMPlugin:
      - plugin_id: str (property)
      - display_name: str (property)
      - supported_models: list[str] (property)
      - complete(request: LLMRequest) → LLMResponse (async abstract)
      - stream_complete(request) → AsyncIterator[str] (async abstract)
      - health_check() → bool (async abstract)
      - initialize(config: dict) → None (hook, override opcional)
      - teardown() → None (hook, override opcional)
  •
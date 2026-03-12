# MANIFEST_PROYECTO.md
## BETO Framework v4.2 — Manifest de Proyecto Completo
### Generado por: BETO Manifest Generator v4.2
### Fecha: 2025-01-31 | Ciclo: ESPECIFICACIÓN | Estado: COMPLETADO

---

## PREÁMBULO

Este documento es el artefacto terminal del ciclo de especificación de BETO v2. Consolida el inventario completo del sistema tal como fue diseñado en los MANIFESTs individuales, establece el plan de materialización ordenado por dependencias, y declara el estado final del ciclo. Es la fuente de verdad para la fase de implementación.

**Fuentes canónicas**:
- `BETO_SYSTEM_GRAPH.md` v1.0.0 — Grafo validado del sistema
- `BETO_CORE_DRAFT.md` v0.1.0 — Draft fundacional
- `BETO_CORE_MOTOR_RAZONAMIENTO.md` v0.1.0 — Motor de razonamiento
- `BETO_CORE_MOTOR_CODIGO.md` v0.1.0 — Motor de código
- `BETO_CORE_GATES_OPERADOR.md` v0.1.0 — Gate Manager
- `BETO_CORE_GESTOR_CICLO.md` v0.1.0 — Orchestrator

---

## PARTE I: INVENTARIO COMPLETO DEL SISTEMA

### I.1 Resumen de Nodos

| Tipo | Cantidad | Estado |
|------|----------|--------|
| Nodos PARALLEL | 7 | Especificados |
| Sub-nodos SUBBETO | 10 | Especificados |
| Componentes INTERNAL (absorbidos) | 8 | Absorbidos en nodo padre |
| Shared Concerns | 5 | Definidos transversalmente |

**Total unidades de entrega autónoma: 7 PARALLEL + 10 SUBBETO = 17 unidades**

---

### I.2 Inventario Completo de Nodos PARALLEL

#### P-01 — Presentation Layer
```
Módulo:       beto/static/
Entregable:   index.html + css/style.css + js/{app,sse-client,api-client}.js
Propósito:    GUI web sin frameworks JS. Interfaz primaria de operación humana.
Estado SPEC:  COMPLETO (BETO_SYSTEM_GRAPH §P-01)
Sub-nodos:    P-01.1, P-01.2, P-01.3
Dependencias: P-02 (API Layer) — todos los contratos HTTP/SSE
SC aplicados: SC-05
ADRs:         ADR-002 (Vanilla JS), ADR-001 (FastAPI sirve estáticos)
OQs abiertas: OQ-010 (Jinja2 vs SPA pura — no resuelto en spec)
```

#### P-02 — API Layer
```
Módulo:       beto/api/ + beto/main.py
Entregable:   FastAPI app con routers + schemas Pydantic
Propósito:    Traducción HTTP↔Dominio. Punto de entrada único REST/SSE.
Estado SPEC:  COMPLETO (BETO_SYSTEM_GRAPH §P-02)
Sub-nodos:    ninguno
Dependencias: P-03.1 (ProjectManager), P-04 (EventBus), P-05 (PluginRegistry),
              P-06 (Persistence), P-07 (GateManager)
SC aplicados: SC-03, SC-04
ADRs:         ADR-001 (FastAPI)
OQs abiertas: ninguna
```

#### P-03 — Orchestrator
```
Módulo:       beto/orchestrator/pipeline_engine.py + project_manager.py
Entregable:   PipelineEngine + ProjectManager
Propósito:    Motor de ejecución de pipelines. Coordinador de stages,
              plugins, gates y proyectos concurrentes.
Estado SPEC:  COMPLETO (BETO_SYSTEM_GRAPH §P-03 + BETO_CORE_GESTOR_CICLO.md)
Sub-nodos:    P-03.1, P-03.2
Dependencias: P-04 (EventBus), P-05 (PluginRegistry),
              P-06 (Persistence), P-07 (GateManager)
SC aplicados: SC-01, SC-02, SC-03, SC-04
ADRs:         ADR-003 (asyncio runtime)
Internals:    C-08 (Run Manager), C-17 (Pipeline State Machine),
              C-25 (Crash Recovery)
OQs abiertas: ninguna relevante a implementación
Config clave: pipeline.max_stage_retries=3, gate_timeout_hours=null,
              max_concurrent_runs=10, reconcile_on_startup=true
```

#### P-04 — Event Bus
```
Módulo:       beto/events/bus.py + broadcaster.py
Entregable:   asyncio.Queue bus + SSE broadcaster
Propósito:    Desacoplar productores (P-03, P-07, P-05) de consumidores
              (P-02 SSE endpoint).
Estado SPEC:  COMPLETO (BETO_SYSTEM_GRAPH §P-04)
Sub-nodos:    ninguno
Dependencias: ninguna (nodo hoja — solo es consumido, no consume otros nodos)
SC aplicados: SC-03
ADRs:         ADR-003 (asyncio)
OQs abiertas: ninguna
Tipo BETOEvent: {event_type, project_id, run_id, stage_id, timestamp, payload}
```

#### P-05 — Plugin Layer
```
Módulo:       beto/plugins/
Entregable:   base.py + registry.py + adapters/
Propósito:    Sistema de plugins LLM intercambiables. Descubrimiento,
              registro, hot-swap y health checks.
Estado SPEC:  COMPLETO (BETO_SYSTEM_GRAPH §P-05 + BETO_CORE_MOTOR_RAZONAMIENTO.md
              + BETO_CORE_MOTOR_CODIGO.md)
Sub-nodos:    P-05.1, P-05.2, P-05.3, P-05.4
Dependencias: P-04 (EventBus — publica plugin_swapped, plugin_health),
              P-06 (Persistence — lee/escribe plugin_roles.json)
SC aplicados: SC-01, SC-02, SC-03, SC-04
ADRs:         ADR-003 (async-first), IADR-R01, IADR-R02, IADR-R03,
              ADR-CE-001, ADR-CE-002, ADR-CE-003
Internals:    C-15 (Reasoning ABC), C-16 (Code ABC) — absorbidos en P-05.1
OQs abiertas: OQ-R01 (confidence_score), OQ-R02 (streaming en reason()),
              OQ-CE-01 (extracción de bloques markdown),
              OQ-CE-02 (resolución automática de source_stage_id),
              OQ-CE-03 (rol code_review_engine separado)
Discovery:    built-in → naming convention (beto_plugin_*.py) → entry_points
Hot-swap:     health_check → assign → atomic_write → SSE event
```

#### P-06 — Persistence Layer
```
Módulo:       beto/persistence/json_store.py + models.py
Entregable:   JsonStore con atomic_write + modelos persistibles
Propósito:    Capa de persistencia JSON local. Única fuente de verdad en disco.
Estado SPEC:  COMPLETO (BETO_SYSTEM_GRAPH §P-06 + §P-06.1)
Sub-nodos:    P-06.1 (JSON Store atomic_write)
Dependencias: ninguna (nodo hoja — solo es consumido)
SC aplicados: SC-01 (es la implementación de SC-01), SC-04
ADRs:         ADR-004 (JSON local sobre SQLite)
Internals:    C-26 (Plugin Roles Store) — absorbido
OQs abiertas: OQ-003 resuelto → atomic_write via rename atómico
Layout disco: data/projects/{id}/project.json
              data/runs/{id}/run.json
              data/runs/{id}/stages/{stage_id}.json
              data/gates/{id}.json
              data/config/plugin_roles.json
```

#### P-07 — Gate Manager
```
Módulo:       beto/orchestrator/gate_manager.py
Entregable:   GateManager con ciclo completo de aprobación humana
Propósito:    Mecanismo de bloqueo activo asyncio.Event. Toda decisión
              crítica del pipeline requiere aprobación explícita del operador.
Estado SPEC:  COMPLETO (BETO_SYSTEM_GRAPH §P-07 + BETO_CORE_GATES_OPERADOR.md)
Sub-nodos:    ninguno
Dependencias: P-04 (EventBus — publica gate_created, gate_resolved),
              P-06 (Persistence — persiste gates),
              P-02 (API Layer — recibe decisiones HTTP)
SC aplicados: SC-01, SC-02, SC-03, SC-04
Internals:    C-18 (Gate State Machine) — absorbido
OQs abiertas: OQ-009 resuelto (sin timeout), OQ-008 resuelto (retry con feedback),
              OQ-005 resuelto (campos editables por stage_type)
Estado PENDING: asyncio.Event en memoria + JSON en disco
Estados terminales: APPROVED, MODIFIED, REJECTED
```

---

### I.3 Inventario Completo de Sub-nodos SUBBETO

#### P-01.1 — SSE Client
```
Archivo:      beto/static/js/sse-client.js
Padre:        P-01 (Presentation Layer)
Propósito:    Gestionar conexión SSE con fallback automático a polling (2000ms).
Contrato:     connect(onEvent) → void | disconnect() → void
Fallback:     3 fallos SSE → polling GET /api/runs/active cada 2000ms
Estado SPEC:  COMPLETO
```

#### P-01.2 — API Client
```
Archivo:      beto/static/js/api-client.js
Padre:        P-01 (Presentation Layer)
Propósito:    Wrapper fetch() tipado para todos los endpoints REST.
Métodos:      projects.{list,create,startRun}, gates.{getPending,decide},
              plugins.{getRoles,swapRole}, runs.{getActive,cancel}
Estado SPEC:  COMPLETO
```

#### P-01.3 — Gate Panel UI
```
Archivo:      beto/static/js/app.js (sección GatePanel)
Padre:        P-01 (Presentation Layer)
Propósito:    Componente de aprobación de gates. Modal/overlay con
              campos editables específicos por stage_type.
Campos edit.: reasoning→{reasoning_text,conclusions}
              code_gen→{code,language,explanation}
              code_review→{review_notes,approved,suggestions}
              custom→{content}
Eventos SSE:  gate_created → mostrar panel | gate_resolved → cerrar panel
Estado SPEC:  COMPLETO (TIS 2/3 — UI detail pendiente de OQ-010)
```

#### P-03.1 — Project Manager
```
Archivo:      beto/orchestrator/project_manager.py
Padre:        P-03 (Orchestrator)
Propósito:    Coordinar ciclo de vida de proyectos y runs concurrentes.
              Mantener Dict[run_id, asyncio.Task]. Crash recovery en startup.
Reconcile:    RUNNING→FAILED | WAITING_GATE→mantener | PENDING→CANCELLED
Estado SPEC:  COMPLETO (TIS 2/3)
```

#### P-03.2 — Stage Execution Engine
```
Archivo:      beto/orchestrator/pipeline_engine.py (métodos run_stage)
Padre:        P-03 (Orchestrator)
Propósito:    Ejecutar stage individual. Late-binding de plugin por rol.
              Retry loop con feedback. Streaming opcional.
Contrato:     run_stage(stage_cfg, context) → (StageExecutionResult, PipelineContext)
Late-binding: plugin resuelto en CADA invocación, no al inicio del run
Estado SPEC:  COMPLETO (TIS 2/3)
```

#### P-05.1 — LLM Plugin Interface (ABCs)
```
Archivo:      beto/plugins/base.py
Padre:        P-05 (Plugin Layer)
Propósito:    Contratos puros: LLMPlugin, ReasoningEnginePlugin, CodeEnginePlugin.
              Dataclasses: LLMMessage, LLMRequest, LLMResponse, TokenUsage,
              ReasoningRequest, ReasoningResult, ReasoningStep,
              CodeGenerationResult, CodeReviewResult, CodeBlock,
              ReviewCriterion, CodeLanguage, ReviewVerdict.
              Excepciones: LLMPluginError, LLMContextLengthError,
              LLMTimeoutError, LLMHealthCheckError.
              Constantes: REASONING_ROLES, PROMPT_FORMAT_MARKERS.
Estado SPEC:  COMPLETO (TIS 2/3)
OQs abiertas: OQ-R01, OQ-R02, OQ-CE-01, OQ-CE-03
```

#### P-05.2 — OpenAI Adapter
```
Archivo:      beto/plugins/adapters/openai_adapter.py
Padre:        P-05 (Plugin Layer)
Propósito:    Adaptador para backends compatibles OpenAI (OpenAI, LM Studio).
              Implementa LLMPlugin + ReasoningEnginePlugin + CodeEnginePlugin.
              httpx async client. Configurable por api_key_env + base_url.
Estado SPEC:  COMPLETO (TIS 3/3*)
Reutilizable: LM Studio usa este mismo adapter con base_url distinto
```

#### P-05.3 — Ollama Adapter
```
Archivo:      beto/plugins/adapters/ollama_adapter.py
Padre:        P-05 (Plugin Layer)
Propósito:    Adaptador para Ollama (compatible OpenAI /v1/).
              Implementa LLMPlugin + ReasoningEnginePlugin + CodeEnginePlugin.
              Timeout extendido (default 120s).
Estado SPEC:  COMPLETO (TIS 3/3*)
```

#### P-05.4 — LM Studio Adapter
```
Archivo:      beto/plugins/adapters/lmstudio_adapter.py
Padre:        P-05 (Plugin Layer)
Propósito:    Adaptador específico para LM Studio.
              Hereda/reutiliza OpenAI Adapter con configuración distinta.
              Timeout extendido (default 180s). api_key puede ser dummy.
Estado SPEC:  COMPLETO (TIS 2/3)
Nota:         Puede implementarse como subclase de P-05.2 o instancia
              configurada del mismo OpenAIAdapter.
```

#### P-06.1 — JSON Store (atomic_write)
```
Archivo:      beto/persistence/json_store.py
Padre:        P-06 (Persistence Layer)
Propósito:    Escritura atómica de JSON via rename atómico del SO.
              Implementación: write a tmp → fsync → rename → original.
              Previene corrupción en crash (OQ-003 resuelto).
Estado SPEC:  COMPLETO (TIS 3/3*)
Patrón:       tmp_path = path.with_suffix('.tmp') → write → rename
```

---

### I.4 Inventario de Shared Concerns

| ID | Nombre | Implementación | Nodos Afectados |
|----|--------|---------------|----------------|
| SC-01 | Atomic Write | `json_store.atomic_write()` — nunca escritura directa | P-06, P-03, P-07, P-05 |
| SC-02 | Structured Logging | Logs JSON en cada operación relevante. Auditoría de decisiones del operador | Todos |
| SC-03 | Async-first Contract | Toda API pública es `async def`. Plugins sync → wrapper en `PluginRegistry.register()` | P-03, P-04, P-05, P-07 |
| SC-04 | Domain Types | Tipos compartidos en `beto/persistence/models.py` y `beto/api/schemas.py` | P-02, P-03, P-05, P-06, P-07 |
| SC-05 | No Code Execution | BETO v2 no ejecuta código generado. Output de code_generation es texto. Reforzado en prompts del sistema | Todos |

---

### I.5 Inventario de Componentes INTERNAL (Absorbidos)

| ID | Nombre | Absorbido en | Justificación |
|----|--------|-------------|---------------|
| C-08 | Run Manager | P-03 + P-06 | Lógica en PipelineEngine; estado en Persistence |
| C-15 | Reasoning Engine ABC | P-05.1 | Extensión de jerarquía, no componente operativo separado |
| C-16 | Code Engine ABC | P-05.1 | Extensión de jerarquía, no componente operativo separado |
| C-17 | Pipeline State Machine | P-03 | Lógica interna de PipelineEngine (execute_run) |
| C-18 | Gate State Machine | P-07 | Lógica interna de GateManager |
| C-20 | GUI Static Server | P-02 | `app.mount('/static', StaticFiles(...))` en main.py |
| C-25 | Crash Recovery | P-03.1 | `ProjectManager.reconcile()` en lifespan de FastAPI |
| C-26 | Plugin Roles Store | P-06 + P-05 | Artefacto de datos; `data/config/plugin_roles.json` |

---

### I.6 Inventario de OQs Abiertas (Pendientes de Resolución)

Las siguientes OQs permanecen abiertas al cierre del ciclo de especificación. Requieren decisión antes de implementación de los componentes afectados.

| ID | OQ | Componente Afectado | Impacto | Prioridad |
|----|----|--------------------|---------|----|
| OQ-010 | ¿Jinja2 SSR vs SPA pura con HTML estático? | P-01, P-02 | Cómo FastAPI sirve la GUI inicial; si Jinja2 es dependencia | ALTA — bloquea inicio de P-01 |
| OQ-R01 | ¿`confidence_score` en ReasoningResult? | P-05.1, P-01.3 | Schema de salida y visualización en Gate Panel | BAJA — puede añadirse después |
| OQ-R02 | ¿`reason()` retorna AsyncIterator o es siempre non-streaming? | P-05.1, P-03.2 | Contrato del ABC y complejidad de Stage Execution Engine | MEDIA — afecta diseño de contrato |
| OQ-CE-01 | ¿Extracción automática de bloques markdown del output de código? | P-05.1, P-01.3 | `CodeGenerationResult.code` (campo único vs lista de bloques) | MEDIA — afecta schema de salida |
| OQ-CE-02 | ¿`source_stage_id` auto-detectado o explícito en code_review? | P-03.2, P-05.1 | Lógica de `PipelineContext.get_for_stage()` para revisión | BAJA — hay default razonable especificado |
| OQ-CE-03 | ¿Rol `code_review_engine` separado del `code_engine`? | P-05, config.yaml | Tabla de roles y PluginRegistry | BAJA — ADR-CE-003 resuelve con `code_engine` unificado; puede revisarse |

**OQs resueltas en el ciclo de especificación** (no reabrir):

| ID | Resolución |
|----|-----------|
| OQ-001 | BETO v2 NO ejecuta código generado (SC-05) |
| OQ-002 | Plugins sync → wrapper automático en `PluginRegistry.register()` |
| OQ-003 | Atomic write via rename atómico del SO (implementado en P-06.1) |
| OQ-004 | Stages completamente configurables por proyecto via `PipelineConfig` |
| OQ-005 | MODIFIED edita campos específicos por stage_type (ver tabla §I.3 P-01.3) |
| OQ-006 | Hot-swap activo en siguiente `get_for_role()`, no interrumpe LLM call en vuelo |
| OQ-007 | Discovery: built-in → naming convention → entry_points (orden de precedencia) |
| OQ-008 | Retry con `[RETRY - Feedback]: {rejection_notes}` inyectado al prompt |
| OQ-009 | Sin timeout de gate (`gate_timeout_hours: null`). No auto-aprobación |

---

## PARTE II: PLAN DE MATERIALIZACIÓN

### II.1 Grafo de Dependencias para Implementación

```
Nivel 0 (Sin dependencias — implementar primero):
  P-06 ──────────────────────────────────────────── JSON Store
  P-06.1                                              (atomic_write)

Nivel 1 (Depende solo de Nivel 0):
  P-04 ──────────────────────────────────────────── Event Bus
  P-05.1 ────────────────────────────────────────── ABCs + Dataclasses

Nivel 2 (Depende de Nivel 0 + Nivel 1):
  P-05.2 ────────────────────────────────────────── OpenAI Adapter
  P-05.3 ────────────────────────────────────────── Ollama Adapter
  P-05.4 ────────────────────────────────────────── LM Studio Adapter
  P-07   ────────────────────────────────────────── Gate Manager
         (depende de P-04, P-06)

Nivel 3 (Depende de Nivel 0 + 1 + 2):
  P-05   ────────────────────────────────────────── Plugin Registry
         (requiere P-05.1, P-05.2, P-05.3, P-05.4)
  P-03.2 ────────────────────────────────────────── Stage Execution Engine
         (requiere P-05, P-04, P-06, P-07)

Nivel 4 (Depende de Nivel 0..3):
  P-03.1 ────────────────────────────────────────── Project Manager
         (requiere P-03.2, P-06, P-04)
  P-03   ────────────────────────────────────────── Orchestrator completo
         (requiere P-03.1 + P-03.2)

Nivel 5 (Depende de Nivel 0..4):
  P-02   ────────────────────────────────────────── API Layer
         (requiere P-03, P-04, P-05, P-06, P-07)

Nivel 6 (Depende de Nivel 5):
  P-01.2 ────────────────────────────────────────── API Client JS
         (requiere P-02 para conocer contratos REST)
  P-01.1 ────────────────────────────────────────── SSE Client JS
         (requiere P-02 para conocer endpoint SSE)
  P-01.3 ────────────────────────────────────────── Gate Panel UI JS
         (requiere P-01.1, P-01.2, P-07 schemas)

Nivel 7 (Integración final):
  P-01   ────────────────────────────────────────── Presentation Layer
         (integra P-01.1, P-01.2, P-01.3 + HTML/CSS)
```

---

### II.2 Plan de Materialización Ordenado

#### WAVE 0 — Fundación (Bloqueante para todo lo demás)

| Orden | Unidad | Archivos | Criterio de Completitud |
|-------|--------|----------|------------------------|
| 0.1 | **P-06** Persistence Layer | `beto/persistence/models.py`, `beto/persistence/__init__.py` | Modelos de dominio persistibles definidos; enumeraciones de estado completas |
| 0.2 | **P-06.1** JSON Store | `beto/persistence/json_store.py` | `atomic_write()` pasa test de corrupción simulada; `read()`, `list()`, `delete()` funcionales |
| 0.3 | Config & Entrypoint | `config.yaml`, `beto/config.py`, `beto/main.py` (skeleton), `pyproject.toml` | App FastAPI levanta sin errores; config cargada correctamente |

**Precondición**: Resolver OQ-010 antes de 0.3 (Jinja2 vs SPA pura).

---

#### WAVE 1 — Infraestructura de Comunicación y Contratos

| Orden | Unidad | Archivos | Criterio de Completitud |
|-------|--------|----------|------------------------|
| 1.1 | **P-04** Event Bus | `beto/events/bus.py`, `beto/events/broadcaster.py`, `beto/events/__init__.py` | `publish()` y `subscribe()` funcionales; fan-out a múltiples suscriptores; filtro por project_id |
| 1.2 | **P-05.1** Plugin ABCs | `beto/plugins/base.py` | ABCs `LLMPlugin`, `ReasoningEnginePlugin`, `CodeEnginePlugin` definidas; todos los dataclasses completos; excepciones definidas |

**Dependencias**: 1.1 requiere Wave 0. 1.2 es paralelo a 1.1.

---

#### WAVE 2 — Adaptadores y Gate Manager

| Orden | Unidad | Archivos | Criterio de Completitud |
|-------|--------|----------|------------------------|
| 2.1 | **P-05.2** OpenAI Adapter | `beto/plugins/adapters/openai_adapter.py` | `complete()`, `stream_complete()`, `health_check()`, `reason()`, `generate_code()`, `review_code()` funcionales contra endpoint real o mock |
| 2.2 | **P-05.3** Ollama Adapter | `beto/plugins/adapters/ollama_adapter.py` | Ídem P-05.2; timeout extendido (120s) configurable |
| 2.3 | **P-05.4** LM Studio Adapter | `beto/plugins/adapters/lmstudio_adapter.py` | Configurado como especialización de OpenAI Adapter con base_url override; timeout 180s |
| 2.4 | **P-07** Gate Manager | `beto/orchestrator/gate_manager.py` | `create_gate()`, `wait_for_decision()`, `process_decision()` funcionales; asyncio.Event lifecycle correcto; persistencia en P-06; eventos en P-04 |

**Dependencias**: 2.1, 2.2, 2.3 requieren P-05.1 (1.2). 2.4 requiere P-04 (1.1) y P-06 (0.1, 0.2). 2.1-2.4 son paralelos entre sí.

---

#### WAVE 3 — Plugin Registry y Stage Execution

| Orden | Unidad | Archivos | Criterio de Completitud |
|-------|--------|----------|------------------------|
| 3.1 | **P-05** Plugin Registry | `beto/plugins/registry.py`, `beto/plugins/__init__.py` | `discover_plugins()` carga built-ins; `register()` con wrapper sync→async; `assign_role()` con health check + atomic_write; `get_for_role()` retorna instancia correcta; hot-swap validado |
| 3.2 | **P-03.2** Stage Execution Engine | `beto/orchestrator/pipeline_engine.py` (métodos `run_stage`, `_build_llm_request`, helpers) | `run_stage()` funcional para stage_types: reasoning, code_generation, code_review; late-binding de plugin; retry loop hasta max_retries; streaming opcional con eventos SSE |

**Dependencias**: 3.1 requiere P-05.1, P-05.2, P-05.3, P-05.4 (Wave 2). 3.2 requiere P-05 (3.1), P-04 (1.1), P-06 (Wave 0), P-07 (2.4).

---

#### WAVE 4 — Orchestrator Completo

| Orden | Unidad | Archivos | Criterio de Completitud |
|-------|--------|----------|------------------------|
| 4.1 | **P-03.1** Project Manager | `beto/orchestrator/project_manager.py` | `create_project()`, `start_run()`, `cancel_run()`, `get_active_runs()`, `archive_project()` funcionales; `reconcile()` detecta y marca runs huérfanos correctamente |
| 4.2 | **P-03** Orchestrator integrado | `beto/orchestrator/pipeline_engine.py` (método `execute_run` completo), `beto/orchestrator/__init__.py` | `execute_run()` completa un pipeline de 4 stages con gates en modo test; concurrencia de ≥3 proyectos simultáneos verificada; crash recovery funcional |
| 4.3 | Excepciones de Orchestrator | `beto/orchestrator/exceptions.py` | Todas las excepciones de dominio definidas y usadas consistentemente |

**Dependencias**: 4.1 requiere P-03.2 (3.2), P-06, P-04. 4.2 requiere 4.1 completo.

---

#### WAVE 5 — API Layer

| Orden | Unidad | Archivos | Criterio de Completitud |
|-------|--------|----------|------------------------|
| 5.1 | Schemas Pydantic | `beto/api/schemas.py` | Todos los modelos request/response definidos; validadores críticos presentes (GateDecisionRequest: notes obligatorio en REJECTED, modified_output en MODIFIED) |
| 5.2 | Router: Projects | `beto/api/routes/projects.py` | CRUD de proyectos + start_run funcional |
| 5.3 | Router: Runs | `beto/api/routes/runs.py` | List, detail, cancel funcional |
| 5.4 | Router: Gates | `beto/api/routes/gates.py` | `GET /pending`, `GET /{id}`, `POST /{id}/decide`, `GET /runs/{id}/gates` funcionales |
| 5.5 | Router: Plugins | `beto/api/routes/plugins.py` | List, health_check, assign_role funcionales
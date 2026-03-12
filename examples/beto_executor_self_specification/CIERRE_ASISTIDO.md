# CIERRE_ASISTIDO.md
## BETO Framework v4.2 — Cierre Asistido de Open Questions
### Modo: BETO_ASSISTED | Fecha: 2025-01-31
### Fuente: BETO_SYSTEM_GRAPH.md + BETO_CORE_DRAFT.md + BETO_CORE_MOTOR_RAZONAMIENTO.md + BETO_CORE_MOTOR_CODIGO.md + BETO_CORE_GATES_OPERADOR.md + BETO_CORE_GESTOR_CICLO.md

---

## PREÁMBULO DEL ASISTENTE DE CIERRE

Este documento cierra todas las Open Questions (OQs) identificadas en los BETO_COREs hijos usando el modo **BETO_ASSISTED**: cada resolución es **derivada del SYSTEM INTENT** declarado en los artefactos, sin requerir intervención del operador. Las resoluciones son consistentes con las decisiones arquitectónicas ya comprometidas (ADRs, SCx, resoluciones previas en BETO_SYSTEM_GRAPH) y maximizan la coherencia interna del sistema.

**Criterio de cierre BETO_ASSISTED**: Una OQ se cierra asistidamente cuando la respuesta es unívocamente derivable de: (a) anti-objetivos explícitos del sistema, (b) ADRs ya comprometidos, (c) contratos de interfaz ya definidos, (d) shared concerns declarados, o (e) el principio de mínima complejidad consistente con los objetivos.

**Estado de todos los BETO_COREs al finalizar este documento**: `SUCCESS_CLOSED`

---

## REGISTRO CONSOLIDADO DE OQs

| ID | Core Origen | Título Breve | Estado Previo | Estado Final |
|----|-------------|--------------|---------------|--------------|
| OQ-001 | BETO_CORE_DRAFT | Ejecución de código generado / dry-run | Resuelto en Graph | ✅ CONFIRMADO |
| OQ-002 | BETO_CORE_DRAFT | Plugins sync → ThreadPoolExecutor o async propio | Resuelto en Graph | ✅ CONFIRMADO |
| OQ-003 | BETO_CORE_DRAFT | Write-ahead para proteger JSON de corrupción | Resuelto en Graph | ✅ CONFIRMADO |
| OQ-004 | BETO_CORE_DRAFT | Stages fijos vs. configurables por proyecto | Abierta | ✅ CERRADA |
| OQ-005 | BETO_CORE_DRAFT | GateType.MODIFIED — campos editables por el operador | Resuelto en Graph | ✅ CONFIRMADO |
| OQ-006 | BETO_CORE_DRAFT | Hot-swap: mid-execution vs. siguiente stage | Resuelto en Graph | ✅ CONFIRMADO |
| OQ-007 | BETO_CORE_DRAFT | Discovery de plugins externos: entry_points vs. naming | Resuelto en Graph | ✅ CONFIRMADO |
| OQ-008 | BETO_CORE_DRAFT | Comportamiento de retry en gate rechazado | Resuelto en Graph | ✅ CONFIRMADO |
| OQ-009 | BETO_CORE_DRAFT | Timeout para gates pendientes | Resuelto en Graph | ✅ CONFIRMADO |
| OQ-010 | BETO_CORE_DRAFT | Jinja2 SSR vs. SPA pura | Abierta | ✅ CERRADA |
| OQ-R01 | BETO_CORE_MOTOR_RAZONAMIENTO | `confidence_score` en ReasoningResult | Abierta | ✅ CERRADA |
| OQ-R02 | BETO_CORE_MOTOR_RAZONAMIENTO | Streaming dentro de `reason()` vs. solo en `stream_complete()` | Abierta | ✅ CERRADA |
| OQ-CE-01 | BETO_CORE_MOTOR_CODIGO | Extracción automática de bloques markdown de código | Abierta | ✅ CERRADA |
| OQ-CE-02 | BETO_CORE_MOTOR_CODIGO | Referencia automática vs. explícita del stage de código a revisar | Abierta | ✅ CERRADA |
| OQ-CE-03 | BETO_CORE_MOTOR_CODIGO | Rol `code_review_engine` separado del `code_engine` | Abierta | ✅ CERRADA |

---

## PARTE I: CONFIRMACIONES DE OQs YA RESUELTAS EN BETO_SYSTEM_GRAPH

Las siguientes OQs fueron resueltas en `BETO_SYSTEM_GRAPH.md` y son referenciadas consistentemente en todos los BETO_COREs hijos. Se confirman aquí como verdad inmutable.

---

### OQ-001 — Ejecución de código generado / dry-run preview

**Core origen**: BETO_CORE_DRAFT §2.2  
**Resolución en Graph**: SC-05 "No Code Execution"  
**Confirmación BETO_ASSISTED**:

> **RESOLUCIÓN FINAL**: BETO v2 **no ejecuta código generado en ninguna forma**, incluyendo dry-run preview. El output de stages `code_generation` es texto plano. SC-05 es un shared concern obligatorio aplicable a todos los nodos.

**Impacto confirmado en COREs hijos**:
- `BETO_CORE_MOTOR_CODIGO §1.3`: Anti-objetivo explícito documentado.
- `BETO_CORE_MOTOR_CODIGO §5.1`: System prompt de `generate_code()` incluye `"No ejecutes ni simules ejecución."` como refuerzo en-prompt de SC-05.
- `BETO_CORE_GATES_OPERADOR §2.2`: Fuera de alcance del Gate Manager.

---

### OQ-002 — Plugins sync → ThreadPoolExecutor automático vs. async propio

**Core origen**: BETO_CORE_DRAFT §3.2 ADR-003  
**Resolución en Graph**: SC-03 "Async-first Contract" + P-05 PluginRegistry  
**Confirmación BETO_ASSISTED**:

> **RESOLUCIÓN FINAL**: Los plugins sync se envuelven **automáticamente** en `asyncio.to_thread()` (o `loop.run_in_executor()` con `ThreadPoolExecutor`) dentro de `PluginRegistry.register()`. Esta envoltura es transparente al invocador. Los plugins nativamente async no reciben envoltura. Es **responsabilidad del registry**, no del plugin ni del orchestrator.

**Especificación de implementación**:
```python
# beto/plugins/registry.py
import asyncio
import inspect

async def _wrap_if_sync(method):
    """Envuelve método sync en coroutine para compatibilidad asyncio."""
    if inspect.iscoroutinefunction(method):
        return method
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(method, *args, **kwargs)
    return wrapper
```

**Impacto confirmado en COREs hijos**:
- `BETO_CORE_MOTOR_RAZONAMIENTO §2.3`: Resolución aplicable, adaptadores pueden ser sync.
- `BETO_CORE_MOTOR_CODIGO §5.1`: Adaptadores `CodeEnginePlugin` pueden implementar métodos sync sin penalización de diseño.

---

### OQ-003 — Write-ahead / atomic rename para proteger JSON de corrupción

**Core origen**: BETO_CORE_DRAFT §3.2 ADR-004  
**Resolución en Graph**: SC-01 "Atomic Write"  
**Confirmación BETO_ASSISTED**:

> **RESOLUCIÓN FINAL**: Toda escritura de JSON usa el patrón **write-to-temp + atomic rename**. Implementado en `P-06.1 JsonStore.atomic_write()`. Ningún nodo escribe JSON directamente; toda escritura pasa por `json_store.atomic_write()`.

**Especificación de implementación**:
```python
# beto/persistence/json_store.py
import os, json, tempfile
from pathlib import Path

async def atomic_write(path: Path, data: dict) -> None:
    """Escribir JSON de forma atómica via write-temp + rename."""
    dir_ = path.parent
    dir_.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode='w', dir=dir_, suffix='.tmp', delete=False, encoding='utf-8'
    ) as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2, default=str)
        tmp_path = tmp.name
    os.replace(tmp_path, path)   # Atómico en POSIX; best-effort en Windows
```

**Nota Windows**: `os.replace()` es atómico en POSIX. En Windows puede no serlo si el archivo destino está abierto; documentar como limitación conocida en v2 (despliegue primario es local Linux/macOS).

---

### OQ-005 — GateType.MODIFIED: campos editables por el operador

**Core origen**: BETO_CORE_DRAFT §4.3  
**Resolución en Graph**: P-01.3 Gate Panel UI + P-07 §4.2  
**Confirmación BETO_ASSISTED**:

> **RESOLUCIÓN FINAL**: Los campos editables en `GateType.MODIFIED` son determinados por `stage_type` del gate. La tabla canónica (ya definida en `BETO_CORE_GATES_OPERADOR §4.2`) es la fuente de verdad. P-07 valida que `modified_output` contenga al menos un campo válido para el `stage_type`.

**Tabla canónica confirmada**:

| `stage_type` | Campos editables | Widget UI |
|---|---|---|
| `reasoning` | `reasoning_text`, `conclusions` | Textarea |
| `code_generation` | `code`, `language`, `explanation` | Textarea monospace / Input / Textarea |
| `code_review` | `review_notes`, `approved`, `suggestions` | Textarea / Checkbox / Textarea |
| `custom` | `content` | Textarea |

---

### OQ-006 — Hot-swap: mid-execution vs. siguiente `get_for_role()`

**Core origen**: BETO_CORE_DRAFT §5.4  
**Resolución en Graph**: P-05 Hot-swap Sequence  
**Confirmación BETO_ASSISTED**:

> **RESOLUCIÓN FINAL**: El hot-swap entra en efecto en la **próxima llamada a `get_for_role()`**, que ocurre al inicio de cada `run_stage()`. Las llamadas LLM **en vuelo** no se interrumpen. El stage en ejecución actual completa con el plugin anterior; el siguiente stage usa el nuevo plugin.

---

### OQ-007 — Discovery de plugins: entry_points vs. naming convention

**Core origen**: BETO_CORE_DRAFT §5.2  
**Resolución en Graph**: P-05 Discovery Order  
**Confirmación BETO_ASSISTED**:

> **RESOLUCIÓN FINAL**: Discovery en orden de precedencia: (1) Built-in adapters en `beto/plugins/adapters/` — siempre cargados. (2) Naming convention `beto_plugin_*.py` en `plugins.search_paths` configurados. (3) Entry points grupo `beto.plugins` si el plugin está instalado como paquete Python.

---

### OQ-008 — Comportamiento de retry en gate rechazado

**Core origen**: BETO_CORE_DRAFT §6.3  
**Resolución en Graph**: P-03.2 Sub-nodo + P-03 config  
**Confirmación BETO_ASSISTED**:

> **RESOLUCIÓN FINAL**: Gate `REJECTED` → **re-ejecutar el mismo stage** con `rejection_notes` del operador inyectadas en el prompt como bloque `[RETRY {n} - Feedback del operador]: {notes}`. Máximo `config.pipeline.max_stage_retries` (default: 3) intentos. Al agotar reintentos: `RunStatus = FAILED`. El operador **no edita el prompt** directamente (eso sería `MODIFIED`); el feedback se inyecta automáticamente por el engine.

---

### OQ-009 — Timeout para gates pendientes

**Core origen**: BETO_CORE_DRAFT §6.3  
**Resolución en Graph**: P-03 config  
**Confirmación BETO_ASSISTED**:

> **RESOLUCIÓN FINAL**: `gate_timeout_hours: null` — **no existe timeout** en v2. Un gate pendiente permanece indefinidamente hasta decisión del operador. Esta es una decisión de diseño deliberada: la supervisión humana es el invariante central del sistema. Los recursos del run (asyncio.Task en `WAITING_GATE`) permanecen suspendidos cooperativamente sin consumir CPU.

---

## PARTE II: CIERRE DE OQs ABIERTAS — MODO BETO_ASSISTED

---

### OQ-004 — Stages del pipeline: ¿fijos o completamente configurables por proyecto?

**Core origen**: BETO_CORE_DRAFT §4.3  
**Estado previo**: ABIERTA — "Determina flexibilidad del PipelineConfig"

#### Análisis de derivación BETO_ASSISTED

**Evidencia del SYSTEM INTENT**:

1. `BETO_CORE_DRAFT §4.3` muestra un `config.yaml` con stages definidos como lista YAML configurable (no hardcoded en código).
2. `BETO_CORE_GESTOR_CICLO §4.3` define `PipelineConfig.stages: list[StageConfig]` como estructura de datos genérica, no un enum de stages fijos.
3. `BETO_CORE_MOTOR_CODIGO §4.3` presenta un ejemplo completo de pipeline configurable con 4 stages incluyendo `extra_config` por stage.
4. El anti-objetivo `"No es un sistema cloud-native en su versión inicial"` y la filosofía "stdlib-first" favorecen configuración sobre convención rígida.
5. `OBJ-01` dice "ejecutar pipelines BETO completos desde la GUI" — sin restricción a un pipeline canónico específico.
6. Sin embargo, `StageType` es un enum con valores definidos (`reasoning`, `code_generation`, `code_review`, `custom`) — hay tipos de stage conocidos, pero su combinación y orden es libre.

**Derivación**:

El sistema soporta pipeline **completamente configurable** por proyecto, con la restricción de que los `stage_type` deben ser valores conocidos del enum `StageType`. No existe un pipeline "canónico" obligatorio. El pipeline en `config.yaml` es el **default global**; cada proyecto puede sobrescribirlo vía `pipeline_config_override` en `CreateProjectCmd`.

---

> **RESOLUCIÓN FINAL OQ-004**: Los stages del pipeline son **completamente configurables** por proyecto. No existe un pipeline canónico obligatorio. La única restricción es que `stage_type` debe ser un valor del enum `StageType` (`reasoning`, `code_generation`, `code_review`, `custom`). El pipeline default se define en `config.yaml` global y puede sobrescribirse por proyecto en `CreateProjectCmd.pipeline_config_override`.

**Especificación de comportamiento**:

```python
# Resolución de pipeline config en ProjectManager.create_project()
def _resolve_pipeline_config(
    self,
    override: Optional[dict],
    global_config: PipelineConfig
) -> PipelineConfig:
    """
    Si override es None → usar global_config sin modificación.
    Si override es dict parcial → merge: override prevalece sobre global.
    Si override es dict completo → reemplaza completamente.
    
    Validación: cada stage.type debe ser valor de StageType enum.
    Validación: cada stage.plugin_role debe ser rol registrado en config.plugins.roles.
    """
    if override is None:
        return global_config
    try:
        return PipelineConfig(**{**global_config.to_dict(), **override})
    except (TypeError, ValueError) as e:
        raise ValueError(f"Pipeline config inválida: {e}")
```

**Impacto en nodos**:
- `P-03.1 ProjectManager`: Implementar `_resolve_pipeline_config()` en `create_project()`.
- `P-02 API Layer`: Schema `ProjectCreate` incluye campo `pipeline_config_override: Optional[dict] = None`.
- `P-06 Persistence`: Serializar `PipelineConfig` como parte del documento `project.json`.
- `P-01 Presentation Layer`: Formulario de creación de proyecto puede incluir editor YAML/JSON para override (campo avanzado, colapsado por defecto).

**Tabla canónica de tipos de stage**:

| `StageType` | Plugin Role por defecto | Descripción |
|---|---|---|
| `reasoning` | `reasoning_engine` | Análisis, diseño, razonamiento estructurado |
| `code_generation` | `code_engine` | Generación de código desde especificación |
| `code_review` | `code_engine` | Revisión de código con criterios |
| `custom` | Configurable | Stage de propósito general |

---

### OQ-010 — Jinja2 SSR vs. SPA pura con HTML estático

**Core origen**: BETO_CORE_DRAFT §7.1  
**Estado previo**: ABIERTA — "Afecta cómo FastAPI sirve la GUI y si Jinja2 es dependencia"

#### Análisis de derivación BETO_ASSISTED

**Evidencia del SYSTEM INTENT**:

1. `ADR-002`: "Vanilla JS sobre frameworks — HTML + CSS + JS mínimo (EventSource API, fetch)". El mandato es **mínima dependencia**.
2. `BETO_CORE_DRAFT §1.3` anti-objetivo: "Mínima dependencia de librerías externas (filosofía stdlib-first)".
3. `requirements.txt` en `BETO_CORE_DRAFT §2.3` **no incluye Jinja2** en la lista de dependencias declaradas.
4. `BETO_SYSTEM_GRAPH P-01` especifica que los entregables son "index.html + css/style.css + js/{app,sse,api}.js" — archivos estáticos.
5. `BETO_SYSTEM_GRAPH C-20` (GUI Static Server) fue clasificado como INTERNAL absorbido en P-02 vía `app.mount` — lo que implica `StaticFiles`, no templates.
6. `P-01.1 SSE Client` usa `EventSource` nativo; `P-01.2 API Client` usa `fetch` nativo — ambos son SPA patterns, no SSR patterns.
7. La GUI "Funcional sin JS para vistas read-only" (progressive enhancement) se logra con HTML estático bien estructurado + CSS, sin necesidad de SSR.

**Derivación**:

La evidencia converge unívocamente en **SPA pura con HTML estático**. Jinja2 no es dependencia del sistema. FastAPI sirve los archivos estáticos via `StaticFiles`. La vista inicial se renderiza cargando datos via fetch/SSE desde JS.

---

> **RESOLUCIÓN FINAL OQ-010**: La GUI es una **SPA pura con archivos HTML/CSS/JS estáticos**. FastAPI usa `StaticFiles` para servir `beto/static/`. **No se usa Jinja2**; no es dependencia del proyecto. El HTML inicial (`index.html`) es un shell estático; los datos se cargan vía `fetch()` y `EventSource` desde JS.

**Especificación de implementación**:

```python
# beto/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

def create_app() -> FastAPI:
    app = FastAPI(title="BETO v2", version="0.1.0")
    
    # Montar archivos estáticos
    static_dir = Path(__file__).parent / "static"
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    # html=True → sirve index.html en rutas sin archivo match (SPA fallback)
    
    # Registrar routers API ANTES del mount estático
    from beto.api.routes import projects, runs, gates, plugins, events
    app.include_router(projects.router, prefix="/api")
    app.include_router(runs.router, prefix="/api")
    app.include_router(gates.router, prefix="/api")
    app.include_router(plugins.router, prefix="/api")
    app.include_router(events.router, prefix="/api")
    
    return app
```

**Estructura de `index.html`**:
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>BETO v2</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <!-- Shell estático: estructura sin datos -->
  <header id="app-header">
    <h1>BETO v2</h1>
    <div id="plugin-status"><!-- Poblado por JS --></div>
  </header>
  <main>
    <section id="projects-panel"><!-- Poblado por JS --></section>
    <section id="runs-panel"><!-- Poblado por JS --></section>
    <div id="gate-overlay" hidden><!-- Gate Panel Modal --></div>
  </main>
  <!-- Scripts al final del body -->
  <script src="/js/api-client.js" type="module"></script>
  <script src="/js/sse-client.js" type="module"></script>
  <script src="/js/app.js" type="module"></script>
</body>
</html>
```

**Impacto en nodos**:
- `P-01 Presentation Layer`: Confirmado como SPA. No requiere template engine.
- `P-02 API Layer`: Confirmado uso de `StaticFiles`. No requiere `Jinja2Templates`.
- `requirements.txt`: Jinja2 **no se incluye**.
- `pyproject.toml`: Jinja2 **no se incluye** en dependencias.

---

### OQ-R01 — `confidence_score` en `ReasoningResult`

**Core origen**: BETO_CORE_MOTOR_RAZONAMIENTO §2  
**Estado previo**: ABIERTA — "¿Campo float 0-1 auto-reportado por el LLM?"

#### Análisis de derivación BETO_ASSISTED

**Evidencia del SYSTEM INTENT**:

1. `BETO_CORE_DRAFT §1.2 OBJ-05`: "100% de gates pasan por aprobación humana." La evaluación de calidad del output es **responsabilidad del operador**, no del sistema.
2. `BETO_CORE_GATES_OPERADOR §1.4` anti-objetivo: "No tiene lógica de negocio para evaluar si un output es 'correcto'; eso es responsabilidad del operador."
3. `BETO_CORE_MOTOR_RAZONAMIENTO §1.3` anti-objetivo: "No implementa evaluación automática de calidad del razonamiento (gate del operador lo cubre)."
4. Los LLMs actuales producen `confidence_score` auto-reportados altamente no confiables (hallucination-prone). Incluir este campo crearía una falsa señal de calidad que podría sesgar la decisión del operador, contradiciendo OBJ-05.
5. El campo está comentado en el código de `ReasoningResult` con el comentario `# OQ-R01: confidence_score pendiente de decisión` — el autor del CORE ya anticipó la posibilidad de omisión.
6. Filosofía "stdlib-first" y mínima complejidad: agregar un campo no confiable agrega complejidad sin valor.

**Derivación**:

El `confidence_score` **se omite** de `ReasoningResult`. Incluirlo contradice el principio de supervisión humana activa (el operador podría confiar ciegamente en un score no confiable) y el anti-objetivo de no evaluar calidad automáticamente.

---

> **RESOLUCIÓN FINAL OQ-R01**: El campo `confidence_score` **no se incluye** en `ReasoningResult` en v2. La evaluación de confianza/calidad del razonamiento es responsabilidad exclusiva del operador humano via el Gate Panel. Los LLMs auto-reportan confianza de forma no confiable; incluir el campo introduciría ruido y potencialmente sesgaría la supervisión humana, contradiciendo OBJ-05.

**Especificación de implementación**:

```python
# beto/plugins/base.py — ReasoningResult FINAL
@dataclass
class ReasoningResult:
    reasoning_text: str
    conclusions: list[str]
    reasoning_steps: list[ReasoningStep] = field(default_factory=list)
    parsed_structured: bool = False
    stage_id: str = ""
    model_used: str = ""
    tokens_used: Optional["TokenUsage"] = None
    raw_output: str = ""
    generated_at: Optional[datetime] = None
    # confidence_score: OMITIDO — ver OQ-R01 en CIERRE_ASISTIDO.md
```

**Nota de extensibilidad**: Si en v3 se requiere evaluación de confianza via LLM-as-judge externo (no auto-reportado), se añade como stage `custom` separado, no como campo de `ReasoningResult`.

**Impacto en nodos**:
- `BETO_CORE_MOTOR_RAZONAMIENTO §4.1`: Remover línea comentada de `confidence_score`.
- `P-01.3 Gate Panel UI`: No renderizar campo de confianza.
- `P-02 schemas.py`: No incluir en `ReasoningResultSchema`.

---

### OQ-R02 — Streaming dentro de `reason()` vs. solo en `stream_complete()`

**Core origen**: BETO_CORE_MOTOR_RAZONAMIENTO §3.2 IADR-R03  
**Estado previo**: ABIERTA — "Impacta contrato de ReasoningEnginePlugin y complejidad de P-03.2"

#### Análisis de derivación BETO_ASSISTED

**Evidencia del SYSTEM INTENT**:

1. `BETO_CORE_MOTOR_RAZONAMIENTO IADR-R03`: "El streaming se activa si `stage_config.streaming: true`. En modo streaming, `run_stage` usa `stream_complete()` y emite eventos `stage_progress`." — El IADR ya resuelve que el streaming es responsabilidad de `run_stage`, no de `reason()`.
2. `BETO_CORE_MOTOR_RAZONAMIENTO §5.3` "Contrato de Streaming": El pseudocódigo usa `plugin.stream_complete(llm_request)` directamente desde `run_stage`, no `plugin.reason()`.
3. `IADR-R01`: "`reason()` encapsula la construcción del prompt y el parsing del output" — su contrato es `async def reason(...) -> ReasoningResult`, retorno único, no iterator.
4. Mantener `reason()` como non-streaming simplifica: (a) el contrato del ABC, (b) el testing de la lógica de parsing, (c) la implementación de adaptadores concretos.
5. El streaming es una optimización de UX (mostrar progreso al operador), no un requisito funcional del razonamiento. La `ReasoningResult` es el artefacto funcional.

**Derivación**:

`reason()` es **siempre non-streaming** y retorna `ReasoningResult`. El streaming de tokens durante razonamiento es responsabilidad de `run_stage()` en P-03.2, que usa `stream_complete()` directamente y acumula tokens para llamar a `parse_reasoning_output()` al finalizar.

---

> **RESOLUCIÓN FINAL OQ-R02**: `reason()` es **siempre non-streaming** y retorna `ReasoningResult` completo. El streaming de tokens se implementa en `P-03.2 run_stage()` usando `plugin.stream_complete(llm_request)` directamente cuando `stage_config.streaming = true`. El flujo streaming en `run_stage()` acumula el texto y llama a `plugin.parse_reasoning_output(accumulated_text)` al finalizar para construir el `ReasoningResult`. El contrato de `ReasoningEnginePlugin.reason()` no cambia.

**Especificación de implementación en `run_stage()`**:

```python
# beto/orchestrator/pipeline_engine.py — P-03.2
async def _execute_reasoning_stage(
    self,
    stage_config: StageConfig,
    context: PipelineContext,
    plugin: ReasoningEnginePlugin,
    reasoning_request: ReasoningRequest,
) -> ReasoningResult:
    """
    Despacha al modo correcto según stage_config.streaming.
    """
    if stage_config.extra_params.get("stream", False):
        # Modo streaming: tokens parciales via EventBus
        llm_request = LLMRequest(
            messages=plugin.build_reasoning_prompt(reasoning_request),
            model=plugin.supported_models[0],
            temperature=reasoning_request.temperature,
            stream=True,
        )
        accumulated = ""
        async for token in plugin.stream_complete(llm_request):
            accumulated += token
            await self._event_bus.publish(BETOEvent(
                event_type="stage_progress",
                project_id=str(context.project_id),
                run_id=str(context.run_id),
                stage_id=stage_config.id,
                payload={"partial_output": accumulated}
            ))
        # Parsear resultado acumulado
        result = plugin.parse_reasoning_output(accumulated, stage_config.id)
        result.model_used = plugin.supported_models[0]
        return result
    else:
        # Modo directo: reason() completo, sin streaming
        return await plugin.reason(reasoning_request)
```

**Impacto en nodos**:
- `BETO_CORE_MOTOR_RAZONAMIENTO §5.1`: ABC `ReasoningEnginePlugin.reason()` permanece sin cambios.
- `P-03.2 StageExecutionEngine`: Implementar `_execute_reasoning_stage()` con doble modo.
- `BETO_CORE_MOTOR_RAZONAMIENTO §4.1 ReasoningResult`: Sin cambios en schema.

---

### OQ-CE-01 — Extracción automática de bloques markdown de código

**Core origen**: BETO_CORE_MOTOR_CODIGO §1  
**Estado previo**: ABIERTA — "¿Extracción de bloques ` ```lang ... ``` ` o output raw es suficiente?"

#### Análisis de derivación BETO_ASSISTED

**Evidencia del SYSTEM INTENT**:

1. `BETO_CORE_MOTOR_CODIGO §4.1` ya define `CodeBlock` como dataclass con campos `language`, `content`, `filename` — indicando que el autor del CORE anticipó la extracción como implementable.
2. `BETO_CORE_MOTOR_CODIGO §4.1 CodeGenerationResult`: El campo `code_blocks: List[CodeBlock]` ya está definido; `code: str` es el raw output. La estructura soporta ambos.
3. Los LLMs con interfaz OpenAI-compatible (GPT-4o, Ollama, LM Studio) **consistentemente** envuelven
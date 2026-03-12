# BETO_CORE_DRAFT.md
## BETO Framework v4.2 — Sistema de Automatización con GUI Web
### Estado: DRAFT | Versión: 0.1.0 | Fecha: 2025-01-31

---

## ÍNDICE DE SECCIONES

1. [Visión y Objetivos](#1-visión-y-objetivos)
2. [Alcance y Límites](#2-alcance-y-límites)
3. [Arquitectura General](#3-arquitectura-general)
4. [Modelo de Dominio](#4-modelo-de-dominio)
5. [Arquitectura de Plugins LLM](#5-arquitectura-de-plugins-llm)
6. [Pipeline y Gates](#6-pipeline-y-gates)
7. [Interfaz Gráfica Web](#7-interfaz-gráfica-web)
8. [Persistencia](#8-persistencia)
9. [Concurrencia y Proyectos Múltiples](#9-concurrencia-y-proyectos-múltiples)
10. [Open Questions (OQs)](#10-open-questions-oqs)

---

## 1. VISIÓN Y OBJETIVOS

### 1.1 Visión

BETO v2 es un sistema de automatización de pipelines de razonamiento y generación de código, operado por un humano como supervisor activo, con motores LLM intercambiables y visualización en tiempo real del estado del pipeline. La GUI web minimalista (sin frameworks JS) es la interfaz primaria de operación.

### 1.2 Objetivos Primarios

| ID | Objetivo | Métrica de Éxito |
|----|----------|-----------------|
| OBJ-01 | Ejecutar pipelines BETO completos desde la GUI | Pipeline ejecuta end-to-end sin CLI |
| OBJ-02 | Intercambiar motores LLM sin reiniciar el sistema | Hot-swap validado en < 30s |
| OBJ-03 | Visualizar progreso en tiempo real | Latencia de actualización ≤ 2s |
| OBJ-04 | Soportar múltiples proyectos concurrentes | ≥ 3 proyectos simultáneos sin degradación |
| OBJ-05 | Gates aprobados por operador desde GUI | 100% de gates pasan por aprobación humana |
| OBJ-06 | Persistencia local sin base de datos externa | Solo archivos JSON en disco local |

### 1.3 Objetivos Secundarios

- Mínima dependencia de librerías externas (filosofía "stdlib-first")
- Despliegue en máquina local sin contenedores (opcional containerización)
- Auditoría completa de decisiones del operador en logs estructurados

### 1.4 Anti-objetivos Explícitos

- **No** es un sistema multi-usuario con autenticación
- **No** requiere base de datos relacional o NoSQL
- **No** usa frameworks JS (React, Vue, Angular, etc.)
- **No** es un sistema cloud-native en su versión inicial
- **No** gestiona secretos en producción (fuera de alcance v2)

---

## 2. ALCANCE Y LÍMITES

### 2.1 Dentro del Alcance (In-Scope)

```
✅ API REST + SSE con FastAPI
✅ GUI web: HTML + CSS + Vanilla JS mínimo (solo para SSE/fetch)
✅ Plugin system para motores LLM (OpenAI-compatible interface)
✅ Pipeline engine con stages configurables
✅ Gate system con aprobación humana desde GUI
✅ Múltiples proyectos concurrentes (asyncio-based)
✅ Persistencia JSON local (proyectos, runs, configuración)
✅ Motor de razonamiento intercambiable vía config
✅ Motor de código intercambiable vía config
✅ Visualización en tiempo real (SSE primario, polling fallback)
✅ Configuración por archivo (YAML/JSON)
```

### 2.2 Fuera del Alcance (Out-of-Scope v2)

```
❌ Autenticación y autorización de usuarios
❌ Despliegue cloud / Kubernetes
❌ Bases de datos SQL/NoSQL
❌ Frameworks JS frontend
❌ Ejecución de código generado en sandbox automático
❌ API pública versionada para terceros
❌ Notificaciones push / email
❌ Métricas y observabilidad distribuida (Prometheus, etc.)
```

> **OQ-001**: ¿La ejecución de código generado por BETO está completamente fuera de alcance v2, o existe un modo "dry-run preview" que debe incluirse? → Requiere decisión de negocio.

### 2.3 Dependencias Externas

| Dependencia | Versión Mínima | Justificación |
|-------------|----------------|---------------|
| Python | 3.11+ | asyncio mejorado, tomllib nativo |
| FastAPI | 0.110+ | SSE support, async nativo |
| Uvicorn | 0.27+ | ASGI server |
| httpx | 0.27+ | Cliente HTTP async para LLM APIs |
| Pydantic | 2.x | Validación de modelos |
| PyYAML | 6.x | Configuración YAML |

---

## 3. ARQUITECTURA GENERAL

### 3.1 Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│         HTML/CSS + Vanilla JS (fetch, EventSource)          │
│                   Servido por FastAPI                        │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP REST + SSE
┌─────────────────────▼───────────────────────────────────────┐
│                    API LAYER (FastAPI)                       │
│  /projects  /runs  /gates  /plugins  /config  /events (SSE) │
└──────┬──────────────────────────────────────┬───────────────┘
       │                                      │
┌──────▼──────────────┐          ┌────────────▼───────────────┐
│   ORCHESTRATOR      │          │    EVENT BUS               │
│   (Pipeline Engine) │◄────────►│    (asyncio.Queue)         │
│   Project Manager   │          │    SSE Broadcaster         │
└──────┬──────────────┘          └────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────────┐
│                    PLUGIN LAYER                              │
│  ┌──────────────────┐    ┌──────────────────────────────┐   │
│  │  Reasoning Engine│    │    Code Engine               │   │
│  │  Plugin Interface│    │    Plugin Interface          │   │
│  └──────┬───────────┘    └──────────────┬───────────────┘   │
│         │                               │                    │
│  ┌──────┴──────────────────────────────┴───────────────┐    │
│  │           LLM Adapter (OpenAI-compatible)            │    │
│  │     [OpenAI] [Anthropic*] [Ollama] [LM Studio]      │    │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────────┐
│                  PERSISTENCE LAYER                           │
│              JSON Store (FileSystem)                        │
│    projects/{id}/  runs/{id}/  config/  plugins/            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Decisiones Arquitectónicas (ADRs)

#### ADR-001: FastAPI sobre Flask/aiohttp
**Decisión**: FastAPI  
**Razón**: SSE nativo via `StreamingResponse`, tipado con Pydantic, async-first, menor boilerplate que aiohttp.  
**Consecuencia**: Requiere Python 3.11+, Pydantic v2.

#### ADR-002: Vanilla JS sobre frameworks
**Decisión**: HTML + CSS + JS mínimo (EventSource API, fetch)  
**Razón**: Mandato explícito del sistema. Reduce complejidad de build.  
**Consecuencia**: UI menos reactiva; compensar con SSE para updates críticos.

#### ADR-003: asyncio como runtime de concurrencia
**Decisión**: asyncio + FastAPI  
**Razón**: Proyectos múltiples concurrentes sin overhead de threads OS.  
**Consecuencia**: Todo código de plugins debe ser async-compatible.

> **OQ-002**: ¿Los plugins LLM bloqueantes (sync) deben ejecutarse en `ThreadPoolExecutor` automáticamente, o es responsabilidad del plugin implementar async? → Impacta contrato de plugin interface.

#### ADR-004: JSON local sobre SQLite
**Decisión**: JSON files  
**Razón**: Mandato explícito. Máxima portabilidad, zero dependencies.  
**Consecuencia**: Sin transacciones ACID. Riesgo de corrupción en crash.

> **OQ-003**: ¿Se requiere mecanismo de write-ahead (atomic rename) para proteger JSON de corrupción por crash? → Impacta diseño de persistence layer.

### 3.3 Estructura de Directorios

```
beto-v2/
├── beto/
│   ├── __init__.py
│   ├── main.py                    # Entrypoint FastAPI app
│   ├── config.py                  # Config loader (YAML/JSON)
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── pipeline_engine.py     # Pipeline runner
│   │   ├── project_manager.py     # Multi-project coordinator
│   │   └── gate_manager.py        # Gate state machine
│   ├── plugins/
│   │   ├── __init__.py
│   │   ├── base.py                # Plugin interfaces (ABC)
│   │   ├── registry.py            # Plugin registry & loader
│   │   └── adapters/
│   │       ├── openai_adapter.py
│   │       ├── ollama_adapter.py
│   │       └── lmstudio_adapter.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── projects.py
│   │   │   ├── runs.py
│   │   │   ├── gates.py
│   │   │   ├── plugins.py
│   │   │   └── events.py         # SSE endpoint
│   │   └── schemas.py            # Pydantic request/response models
│   ├── events/
│   │   ├── __init__.py
│   │   ├── bus.py                # asyncio.Queue-based event bus
│   │   └── broadcaster.py        # SSE fan-out
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── json_store.py         # Atomic JSON R/W
│   │   └── models.py             # Dataclasses persistibles
│   └── static/                   # Servido por FastAPI
│       ├── index.html
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── app.js
│           ├── sse-client.js
│           └── api-client.js
├── data/                          # Persistencia JSON (gitignored)
│   ├── projects/
│   ├── runs/
│   └── config/
├── plugins_ext/                   # Plugins externos (descubiertos en runtime)
├── config.yaml                    # Configuración principal
├── pyproject.toml
├── requirements.txt
└── tests/
```

---

## 4. MODELO DE DOMINIO

### 4.1 Entidades Principales

```
┌─────────────────────────────────────────────────────────────┐
│  PROJECT                                                     │
│  ─────────────────────────────────────────────────────────  │
│  id: UUID                                                    │
│  name: str                                                   │
│  description: str                                            │
│  status: ProjectStatus                                       │
│  pipeline_config: PipelineConfig                            │
│  plugin_assignments: PluginAssignmentMap                    │
│  created_at: datetime                                        │
│  updated_at: datetime                                        │
│  runs: List[RunRef]                                          │
└─────────────────────────────────────────────────────────────┘
         │ 1
         │ has many
         ▼ N
┌─────────────────────────────────────────────────────────────┐
│  RUN                                                         │
│  ─────────────────────────────────────────────────────────  │
│  id: UUID                                                    │
│  project_id: UUID                                            │
│  status: RunStatus                                           │
│  stages: List[StageExecution]                               │
│  current_stage_index: int                                    │
│  started_at: datetime                                        │
│  completed_at: Optional[datetime]                            │
│  error: Optional[str]                                        │
└─────────────────────────────────────────────────────────────┘
         │ 1
         │ contains
         ▼ N
┌─────────────────────────────────────────────────────────────┐
│  STAGE_EXECUTION                                             │
│  ─────────────────────────────────────────────────────────  │
│  stage_id: str                                               │
│  stage_type: StageType                                       │
│  status: StageStatus                                         │
│  plugin_used: str                                            │
│  input_snapshot: dict                                        │
│  output_snapshot: dict                                       │
│  gate: Optional[Gate]                                        │
│  started_at: datetime                                        │
│  completed_at: Optional[datetime]                            │
│  tokens_used: Optional[TokenUsage]                           │
└─────────────────────────────────────────────────────────────┘
         │ 0..1
         │ may have
         ▼
┌─────────────────────────────────────────────────────────────┐
│  GATE                                                        │
│  ─────────────────────────────────────────────────────────  │
│  id: UUID                                                    │
│  stage_id: str                                               │
│  run_id: UUID                                                │
│  status: GateStatus                                          │
│  gate_type: GateType                                         │
│  prompt_to_operator: str                                     │
│  operator_decision: Optional[OperatorDecision]               │
│  operator_notes: Optional[str]                               │
│  created_at: datetime                                        │
│  decided_at: Optional[datetime]                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Enumeraciones de Estado

```python
class ProjectStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"          # Esperando gate approval
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"

class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_GATE = "waiting_gate"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StageStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_GATE = "waiting_gate"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class GateStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"       # Aprobado con modificaciones del operador

class GateType(str, Enum):
    STAGE_TRANSITION = "stage_transition"
    OUTPUT_REVIEW = "output_review"
    ERROR_RECOVERY = "error_recovery"
    MANUAL = "manual"

class StageType(str, Enum):
    REASONING = "reasoning"
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    CUSTOM = "custom"
```

### 4.3 Configuración de Pipeline

```python
# Ejemplo config.yaml → PipelineConfig
pipeline:
  stages:
    - id: "problem_analysis"
      type: "reasoning"
      plugin_role: "reasoning_engine"
      gate_before: false
      gate_after: true
      gate_type: "output_review"
      prompt_template: "templates/problem_analysis.txt"
      
    - id: "solution_design"
      type: "reasoning"
      plugin_role: "reasoning_engine"
      gate_before: false
      gate_after: true
      gate_type: "stage_transition"
      
    - id: "code_generation"
      type: "code_generation"
      plugin_role: "code_engine"
      gate_before: true
      gate_after: true
      gate_type: "output_review"
      
    - id: "code_review"
      type: "code_review"
      plugin_role: "reasoning_engine"
      gate_before: false
      gate_after: true
      gate_type: "output_review"
```

> **OQ-004**: ¿Los stages del pipeline son fijos (definidos en BETO v1) o completamente configurables por proyecto? ¿Existe un pipeline "canónico" que debe respetarse? → Determina flexibilidad del PipelineConfig.

> **OQ-005**: ¿Un `GateType.MODIFIED` implica que el operador puede editar directamente el output del LLM antes de pasarlo al siguiente stage? Si es así, ¿qué campos son editables? → Impacta UI y modelo Gate.

---

## 5. ARQUITECTURA DE PLUGINS LLM

### 5.1 Contratos de Interfaz (ABCs)

```python
# beto/plugins/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, Optional, Any

@dataclass
class LLMMessage:
    role: str          # "system" | "user" | "assistant"
    content: str

@dataclass
class LLMRequest:
    messages: list[LLMMessage]
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    extra_params: dict = None   # Parámetros vendor-specific

@dataclass
class LLMResponse:
    content: str
    model: str
    finish_reason: str
    usage: TokenUsage
    raw_response: Optional[dict] = None   # Para debugging

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class LLMPlugin(ABC):
    """
    Contrato base para todos los plugins LLM.
    Compatible con la interfaz OpenAI v1.
    """
    
    @property
    @abstractmethod
    def plugin_id(self) -> str:
        """Identificador único del plugin. Ej: 'openai-gpt4', 'ollama-llama3'"""
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Nombre legible para la GUI"""
    
    @property
    @abstractmethod
    def supported_models(self) -> list[str]:
        """Modelos disponibles en este plugin"""
    
    @abstractmethod
    async def complete(self, request: LLMRequest) -> LLMResponse:
        """Completar una conversación. Non-streaming."""
    
    @abstractmethod
    async def stream_complete(
        self, request: LLMRequest
    ) -> AsyncIterator[str]:
        """Streaming token por token."""
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Verificar conectividad con el backend LLM."""
    
    async def initialize(self, config: dict) -> None:
        """Hook de inicialización. Override si necesario."""
        pass
    
    async def teardown(self) -> None:
        """Hook de cleanup. Override si necesario."""
        pass


class ReasoningEnginePlugin(LLMPlugin):
    """
    Especialización para motores de razonamiento.
    Añade capacidades de chain-of-thought.
    """
    
    @abstractmethod
    async def reason(
        self,
        problem: str,
        context: dict,
        constraints: list[str]
    ) -> "ReasoningResult":
        """Razonamiento estructurado sobre un problema."""


class CodeEnginePlugin(LLMPlugin):
    """
    Especialización para motores de generación de código.
    """
    
    @abstractmethod
    async def generate_code(
        self,
        specification: str,
        language: str,
        context: dict
    ) -> "CodeGenerationResult":
        """Generación de código a partir de especificación."""
    
    @abstractmethod
    async def review_code(
        self,
        code: str,
        criteria: list[str]
    ) -> "CodeReviewResult":
        """Revisión de código con criterios específicos."""
```

### 5.2 Plugin Registry

```python
# beto/plugins/registry.py — Pseudocódigo estructural

class PluginRegistry:
    """
    Registro central de plugins. Soporta:
    - Plugins built-in (en beto/plugins/adapters/)
    - Plugins externos (en plugins_ext/ o paths configurados)
    - Hot-swap de plugin activo por rol
    """
    
    _plugins: dict[str, LLMPlugin]        # plugin_id → instance
    _role_assignments: dict[str, str]      # role → plugin_id
    # Roles: "reasoning_engine", "code_engine", "review_engine"
    
    async def discover_plugins(self, search_paths: list[Path]) -> None:
        """Descubrir plugins via entry points o convención de naming."""
    
    async def register(self, plugin: LLMPlugin, config: dict) -> None:
        """Registrar y inicializar un plugin."""
    
    async def assign_role(self, role: str, plugin_id: str) -> None:
        """Asignar plugin a un rol. Hot-swap sin restart."""
    
    def get_for_role(self, role: str) -> LLMPlugin:
        """Obtener plugin activo para un rol."""
    
    async def health_check_all(self) -> dict[str, bool]:
        """Health check de todos los plugins registrados."""
```

### 5.3 Configuración de Plugins

```yaml
# config.yaml — sección plugins

plugins:
  # Asignaciones de rol (hot-swappable vía GUI)
  roles:
    reasoning_engine: "ollama-deepseek-r1"
    code_engine: "openai-gpt4o"
    review_engine: "ollama-deepseek-r1"
  
  # Definiciones de plugins disponibles
  definitions:
    - id: "openai-gpt4o"
      adapter: "openai"
      model: "gpt-4o"
      config:
        api_key_env: "OPENAI_API_KEY"
        base_url: "https://api.openai.com/v1"
        timeout: 60
        
    - id: "ollama-deepseek-r1"
      adapter: "ollama"
      model: "deepseek-r1:7b"
      config:
        base_url: "http://localhost:11434/v1"
        timeout: 120
        
    - id: "lmstudio-local"
      adapter: "openai"             # Reusar OpenAI adapter (compatible)
      model: "local-model"
      config:
        base_url: "http://localhost:1234/v1"
        api_key_env: "LMSTUDIO_KEY"   # Puede ser dummy
        timeout: 180
```

### 5.4 Mecanismo de Hot-Swap

```
Operador en GUI → PUT /api/plugins/roles/{role}
                         │
                    API Layer valida request
                         │
                    Registry.assign_role(role, new_plugin_id)
                         │
                    ┌────▼────────────────────────────────────┐
                    │ 1. Health check nuevo plugin             │
                    │ 2. Si OK → actualizar _role_assignments  │
                    │ 3. Persistir en config JSON              │
                    │ 4. Emitir evento SSE: plugin_swapped     │
                    │ 5. Runs EN CURSO usan nuevo plugin       │
                    │    desde el siguiente LLM call           │
                    └─────────────────────────────────────────┘
```

> **OQ-006**: ¿El hot-swap de plugin afecta runs en curso en el stage ACTUAL (mid-execution), o solo entra en efecto al inicio del siguiente stage? → Impacta atomicidad del swap.

> **OQ-007**: ¿Los plugins externos en `plugins_ext/` deben seguir el sistema de entry_points de Python, o es suficiente con convención de naming (ej: `beto_plugin_*.py`)? → Impacta mecanismo de discovery.

---

## 6. PIPELINE Y GATES

### 6.1 Pipeline Engine — Máquina de Estados

```
                    ┌──────────────┐
                    │   PENDING    │
                    └──────┬───────┘
                           │ start_run()
                    ┌──────▼───────┐
               ┌───►│   RUNNING    │◄──────────────────┐
               │    └──────┬───────┘                   │
               │           │ stage completes             │
               │    ┌──────▼───────┐                   │
               │    │  GATE CHECK  │                   │
               │    └──────┬───────┘                   │
               │     gate? │ no gate                    │
               │    ┌──────▼───────┐                   │
               │    │ WAITING_GATE │                   │
               │    └──────┬───────┘                   │
               │           │ operator decides           │
               │    ┌──────▼──────────────────────┐    │
               │    │      GATE DECISION           │    │
               │    │  APPROVED → next stage      ├────┘
               │    │  MODIFIED  → next stage     │
               │    │  REJECTED  → error/retry    │
               │    └─────────────────────────────┘
               │
        ┌──────┴───────┐         ┌──────────────┐
        │   COMPLETED  │         │    FAILED    │
        └──────────────┘         └──────────────┘
```

### 6.2 Gate Manager

```python
# beto/orchestrator/gate_manager.py — Estructura

class GateManager:
    """
    Gestiona el ciclo de vida de los gates.
    Bloquea la ejecución del pipeline hasta decisión del operador.
    """
    
    async def create_gate(
        self,
        run_id: UUID,
        stage_id: str,
        gate_type: GateType,
        context: dict
    ) -> Gate:
        """
        Crea gate, persiste en JSON, emite evento SSE.
        El pipeline queda suspendido (await en asyncio.Event).
        """
    
    async def process_decision(
        self,
        gate_id: UUID,
        decision: OperatorDecision,
        notes: Optional[str] = None,
        modified_output: Optional[dict] = None
    ) -> GateResolution:
        """
        Procesa decisión del operador.
        Resuelve el asyncio.Event bloqueante.
        Emite evento SSE de resolución.
        """
    
    async def wait_for_decision(self, gate_id: UUID) -> GateResolution:
        """
        Called by PipelineEngine. Blocks (async) hasta resolución.
        Implementado via asyncio.Event per gate.
        """
    
    async def get_pending_gates(self) -> list[Gate]:
        """Gates pendientes de todos los proyectos activos."""
```

### 6.3 Flujo de Ejecución de Stage

```
PipelineEngine.run_stage(stage_config, context)
│
├─► [gate_before = true] → GateManager.create_gate(STAGE_TRANSITION)
│                          → await GateManager.wait_for_decision()
│                          → if REJECTED: raise StageSkippedException
│
├─► Plugin.complete(request) / Plugin.reason() / Plugin.generate_code()
│   └─► emit SSE: stage_progress (tokens parciales si streaming)
│
├─► StageExecution guardado en JSON
│
└─► [gate_after = true] → GateManager.create_gate(OUTPUT_REVIEW)
                          → await GateManager.wait_for_decision()
                          → if MODIFIED: context.update(modified_output)
                          → if REJECTED: raise StageRetryException
```

> **OQ-008**: Cuando el operador RECHAZA un gate de OUTPUT_REVIEW, ¿el sistema debe: (a) re-ejecutar el mismo stage con el mismo prompt, (b) permitir al operador modificar el prompt antes de re-ejecutar, o (c) marcar el run como FAILED? → Define comportamiento de retry.

> **OQ-009**: ¿Existe un timeout para gates pendientes? ¿Un gate sin respuesta del operador en N horas debe auto-cancelarse? → Afecta recursos retenidos y UX.

### 6.4 Context Pipeline

El contexto fluye entre stages como un diccionario acumulativo:

```python
@dataclass
class PipelineContext:
    run_id: UUID
    project_id: UUID
    initial_input: dict          # Input del operador al iniciar run
    stage_outputs: dict[str, Any]  # stage_id → output
    metadata: dict               # Tokens usados, timestamps, etc.
    
    def get_for_stage(self, stage_id: str) -> dict:
        """Vista del contexto relevante para un stage específico."""
```

---

## 7. INTERFAZ GRÁFICA WEB

### 7.1 Principios de Diseño

- **Zero-framework**: Solo HTML5 + CSS3 + Vanilla JS (ES6+)
- **Server-first**: HTML generado/servido por FastAPI (`StaticFiles` + `Jinja2` opcional)
- **Progressive Enhancement**: Funcional sin JS para vistas read-only
- **SSE para updates**: `EventSource` API nativa del navegador

> **OQ-010**: ¿Se usa Jinja2 para server-side rendering del HTML inicial, o es SPA pura con HTML estático y API calls? → Afecta cómo FastAPI sirve la GUI y si Jinja2
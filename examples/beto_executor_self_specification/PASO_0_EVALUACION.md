# PASO_0_EVALUACION.md
## BETO Framework v4.2 — Evaluación de Elegibilidad

---

### METADATOS

```
Evaluador  : BETO Framework v4.2
Timestamp  : 2025-01-31T00:00:00Z
IDEA_ID    : BETO-v2-GUI-PLUGINS
Versión    : 1.0
```

---

### 1. RESUMEN DE LA IDEA RECIBIDA

Sistema BETO v2 con los siguientes componentes declarados:

| Componente | Descripción |
|---|---|
| GUI Web | FastAPI + HTML plano (sin frameworks JS) |
| Arquitectura | Plugin system para motores LLM intercambiables |
| Interfaz LLM | Compatible OpenAI API |
| Visualización | Pipeline en tiempo real (SSE o polling) |
| Concurrencia | Múltiples proyectos simultáneos |
| Gates | Aprobación humana desde GUI |
| Persistencia | JSON local |

---

### 2. CHECKLIST DE ELEGIBILIDAD

#### 2.1 Criterios Fundamentales

| # | Criterio | Estado | Notas |
|---|---|---|---|
| F-01 | ¿La idea tiene un objetivo central claro? | ✅ PASS | Automatización BETO con GUI operacional |
| F-02 | ¿Es implementable con tecnología existente? | ✅ PASS | FastAPI, SSE, JSON son tecnologías maduras |
| F-03 | ¿El scope es acotable en un sprint? | ⚠️ WARN | Múltiples subsistemas de alta complejidad |
| F-04 | ¿Existe un operador humano definido? | ✅ PASS | Explícito: aprobación de gates desde GUI |
| F-05 | ¿La persistencia está especificada? | ✅ PASS | JSON local declarado |

#### 2.2 Criterios de Arquitectura

| # | Criterio | Estado | Notas |
|---|---|---|---|
| A-01 | ¿Las interfaces entre componentes son definibles? | ✅ PASS | OpenAI-compatible es estándar conocido |
| A-02 | ¿La arquitectura de plugins está suficientemente especificada? | ⚠️ WARN | Falta definir contrato mínimo del plugin |
| A-03 | ¿El modelo de concurrencia está especificado? | ⚠️ WARN | "Múltiples proyectos" sin definir aislamiento |
| A-04 | ¿SSE vs polling está resuelto? | ⚠️ WARN | Ambigüedad "SSE o polling" — decisión pendiente |
| A-05 | ¿El esquema JSON de persistencia está definido? | ⚠️ WARN | No especificado — riesgo de deuda técnica |

#### 2.3 Criterios de Riesgo

| # | Criterio | Estado | Notas |
|---|---|---|---|
| R-01 | ¿Existe riesgo de scope creep? | ⚠️ WARN | Plugin system + concurrencia + GUI = superficie amplia |
| R-02 | ¿Hay dependencias externas críticas sin fallback? | ✅ PASS | Diseño intercambiable mitiga lock-in |
| R-03 | ¿El estado del pipeline es observable y recuperable? | ⚠️ WARN | Sin especificación de manejo de estado corrupto |
| R-04 | ¿Los gates de aprobación son auditables? | ⚠️ WARN | No se menciona log de decisiones del operador |
| R-05 | ¿Hay riesgo de condición de carrera en proyectos concurrentes? | ⚠️ WARN | JSON local + concurrencia = riesgo real no mitigado |

---

### 3. CONTEO DE RESULTADOS

```
✅ PASS   : 7
⚠️ WARN   : 8
❌ FAIL   : 0
```

---

### 4. WARNINGS ACTIVOS

A continuación se listan todos los warnings que deben ser resueltos o aceptados conscientemente antes de PASO_1.

---

#### ⚠️ WARN-01 — Ambigüedad en mecanismo de visualización en tiempo real
```
Componente : Visualización de pipeline
Riesgo     : MEDIO
Descripción: La idea declara "SSE o polling" sin tomar decisión. Son
             mecanismos con implicaciones arquitectónicas distintas.
             SSE requiere conexión persistente y manejo de reconexión.
             Polling es más simple pero introduce latencia configurable.
Impacto    : Afecta diseño de endpoints FastAPI y comportamiento del
             cliente HTML. Decidir post-PASO_0 genera retrabajo.
Acción     : Decidir mecanismo ANTES de PASO_1. Recomendación: SSE
             como primario con fallback a polling documentado.
```

---

#### ⚠️ WARN-02 — Contrato de plugin no especificado
```
Componente : Arquitectura de plugins LLM
Riesgo     : ALTO
Descripción: No existe definición del contrato mínimo que debe cumplir
             un plugin (métodos requeridos, manejo de errores,
             timeouts, formato de respuesta normalizado).
Impacto    : Sin contrato formal, los plugins serán incompatibles entre
             sí o requerirán adaptadores ad-hoc. Bloquea testabilidad.
Acción     : Definir PluginInterface (ABC o Protocol) en PASO_1 antes
             de cualquier implementación concreta.
```

---

#### ⚠️ WARN-03 — Modelo de concurrencia sin especificar para proyectos múltiples
```
Componente : Soporte multi-proyecto
Riesgo     : ALTO
Descripción: "Múltiples proyectos concurrentes" no define si el
             aislamiento es por proceso, por hilo, por asyncio task,
             o por worker. FastAPI es async por defecto, pero los
             LLM calls pueden ser bloqueantes según el plugin.
Impacto    : Sin modelo claro, un proyecto puede bloquear a otros.
             Posible starvation o contaminación de contexto.
Acción     : Especificar modelo de ejecución: asyncio tasks + executor
             para llamadas síncronas, o worker pool dedicado por
             proyecto. Decidir en PASO_1.
```

---

#### ⚠️ WARN-04 — Riesgo de condición de carrera en persistencia JSON
```
Componente : Persistencia JSON local + concurrencia
Riesgo     : ALTO
Descripción: JSON local con múltiples proyectos concurrentes escribiendo
             simultáneamente es una condición de carrera clásica.
             Sin mecanismo de locking, la corrupción de estado es
             probable bajo carga real.
Impacto    : Pérdida de estado de proyecto, resultados sobreescritos,
             pipeline en estado inconsistente.
Acción     : Implementar filelock por proyecto (un JSON por proyecto)
             O migrar a SQLite (compatible con "local", sin servidor).
             Definir estrategia en PASO_1.
```

---

#### ⚠️ WARN-05 — Esquema de persistencia JSON no definido
```
Componente : Persistencia / Estado del sistema
Riesgo     : MEDIO
Descripción: No existe definición del esquema de datos para proyectos,
             runs, estados de pipeline, resultados de gates ni
             historial de artefactos.
Impacto    : Sin esquema, las lecturas/escrituras serán inconsistentes
             entre componentes. Migraciones futuras serán costosas.
Acción     : Definir esquema base (Pydantic models) en PASO_1.
             Incluir versión de esquema para migraciones.
```

---

#### ⚠️ WARN-06 — Ausencia de log de auditoría para decisiones del operador
```
Componente : Gate de aprobación humana
Riesgo     : MEDIO
Descripción: Los gates de aprobación son decisiones críticas del
             operador. No se especifica si estas decisiones se registran
             con timestamp, usuario, contexto presentado y decisión
             tomada.
Impacto    : Sin auditoría, no es posible reproducir ni auditar por qué
             un pipeline avanzó o fue rechazado. Riesgo de compliance
             y debugging.
Acción     : Agregar gate_log a esquema de persistencia. Cada decisión
             debe registrar: timestamp, gate_id, decisión, contexto
             hash, operador_id (aunque sea "local").
```

---

#### ⚠️ WARN-07 — Manejo de estado corrupto o pipeline interrumpido
```
Componente : Estado del pipeline / Recuperación
Riesgo     : MEDIO
Descripción: No se especifica qué ocurre si un proyecto se interrumpe
             a mitad de ejecución (crash, timeout, error de plugin).
             ¿El pipeline es reanudable? ¿Se marca como FAILED?
             ¿Qué ve el operador en la GUI?
Impacto    : Sin manejo explícito, los proyectos quedarán en estado
             RUNNING indefinidamente. La GUI mostrará información
             incorrecta.
Acción     : Definir estados canónicos del pipeline (PENDING, RUNNING,
             AWAITING_GATE, FAILED, COMPLETED) y transiciones válidas.
             Incluir timeout y heartbeat mínimo.
```

---

#### ⚠️ WARN-08 — Scope potencialmente excesivo para implementación incremental
```
Componente : Scope general
Riesgo     : MEDIO
Descripción: La combinación de plugin system + concurrencia + GUI +
             SSE + multi-proyecto + gates es un scope que puede no
             ser completable en un ciclo. Ningún componente está
             marcado como MVP vs nice-to-have.
Impacto    : Riesgo de entrega parcial sin valor operacional.
             El sistema puede quedar en estado "casi funciona".
Acción     : Declarar explícitamente el MVP mínimo en PASO_1.
             Sugerencia de prioridad:
               P0: Un proyecto, un plugin, gates básicos, JSON simple
               P1: Multi-proyecto, plugin system formal
               P2: SSE, GUI avanzada, auditoría completa
```

---

### 5. DECISIÓN DE ELEGIBILIDAD

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   DECISIÓN:   GO_WITH_WARNINGS                               ║
║                                                              ║
║   Warnings críticos (ALTO):  3  [WARN-02, WARN-03, WARN-04] ║
║   Warnings medios (MEDIO):   5  [WARN-01, 05, 06, 07, 08]   ║
║   Blockers (FAIL):           0                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Justificación:**
La idea es técnicamente sólida y el objetivo es claro. No existen blockers fundamentales que impidan la implementación. Sin embargo, **3 warnings de riesgo ALTO** deben ser resueltos o explícitamente aceptados con mitigación documentada antes de avanzar a PASO_1. El sistema es viable si se establece un MVP disciplinado y se resuelven las ambigüedades de concurrencia, contrato de plugins y persistencia concurrente.

---

### 6. CONDICIONES PARA AVANCE A PASO_1

El equipo debe resolver o documentar posición sobre los siguientes puntos **antes** de ejecutar PASO_1:

- [ ] **C-01** Decisión tomada: SSE vs polling (resolver WARN-01)
- [ ] **C-02** PluginInterface definida conceptualmente (resolver WARN-02)
- [ ] **C-03** Modelo de concurrencia seleccionado (resolver WARN-03)
- [ ] **C-04** Estrategia de persistencia concurrente definida (resolver WARN-04)
- [ ] **C-05** MVP scope declarado con P0/P1/P2 (resolver WARN-08)

> Los WARN-05, WARN-06 y WARN-07 pueden resolverse dentro de PASO_1 como parte del diseño de esquemas.

---

### 7. FIRMA DEL EVALUADOR

```
Framework  : BETO Framework v4.2
Evaluador  : Módulo PASO_0 — Eligibility Gate
Estado     : CERRADO
Siguiente  : PASO_1_BLUEPRINT.md (condicionado a C-01..C-05)
Checksum   : BETO-v2-GUI-PLUGINS::GO_WITH_WARNINGS::8W::0F
```

---
*BETO Framework v4.2 — PASO_0_EVALUACION.md — FIN DEL DOCUMENTO*
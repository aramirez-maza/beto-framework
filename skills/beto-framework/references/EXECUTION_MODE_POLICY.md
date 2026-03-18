# EXECUTION_MODE_POLICY
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_1_ROUTING_TEMPLATES -->

---

## Propósito

Define la política oficial de modos de ejecución de BETO v4.4. Este documento es la fuente de verdad para qué puede y qué no puede hacer cada modo de ejecución. Las reglas aquí declaradas son de cumplimiento obligatorio y no pueden ser sobreescritas por optimizaciones locales.

---

## Principio de unificación

Todos los modos de ejecución viven bajo el mismo executor BETO, compartiendo:
- Reglas nucleares de no invención
- Trazabilidad completa
- Logging de auditoría
- Versión del framework
- Política de no invención
- Compatibilidad con OSC (BETO v4.3)

La diferencia entre modos es **de alcance y carga contextual**, no de autoridad epistemológica.

No existe una implementación paralela separada para tareas simples. BETO_LIGHT_PATH es una optimización interna, no un subsistema autónomo.

---

## Definición de modos

### BETO_LIGHT_PATH

**Alcance autorizado:**
- Tareas simples de una sola pieza
- Salida puntual sin múltiples artefactos estructurales
- Subproblemas locales dentro de un ciclo existente
- Tareas antes delegadas a un skill externo

**Contexto autorizado:**
- STABLE_CORE_CONTEXT (obligatorio)
- LOCAL_EXECUTION_CONTEXT del subproblema (obligatorio)
- CYCLE_CONTEXT mínimo si el subproblema lo requiere (opcional — solo campos declarados como necesarios)

**Prohibido en BETO_LIGHT_PATH:**
- Cargar BETO_SYSTEM_GRAPH completo
- Cargar MANIFEST_PROYECTO completo
- Cargar PHASE documents no requeridos
- Cargar más de 2 artefactos estructurales globales sin justificación
- Inventar alcance más allá del subproblema declarado
- Ignorar trazabilidad cuando aplique
- Generar artefactos incompatibles con el núcleo

**Condiciones de promoción automática:**
- Si se detecta OQ crítica no absorbible localmente → PROMOVER A PARTIAL o FULL
- Si se requiere graph → PROMOVER A FULL
- Si el scope se vuelve multiunidad → PROMOVER A PARTIAL o FULL
- Si la ambigüedad supera nivel 2 → PROMOVER A PARTIAL

---

### BETO_PARTIAL_PATH

**Alcance autorizado:**
- Tareas medianas o localizadas dentro de un ciclo BETO existente
- Cierre, validación o generación de artefactos puntuales
- Operaciones en una unidad específica del sistema

**Contexto autorizado:**
- STABLE_CORE_CONTEXT (obligatorio)
- CYCLE_CONTEXT de la unidad activa (obligatorio)
- LOCAL_EXECUTION_CONTEXT del subproblema (obligatorio)
- Artefactos declarados en MATERIALIZATION_SCOPE de la unidad

**Prohibido en BETO_PARTIAL_PATH:**
- Reconstruir el sistema completo sin necesidad declarada
- Cargar BETO_SYSTEM_GRAPH completo si solo se opera sobre una unidad
- Generar MANIFEST_PROYECTO nuevo si no fue autorizado

**Condiciones de promoción automática:**
- Si el scope se vuelve multiunidad → PROMOVER A FULL
- Si se requiere reconstrucción de autoridad estructural global → PROMOVER A FULL

---

### BETO_FULL_PATH

**Alcance autorizado:**
- Sistemas completos o ideas nuevas
- Arquitectura nueva o restructuración
- Generación de BETO_SYSTEM_GRAPH
- Generación de MANIFEST_PROYECTO
- Materialización integral
- Múltiples unidades con dependencias complejas

**Contexto autorizado:**
- Todo el contexto disponible del ciclo activo
- No hay restricciones de carga de contexto en FULL

**Responsabilidades adicionales:**
- El EXECUTION_ROUTER debe verificar que realmente se justifica el FULL antes de invocarlo
- Si el complexity_score es < 13 pero el operador o el route_promotion_evaluator lo declara necesario, debe dejarse traza en ROUTING_DECISION_RECORD

---

## Política de OSC en modo liviano

Si una tarea ejecutada en BETO_LIGHT_PATH activa una OQ crítica o un criterio OSC relevante:

1. Si el subproblema sigue siendo local y la OQ es resoluble localmente → ejecutar evaluación local OSC sin promover
2. Si la OQ crítica no puede cerrarse bajo contexto mínimo → PROMOVER A PARTIAL o FULL, registrar en ROUTE_PROMOTION_RECORD

Esta regla preserva la compatibilidad total con BETO v4.3 (OSC Layer).

---

## Política de caché por modo

| Capa de caché | LIGHT | PARTIAL | FULL |
|--------------|-------|---------|------|
| PREFIX_CACHE (instructivo, reglas, templates invariantes) | Siempre activa | Siempre activa | Siempre activa |
| SEMANTIC_CACHE (BETO_CORE cerrado, graph validado, manifests cerrados) | Opcional | Activa para unidad | Activa completa |
| OPERATIONAL_CACHE (snapshots activos, diffs recientes, outputs recientes, decisiones de ruta) | Solo para subproblema | Activa para unidad | Activa completa |

La caché no puede reemplazar autoridad semántica. Solo acelera reutilización de contexto ya autorizado.

---

## Configuración de umbrales

Los umbrales de routing son configurables por proyecto mediante una sección `routing_config` en el contexto del ciclo. Si no se declara configuración, se aplican los defaults:

```json
{
  "routing_thresholds": {
    "light_max": 5,
    "partial_max": 12,
    "full_min": 13
  },
  "weights": {
    "w1": 1, "w2": 1, "w3": 1, "w4": 2,
    "w5": 3, "w6": 2, "w7": 2, "w8": 2
  },
  "version": "v4.4_defaults"
}
```

**Los defaults deben documentarse explícitamente en todo ROUTING_DECISION_RECORD que los use.**

---

## Historial de versiones

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | 2026-03-18 | Versión inicial — BETO v4.4 |

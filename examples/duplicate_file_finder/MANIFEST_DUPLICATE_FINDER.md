# MANIFEST_BETO_DUPLICATE_FINDER.md

## METADATA

```
Name: BETO_CORE_DUPLICATE_FINDER
Type: Root (parallel)
Parent: None
Location: BETO_CORE_DUPLICATE_FINDER.md
Manifest generation timestamp: 2025-01-31T00:00:00Z
```

---

## PURPOSE AND SCOPE

```
Purpose: Define el sistema CLI que escanea un directorio recursivamente,
         detecta archivos duplicados por hash de contenido y genera un
         reporte con grupos de duplicados, rutas y espacio total recuperable.

Scope boundaries:
  In scope:
    - Aceptar un directorio objetivo como argumento CLI
    - Traversal recursivo del directorio objetivo
    - Cómputo de content_hash por archivo
    - Agrupación de archivos por content_hash idéntico
    - Cálculo del espacio recuperable por grupo y total
    - Generación de reporte con grupos, rutas y espacio recuperable

  Exclusions declared:
    - Eliminación o modificación de archivos
    - Deduplicación o acción destructiva sobre el filesystem
    - Escaneo de rutas remotas o montadas en red
    - Resolución de enlaces simbólicos o hard links (no declarada)
    - Scheduling, automatización o ejecución en background
```

---

## INPUT OUTPUT CONTRACT

```
Input contract source
  Reference: BETO_CORE_DUPLICATE_FINDER.md — Sección 3 (INPUTS AND OUTPUTS),
             Sección 7 (PHASE ARCHITECTURE — Phase 1 input)
  Summary:   Un único argumento CLI: la ruta del directorio objetivo.
             Todos los archivos alcanzables por traversal recursivo
             de ese directorio constituyen el dominio de procesamiento.

Output contract source
  Reference: BETO_CORE_DUPLICATE_FINDER.md — Sección 3 (INPUTS AND OUTPUTS),
             Sección 7 (PHASE ARCHITECTURE — Phase 5 output)
  Summary:   Un artefacto de reporte que contiene obligatoriamente:
             (1) uno o más grupos de archivos duplicados,
             (2) la lista de file_paths por grupo,
             (3) el total de espacio recuperable en bytes.
             El formato, estructura y canal de entrega están pendientes
             de resolución de OQ-6.
```

---

## DEPENDENCIES

```
Build prerequisites
  None (can be built independently)

Runtime dependencies
  None
```

---

## SUB BETO REGISTRY

```
Children list:

  - BETO_CORE_SCANNER
    Location:  not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Node ID:   GRAPH.SCANNER
    Phase:     1 — Discovery
    OQs own:   OQ-3 (non-critical), OQ-4 (critical), OQ-8 (critical)

  - BETO_CORE_HASHER
    Location:  not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Node ID:   GRAPH.HASHER
    Phase:     2 — Hashing
    OQs own:   OQ-1 (critical)

  - BETO_CORE_DUPLICATE_DETECTOR
    Location:  not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Node ID:   GRAPH.DUPLICATE_DETECTOR
    Phase:     3 — Grouping
    OQs own:   none

  - BETO_CORE_SPACE_CALCULATOR
    Location:  not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Node ID:   GRAPH.SPACE_CALCULATOR
    Phase:     4 — Space Calculation
    OQs own:   none

  - BETO_CORE_REPORT_COMPOSER
    Location:  not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Node ID:   GRAPH.REPORT_COMPOSER
    Phase:     5 — Report Generation
    OQs own:   OQ-6 (critical) — Gate G-2B OSC obligatorio antes de
               materialización

Depth
  Direct children only.
  Profundidad máxima observada: 1.
  No existen nodos SUBBETO. Todos los hijos son PARALLEL.
  Ningún nieto declarado.
```

---

## OPEN QUESTIONS STATUS

```
Open questions count: 8

Open questions summary:
  OQ-1 (OPEN — critical):   Algoritmo de hashing para content_hash.
                             Bloquea materialización de BETO_CORE_HASHER.
  OQ-2 (OPEN — non-critical): Pre-filtro por tamaño antes de hashing.
                             No bloquea ejecución.
  OQ-3 (OPEN — non-critical): Inclusión o exclusión de archivos de cero bytes.
                             Cierre interno de BETO_CORE_SCANNER.
  OQ-4 (OPEN — critical):   Comportamiento ante enlaces simbólicos.
                             Bloquea materialización de BETO_CORE_SCANNER.
  OQ-5 (OPEN — critical):   Lenguaje de implementación o runtime.
                             Bloquea materialización de todos los nodos hijos.
  OQ-6 (OPEN — critical):   Formato, estructura y canal de entrega del reporte.
                             Bloquea materialización de BETO_CORE_REPORT_COMPOSER.
                             Gate G-2B OSC obligatorio.
  OQ-7 (OPEN — non-critical): Opciones CLI adicionales más allá del directorio
                             objetivo.
  OQ-8 (OPEN — critical):   Comportamiento ante errores de permisos durante
                             traversal o hashing.
                             Bloquea materialización de BETO_CORE_SCANNER.

Closure policy reference:
  BETO_CORE_DUPLICATE_FINDER.md — Sección 9 (CURRENT SYSTEM STATE).
  OQs críticas con execution_readiness_check = FAIL_EXECUTIONAL_GAP bloquean
  la materialización del nodo afectado hasta resolución declarada por el operador.
  OQs no críticas pueden cerrarse con política por defecto si el operador lo
  autoriza. OQ-5 es global y debe cerrarse en el BETO_CORE raíz antes de que
  cualquier BETO_CORE hijo avance al Paso 8.
```

---

## EXECUTION AND CLOSURE STATE

```
BETO_CORE_STATUS.mode:          NORMAL
BETO_CORE_STATUS.compile_state: SUCCESS_WITH_WARNINGS

Warnings activos:
  - OQ-1, OQ-2, OQ-3, OQ-4, OQ-5, OQ-6, OQ-7, OQ-8 sin resolver
  - Ningún BETO_CORE hijo ha sido generado aún
  - OQ-5 (lenguaje) bloquea materialización global

Manifest eligibility rule:
  Este manifest solo se considera "entregable" cuando compile_state es
  SUCCESS_CLOSED. El estado actual es SUCCESS_WITH_WARNINGS.
  El manifest es válido para uso interno de planificación y expansión
  estructural, pero NO es un entregable final del sistema.
```

---

## DELIVERY STATUS

```
Status:        In progress
Manifest state: WARNING

Blocked reason:
  Las siguientes condiciones impiden el estado COMPLETE de este manifest:

  1. OQ-5 (lenguaje de implementación) sin resolver — bloquea
     materialización de todos los nodos hijos.
  2. OQ-1, OQ-4, OQ-6, OQ-8 (críticas) sin resolver — bloquean
     materialización de sus respectivos nodos hijos
     (HASHER, SCANNER, REPORT_COMPOSER, SCANNER).
  3. Ningún BETO_CORE hijo ha sido generado ni tiene estado COMPLETE.
  4. compile_state no ha alcanzado SUCCESS_CLOSED.

  Condición de desbloqueo:
  El manifest alcanzará estado COMPLETE cuando:
    (a) Todas las OQs críticas estén resueltas (DECLARED)
    (b) Todos los BETO_CORE hijos estén en estado COMPLETE
    (c) compile_state sea SUCCESS_CLOSED
```

---

## EVIDENCE

```
Primary evidence:
  - BETO_CORE file:      BETO_CORE_DUPLICATE_FINDER.md
  - TRACE_REGISTRY file: TRACE_REGISTRY_DUPLICATE_FINDER.md
                         (pendiente de generación en Paso 6)
  - Related outputs:
      BETO_SYSTEM_GRAPH.md                     — COMPLETE (VALIDATED)
      BETO_CORE_INTERVIEW_COMPLETED.md         — COMPLETE
      STRUCTURAL_CLASSIFICATION_REGISTRY.md    — COMPLETE
  - Tests or validations: no declarado
```

---

## CHANGELOG

```
2025-01-31T00:00:00Z  Created — MANIFEST_BETO_DUPLICATE_FINDER.md generado
                      desde BETO_CORE_DUPLICATE_FINDER.md v4.2 y
                      BETO_SYSTEM_GRAPH.md (VALIDATED)

2025-01-31T00:00:00Z  Status set: In progress / WARNING
                      compile_state: SUCCESS_WITH_WARNINGS
                      OQs 1–8 registradas como abiertas

2025-01-31T00:00:00Z  Sub BETO Registry poblado con 5 nodos PARALLEL
                      derivados de BETO_SYSTEM_GRAPH.md Sección 7

2025-01-31T00:00:00Z  Blocked reason declarado: OQ-5 global sin resolver,
                      OQs críticas por nodo sin resolver,
                      ningún BETO_CORE hijo generado
```
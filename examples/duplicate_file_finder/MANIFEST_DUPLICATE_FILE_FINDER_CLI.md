# MANIFEST_DUPLICATE_FILE_FINDER_CLI.md

# MANIFEST DE BETO

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
         reporte con grupos de duplicados, rutas de archivo y espacio
         total recuperable.

Scope boundaries:
  In scope:
    - Aceptar un directorio objetivo como argumento CLI
    - Traversal recursivo del directorio objetivo
    - Cómputo de content_hash por archivo
    - Agrupación de archivos por content_hash idéntico
    - Cálculo de espacio recuperable por grupo y total
    - Generación de reporte con grupos, rutas y espacio recuperable

  Out of scope:
    - Eliminación, modificación o movimiento de archivos
    - Deduplicación o cualquier acción destructiva sobre el filesystem
    - Escaneo de rutas remotas o montadas en red (no declarado)
    - Resolución de enlaces simbólicos o hard links (no declarado)
    - Programación, automatización o ejecución en background
```

---

## INPUT OUTPUT CONTRACT

```
Input contract source
  Reference: BETO_CORE_DUPLICATE_FINDER.md — Sección 3 (Inputs and Outputs)
  Summary: Un único directorio objetivo provisto como argumento CLI.
           Todos los archivos alcanzables mediante traversal recursivo
           de ese directorio.

Output contract source
  Reference: BETO_CORE_DUPLICATE_FINDER.md — Sección 3 (Inputs and Outputs)
  Summary: Un artefacto de reporte que contiene obligatoriamente:
           (1) uno o más grupos de archivos duplicados,
           (2) la lista de rutas de archivo por grupo,
           (3) el espacio total recuperable entre todos los grupos.
           Formato, estructura y canal de entrega pendientes de resolución
           de OQ-6.
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
Children list

  - BETO_CORE_SCANNER
    Location: not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Graph node: GRAPH.SCANNER
    Node type:  PARALLEL

  - BETO_CORE_HASHER
    Location: not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Graph node: GRAPH.HASHER
    Node type:  PARALLEL

  - BETO_CORE_DUPLICATE_DETECTOR
    Location: not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Graph node: GRAPH.DUPLICATE_DETECTOR
    Node type:  PARALLEL

  - BETO_CORE_SPACE_CALCULATOR
    Location: not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Graph node: GRAPH.SPACE_CALCULATOR
    Node type:  PARALLEL

  - BETO_CORE_REPORT_COMPOSER
    Location: not_generated_yet
    Manifest:  not_generated_yet
    Status:    DRAFT
    Graph node: GRAPH.REPORT_COMPOSER
    Node type:  PARALLEL

Depth
  Direct children only
  Profundidad máxima observada: 1
  Nietos declarados: ninguno
  Todos los nodos PARALLEL son hijos directos de GRAPH.ROOT.
  No existen nodos SUBBETO en la topología autorizada.
```

---

## OPEN QUESTIONS STATUS

```
Open questions count: 8

Open questions summary:

  OQ-1 [CRITICAL — OPEN]
    Algoritmo de hashing para content_hash (MD5, SHA-1, SHA-256, BLAKE2b u otro).
    execution_readiness_check: FAIL_EXECUTIONAL_GAP
    Nodo responsable de cierre: BETO_CORE_HASHER

  OQ-2 [NON-CRITICAL — OPEN]
    Pre-filtrado por tamaño antes del hashing para optimización de rendimiento.
    execution_readiness_check: NOT_EVALUATED
    Nodo responsable de cierre: BETO_CORE_HASHER o BETO_CORE_DUPLICATE_DETECTOR

  OQ-3 [NON-CRITICAL — OPEN]
    Inclusión o exclusión de archivos de cero bytes del proceso de detección.
    execution_readiness_check: NOT_EVALUATED
    Nodo responsable de cierre: BETO_CORE_SCANNER

  OQ-4 [CRITICAL — OPEN]
    Comportamiento ante enlaces simbólicos durante el traversal recursivo.
    execution_readiness_check: FAIL_EXECUTIONAL_GAP
    Nodo responsable de cierre: BETO_CORE_SCANNER

  OQ-5 [CRITICAL — OPEN]
    Lenguaje de programación o runtime de implementación.
    execution_readiness_check: FAIL_EXECUTIONAL_GAP
    Nodo responsable de cierre: BETO_CORE_DUPLICATE_FINDER (raíz)
    Efecto: global — bloquea materialización de todos los nodos hijos

  OQ-6 [CRITICAL — OPEN]
    Formato, estructura y canal de entrega del reporte (stdout, archivo,
    JSON, texto plano, CSV). Inclusión opcional de sección de resumen separada.
    execution_readiness_check: FAIL_EXECUTIONAL_GAP
    Nodo responsable de cierre: BETO_CORE_REPORT_COMPOSER
    Gate G-2B OSC obligatorio antes de materialización.

  OQ-7 [NON-CRITICAL — OPEN]
    Opciones CLI adicionales más allá del directorio objetivo
    (--output, --min-size, --exclude, --verbose u otras).
    execution_readiness_check: NOT_EVALUATED
    Nodo responsable de cierre: BETO_CORE_DUPLICATE_FINDER (raíz)

  OQ-8 [CRITICAL — OPEN]
    Comportamiento ante errores de permisos durante traversal o hashing
    (omitir silenciosamente, omitir con advertencia, abortar).
    execution_readiness_check: FAIL_EXECUTIONAL_GAP
    Nodo responsable de cierre: BETO_CORE_SCANNER

Closure policy reference:
  Las OQs críticas con execution_readiness_check = FAIL_EXECUTIONAL_GAP
  bloquean la materialización (Paso 8) del nodo responsable y de los
  nodos dependientes aguas abajo del pipeline. OQ-5 bloquea la
  materialización de todos los nodos hijos hasta su resolución en el
  BETO_CORE raíz. Las OQs no críticas con execution_readiness_check =
  NOT_EVALUATED pueden cerrarse con política por defecto declarada si el
  operador lo autoriza. Ninguna OQ puede resolverse por inferencia fuera
  de la frontera de expansión controlada (cerrada con aprobación del
  BETO_CORE_DRAFT). Toda resolución debe registrar estado DECLARED en
  Sección 9 del BETO_CORE correspondiente.
  Referencia formal: BETO_CORE_DUPLICATE_FINDER.md — Sección 5
  (Global Invariants), Sección 9 (Current System State).
```

---

## EXECUTION AND CLOSURE STATE

```
BETO_CORE_STATUS.mode: NORMAL
BETO_CORE_STATUS.compile_state: SUCCESS_WITH_WARNINGS

Warnings activos:
  - OQ-5 abierta: lenguaje de implementación no declarado.
    Bloquea materialización de todos los nodos hijos.
  - OQ-1 abierta: algoritmo de hashing no declarado.
    Bloquea materialización de BETO_CORE_HASHER.
  - OQ-4 abierta: comportamiento ante symlinks no declarado.
    Bloquea materialización de BETO_CORE_SCANNER.
  - OQ-6 abierta: formato y canal del reporte no declarados.
    Bloquea materialización de BETO_CORE_REPORT_COMPOSER.
    Gate G-2B OSC obligatorio.
  - OQ-8 abierta: comportamiento ante errores de permisos no declarado.
    Bloquea materialización de BETO_CORE_SCANNER.
  - Todos los BETO_CORE hijos en estado not_generated_yet.

Manifest eligibility rule:
  Este manifest solo se considera "entregable" cuando compile_state
  es SUCCESS_CLOSED. El estado actual es SUCCESS_WITH_WARNINGS debido
  a OQs críticas abiertas y BETO_CORE hijos no generados. El manifest
  no es entregable en este estado.
```

---

## DELIVERY STATUS

```
Status: In progress

Manifest state: WARNING

Blocked reason:
  Este manifest no alcanza estado COMPLETE por las siguientes razones:

  1. OQ-5 (lenguaje de implementación) permanece OPEN con
     execution_readiness_check = FAIL_EXECUTIONAL_GAP.
     Impacto: bloquea la materialización de los cinco nodos PARALLEL.

  2. OQs críticas adicionales abiertas: OQ-1, OQ-4, OQ-6, OQ-8.
     Cada una bloquea la materialización del nodo responsable respectivo.

  3. Los cinco BETO_CORE hijos están en estado not_generated_yet:
     BETO_CORE_SCANNER, BETO_CORE_HASHER, BETO_CORE_DUPLICATE_DETECTOR,
     BETO_CORE_SPACE_CALCULATOR, BETO_CORE_REPORT_COMPOSER.

  4. Ningún manifest hijo ha sido generado.

  El manifest alcanzará estado COMPLETE únicamente cuando:
  - Todas las OQs críticas estén en estado DECLARED (resueltas)
  - Los cinco BETO_CORE hijos hayan sido generados y sus manifests
    registren compile_state = SUCCESS_CLOSED
  - El BETO_CORE raíz actualice compile_state a SUCCESS_CLOSED
```

---

## EVIDENCE

```
Primary evidence
  - BETO_CORE file:      BETO_CORE_DUPLICATE_FINDER.md
  - TRACE_REGISTRY file: TRACE_REGISTRY_DUPLICATE_FINDER.md
                         (pendiente de generación en Paso 6)
  - Related outputs:
      BETO_SYSTEM_GRAPH.md                    (VALIDATED)
      BETO_CORE_INTERVIEW_COMPLETED.md        (referenciado en SYSTEM_GRAPH)
      STRUCTURAL_CLASSIFICATION_REGISTRY.md   (referenciado en SYSTEM_GRAPH)
  - Tests or validations: no declarado
```

---

## CHANGELOG

```
2025-01-31T00:00:00Z  Created — MANIFEST_DUPLICATE_FILE_FINDER_CLI.md generado
                      desde BETO_CORE_DUPLICATE_FINDER.md y
                      BETO_SYSTEM_GRAPH.md (status VALIDATED)

2025-01-31T00:00:00Z  Delivery status set: In progress / WARNING
                      Razón: cinco BETO_CORE hijos en not_generated_yet;
                      OQs críticas OQ-1, OQ-4, OQ-5, OQ-6, OQ-8 abiertas

2025-01-31T00:00:00Z  Sub BETO Registry poblado con cinco nodos PARALLEL
                      conforme a BETO_SYSTEM_GRAPH.md Sección 7

2025-01-31T00:00:00Z  Open questions count: 8 (5 críticas, 3 no críticas)
                      compile_state: SUCCESS_WITH_WARNINGS
```
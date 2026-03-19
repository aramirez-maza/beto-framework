# BETO_SYSTEM_GRAPH.md

## 1. METADATA

```
System name: Duplicate File Finder CLI
Graph generation timestamp: 2025-01-31T00:00:00Z
Source BETO_CORE: BETO_CORE_DUPLICATE_FINDER.md
Source interview: BETO_CORE_INTERVIEW_COMPLETED.md
Graph version: 1.0.0
Graph status: DRAFT
```

---

## 2. PURPOSE

Este artefacto representa la topología estructural formal del sistema BETO
después de la entrevista y de la clasificación estructural.

Su propósito es:

- Congelar la estructura del sistema antes de expandir BETO_CORE hijos
- Registrar nodos autorizados y sus relaciones
- Servir como base formal para PHASES, MANIFEST_BETO y MANIFEST_PROYECTO
- Impedir creación de nodos o relaciones no autorizadas en pasos posteriores

Este documento NO redefine el SYSTEM INTENT.
Este documento NO reemplaza al BETO_CORE.
Este documento NO introduce capacidades nuevas.

---

## 3. SOURCE OF AUTHORITY

```
Autoridad semántica:
  BETO_CORE_DUPLICATE_FINDER.md

Autoridad de descubrimiento estructural:
  BETO_CORE_INTERVIEW_COMPLETED.md

Autoridad de clasificación:
  STRUCTURAL_CLASSIFICATION_REGISTRY.md
  (Regla de Clasificación Estructural del BETO_INSTRUCTIVO v4.2)

Autoridad topológica:
  Este BETO_SYSTEM_GRAPH
```

Regla:
Todo nodo y toda relación declarados en este grafo deben ser derivables
de una detección realizada durante la entrevista y de una clasificación
formal válida según el instructivo.

Si un nodo o relación no puede trazarse a esas fuentes:
no puede existir en este grafo.

---

## 4. NODE TYPES AUTHORIZED

Tipos de nodo permitidos exclusivamente:

- ROOT
- PARALLEL
- SUBBETO

Definiciones:

```
ROOT
  Nodo troncal del sistema. Debe existir exactamente uno.

PARALLEL
  Capacidad funcional autónoma del sistema.
  Debe haber sido promovida mediante la regla de independencia semántica.

SUBBETO
  Nodo de refinamiento estructural.
  Debe haber sido promovido por ambigüedad estructural.
```

No se permiten otros tipos de nodo.

Nota de aplicación:
En este sistema no existen nodos SUBBETO. La clasificación formal
(STRUCTURAL_CLASSIFICATION_REGISTRY.md, Sección 4) determinó que todos
los candidatos evaluados satisfacen la condición de independencia de
internals ajenos y fueron clasificados como PARALLEL. Las OQs propias
de algunos nodos (OQ-3, OQ-4, OQ-6, OQ-8) se cierran dentro del
alcance de su respectivo BETO_CORE hijo y no constituyen fundamento
para clasificación SUBBETO.

---

## 5. EDGE TYPES AUTHORIZED

Tipos de relación permitidos exclusivamente:

- FUNCTIONAL_BRANCH
- STRUCTURAL_REFINEMENT
- DECLARED_DEPENDENCY

Definiciones:

```
FUNCTIONAL_BRANCH
  Relación entre ROOT y un nodo PARALLEL.
  Representa una rama funcional del sistema.

STRUCTURAL_REFINEMENT
  Relación entre cualquier nodo y un nodo SUBBETO.
  Representa descomposición vertical por ambigüedad estructural.

DECLARED_DEPENDENCY
  Relación declarativa entre nodos cuando uno requiere output del otro.
  No reemplaza la relación padre-hijo.
  No autoriza creación de nuevos nodos.
  No puede crear ciclos.
```

No se permiten otros tipos de relación.

Nota de aplicación:
En este sistema no se utilizan relaciones de tipo STRUCTURAL_REFINEMENT
dado que no existen nodos SUBBETO. Las relaciones de tipo
DECLARED_DEPENDENCY se utilizan para registrar el pipeline de datos
secuencial Scanner → Hasher → Duplicate Detector → Space Calculator →
Report Composer, conforme a la Advertencia-03 del
STRUCTURAL_CLASSIFICATION_REGISTRY.md (Sección 6).

---

## 6. ROOT NODE

```
Node ID:         GRAPH.ROOT
Node type:       ROOT
Name:            Duplicate File Finder CLI
Source:          BETO_CORE_DUPLICATE_FINDER.md
Parent:          NONE
Parent edge type: NONE
Purpose:         Nodo troncal del sistema. Orquesta el pipeline completo
                 de cinco fases: Discovery, Hashing, Grouping, Space
                 Calculation y Report Generation. Acepta un directorio
                 objetivo como argumento CLI, coordina la ejecución no
                 destructiva de todos los componentes PARALLEL, y produce
                 un reporte que expone grupos de archivos duplicados,
                 rutas por grupo y espacio total recuperable.
Status:          DRAFT
```

---

## 7. NODE REGISTRY

```
- Node ID:                        GRAPH.ROOT
  Node type:                      ROOT
  Name:                           Duplicate File Finder CLI
  Source section:                 BETO_CORE_INTERVIEW_COMPLETED.md — Sección 1,
                                  Sección 6 (Conceptual Model), Sección 7 (Phase
                                  Architecture)
  Parent:                         NONE
  Parent edge type:               NONE
  Purpose:                        Nodo troncal. Orquesta el pipeline completo de
                                  cinco fases sobre el sistema de archivos local.
                                  Punto de entrada CLI del usuario.
  Can exist independently:        YES
  Depends on internal logic
  of siblings:                    NO
  Classified by rule as:          ROOT
  Associated BETO_CORE target:    BETO_CORE_DUPLICATE_FINDER.md
  Status:                         DRAFT


- Node ID:                        GRAPH.SCANNER
  Node type:                      PARALLEL
  Name:                           Scanner
  Source section:                 BETO_CORE_INTERVIEW_COMPLETED.md — P3.6, P6.3,
                                  P6.4, P11.1, P11.4 (Sub-BETO 1);
                                  STRUCTURAL_CLASSIFICATION_REGISTRY.md —
                                  CAND-01, Sección 4
  Parent:                         GRAPH.ROOT
  Parent edge type:               FUNCTIONAL_BRANCH
  Purpose:                        Traversar recursivamente el directorio objetivo
                                  provisto como argumento CLI y producir la
                                  colección completa de File Entries con
                                  file_path y file_size. Implementa la Fase 1
                                  (Discovery) del pipeline declarado. Cierra
                                  las políticas de comportamiento ante enlaces
                                  simbólicos (OQ-4), errores de permisos (OQ-8)
                                  y archivos de cero bytes (OQ-3) dentro de su
                                  propio BETO_CORE hijo.
  Can exist independently:        YES
  Depends on internal logic
  of siblings:                    NO
  Classified by rule as:          PARALLEL
  Associated BETO_CORE target:    not_generated_yet
  Status:                         DRAFT


- Node ID:                        GRAPH.HASHER
  Node type:                      PARALLEL
  Name:                           Hasher
  Source section:                 BETO_CORE_INTERVIEW_COMPLETED.md — P6.3,
                                  P6.4, P11.1;
                                  STRUCTURAL_CLASSIFICATION_REGISTRY.md —
                                  CAND-02, Sección 4
  Parent:                         GRAPH.ROOT
  Parent edge type:               FUNCTIONAL_BRANCH
  Purpose:                        Computar el content_hash para cada File Entry
                                  a partir del contenido completo del archivo
                                  referenciado por file_path. Recibe la colección
                                  de File Entries (file_path, file_size) y emite
                                  la misma colección con content_hash añadido.
                                  Implementa la Fase 2 (Hashing) del pipeline.
                                  Cierra la selección del algoritmo de hashing
                                  (OQ-1) dentro de su propio BETO_CORE hijo.
  Can exist independently:        YES
  Depends on internal logic
  of siblings:                    NO
  Classified by rule as:          PARALLEL
  Associated BETO_CORE target:    not_generated_yet
  Status:                         DRAFT


- Node ID:                        GRAPH.DUPLICATE_DETECTOR
  Node type:                      PARALLEL
  Name:                           Duplicate Detector
  Source section:                 BETO_CORE_INTERVIEW_COMPLETED.md — P4.5,
                                  P6.1, P6.3, P6.4, P7.1 (Fase 3);
                                  STRUCTURAL_CLASSIFICATION_REGISTRY.md —
                                  CAND-03, Sección 4
  Parent:                         GRAPH.ROOT
  Parent edge type:               FUNCTIONAL_BRANCH
  Purpose:                        Agrupar File Entries por content_hash idéntico
                                  y retener exclusivamente los grupos con
                                  cardinalidad mayor o igual a dos. Recibe la
                                  colección de File Entries (file_path, file_size,
                                  content_hash) y emite la colección de Duplicate
                                  Groups (content_hash, [file_paths], group_size).
                                  Implementa la Fase 3 (Grouping) del pipeline.
                                  Sin OQs propias no resueltas.
  Can exist independently:        YES
  Depends on internal logic
  of siblings:                    NO
  Classified by rule as:          PARALLEL
  Associated BETO_CORE target:    not_generated_yet
  Status:                         DRAFT


- Node ID:                        GRAPH.SPACE_CALCULATOR
  Node type:                      PARALLEL
  Name:                           Space Calculator
  Source section:                 BETO_CORE_INTERVIEW_COMPLETED.md — P3.2,
                                  P6.1, P6.3, P6.4, P7.1 (Fase 4);
                                  STRUCTURAL_CLASSIFICATION_REGISTRY.md —
                                  CAND-04, Sección 4
  Parent:                         GRAPH.ROOT
  Parent edge type:               FUNCTIONAL_BRANCH
  Purpose:                        Calcular el espacio recuperable por grupo de
                                  duplicados y el total recuperable acumulado
                                  entre todos los grupos. Recibe la colección de
                                  Duplicate Groups y emite los grupos anotados
                                  con recoverable_bytes más el escalar
                                  total_recoverable_bytes. Fórmula declarada:
                                  recoverable_bytes = file_size × (count − 1).
                                  Implementa la Fase 4 (Space Calculation) del
                                  pipeline. Sin OQs propias no resueltas.
  Can exist independently:        YES
  Depends on internal logic
  of siblings:                    NO
  Classified by rule as:          PARALLEL
  Associated BETO_CORE target:    not_generated_yet
  Status:                         DRAFT


- Node ID:                        GRAPH.REPORT_COMPOSER
  Node type:                      PARALLEL
  Name:                           Report Composer
  Source section:                 BETO_CORE_INTERVIEW_COMPLETED.md — P3.2,
                                  P3.4, P6.1, P6.3, P6.4, P7.1 (Fase 5),
                                  P11.1, P11.4 (Sub-BETO 2);
                                  STRUCTURAL_CLASSIFICATION_REGISTRY.md —
                                  CAND-05, Sección 4
  Parent:                         GRAPH.ROOT
  Parent edge type:               FUNCTIONAL_BRANCH
  Purpose:                        Componer y emitir el artefacto de reporte
                                  final a partir de los Duplicate Groups anotados
                                  con recoverable_bytes y el valor escalar
                                  total_recoverable_bytes. El reporte debe
                                  incluir obligatoriamente: grupos de duplicados,
                                  rutas de archivo por grupo y espacio total
                                  recuperable. Implementa la Fase 5 (Report
                                  Generation) del pipeline. Cierra las
                                  decisiones de formato, estructura y canal de
                                  entrega del reporte (OQ-6) dentro de su propio
                                  BETO_CORE hijo. Gate G-2B OSC obligatorio
                                  antes de materialización.
  Can exist independently:        YES
  Depends on internal logic
  of siblings:                    NO
  Classified by rule as:          PARALLEL
  Associated BETO_CORE target:    not_generated_yet
  Status:                         DRAFT
```

---

## 8. EDGE REGISTRY

```
- Edge ID:              EDGE.ROOT-SCANNER
  From node:            GRAPH.ROOT
  To node:              GRAPH.SCANNER
  Edge type:            FUNCTIONAL_BRANCH
  Justification source: Entrevista (P6.3, P7.1 Fase 1) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY CAND-01)
  Justification:        El Scanner es la primera rama funcional del sistema.
                        Implementa la Fase 1 (Discovery) del pipeline declarado.
                        Fue promovido a PARALLEL por independencia de internals
                        ajenos confirmada en la clasificación formal.
  Status:               DRAFT


- Edge ID:              EDGE.ROOT-HASHER
  From node:            GRAPH.ROOT
  To node:              GRAPH.HASHER
  Edge type:            FUNCTIONAL_BRANCH
  Justification source: Entrevista (P6.3, P7.1 Fase 2) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY CAND-02)
  Justification:        El Hasher es la segunda rama funcional del sistema.
                        Implementa la Fase 2 (Hashing) del pipeline declarado.
                        Fue promovido a PARALLEL por independencia de internals
                        ajenos y resolución de su única OQ propia (OQ-1) mediante
                        estándar externo.
  Status:               DRAFT


- Edge ID:              EDGE.ROOT-DUPLICATE_DETECTOR
  From node:            GRAPH.ROOT
  To node:              GRAPH.DUPLICATE_DETECTOR
  Edge type:            FUNCTIONAL_BRANCH
  Justification source: Entrevista (P4.5, P6.3, P7.1 Fase 3) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY CAND-03)
  Justification:        El Duplicate Detector es la tercera rama funcional del
                        sistema. Implementa la Fase 3 (Grouping) del pipeline.
                        Fue promovido a PARALLEL por independencia de internals
                        ajenos y ausencia de OQs propias no resueltas.
  Status:               DRAFT


- Edge ID:              EDGE.ROOT-SPACE_CALCULATOR
  From node:            GRAPH.ROOT
  To node:              GRAPH.SPACE_CALCULATOR
  Edge type:            FUNCTIONAL_BRANCH
  Justification source: Entrevista (P3.2, P6.3, P7.1 Fase 4) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY CAND-04)
  Justification:        El Space Calculator es la cuarta rama funcional del
                        sistema. Implementa la Fase 4 (Space Calculation) del
                        pipeline. Fue promovido a PARALLEL por independencia de
                        internals ajenos, fórmula declarada sin ambigüedad y
                        ausencia de OQs propias no resueltas.
  Status:               DRAFT


- Edge ID:              EDGE.ROOT-REPORT_COMPOSER
  From node:            GRAPH.ROOT
  To node:              GRAPH.REPORT_COMPOSER
  Edge type:            FUNCTIONAL_BRANCH
  Justification source: Entrevista (P3.2, P6.3, P7.1 Fase 5) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY CAND-05)
  Justification:        El Report Composer es la quinta rama funcional del
                        sistema. Implementa la Fase 5 (Report Generation) del
                        pipeline. Fue promovido a PARALLEL por independencia de
                        internals ajenos. OQ-6 es una decisión de diseño interna
                        de este nodo, cerrable dentro de su BETO_CORE hijo.
  Status:               DRAFT


- Edge ID:              EDGE.DEP-SCANNER-HASHER
  From node:            GRAPH.SCANNER
  To node:              GRAPH.HASHER
  Edge type:            DECLARED_DEPENDENCY
  Justification source: Entrevista (P7.1 Fases 1-2) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY Sección 6
                        Advertencia-03)
  Justification:        El Hasher requiere como input la colección de File
                        Entries (file_path, file_size) producida por el Scanner.
                        Dependencia de datos declarada en el pipeline secuencial.
                        No reemplaza la relación padre-hijo de ambos nodos con
                        GRAPH.ROOT.
  Status:               DRAFT


- Edge ID:              EDGE.DEP-HASHER-DUPLICATE_DETECTOR
  From node:            GRAPH.HASHER
  To node:              GRAPH.DUPLICATE_DETECTOR
  Edge type:            DECLARED_DEPENDENCY
  Justification source: Entrevista (P7.1 Fases 2-3) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY Sección 6
                        Advertencia-03)
  Justification:        El Duplicate Detector requiere como input la colección
                        de File Entries con content_hash añadido, producida por
                        el Hasher. Dependencia de datos declarada en el pipeline
                        secuencial. No reemplaza la relación padre-hijo de ambos
                        nodos con GRAPH.ROOT.
  Status:               DRAFT


- Edge ID:              EDGE.DEP-DUPLICATE_DETECTOR-SPACE_CALCULATOR
  From node:            GRAPH.DUPLICATE_DETECTOR
  To node:              GRAPH.SPACE_CALCULATOR
  Edge type:            DECLARED_DEPENDENCY
  Justification source: Entrevista (P7.1 Fases 3-4) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY Sección 6
                        Advertencia-03)
  Justification:        El Space Calculator requiere como input la colección de
                        Duplicate Groups (content_hash, [file_paths], group_size)
                        producida por el Duplicate Detector. Dependencia de datos
                        declarada en el pipeline secuencial. No reemplaza la
                        relación padre-hijo de ambos nodos con GRAPH.ROOT.
  Status:               DRAFT


- Edge ID:              EDGE.DEP-SPACE_CALCULATOR-REPORT_COMPOSER
  From node:            GRAPH.SPACE_CALCULATOR
  To node:              GRAPH.REPORT_COMPOSER
  Edge type:            DECLARED_DEPENDENCY
  Justification source: Entrevista (P7.1 Fases 4-5) + Clasificación
                        (STRUCTURAL_CLASSIFICATION_REGISTRY Sección 6
                        Advertencia-03)
  Justification:        El Report Composer requiere como input los Duplicate
                        Groups anotados con recoverable_bytes y el escalar
                        total_recoverable_bytes, producidos por el Space
                        Calculator. Dependencia de datos declarada en el pipeline
                        secuencial. No reemplaza la relación padre-hijo de ambos
                        nodos con GRAPH.ROOT.
  Status:               DRAFT
```

---

## 9. CLASSIFICATION TRACE

```
- Node ID:            GRAPH.SCANNER
  Candidate name:     Scanner / Traversal de Sistema de Archivos
  Classification result: PARALLEL
  Independence semantic test:
    Can be specified with external contracts only:
      YES — Input (ruta de directorio) y output (colección de File Entries con
      file_path y file_size) son contratos completamente definibles externamente.
      La API del sistema de archivos del SO es un estándar externo. Las políticas
      de comportamiento ante symlinks, permisos y cero bytes son decisiones internas
      de este componente, no dependencias de internals ajenos.
    Requires internal knowledge of another component:
      NO — El Scanner no requiere conocer la lógica interna del Hasher, del
      Duplicate Detector, del Space Calculator ni del Report Composer para ser
      diseñado, especificado y materializado.
    Can be given to an independent team with only purpose + inputs + outputs +
    contracts:
      YES — Un equipo independiente puede diseñar y materializar el Scanner con
      un documento que declare: (a) input: ruta de directorio objetivo, (b) output:
      colección de File Entries (file_path, file_size), (c) responsabilidad:
      traversal recursivo completo, (d) políticas ante symlinks, permisos y
      archivos de cero bytes a cerrar internamente. No se requiere ninguna
      información de los internals de los demás componentes.
  Final reason:       PARALLEL confirmado por STRUCTURAL_CLASSIFICATION_REGISTRY
                      CAND-01. La doble designación entrevista (Sub-BETO en P11.2
                      + PARALLEL en P6.3) se resuelve a favor de PARALLEL porque
                      las OQs propias (OQ-3, OQ-4, OQ-8) son políticas internas
                      del Scanner, no evidencia de dependencia de internals ajenos.
                      Fuente formal: Sección 2 CAND-01 y Sección 3 del
                      STRUCTURAL_CLASSIFICATION_REGISTRY.


- Node ID:            GRAPH.HASHER
  Candidate name:     Hasher
  Classification result: PARALLEL
  Independence semantic test:
    Can be specified with external contracts only:
      YES — Input (colección de File Entries con file_path y file_size) y output
      (misma colección con content_hash añadido) son contratos completamente
      definibles externamente. El algoritmo de hashing es un estándar externo
      (SHA-256, BLAKE2b, etc.) seleccionable mediante resolución de OQ-1 sin
      requerir conocimiento de ningún otro componente interno.
    Requires internal knowledge of another component:
      NO — El Hasher no requiere conocer la lógica interna del Scanner, del
      Duplicate Detector ni de ningún otro componente. Opera exclusivamente sobre
      el contenido del archivo referenciado por file_path y sobre el estándar
      externo del algoritmo de hashing.
    Can be given to an independent team with only purpose + inputs + outputs +
    contracts:
      YES — Un equipo independiente puede diseñar y materializar el Hasher con
      un documento que declare: (a) input: File Entries (file_path, file_size),
      (b) output: File Entries con content_hash, (c) algoritmo: el resuelto por
      OQ-1. No se requiere ninguna información de los internals de los demás
      componentes.
  Final reason:       PARALLEL confirmado por STRUCTURAL_CLASSIFICATION_REGISTRY
                      CAND-02. La entrevista no lo marcó como candidato SubBETO.
                      La única OQ propia (OQ-1) es una decisión de configuración
                      resoluble mediante estándar externo. Sin dependencia de
                      internals ajenos. Fuente formal: Sección 2 CAND-02 y
                      Sección 4 del STRUCTURAL_CLASSIFICATION_REGISTRY.


- Node ID:            GRAPH.DUPLICATE_DETECTOR
  Candidate name:     Duplicate Detector
  Classification result: PARALLEL
  Independence semantic test:
    Can be specified with external contracts only:
      YES — Input (colección de File Entries con content_hash) y output (colección
      de Duplicate Groups con cardinalidad ≥ 2) son contratos completamente
      definibles externamente. La regla de agrupación (clave = content_hash,
      filtro = cardinalidad > 1) está completamente declarada sin ambigüedad en
      la entrevista (P4.5, P7.1 Fase 3).
    Requires internal knowledge of another component:
      NO — El Duplicate Detector no requiere conocer la lógica interna del
      Hasher (sólo consume el valor de content_hash), ni la lógica del Space
      Calculator ni del Report Composer. Su lógica de agrupación es autocontenida.
    Can be given to an independent team with only purpose + inputs + outputs +
    contracts:
      YES — Un equipo independiente puede diseñar y materializar el Duplicate
      Detector con un documento que declare: (a) input: File Entries con
      content_hash, (b) output: Duplicate Groups (content_hash, [file_paths],
      group_size) con cardinalidad ≥ 2, (c) lógica: agrupación por clave y
      filtro de cardinalidad. Sin OQs propias. Sin información de internals
      ajenos requerida.
  Final reason:       PARALLEL confirmado por STRUCTURAL_CLASSIFICATION_REGISTRY
                      CAND-03. La entrevista (P6.4) confirmó definición operacional
                      suficiente y no generó candidato SubBETO. Sin OQs propias
                      no resueltas. Sin dependencia de internals ajenos. Fuente
                      formal: Sección 2 CAND-03 y Sección 4 del
                      STRUCTURAL_CLASSIFICATION_REGISTRY.


- Node ID:            GRAPH.SPACE_CALCULATOR
  Candidate name:     Space Calculator
  Classification result: PARALLEL
  Independence semantic test:
    Can be specified with external contracts only:
      YES — Input (Duplicate Groups con file_size y count) y output (grupos
      anotados con recoverable_bytes + escalar total_recoverable_bytes) son
      contratos completamente definibles externamente. La fórmula está declarada
      sin ambigüedad: recoverable_bytes = file_size × (count − 1). No existe
      ninguna decisión de diseño que requiera información de los internals de
      otros componentes.
    Requires internal knowledge of another component:
      NO — El Space Calculator opera exclusivamente con valores numéricos
      declarados en el schema del Duplicate Group. No requiere conocer la lógica
      de agrupación del Duplicate Detector ni la lógica de composición del
      Report Composer.
    Can be given to an independent team with only purpose + inputs + outputs +
    contracts:
      YES — Un equipo independiente puede diseñar y materializar el Space
      Calculator con un documento que declare: (a) input: Duplicate Groups con
      file_size y count, (b) output: grupos anotados con recoverable_bytes y
      total_recoverable_bytes, (c) fórmula: recoverable_bytes = file_size ×
      (count − 1). Sin OQs propias. Sin información de internals ajenos requerida.
  Final reason:       PARALLEL confirmado por STRUCTURAL_CLASSIFICATION_REGISTRY
                      CAND-04. La entrevista (P6.4) confirmó definición operacional
                      suficiente con fórmula declarada y no generó candidato
                      SubBETO. Sin OQs propias no resueltas. Sin dependencia de
                      internals ajenos. Fuente formal: Sección 2 CAND-04 y
                      Sección 4 del STRUCTURAL_CLASSIFICATION_REGISTRY.


- Node ID:            GRAPH.REPORT_COMPOSER
  Candidate name:     Report Composer
  Classification result: PARALLEL
  Independence semantic test:
    Can be specified with external contracts only:
      YES — Input (Duplicate Groups anotados con recoverable_bytes +
      total_recoverable_bytes) es un contrato completamente definible
      externamente. El output (artefacto de reporte) tiene sus especificaciones
      de formato, canal y estructura como decisiones propias de este componente,
      cerradas por OQ-6 dentro de su alcance interno. No requiere acceso a los
      internals de los demás componentes para definir su output.
    Requires internal knowledge of another component:
      NO — El Report Composer no requiere conocer cómo el Scanner recorrió el
      árbol, cómo el Hasher computó hashes, cómo el Duplicate Detector agrupó,
      ni cómo el Space Calculator calculó el espacio recuperable. Opera
      exclusivamente sobre el schema del input declarado como contrato externo.
    Can be given to an independent team with only purpose + inputs + outputs +
    contracts:
      YES, una vez resuelta OQ-6 — Un equipo independiente puede diseñar y
      materializar el Report Composer con un documento que declare: (a) input:
      Duplicate Groups anotados + total_recoverable_bytes, (b) output: artefacto
      de reporte con formato y canal declarados por resolución de OQ-6, (c)
      contenido obligatorio: grupos de duplicados, rutas por grupo, espacio total
      recuperable. No se requiere ninguna información de los internals de los
      demás componentes. Gate G-2B OSC obligatorio antes de materialización.
  Final reason:       PARALLEL confirmado por STRUCTURAL_CLASSIFICATION_REGISTRY
                      CAND-05. La doble designación entrevista (SubBETO en P11.2
                      + PARALLEL en P6.3) se resuelve a favor de PARALLEL porque
                      OQ-6 es una decisión de diseño interna del Report Composer,
                      no una dependencia de internals ajenos. Fuente formal:
                      Sección 2 CAND-05, Sección 3 y Sección 4 del
                      STRUCTURAL_CLASSIFICATION_REGISTRY.
```

---

## 10. TOPOLOGY CONSTRAINTS

Checklist de validación topológica:

```
- Exactly one ROOT exists:
    PASS
    Justificación: Existe exactamente un nodo ROOT declarado (GRAPH.ROOT).
    No se declararon nodos ROOT adicionales.

- Every non-root node has exactly one structural parent:
    PASS
    Justificación: Los cinco nodos PARALLEL (GRAPH.SCANNER, GRAPH.HASHER,
    GRAPH.DUPLICATE_DETECTOR, GRAPH.SPACE_CALCULATOR, GRAPH.REPORT_COMPOSER)
    tienen cada uno exactamente un Parent declarado: GRAPH.ROOT. Ningún nodo
    no-ROOT tiene Parent = NONE ni Parent múltiple.

- No structural cycles exist:
    PASS
    Justificación: La topología es un árbol plano de profundidad uno: un ROOT
    con cinco PARALLEL directos. No existen relaciones FUNCTIONAL_BRANCH ni
    STRUCTURAL_REFINEMENT que formen ciclos. La estructura árbol garantiza
    aciclicidad estructural.

- No dependency cycles exist:
    PASS
    Justificación: Las relaciones DECLARED_DEPENDENCY forman el pipeline lineal:
    SCANNER → HASHER → DUPLICATE_DETECTOR → SPACE_CALCULATOR → REPORT_COMPOSER.
    Esta cadena es estrictamente dirigida y no contiene aristas de retorno.
    No existen ciclos de dependencia.

- Every edge connects declared nodes:
    PASS
    Justificación: Todas las aristas registradas en la Sección 8 conectan
    exclusivamente nodos presentes en el Node Registry (Sección 7):
    EDGE.ROOT-SCANNER, EDGE.ROOT-HASHER, EDGE.ROOT-DUPLICATE_DETECTOR,
    EDGE.ROOT-SPACE_CALCULATOR, EDGE.ROOT-REPORT_COMPOSER (FUNCTIONAL_BRANCH)
    y EDGE.DEP-SCANNER-HASHER, EDGE.DEP-HASHER-DUPLICATE_DETECTOR,
    EDGE.DEP-DUPLICATE_DETECTOR-SPACE_CALCULATOR,
    EDGE.DEP-SPACE_CALCULATOR-REPORT_COMPOSER (DECLARED_DEPENDENCY).
    Ninguna arista referencia un nodo no declarado.

- Every PARALLEL is attached by FUNCTIONAL_BRANCH:
    PASS
    Justificación: Los cinco nodos PARALLEL tienen Parent edge type =
    FUNCTIONAL_BRANCH. Las aristas EDGE.ROOT-SCANNER, EDGE.ROOT-HASHER,
    EDGE.ROOT-DUPLICATE_DETECTOR, EDGE.ROOT-SPACE_CALCULATOR y
    EDGE.ROOT-REPORT_COMPOSER son todas de tipo FUNCTIONAL_BRANCH.
    Ningún PARALLEL tiene Parent edge type distinto a FUNCTIONAL_BRANCH.

- Every SUBBETO is attached by STRUCTURAL_REFINEMENT:
    PASS
    Justificación: No existen nodos SUBBETO en este grafo. La condición
    es vacuamente verdadera. La clasificación formal determinó que todos
    los candidatos satisfacen la condición de independencia de internals
    ajenos y fueron clasificados como PARALLEL.

- No orphan nodes exist:
    PASS
    Justificación: Todos los nodos no-ROOT tienen exactamente un padre
    estructural declarado (GRAPH.ROOT). El nodo ROOT no tiene padre por
    definición de su tipo. No existen nodos sin conexión estructural al
    árbol.

- No unauthorized node types exist:
    PASS
    Justificación: Los tipos de nodo utilizados son exclusivamente ROOT
    (1 instancia) y PARALLEL (5 instancias). Ambos tipos están incluidos
    en la lista de tipos autorizados de la Sección 4. No se utilizan tipos
    no autorizados.

- No unauthorized edge types exist:
    PASS
    Justificación: Los tipos de arista utilizados son exclusivamente
    FUNCTIONAL_BRANCH (5 aristas) y DECLARED_DEPENDENCY (4 aristas).
    Ambos tipos están incluidos en la lista de tipos autorizados de la
    Sección 5. No se utilizan tipos no autorizados. El tipo
    STRUCTURAL_REFINEMENT no se utiliza dado que no existen nodos SUBBETO.
```

**Estado topológico:** Todos los checks en PASS.
**Blocking issues:** ninguno declarado.

---

## 11. EXPANSION ORDER RECOMMENDATION

El orden de expansión respeta el pipeline de datos declarado en la Fase
Architecture (P7.1) y las dependencias DECLARED_DEPENDENCY registradas
en la Sección 8. Los nodos PARALLEL que no tienen OQs críticas propias
pueden expandirse antes o en paralelo. Los nodos con OQs críticas que
impactan los contratos de transferencia entre fases deben cerrarse antes
de que el nodo dependiente avance a materialización.

Adicionalmente, OQ-5 (lenguaje de implementación) es una OQ crítica del
BETO_CORE raíz que afecta a todos los nodos. Debe cerrarse en el Paso 6
del BETO_CORE raíz antes de que cualquier BETO_CORE hijo avance al Paso 8.

```
Phase 1 — Generación prioritaria (sin OQs propias bloqueantes de diseño):
  - GRAPH.DUPLICATE_DETECTOR
  - GRAPH.SPACE_CALCULATOR

  Justificación: Estos dos nodos no tienen OQs propias no resueltas.
  Sus contratos de input y output están completamente declarados.
  Pueden ser expandidos a BETO_CORE hijo inmediatamente.

Phase 2 — Generación con OQ de configuración (OQ resuelta externamente):
  - GRAPH.HASHER

  Justificación: El Hasher tiene una única OQ propia (OQ-1 — algoritmo
  de hashing). Una vez resuelta OQ-1 en el Paso 6 del BETO_CORE raíz
  o del propio BETO_CORE_HASHER, el nodo puede avanzar a materialización.
  El diseño estructural del BETO_CORE_HASHER puede comenzar en paralelo
  con la Phase 1; la materialización espera cierre de OQ-1.

Phase 3 — Generación con OQs de política y comportamiento:
  - GRAPH.SCANNER

  Justificación: El Scanner tiene tres OQs propias (OQ-3, OQ-4, OQ-8)
  de las cuales dos son críticas con execution_readiness_check =
  FAIL_EXECUTIONAL_GAP (OQ-4, OQ-8). El diseño estructural del
  BETO_CORE_SCANNER puede comenzar, pero la materialización requiere
  cierre de OQ-4 y OQ-8. OQ-3 es no crítica y puede cerrarse con
  política por defecto declarada si el operador lo autoriza.
  GRAPH.SCANNER debe expandirse antes de que GRAPH.HASHER avance a
  materialización, dado que GRAPH.HASHER depende del output del Scanner.

Phase 4 — Generación con Gate G-2B OSC obligatorio:
  - GRAPH.REPORT_COMPOSER

  Justificación: El Report Composer tiene una OQ crítica propia (OQ-6)
  con execution_readiness_check = FAIL_EXECUTIONAL_GAP. Gate G-2B OSC
  es obligatorio antes de materialización. El diseño estructural del
  BETO_CORE_REPORT_COMPOSER puede comenzar en paralelo con las fases
  anteriores, pero la materialización está bloqueada hasta el cierre
  de OQ-6. GRAPH.REPORT_COMPOSER es el último nodo del pipeline y su
  expansión completa es la condición de cierre del sistema.
```

**Resumen de orden:**

```
Phase 1: GRAPH.DUPLICATE_DETECTOR, GRAPH.SPACE_CALCULATOR
Phase 2: GRAPH.HASHER
Phase 3: GRAPH.SCANNER
Phase 4: GRAPH.REPORT_COMPOSER
```

**Nota de concurrencia:** Las Phases 1, 2, 3 y 4 pueden solaparse en la
fase de diseño estructural (generación de BETO_CORE hijo). La restricción
de orden aplica exclusivamente a la materialización (Paso 8), donde las
dependencias de datos del pipeline deben respetarse.

---

## 12. DERIVATION CONTRACT

Este grafo autoriza exclusivamente:

- La generación de BETO_CORE hijos para los nodos PARALLEL declarados:
  GRAPH.SCANNER, GRAPH.HASHER, GRAPH.DUPLICATE_DETECTOR,
  GRAPH.SPACE_CALCULATOR, GRAPH.REPORT_COMPOSER
- La construcción de manifests consistentes con esta topología de seis
  nodos (un ROOT y cinco PARALLEL)
- La derivación del MANIFEST_PROYECTO desde esta estructura topológica
- La planificación de materialización respetando el pipeline secuencial
  y las dependencias DECLARED_DEPENDENCY registradas en la Sección 8
- El cierre de OQs propias (OQ-1, OQ-3, OQ-4, OQ-6, OQ-8) dentro del
  alcance de sus respectivos BETO_CORE hijos
- El cierre de OQ-5 en el BETO_CORE raíz con efecto global sobre todos
  los nodos

Este grafo NO autoriza:

- Agregar nodos nuevos no registrados en la Sección 7
- Agregar relaciones nuevas no registradas en la Sección 8
- Reclasificar nodos sin rehacer formalmente el grafo completo
- Derivar manifests para nodos no presentes en este documento
- Materializar componentes no presentes en este documento
- Crear nodos SUBBETO que no fueron autorizados por la clasificación formal
- Crear relaciones STRUCTURAL_REFINEMENT dado que no existen nodos SUBBETO
- Reinterpretar las OQs propias de cada nodo como justificación para crear
  nodos adicionales no declarados en este grafo

---

## 13. CHANGELOG

```
2025-01-31T00:00:00Z  Graph created from BETO_CORE_INTERVIEW_COMPLETED.md
                      and STRUCTURAL_CLASSIFICATION_REGISTRY.md

2025-01-31T00:00:00Z  Node added: GRAPH.ROOT (ROOT — Duplicate File Finder CLI)

2025-01-31T00:00:00Z  Node added: GRAPH.SCANNER (PARALLEL — Scanner)

2025-01-31T00:00:00Z  Node added: GRAPH.HASHER (PARALLEL — Hasher)

2025-01-31T00:00:00Z  Node added: GRAPH.DUPLICATE_DETECTOR
                      (PARALLEL — Duplicate Detector)

2025-01-31T00:00:00Z  Node added: GRAPH.SPACE_CALCULATOR
                      (PARALLEL — Space Calculator)

2025-01-31T00:00:00Z  Node added: GRAPH.REPORT_COMPOSER
                      (PARALLEL — Report Composer)

2025-01-31T00:00:00Z  Edge added: EDGE.ROOT-SCANNER (FUNCTIONAL_BRANCH)

2025-01-31T00:00:00Z  Edge added: EDGE.ROOT-HASHER (FUNCTIONAL_BRANCH)

2025-01-31T00:00:00Z  Edge added: EDGE.ROOT-DUPLICATE_DETECTOR
                      (FUNCTIONAL_BRANCH)

2025-01-31T00:00:00Z  Edge added: EDGE.ROOT-SPACE_CALCULATOR (FUNCTIONAL_BRANCH)

2025-01-31T00:00:00Z  Edge added: EDGE.ROOT-REPORT_COMPOSER (FUNCTIONAL_BRANCH)

2025-01-31T00:00:00Z  Edge added: EDGE.DEP-SCANNER-HASHER (DECLARED_DEPENDENCY)

2025-01-31T00:00:00Z  Edge added: EDGE.DEP-HASHER-DUPLICATE_DETECTOR
                      (DECLARED_DEPENDENCY)

2025-01-31T00:00:00Z  Edge added: EDGE.DEP-DUPLICATE_DETECTOR-SPACE_CALCULATOR
                      (DECLARED_DEPENDENCY)

2025-01-31T00:00:00Z  Edge added: EDGE.DEP-SPACE_CALCULATOR-REPORT_COMPOSER
                      (DECLARED_DEPENDENCY)

2025-01-31T00:00:00Z  Classification trace completed for all PARALLEL nodes:
                      GRAPH.SCANNER, GRAPH.HASHER, GRAPH.DUPLICATE_DETECTOR,
                      GRAPH.SPACE_CALCULATOR, GRAPH.REPORT_COMPOSER

2025-01-31T00:00:00Z  Topology constraints validated: all 10 checks PASS

2025-01-31T00:00:00Z  Expansion order recommendation declared: 4 phases

2025-01-31T00:00:00Z  Derivation contract declared

2025-01-31T00:00:00Z  Graph status: DRAFT — pending Sección 14 validation
```

---

*Secciones 1 a 13 completadas. Detenido antes de Sección 14 conforme a instrucción.*

## 14. FINAL VALIDATION STATUS

```
Graph status: VALIDATED

Ready to generate BETO_CORE children: YES
```

Blocking issues:
- none declared

Validación ejecutada sobre:

```
Sección 10 — Topology Constraints: 10/10 checks PASS
  - Exactly one ROOT exists:                        PASS
  - Every non-root node has exactly one parent:     PASS
  - No structural cycles exist:                     PASS
  - No dependency cycles exist:                     PASS
  - Every edge connects declared nodes:             PASS
  - Every PARALLEL is attached by FUNCTIONAL_BRANCH: PASS
  - Every SUBBETO is attached by STRUCTURAL_REFINEMENT: PASS
  - No orphan nodes exist:                          PASS
  - No unauthorized node types exist:               PASS
  - No unauthorized edge types exist:               PASS

Nodes validated: 6
  ROOT:     1  (GRAPH.ROOT)
  PARALLEL: 5  (GRAPH.SCANNER, GRAPH.HASHER, GRAPH.DUPLICATE_DETECTOR,
                GRAPH.SPACE_CALCULATOR, GRAPH.REPORT_COMPOSER)
  SUBBETO:  0

Edges validated: 9
  FUNCTIONAL_BRANCH:    5
  DECLARED_DEPENDENCY:  4
  STRUCTURAL_REFINEMENT: 0

Classification traces: 5/5 complete
Source authority: STRUCTURAL_CLASSIFICATION_REGISTRY.md — COMPLETO
Source interview: BETO_CORE_INTERVIEW_COMPLETED.md — COMPLETO
```

---

## END OF DOCUMENT
# BETO_SYSTEM_GRAPH

## 1. METADATA

System name: [Nombre del sistema]
Graph generation timestamp: [ISO timestamp]
Source BETO_CORE: [Ruta al BETO_CORE raíz]
Source interview: [Ruta al BETO_CORE_INTERVIEW aplicado]
Graph version: [Versión del grafo]
Graph status: [DRAFT | VALIDATED | CLOSED]

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

## 3. SOURCE OF AUTHORITY

Autoridad semántica:
- BETO_CORE raíz

Autoridad de descubrimiento estructural:
- BETO_CORE_INTERVIEW

Autoridad de clasificación:
- Regla de Clasificación Estructural del BETO_INSTRUCTIVO

Autoridad topológica:
- Este BETO_SYSTEM_GRAPH

Regla:
Todo nodo y toda relación declarados en este grafo deben ser derivables
de una detección realizada durante la entrevista y de una clasificación
formal válida según el instructivo.

Si un nodo o relación no puede trazarse a esas fuentes:
no puede existir en este grafo.

## 4. NODE TYPES AUTHORIZED

Tipos de nodo permitidos exclusivamente:

- ROOT
- PARALLEL
- SUBBETO

Definiciones:

ROOT
Nodo troncal del sistema. Debe existir exactamente uno.

PARALLEL
Capacidad funcional autónoma del sistema.
Debe haber sido promovida mediante la regla de independencia semántica.

SUBBETO
Nodo de refinamiento estructural.
Debe haber sido promovido por ambigüedad estructural.

No se permiten otros tipos de nodo.

## 5. EDGE TYPES AUTHORIZED

Tipos de relación permitidos exclusivamente:

- FUNCTIONAL_BRANCH
- STRUCTURAL_REFINEMENT
- DECLARED_DEPENDENCY

Definiciones:

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

No se permiten otros tipos de relación.

## 6. ROOT NODE

Debe declararse exactamente un nodo raíz.

Formato:

Node ID: [GRAPH.<slug>]
Node type: ROOT
Name: [Nombre del BETO raíz]
Source: [BETO_CORE_<name>.md]
Parent: NONE
Parent edge type: NONE
Purpose: [Resumen funcional]
Status: [DRAFT | VALIDATED | CLOSED]

Si no existe exactamente un ROOT:
el grafo es inválido.

## 7. NODE REGISTRY

Registrar aquí todos los nodos del sistema.

Formato obligatorio por nodo:

- Node ID: [GRAPH.<slug único>]
  Node type: [ROOT | PARALLEL | SUBBETO]
  Name: [Nombre del nodo]
  Source section: [Referencia al origen en entrevista o clasificación]
  Parent: [GRAPH.<slug padre> | NONE]
  Parent edge type: [FUNCTIONAL_BRANCH | STRUCTURAL_REFINEMENT | NONE]
  Purpose: [Qué representa]
  Can exist independently: [YES | NO]
  Depends on internal logic of siblings: [YES | NO]
  Classified by rule as: [PARALLEL | SUBBETO | ROOT]
  Associated BETO_CORE target: [BETO_CORE_<name> | not_generated_yet]
  Status: [DRAFT | VALIDATED | CLOSED]

Reglas:

- Todo nodo no ROOT debe tener Parent declarado
- Todo nodo no ROOT debe tener Parent edge type declarado
- Todo PARALLEL debe tener Parent edge type = FUNCTIONAL_BRANCH
- Todo SUBBETO debe tener Parent edge type = STRUCTURAL_REFINEMENT
- Ningún PARALLEL puede tener Parent edge type = STRUCTURAL_REFINEMENT
- Ningún SUBBETO puede tener Parent edge type = FUNCTIONAL_BRANCH

## 8. EDGE REGISTRY

Registrar aquí todas las relaciones explícitas entre nodos.

Formato obligatorio por relación:

- Edge ID: [EDGE.<slug único>]
  From node: [GRAPH.<slug origen>]
  To node: [GRAPH.<slug destino>]
  Edge type: [FUNCTIONAL_BRANCH | STRUCTURAL_REFINEMENT | DECLARED_DEPENDENCY]
  Justification source: [Entrevista | Clasificación | BETO_CORE]
  Justification: [Texto breve]
  Status: [DRAFT | VALIDATED | CLOSED]

Reglas:

- Toda relación debe conectar nodos existentes
- Toda relación debe usar un tipo autorizado
- Toda relación debe ser justificable desde una fuente válida
- DECLARED_DEPENDENCY no reemplaza la relación padre-hijo
- No se permite duplicar relaciones idénticas entre los mismos nodos

## 9. CLASSIFICATION TRACE

Registrar la justificación de por qué cada nodo fue clasificado
como PARALLEL o SUBBETO.

Formato obligatorio:

- Node ID: [GRAPH.<slug>]
  Candidate name: [Nombre original]
  Classification result: [PARALLEL | SUBBETO]
  Independence semantic test:
    Can be specified with external contracts only: [YES | NO]
    Requires internal knowledge of another component: [YES | NO]
    Can be given to an independent team with only purpose + inputs + outputs + contracts: [YES | NO]
  Final reason: [Texto breve]

Regla:
Toda clasificación debe corresponder exactamente a la
Regla de Clasificación Estructural del BETO_INSTRUCTIVO.

## 10. TOPOLOGY CONSTRAINTS

Declarar aquí el estado de validación topológica del sistema.

Checklist obligatorio:

- Exactly one ROOT exists: [PASS | FAIL]
- Every non-root node has exactly one structural parent: [PASS | FAIL]
- No structural cycles exist: [PASS | FAIL]
- No dependency cycles exist: [PASS | FAIL]
- Every edge connects declared nodes: [PASS | FAIL]
- Every PARALLEL is attached by FUNCTIONAL_BRANCH: [PASS | FAIL]
- Every SUBBETO is attached by STRUCTURAL_REFINEMENT: [PASS | FAIL]
- No orphan nodes exist: [PASS | FAIL]
- No unauthorized node types exist: [PASS | FAIL]
- No unauthorized edge types exist: [PASS | FAIL]

Si algún check está en FAIL:
Graph status no puede ser VALIDATED ni CLOSED.

## 11. EXPANSION ORDER RECOMMENDATION

Definir el orden recomendado para generar BETO_CORE hijos.

Formato:

Phase 1:
- [GRAPH.<slug>]
- [GRAPH.<slug>]

Phase 2:
- [GRAPH.<slug>]

Reglas:

- El orden debe respetar el padre estructural
- Un SUBBETO no puede expandirse antes que su padre
- Los PARALLEL pueden expandirse en paralelo si no tienen dependencias declaradas incompatibles
- Las dependencias DECLARED_DEPENDENCY deben respetarse

## 12. DERIVATION CONTRACT

Este grafo autoriza exclusivamente:

- La generación de BETO_CORE hijos para nodos PARALLEL y SUBBETO declarados
- La construcción de manifests consistentes con esta topología
- La derivación del MANIFEST_PROYECTO desde esta estructura
- La planificación de materialización respetando esta topología

Este grafo NO autoriza:

- Agregar nodos nuevos no registrados
- Agregar relaciones nuevas no registradas
- Reclasificar nodos sin rehacer el graph
- Derivar manifests para nodos no presentes
- Materializar componentes no presentes en este documento

## 13. CHANGELOG

Formato sugerido:

[Timestamp] Graph created
[Timestamp] Node added
[Timestamp] Edge added
[Timestamp] Classification updated
[Timestamp] Validation status changed

## 14. FINAL VALIDATION STATUS

Graph status: [DRAFT | VALIDATED | CLOSED]

Ready to generate BETO_CORE children: [YES | NO]

Blocking issues:
- [Issue 1]
- [Issue 2]

If none:
- none declared

## END OF DOCUMENT
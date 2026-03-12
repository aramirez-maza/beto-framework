MANIFEST_PROYECTO_TEMPLATE.md

MANIFEST DEL PROYECTO BETO

Este documento describe la estructura completa del proyecto derivado de una IDEA_RAW elegible, consolidando todos los BETO_CORE generados y validando su consistencia estructural con el BETO_SYSTEM_GRAPH.

Este manifest no crea estructura nueva.  
Este manifest deriva su estructura exclusivamente del BETO_SYSTEM_GRAPH validado.

------------------------------------------------------------

SECCIÓN 1 — METADATA DEL PROYECTO

Project name:
[Nombre del sistema]

Project ID:
[ID único]

Origin IDEA_RAW:
[Texto original de la idea]

Eligibility status:
[GO | GO_WITH_WARNINGS]

PROMPT_CANONICO version:
[Versión del prompt]

BETO framework version:
[Versión del framework]

BETO_SYSTEM_GRAPH source:
[Ruta o referencia al archivo BETO_SYSTEM_GRAPH.md]

Graph status at manifest generation:
[VALIDATED]

Manifest generation timestamp:
[ISO timestamp]

------------------------------------------------------------

SECCIÓN 2 — SYSTEM INTENT

Declaración del propósito global del sistema.

Este texto debe derivar exclusivamente del BETO_CORE raíz.

Debe describir:

El objetivo del sistema  
El tipo de artefacto o proceso a crear  
El dominio de aplicación  
La transformación principal que el sistema realiza

No se permiten reinterpretaciones ni ampliaciones.

Fuente:
BETO_CORE raíz

------------------------------------------------------------

SECCIÓN 3 — BETO RAÍZ

Registrar el único BETO_CORE generado directamente desde IDEA_RAW.

BETO_ROOT

Name:
[Nombre del BETO_CORE raíz]

BETO_CORE file:
[Ruta al archivo BETO_CORE correspondiente]

Purpose summary:
[Resumen funcional]

Status:
SUCCESS_CLOSED

------------------------------------------------------------

SECCIÓN 4 — TOPOLOGÍA DEL SISTEMA

La topología del sistema debe derivarse exclusivamente del BETO_SYSTEM_GRAPH validado.

El MANIFEST_PROYECTO no puede:

crear nodos nuevos  
modificar relaciones  
reclasificar nodos  
introducir dependencias adicionales

Si una estructura no existe en el graph, no puede existir en este manifest.

------------------------------------------------------------

SECCIÓN 5 — REGISTRO DE BETO_PARALELOS

Registrar todos los nodos clasificados como PARALLEL en el BETO_SYSTEM_GRAPH.

Formato:

BETO_PARALLEL

Node ID:
[GRAPH.<slug>]

Name:
[Nombre]

BETO_CORE file:
[Ruta al archivo BETO_CORE correspondiente]

Parent:
[GRAPH.<root>]

Relationship type:
FUNCTIONAL_BRANCH

Purpose summary:
[Resumen funcional]

Dependencies declared:
[Listado o NONE]

Status:
SUCCESS_CLOSED

------------------------------------------------------------

SECCIÓN 6 — REGISTRO DE SUBBETOS

Registrar todos los nodos clasificados como SUBBETO en el BETO_SYSTEM_GRAPH.

Formato:

SUBBETO

Node ID:
[GRAPH.<slug>]

Name:
[Nombre]

BETO_CORE file:
[Ruta al archivo BETO_CORE correspondiente]

Parent:
[GRAPH.<parent>]

Relationship type:
STRUCTURAL_REFINEMENT

Purpose summary:
[Resumen funcional]

Dependencies declared:
[Listado o NONE]

Status:
SUCCESS_CLOSED

------------------------------------------------------------

SECCIÓN 7 — MATRIZ DE DEPENDENCIAS

Registrar dependencias funcionales entre nodos declaradas en el graph.

Formato:

DEPENDENCY

From node:
[GRAPH.<slug>]

To node:
[GRAPH.<slug>]

Dependency type:
DECLARED_DEPENDENCY

Description:
[Explicación breve]

Validation source:
BETO_SYSTEM_GRAPH

Reglas:

No declarar dependencias no presentes en el graph.  
No introducir dependencias implícitas.

------------------------------------------------------------

SECCIÓN 8 — ORDEN DE CONSTRUCCIÓN

Derivar el orden recomendado de materialización usando la topología del BETO_SYSTEM_GRAPH.

Formato sugerido:

CONSTRUCTION_PHASE_1

[Listado de BETO_CORE que pueden construirse primero]

CONSTRUCTION_PHASE_2

[Listado de BETO_CORE que dependen de la fase anterior]

CONSTRUCTION_PHASE_3

[...]

Reglas:

Un SubBETO no puede construirse antes que su padre.  
Dependencias DECLARED_DEPENDENCY deben respetarse.

------------------------------------------------------------

SECCIÓN 9 — MATRIZ DE TRAZABILIDAD GLOBAL

Registrar la trazabilidad de todos los BETO_CORE del proyecto.

Formato:

BETO_TRACE

BETO name:
[Nombre]

TRACE_REGISTRY file:
[Ruta al TRACE_REGISTRY_<name>.md]

TRACE verification status:
[TRACE_VERIFIED]

Regla:

Todo BETO_CORE debe tener TRACE_REGISTRY asociado.

------------------------------------------------------------

SECCIÓN 10 — VALIDACIÓN ESTRUCTURAL

Checklist obligatorio antes de declarar el manifest válido.

Exactly one ROOT:
[PASS | FAIL]

All nodes declared in graph appear in manifest:
[PASS | FAIL]

No nodes exist in manifest outside graph:
[PASS | FAIL]

All BETO_CORE status SUCCESS_CLOSED:
[PASS | FAIL]

All TRACE_REGISTRY present:
[PASS | FAIL]

All dependencies valid:
[PASS | FAIL]

Graph reference VALIDATED:
[PASS | FAIL]

STRUCTURAL_CLASSIFICATION_REGISTRY present:
[PASS | FAIL]

Si algún check es FAIL:

Manifest status = INVALID

------------------------------------------------------------

SECCIÓN 11 — CONSISTENCY CHECK

Verificación de consistencia entre:

BETO_CORE  
BETO_SYSTEM_GRAPH  
MANIFEST_PROYECTO

Checklist:

Todos los BETO_PARALLEL declarados en graph existen en manifest  
Todos los SUBBETO declarados en graph existen en manifest  
Ningún BETO_CORE existe sin nodo en graph  
Ninguna dependencia existe fuera del graph  

Resultado:

[CONSISTENT | INCONSISTENT]

Si resultado = INCONSISTENT:

Parada obligatoria.

------------------------------------------------------------

SECCIÓN 12 — ESTADO FINAL DEL PROYECTO

Project manifest status:
[VALID | INVALID]

Ready for materialization:
[YES | NO]

Blocking issues:
[Listado o NONE]

------------------------------------------------------------

SECCIÓN 13 — CHANGELOG

Formato:

[Timestamp] Manifest created  
[Timestamp] Node registered  
[Timestamp] Dependency registered  
[Timestamp] Validation completed  

------------------------------------------------------------

FIN DEL DOCUMENTO
# MANIFEST_BETO_TEMPLATE.md

# MANIFEST DE BETO

## METADATA

Name: BETO_CORE_<name>
Type: [Root (parallel) | Child (Sub BETO)]
Parent: [None | BETO_CORE_<parent_name>]
Location: [Ruta al BETO_CORE correspondiente]
Manifest generation timestamp: [ISO timestamp]

## PURPOSE AND SCOPE

Purpose: [Una frase, qué define este BETO]
Scope boundaries: [Resumen breve de alcance y exclusiones declaradas]

## INPUT OUTPUT CONTRACT

Input contract source
Reference: [Sección del BETO_CORE donde se define]
Summary: [Qué entra, en términos funcionales]

Output contract source
Reference: [Sección del BETO_CORE donde se define]
Summary: [Qué sale, en términos funcionales]

## DEPENDENCIES

Build prerequisites
None (can be built independently)
o lista:
- BETO_CORE_<other> must be COMPLETE before starting this

Runtime dependencies
None
o lista:
- BETO_CORE_<other> provides output consumed by this BETO

## SUB BETO REGISTRY

Children list
None
o lista:
- BETO_CORE_<child_name>  location: [ruta]  manifest: [ruta]  status: [state]

Depth
Direct children only
o indicar si existen nietos y profundidad máxima observada

## OPEN QUESTIONS STATUS

Open questions count: [count]
Open questions summary: [Breve resumen, sin resolver]
Closure policy reference: [Cómo se trataron incertidumbres según BETO_CORE]

## EXECUTION AND CLOSURE STATE

BETO_CORE_STATUS.mode: [NORMAL | CLOSURE]
BETO_CORE_STATUS.compile_state: [SUCCESS_WITH_WARNINGS | SUCCESS_CLOSED | CLOSURE_ABORTED]

Manifest eligibility rule
Este manifest solo se considera “entregable” cuando compile_state es SUCCESS_CLOSED

## DELIVERY STATUS

Status: [Not started | In progress | Complete | Blocked]
Manifest state: [COMPLETE | INCOMPLETE | WARNING | BLOCKED]

Blocked reason
None
o explicación: [Qué dependencia falta, o qué falta por cerrar]

## IMPLEMENTATION CONTRACT STATUS

Implementation contract:
[Present | Omitted - not applicable]

Implementation contract path:
[ruta al IMPLEMENTATION_CONTRACT_<name>.md | not_applicable]

Activation basis:
[por qué fue requerido | por qué se omitió]

## EVIDENCE

Primary evidence
- BETO_CORE file: [ruta]
- TRACE_REGISTRY file: [ruta al TRACE_REGISTRY_<name>.md generado en Paso 6]
- IMPLEMENTATION_CONTRACT file: [ruta o not_applicable]
- Related outputs: [rutas]
- Tests or validations: [rutas o no declarado]

## CHANGELOG

[Timestamp] Created
[Timestamp] Status updated
[Timestamp] Dependencies updated
[Timestamp] Child added or removed

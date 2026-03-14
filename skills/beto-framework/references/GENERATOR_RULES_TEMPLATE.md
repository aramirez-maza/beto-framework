# GENERATOR_RULES

Propósito
---------

Este artefacto define las reglas propias del generador.
Aplica a sistemas cuyo propósito es crear, materializar, validar
u orquestar productos de terceros.

Estas reglas no reemplazan las reglas del framework.
Las complementan en la capa del generador.


## RULE_001
Name: CONTRACT_ENFORCEMENT_BY_CONSTRUCTION
Description: Ningún contrato crítico de salida puede depender solo de obediencia por prompt del modelo materializador.
Enforcement:
- construcción automática previa
- verificación posterior
Status: ACTIVE


## RULE_002
Name: MATERIALIZATION_RETRY_SCOPE
Description: Una falla localizada en materialización no autoriza rerun de pasos de razonamiento ya cerrados.
Enforcement:
- reintento por archivo o componente
- preservación del cycle state
Status: ACTIVE


## RULE_003
Name: GENERATOR_RULES_ARE_MANDATORY
Description: Todo sistema generador debe cargar y aplicar sus reglas propias antes de iniciar materialización.
Enforcement:
- lectura obligatoria de este artefacto al inicio del ciclo
Status: ACTIVE


## RULE_004
Name: DEFENSIVE_OUTPUT_NORMALIZATION
Description: El generador no puede asumir que el output del modelo materializador está libre de artefactos estructurales espurios. El generador es responsable de normalizar el output antes de la verificación formal.
Enforcement:
- normalización automática post-generación
- la normalización opera sobre estructura, nunca sobre semántica
Status: ACTIVE

# GENERATOR_RULES — BETO_EXECUTOR

Propósito
---------

Este artefacto define las reglas propias del generador BETO_EXECUTOR.
BETO_EXECUTOR es un sistema generador: su propósito es materializar sistemas
de software completos a partir de una IDEA_RAW procesada por el Motor de Razonamiento.

Estas reglas aplican específicamente al Motor de Código (Paso 10).
No reemplazan las reglas del BETO Framework v4.3.
Las complementan en la capa del generador.

Artefacto requerido por: REGLA SISTEMAS_GENERADORES (BETO_INSTRUCTIVO.md v4.3)
Template base: GENERATOR_RULES_TEMPLATE.md


## RULE_001
Name: CONTRACT_ENFORCEMENT_BY_CONSTRUCTION
Description: Ningún contrato crítico de salida puede depender solo de obediencia por prompt del modelo materializador (Qwen2.5-Coder o equivalente).
Enforcement en BETO_EXECUTOR:
- El scaffold de cada archivo se construye programáticamente con stubs Python reales
  (funciones y clases con sus firmas exactas) antes de llamar al modelo.
- El modelo recibe estructura declarada, no instrucciones para inventarla.
- La preservación de BETO-TRACE se verifica mecánicamente post-generación
  mediante verificar_preservacion() — no se confía solo en el prompt.
Status: ACTIVE
Implementado en: motor_codigo/file_generator.py (_build_stubs_from_symbols)


## RULE_002
Name: MATERIALIZATION_RETRY_SCOPE
Description: Una falla localizada en materialización no autoriza rerun de pasos de razonamiento ya cerrados.
Enforcement en BETO_EXECUTOR:
- Si un archivo ya existe en output_dir al inicio del ciclo, se salta sin regenerar.
- Los Pasos 0-9 (Motor Razonamiento) nunca se re-ejecutan desde el Motor Código.
- Un RuntimeError en Paso 10 deja el estado en PENDIENTE y preserva
  los archivos ya escritos para reanudación parcial.
Status: ACTIVE
Implementado en: motor_codigo/motor.py (skip por archivo existente en ejecutar())


## RULE_003
Name: GENERATOR_RULES_ARE_MANDATORY
Description: El Motor de Código debe cargar y verificar este artefacto antes de iniciar materialización.
Enforcement en BETO_EXECUTOR:
- Lectura obligatoria al inicio de MotorCodigo.ejecutar().
- Si el artefacto no existe o está incompleto, la ejecución se detiene
  con RuntimeError antes de realizar cualquier llamada al modelo.
Status: ACTIVE
Implementado en: motor_codigo/motor.py (_cargar_generator_rules)


## RULE_004
Name: DEFENSIVE_OUTPUT_NORMALIZATION
Description: El generador no puede asumir que el output del modelo materializador está libre de artefactos estructurales espurios.
Enforcement en BETO_EXECUTOR:
- Post-generación y post-inject, se aplican dos normalizaciones deterministas:
  1. _dedup_module_strings(): elimina docstrings de módulo flotantes duplicados.
  2. _dedup_trace_ids_in_code(): elimina IDs BETO-TRACE duplicados dentro
     del mismo docstring.
- La normalización opera sobre estructura, nunca sobre semántica.
- La verificación de preservación ocurre después de la normalización.
Status: ACTIVE
Implementado en: motor_codigo/motor.py (_dedup_module_strings, _dedup_trace_ids_in_code)

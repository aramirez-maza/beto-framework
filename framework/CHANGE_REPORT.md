# CHANGE_REPORT

## Archivos modificados
- /home/aramirez/codex_test/framework/BETO_INSTRUCTIVO.md
- /home/aramirez/codex_test/framework/PHASE_TEMPLATE.md
- /home/aramirez/codex_test/framework/MANIFEST_BETO_TEMPLATE.md

## Archivo nuevo creado
- /home/aramirez/codex_test/framework/IMPLEMENTATION_CONTRACT_TEMPLATE.md

## Resumen preciso del cambio
Se introdujo `IMPLEMENTATION_CONTRACT` como capa opcional entre `PHASE` y `MATERIALIZATION`.
La mejora no altera la autoridad semántica del `BETO_CORE` ni la autoridad lógica-operativa de `PHASE`.
Su función es congelar la proyección estructural mínima hacia materialización cuando existe riesgo real de variabilidad estructural en sistemas medianos o complejos.

## Reglas de activación del IMPLEMENTATION_CONTRACT
Generarlo solo si existe al menos una de estas condiciones:
- múltiples archivos por fase
- shared contracts entre fases
- más de un output materializable no trivial
- dependencia fina entre componentes dentro del mismo BETO
- riesgo real de variabilidad estructural entre implementaciones válidas

Omitirlo si `BETO_CORE + PHASE + MANIFEST` ya gobiernan la materialización sin ambigüedad estructural relevante.

## Impacto esperado
- Reduce variabilidad estructural en materialización de BETOs medianos o complejos.
- Evita inflar `PHASE_TEMPLATE` con detalle estructural excesivo.
- Mantiene simple el flujo para sistemas pequeños.
- Añade una autoridad local y acotada para naming estructural, ownership y orden fino cuando realmente hace falta.

## Compatibilidad con proyectos BETO existentes
- Totalmente compatible hacia atrás para proyectos simples: pueden omitir `IMPLEMENTATION_CONTRACT` sin cambiar el flujo.
- Compatible con proyectos ya cerrados: la omisión explícita se considera válida.
- No rompe el flujo validado en `repeated_log_monitor`, porque ese proyecto puede seguir sin `IMPLEMENTATION_CONTRACT`.

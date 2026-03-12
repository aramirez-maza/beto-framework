# OPERATIONAL_LESSONS — [NOMBRE DEL PROYECTO]
**Paso 11 — Memoria Operacional del Proyecto**
**Proyecto:** [nombre]
**Sistema materializado:** [identificador del BETO raíz]
**Fecha de cierre:** [YYYY-MM-DD]
**Estado:** ABIERTO / CERRADO

---

## Propósito

Este documento captura lo que el sistema enseñó durante su operación real
y que no es interceptable por ningún template — solo emerge con el producto en uso.

Su destino es este proyecto. No sube al framework directamente.
Es la memoria operacional para quien trabaje con este sistema en ciclos futuros.

---

## Extensiones aplicadas durante el ciclo

[Lista de capacidades que se añadieron al sistema después de la materialización inicial,
con su justificación y resultado.]

### Extensión [N]

**Qué se añadió:**
[Nombre y descripción de la extensión]

**Por qué emergió:**
[Qué situación operacional la reveló como necesaria]

**Cómo se implementó:**
[Descripción breve del approach — no es documentación técnica detallada]

**Resultado:**
[ ] Resuelve el problema completamente
[ ] Resuelve parcialmente — deuda declarada pendiente
[ ] Solución provisional — requiere ciclo formal para cerrar bien

**Artefactos generados:**
[Archivos creados o modificados]

---

## Limitaciones estructurales identificadas

[Gaps que solo emergen al operar — no interceptables por los templates.]

### Limitación [N]

**Descripción:**
[Qué no puede hacer el sistema que el diseño asumía implícitamente que podría]

**Cuándo se manifiesta:**
[Condición operacional que la activa]

**Impacto operacional:**
[ ] Bloqueante — no puede completar el caso de uso
[ ] Degradado — puede completar con workaround manual
[ ] Menor — señal de calidad pero no bloquea

**¿Abre un ciclo nuevo?**
[ ] Sí — se recomienda iniciar BETO corto para cerrar este gap
[ ] No — absorbe como deuda declarada aceptable
[ ] Pendiente de decisión del operador

---

## Deuda declarada al cierre

[Gaps conocidos que se aceptan conscientemente al cerrar este ciclo.
No son errores — son decisiones de scope.]

| Ítem | Impacto | Condición para reabrir |
|---|---|---|
| [descripción] | [Alto/Medio/Bajo] | [qué haría que valga la pena atacarlo] |

---

## Recomendaciones para el siguiente ciclo

[Si se iniciara un nuevo ciclo BETO sobre este sistema o uno similar,
¿qué debería hacerse diferente o primero?]

1. [recomendación]
2. [recomendación]

---

## Firma de cierre

**Operador:** [nombre]
**Fecha:** [YYYY-MM-DD]
**Estado final:** CERRADO

Una vez firmado, este documento no se reabre.
Nuevas lecciones → nuevo ciclo BETO o nueva entrada en el siguiente OPERATIONAL_LESSONS.

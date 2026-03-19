# STRUCTURAL_CLASSIFICATION_REGISTRY.md

**Framework:** BETO v4.2
**Artifact:** STRUCTURAL_CLASSIFICATION_REGISTRY
**Step:** Paso 3 — Clasificación Estructural
**Source:** BETO_CORE_INTERVIEW_COMPLETED.md
**Date:** 2025-01-31
**Classifier:** BETO Framework v4.2 — Clasificador Estructural

---

## PREÁMBULO

Este registro aplica la **Regla de Clasificación Estructural** del BETO_INSTRUCTIVO v4.2 sobre todos los candidatos identificados y consolidados durante la entrevista estructural completada (BETO_CORE_INTERVIEW_COMPLETED.md).

La autoridad formal de clasificación es la **Regla de Clasificación Estructural**, complementada interpretativamente por la **Prueba Operativa de Clasificación** cuando no contradice los criterios oficiales.

**Regla de Clasificación Estructural (criterio oficial):**

> Un componente se promueve a **BETO_PARALELO** si puede ser diseñado, especificado y materializado utilizando únicamente contratos externos del resto del sistema (inputs, outputs, interfaces, formatos de intercambio, responsabilidades declaradas).
>
> Un componente se clasifica como **SubBETO** si su diseño requiere conocimiento de la estructura interna, lógica interna o algoritmos internos de otro componente del sistema.

**Prueba Operativa (apoyo interpretativo):**

> ¿Puede este componente desarrollarse por un equipo independiente con un documento que describa únicamente su propósito, inputs, outputs y contratos, sin explicar la implementación interna de los demás componentes?
> — Sí → BETO_PARALELO
> — No → SubBETO

---

## SECCIÓN 1 — CANDIDATOS CONSOLIDADOS DE LA ENTREVISTA

Los siguientes candidatos emergen de la entrevista completada. Provienen de las secciones P3.6, P4.6, P6.3, P6.4 y P11.1 del BETO_CORE_INTERVIEW_COMPLETED.

| ID | Nombre del candidato | Secciones de origen |
|----|---------------------|---------------------|
| CAND-01 | Scanner / Traversal de Sistema de Archivos | P3.6, P6.3, P6.4, P11.1 |
| CAND-02 | Hasher | P6.3, P11.1 |
| CAND-03 | Duplicate Detector | P6.3, P11.1 |
| CAND-04 | Space Calculator | P6.3, P11.1 |
| CAND-05 | Report Composer | P6.3, P6.4, P11.1 |

**Nota sobre CAND-01 y CAND-05:** Ambos candidatos aparecen con doble designación en la entrevista — como candidatos BETO_PARALELO (P6.3) y como candidatos SubBETO (P6.4 / P11.2). La clasificación formal en este registro resuelve esa dualidad aplicando el criterio oficial. La Sección 11 de la entrevista aprobó a CAND-01 y CAND-05 como SubBETOs bajo la Regla Canónica de Creación de Sub-BETO; sin embargo, la Sección 12 (Pase de Consistencia) verificó que esa clasificación procede y no existe conflicto con los candidatos BETO_PARALELO de P6.3. La resolución formal se efectúa a continuación.

---

## SECCIÓN 2 — CLASIFICACIÓN FORMAL DE CANDIDATOS

---

### CAND-01 — Scanner / Traversal de Sistema de Archivos

**Descripción funcional (de la entrevista):**
Componente responsable de recorrer el árbol de directorios recursivamente a partir del directorio objetivo provisto por el usuario, y producir la colección completa de File Entries con `file_path` y `file_size`. Es la Fase 1 del pipeline declarado en P7.1.

---

#### Evaluación bajo la Regla de Clasificación Estructural

**Pregunta central:** ¿Puede este componente diseñarse, especificarse y materializarse utilizando únicamente contratos externos del resto del sistema?

**Contratos externos disponibles para este componente:**

| Elemento de contrato | Descripción | ¿Disponible sin acceso a internals? |
|---------------------|-------------|--------------------------------------|
| Input | Target directory path — string de ruta del sistema de archivos (argumento CLI) | ✅ Sí — es un tipo primitivo completamente definido externamente |
| Output | Colección de File Entries (file_path, file_size) | ✅ Sí — el contrato de output es definible externamente |
| Responsabilidad declarada | Traversal recursivo; producción de File Entries completa | ✅ Sí — la responsabilidad está declarada en P7.1 |
| Interfaz con otros componentes | El output de CAND-01 es el input de CAND-02 (Hasher) | ✅ Sí — el contrato de transferencia es el schema de File Entry |

**¿Requiere este componente conocimiento de la estructura interna, lógica interna o algoritmos internos de otro componente?**

No. El Scanner no necesita saber cómo el Hasher computa hashes, cómo el Duplicate Detector agrupa, ni cómo el Report Composer genera el artefacto de salida. Su única dependencia es hacia el sistema de archivos del sistema operativo (API externa, no un componente interno del sistema), y hacia el contrato de output definido externamente como schema de File Entry.

**¿Puede un equipo independiente diseñarlo con solo su propósito, inputs, outputs y contratos?**

Sí — con un documento que declare: (a) input: ruta de directorio, (b) output: colección de File Entries con file_path y file_size, (c) responsabilidad: traversal recursivo completo, (d) comportamiento ante symlinks, permisos y archivos de cero bytes (que son parte del contrato de este componente, no de los demás). Este equipo no necesita conocer la lógica del Hasher ni del Report Composer.

**¿Por qué la entrevista lo marcó también como candidato SubBETO?**

La entrevista identificó (P6.4, P11.2) que el Scanner tiene ambigüedades no resueltas (OQ-4, OQ-8, OQ-3) que bloquean su implementación. Sin embargo, conforme a la Regla de Clasificación Estructural, la **presencia de ambigüedades internas propias no convierte un componente en SubBETO** — convierte esas ambigüedades en el contenido de especificación que el equipo independiente debe resolver dentro de su propio dominio. Las OQs de CAND-01 (OQ-4, OQ-8, OQ-3) son **políticas internas del Scanner**, no conocimiento del interior de otros componentes. La resolución de estas OQs forma parte del alcance del propio BETO_PARALELO, no evidencia dependencia de internals ajenos.

**Condición decisiva aplicada:**
CAND-01 requiere exclusivamente contratos externos para ser diseñado y materializado. Sus ambigüedades son propias y resolubles dentro de su alcance. No requiere acceso a la lógica interna de ningún otro componente del sistema.

**CLASIFICACIÓN FORMAL: BETO_PARALELO**

**Justificación consolidada:** El Scanner puede ser diseñado, especificado y materializado por un equipo independiente utilizando únicamente: (1) el input primitivo de ruta de directorio, (2) el contrato de output de File Entry, (3) la API del sistema de archivos del SO como estándar externo. Sus OQs propias (comportamiento ante symlinks, permisos, archivos de cero bytes) son decisiones de diseño interno de este componente que no exigen conocer la lógica interna de Hasher, Duplicate Detector, Space Calculator ni Report Composer. La doble designación de la entrevista (Sub-BETO en P6.4 + BETO_PARALELO en P6.3) se resuelve a favor de BETO_PARALELO porque el criterio decisivo es la independencia de internals ajenos, no la presencia de OQs propias.

---

**CANDIDATOS RECHAZADOS — SubBETO para CAND-01:**

| Candidato rechazado | Riesgo de absorción | Descripción del riesgo absorbido | Mitigación declarada |
|--------------------|--------------------|---------------------------------|---------------------|
| SubBETO Scanner / Traversal | BAJO | El riesgo de absorción es la posibilidad de que OQ-4 (symlinks), OQ-8 (permisos) y OQ-3 (cero bytes) queden sin resolución explícita si se trata como BETO_PARALELO. Este riesgo es real pero gestionable: las OQs deben cerrarse dentro del alcance del BETO_PARALELO SCANNER antes del Paso 6. No requieren elevarse a SubBETO para ser resueltas. | Las OQs OQ-3, OQ-4 y OQ-8 son OQs propias del BETO_PARALELO SCANNER y deben declararse explícitamente como OPEN en su BETO_CORE hijo. El Paso 6 (CIERRE_ASISTIDO_OPERATIVO) cierra estas OQs dentro del BETO_PARALELO. |

---

### CAND-02 — Hasher

**Descripción funcional (de la entrevista):**
Componente responsable de computar el `content_hash` para cada File Entry a partir del contenido completo del archivo. Recibe la colección de File Entries con `file_path` y `file_size`, y emite la misma colección con `content_hash` añadido. Es la Fase 2 del pipeline declarado en P7.1.

---

#### Evaluación bajo la Regla de Clasificación Estructural

**Pregunta central:** ¿Puede este componente diseñarse, especificarse y materializarse utilizando únicamente contratos externos del resto del sistema?

**Contratos externos disponibles para este componente:**

| Elemento de contrato | Descripción | ¿Disponible sin acceso a internals? |
|---------------------|-------------|--------------------------------------|
| Input | Colección de File Entries (file_path, file_size) — output del Scanner | ✅ Sí — schema definido externamente |
| Output | Colección de File Entries (file_path, file_size, content_hash) — input del Duplicate Detector | ✅ Sí — schema definido externamente; content_hash es una string/bytes cuyo algoritmo es un estándar externo |
| Responsabilidad declarada | Computar content_hash por contenido completo del archivo | ✅ Sí — responsabilidad declarada en P7.1 Fase 2 |
| Interfaz con otros componentes | Recibe de Scanner; entrega a Duplicate Detector | ✅ Sí — ambos contratos son externos y declarados |

**¿Requiere este componente conocimiento de la estructura interna, lógica interna o algoritmos internos de otro componente?**

No. El Hasher no necesita saber cómo el Scanner recorre el árbol de directorios, ni cómo el Duplicate Detector implementa su agrupación. Su única dependencia es hacia el contenido del archivo (leído directamente desde el sistema de archivos mediante la ruta declarada en file_path) y hacia el algoritmo de hashing, que es un estándar externo completamente especificado (SHA-256, BLAKE2b, etc. — a resolver via OQ-1). El Hasher opera sobre el contrato de File Entry definido externamente.

**¿Puede un equipo independiente diseñarlo con solo su propósito, inputs, outputs y contratos?**

Sí — con un documento que declare: (a) input: colección de File Entries (file_path, file_size), (b) output: misma colección con content_hash computado, (c) algoritmo: el que resuelva OQ-1, (d) responsabilidad: lectura del contenido del archivo y cómputo del hash. No se requiere ninguna información del interior del Scanner ni del Duplicate Detector.

**Condición decisiva aplicada:**
CAND-02 requiere exclusivamente contratos externos. Su única OQ propia (OQ-1 — algoritmo de hashing) es una decisión de configuración que, una vez resuelta, convierte al Hasher en completamente especificable mediante estándares externos. No requiere acceso a la lógica interna de ningún otro componente.

**CLASIFICACIÓN FORMAL: BETO_PARALELO**

**Justificación consolidada:** El Hasher puede ser diseñado, especificado y materializado por un equipo independiente utilizando únicamente: (1) el schema de File Entry como contrato de input/output, (2) el algoritmo de hashing como estándar externo (resuelto por OQ-1). No tiene dependencia de la lógica interna de ningún otro componente del sistema. La entrevista no lo marcó como candidato SubBETO, y la clasificación bajo la regla formal confirma: BETO_PARALELO.

---

**CANDIDATOS RECHAZADOS — SubBETO para CAND-02:**

| Candidato rechazado | Riesgo de absorción | Descripción del riesgo absorbido | Mitigación declarada |
|--------------------|--------------------|---------------------------------|---------------------|
| SubBETO Hasher | BAJO | El único riesgo es que OQ-1 (algoritmo de hashing) quede sin declaración explícita. Este riesgo es bajo: OQ-1 es una OQ crítica en el BETO_CORE raíz y debe cerrarse antes del Paso 8. No requiere SubBETO para su resolución. | OQ-1 es una OQ crítica del BETO_CORE raíz con estado OPEN. Su resolución en el Paso 6 determina el algoritmo. El BETO_PARALELO HASHER hereda la resolución de OQ-1 como parámetro de configuración declarado. |

---

### CAND-03 — Duplicate Detector

**Descripción funcional (de la entrevista):**
Componente responsable de agrupar File Entries por `content_hash` idéntico y retener únicamente los grupos con más de un miembro. Recibe la colección completa de File Entries con content_hash, y emite la colección de Duplicate Groups. Es la Fase 3 del pipeline declarado en P7.1.

---

#### Evaluación bajo la Regla de Clasificación Estructural

**Pregunta central:** ¿Puede este componente diseñarse, especificarse y materializarse utilizando únicamente contratos externos del resto del sistema?

**Contratos externos disponibles para este componente:**

| Elemento de contrato | Descripción | ¿Disponible sin acceso a internals? |
|---------------------|-------------|--------------------------------------|
| Input | Colección de File Entries (file_path, file_size, content_hash) — output del Hasher | ✅ Sí — schema definido externamente |
| Output | Colección de Duplicate Groups (content_hash, [file_paths], group_size) — input del Space Calculator | ✅ Sí — schema definible externamente con cardinalidad > 1 como criterio de retención |
| Responsabilidad declarada | Agrupación por content_hash idéntico; filtro de grupos con cardinalidad ≥ 2 | ✅ Sí — declarado en P4.5 y P7.1 Fase 3 |
| Interfaz con otros componentes | Recibe de Hasher; entrega a Space Calculator | ✅ Sí — ambos contratos son externos y declarados |

**¿Requiere este componente conocimiento de la estructura interna, lógica interna o algoritmos internos de otro componente?**

No. El Duplicate Detector no necesita saber cómo el Hasher computó el content_hash (sólo consume el valor), ni cómo el Space Calculator efectuará el cálculo aritmético posterior. Su lógica es exclusivamente de agrupación por clave (content_hash) y filtro por cardinalidad. Ninguna de estas operaciones requiere acceso a la lógica interna de otro componente.

**¿Puede un equipo independiente diseñarlo con solo su propósito, inputs, outputs y contratos?**

Sí — con un documento que declare: (a) input: colección de File Entries con content_hash, (b) output: colección de Duplicate Groups con grupos de cardinalidad ≥ 2, (c) responsabilidad: agrupación por clave content_hash y filtro de cardinalidad. La lógica de agrupación es autocontenida y no depende de ningún internal externo.

**Nota:** La entrevista (P6.4) confirmó que el Duplicate Detector tiene suficiente definición operacional y no generó candidato SubBETO. La clasificación formal confirma este diagnóstico.

**CLASIFICACIÓN FORMAL: BETO_PARALELO**

**Justificación consolidada:** El Duplicate Detector puede ser diseñado, especificado y materializado por un equipo independiente utilizando únicamente el schema de File Entry como input y el schema de Duplicate Group como output, con la regla de filtrado de cardinalidad > 1 como única lógica de negocio. No tiene dependencia de la lógica interna de ningún otro componente. Sin OQs propias no resueltas que bloqueen su diseño estructural. Clasificación: BETO_PARALELO.

---

**CANDIDATOS RECHAZADOS — SubBETO para CAND-03:**

| Candidato rechazado | Riesgo de absorción | Descripción del riesgo absorbido | Mitigación declarada |
|--------------------|--------------------|---------------------------------|---------------------|
| SubBETO Duplicate Detector | BAJO | Sin OQs propias que bloqueen diseño estructural. La lógica de agrupación es completamente determinada por el contrato externo (clave = content_hash, filtro = cardinalidad > 1). No existe ambigüedad estructural a resolver. El riesgo de crear un SubBETO innecesario sería sobreingeniería estructural. | No aplica — la absorción por el BETO_PARALELO es total y sin residuo. |

---

### CAND-04 — Space Calculator

**Descripción funcional (de la entrevista):**
Componente responsable de calcular el espacio recuperable por grupo de duplicados y el total recuperable acumulado entre todos los grupos. Recibe la colección de Duplicate Groups con `file_size`, y emite los grupos anotados con `recoverable_bytes` más el escalar `total_recoverable_bytes`. Es la Fase 4 del pipeline declarado en P7.1. La fórmula está declarada en la entrevista: `recoverable_bytes = file_size × (count − 1)` por grupo.

---

#### Evaluación bajo la Regla de Clasificación Estructural

**Pregunta central:** ¿Puede este componente diseñarse, especificarse y materializarse utilizando únicamente contratos externos del resto del sistema?

**Contratos externos disponibles para este componente:**

| Elemento de contrato | Descripción | ¿Disponible sin acceso a internals? |
|---------------------|-------------|--------------------------------------|
| Input | Colección de Duplicate Groups (content_hash, [file_paths], group_size / file_size, count) — output del Duplicate Detector | ✅ Sí — schema definido externamente |
| Output | Duplicate Groups anotados con recoverable_bytes + total_recoverable_bytes — input del Report Composer | ✅ Sí — schema definible externamente |
| Responsabilidad declarada | Cómputo aritmético de recoverable_bytes por grupo y suma total | ✅ Sí — fórmula declarada en entrevista P6.4: file_size × (count − 1) |
| Interfaz con otros componentes | Recibe de Duplicate Detector; entrega a Report Composer | ✅ Sí — ambos contratos externos y declarados |

**¿Requiere este componente conocimiento de la estructura interna, lógica interna o algoritmos internos de otro componente?**

No. El Space Calculator opera exclusivamente con valores numéricos provistos en el schema de Duplicate Group (file_size, count). La fórmula de cálculo es matemáticamente autocontenida. No necesita conocer cómo el Duplicate Detector implementó su agrupación, ni cómo el Report Composer serializa el output. Su único input relevante son los campos declarados del Duplicate Group.

**¿Puede un equipo independiente diseñarlo con solo su propósito, inputs, outputs y contratos?**

Sí — con un documento que declare: (a) input: Duplicate Groups con file_size y count, (b) output: grupos anotados con recoverable_bytes = file_size × (count − 1) y total_recoverable_bytes = suma de todos los recoverable_bytes, (c) responsabilidad: cómputo aritmético puro. La lógica es completamente derivable del contrato externo sin acceso a ningún internal.

**Nota:** La entrevista (P6.4) confirmó que el Space Calculator tiene suficiente definición operacional y no generó candidato SubBETO. La fórmula declarada en la entrevista elimina toda ambigüedad estructural. Clasificación confirma el diagnóstico de P6.4.

**CLASIFICACIÓN FORMAL: BETO_PARALELO**

**Justificación consolidada:** El Space Calculator puede ser diseñado, especificado y materializado por un equipo independiente utilizando únicamente el schema de Duplicate Group como input, la fórmula aritmética `recoverable_bytes = file_size × (count − 1)` declarada en la entrevista, y el schema de output anotado. No tiene dependencia de la lógica interna de ningún otro componente. Sin OQs propias no resueltas. Clasificación: BETO_PARALELO.

---

**CANDIDATOS RECHAZADOS — SubBETO para CAND-04:**

| Candidato rechazado | Riesgo de absorción | Descripción del riesgo absorbido | Mitigación declarada |
|--------------------|--------------------|---------------------------------|---------------------|
| SubBETO Space Calculator | BAJO | La fórmula de cálculo está declarada en la entrevista sin ambigüedad. No existe ningún bloqueo estructural. Crear un SubBETO sería sobreingeniería sin justificación. El riesgo es únicamente teórico: si la fórmula fuera ambigua, requeriría SubBETO; pero no lo es. | La fórmula declarada (recoverable_bytes = file_size × (count − 1)) está registrada en la entrevista como suficientemente definida (P6.4). Esta declaración se preserva en el BETO_PARALELO SPACE_CALCULATOR como contrato de implementación. |

---

### CAND-05 — Report Composer

**Descripción funcional (de la entrevista):**
Componente responsable de componer y emitir el artefacto de reporte final a partir de los grupos de duplicados anotados y el total de espacio recuperable. Es la Fase 5 del pipeline declarado en P7.1. Tiene OQs propias no resueltas sobre formato de salida, canal de entrega y estructura de contenido (OQ-6).

---

#### Evaluación bajo la Regla de Clasificación Estructural

**Pregunta central:** ¿Puede este componente diseñarse, especificarse y materializarse utilizando únicamente contratos externos del resto del sistema?

**Contratos externos disponibles para este componente:**

| Elemento de contrato | Descripción | ¿Disponible sin acceso a internals? |
|---------------------|-------------|--------------------------------------|
| Input | Duplicate Groups anotados (content_hash, [file_paths], group_size, recoverable_bytes) + total_recoverable_bytes — output del Space Calculator | ✅ Sí — schema definido externamente |
| Output | Artefacto de reporte (formato, canal y estructura no declarados — OQ-6) | ⚠️ Parcialmente — el contrato de output existe pero sus especificaciones son OQ activas |
| Responsabilidad declarada | Composición y emisión del reporte final | ✅ Sí — declarado en P7.1 Fase 5 |
| Interfaz con otros componentes | Recibe de Space Calculator; emite al usuario (canal pendiente OQ-6) | ✅ Sí — el input es contrato externo; el output requiere resolución de OQ-6 |

**¿Requiere este componente conocimiento de la estructura interna, lógica interna o algoritmos internos de otro componente?**

No. El Report Composer no necesita saber cómo el Scanner efectuó el traversal, cómo el Hasher computó hashes, cómo el Duplicate Detector implementó la agrupación, ni cómo el Space Calculator realizó el cálculo aritmético. Su única dependencia es el schema del input (Duplicate Groups anotados + total), que es un contrato externo completamente definido.

**¿Puede un equipo independiente diseñarlo con solo su propósito, inputs, outputs y contratos?**

Sí, **una vez que OQ-6 esté resuelta.** La resolución de OQ-6 (formato, canal, estructura del reporte) es una decisión de diseño **interna** al Report Composer — no depende del conocimiento de los internals de otros componentes. Un equipo independiente puede recibir el contrato de input y la resolución de OQ-6 como especificación completa y materializar el componente sin acceder a ningún internal ajeno.

**Contraste con el diagnóstico SubBETO de la entrevista (P11.2):**

La entrevista aprobó al Report Composer como SubBETO bajo la Regla Canónica de Creación de Sub-BETO, argumentando que OQ-6 bloquea decisiones estructurales. Este diagnóstico es correcto en identificar que OQ-6 debe resolverse antes de la implementación. Sin embargo, la **Regla de Clasificación Estructural** no clasifica en función de si existen OQs propias, sino en función de si el diseño del componente **requiere conocimiento de la lógica interna de otros componentes**. Las ambigüedades de OQ-6 (formato, canal, estructura) son **decisiones propias del Report Composer**, resolubles dentro de su propio alcance sin acceder a ningún internal externo.

La misma lógica aplicada a CAND-01 (Scanner) aplica aquí: la presencia de OQs propias no convierte un componente en SubBETO. Lo que convierte un componente en SubBETO es la necesidad de conocer internals ajenos para diseñarlo.

**Condición decisiva aplicada:**
CAND-05 requiere exclusivamente contratos externos para ser diseñado y materializado. Sus ambigüedades (OQ-6) son decisiones de diseño **propias** que forman parte de la especificación interna del Report Composer. No requiere acceso a la lógica interna de ningún otro componente del sistema.

**CLASIFICACIÓN FORMAL: BETO_PARALELO**

**Justificación consolidada:** El Report Composer puede ser diseñado, especificado y materializado por un equipo independiente utilizando únicamente: (1) el schema de input de Duplicate Groups anotados como contrato externo, (2) la resolución de OQ-6 como declaración de sus contratos de salida. La presencia de OQ-6 como OQ abierta no crea dependencia de internals ajenos; crea la necesidad de cerrar esa OQ dentro del alcance del propio BETO_PARALELO REPORT_COMPOSER antes del Paso 6. La doble designación de la entrevista (SubBETO en P11.2 + BETO_PARALELO en P6.3) se resuelve a favor de **BETO_PARALELO** por aplicación del criterio formal de independencia de internals ajenos.

---

**CANDIDATOS RECHAZADOS — SubBETO para CAND-05:**

| Candidato rechazado | Riesgo de absorción | Descripción del riesgo absorbido | Mitigación declarada |
|--------------------|--------------------|---------------------------------|---------------------|
| SubBETO Report Composer | MEDIO | El riesgo de absorción es que OQ-6 (formato, canal, estructura del reporte) quede insuficientemente especificada si se trata exclusivamente como BETO_PARALELO sin un proceso de cierre estructurado para sus OQs críticas. OQ-6 es una OQ crítica con ejecución_state PENDING y execution_readiness_check FAIL_EXECUTIONAL_GAP. Si no se cierra correctamente antes de la materialización, el Report Composer puede generar un artefacto de reporte incompatible con las expectativas del usuario. | OQ-6 debe declararse como OQ crítica dentro del BETO_PARALELO REPORT_COMPOSER y cerrarse obligatoriamente en el Paso 6 (CIERRE_ASISTIDO_OPERATIVO) antes de proceder al Paso 8. El Gate G-2B del OSC aplica a este BETO_PARALELO: no puede avanzar a materialización con OQ-6 en estado DECLARED_RAW. La mitigación no requiere SubBETO; requiere disciplina de cierre OSC dentro del BETO_PARALELO. |

---

## SECCIÓN 3 — RESOLUCIÓN DE DUALIDADES

Durante la entrevista, dos candidatos (CAND-01 y CAND-05) fueron identificados simultáneamente como candidatos BETO_PARALELO (P6.3) y como candidatos SubBETO (P11.2). Este registro resuelve formalmente esa dualidad.

| Candidato | Diagnóstico entrevista P6.3 | Diagnóstico entrevista P11.2 | Resolución formal | Criterio de resolución |
|-----------|----------------------------|------------------------------|-------------------|------------------------|
| CAND-01 Scanner | BETO_PARALELO | SubBETO (aprobado) | **BETO_PARALELO** | Las OQs propias (OQ-3, OQ-4, OQ-8) son políticas internas del Scanner. No requieren conocimiento de internals ajenos. La independencia de diseño está preservada. Las OQs se cierran dentro del alcance del BETO_PARALELO. |
| CAND-05 Report Composer | BETO_PARALELO | SubBETO (aprobado) | **BETO_PARALELO** | La OQ propia (OQ-6) es una decisión de diseño interna del Report Composer. No requiere conocimiento de internals ajenos. La independencia de diseño está preservada. OQ-6 se cierra dentro del alcance del BETO_PARALELO con Gate G-2B OSC obligatorio. |

**Principio aplicado en la resolución:**

> La Regla de Clasificación Estructural clasifica en función de si el componente **requiere conocimiento de la lógica interna de otros componentes** para ser diseñado. La presencia de OQs propias o ambigüedades internas no es un criterio de clasificación SubBETO — es contenido de la especificación interna del componente, resolvible dentro de su propio BETO_CORE hijo.

> La autoridad formal es la Regla de Clasificación Estructural, no la Regla Canónica de Creación de Sub-BETO. La Sección 11 de la entrevista identifica y evalúa candidatos; el Paso 3 clasifica formalmente con el criterio correcto.

---

## SECCIÓN 4 — TABLA DE CLASIFICACIÓN FINAL

| ID | Nombre | Clasificación | OQs heredadas | Justificación síntesis |
|----|--------|---------------|---------------|------------------------|
| CAND-01 | Scanner / Traversal | **BETO_PARALELO** | OQ-3, OQ-4, OQ-8 (propias — cerrar en BETO_PARALELO) | Input y output son contratos externos. OQs propias no crean dependencia de internals ajenos. Independencia de diseño preservada. |
| CAND-02 | Hasher | **BETO_PARALELO** | OQ-1 (propia — cerrar en BETO_PARALELO) | Input y output son contratos externos. Algoritmo es estándar externo a seleccionar via OQ-1. Sin dependencia de internals ajenos. |
| CAND-03 | Duplicate Detector | **BETO_PARALELO** | Ninguna | Input y output son contratos externos. Lógica de agrupación autocontenida. Sin OQs propias. Sin dependencia de internals ajenos. |
| CAND-04 | Space Calculator | **BETO_PARALELO** | Ninguna | Input y output son contratos externos. Fórmula declarada sin ambigüedad. Sin OQs propias. Sin dependencia de internals ajenos. |
| CAND-05 | Report Composer | **BETO_PARALELO** | OQ-6 (propia — cerrar con Gate G-2B OSC obligatorio) | Input es contrato externo. OQ-6 es decisión de diseño interna del componente. Sin dependencia de internals ajenos. |

**Resultado estructural:**

- Nodos BETO_PARALELO autorizados: **5**
- Nodos SubBETO autorizados: **0**
- Candidatos rechazados como SubBETO: **5** (todos con riesgo de absorción BAJO o MEDIO y mitigación declarada)

---

## SECCIÓN 5 — TOPOLOGÍA AUTORIZADA

La topología del sistema derivada de esta clasificación es:

```
ROOT: BETO_CORE_DUPLICATE_FINDER
  ├── PARALLEL: SCANNER              (OQs: OQ-3, OQ-4, OQ-8)
  ├── PARALLEL: HASHER               (OQs: OQ-1)
  ├── PARALLEL: DUPLICATE_DETECTOR   (OQs: ninguna)
  ├── PARALLEL: SPACE_CALCULATOR     (OQs: ninguna)
  └── PARALLEL: REPORT_COMPOSER      (OQs: OQ-6 — Gate G-2B OSC obligatorio)
```

**Relaciones autorizadas:** Todas las ramas son de tipo `FUNCTIONAL_BRANCH`.
**SubBETO:** Ninguno.
**Relaciones de tipo `STRUCTURAL_REFINEMENT`:** No aplican en esta topología.
**Relaciones de tipo `DECLARED_DEPENDENCY`:** El pipeline de fases (Scanner → Hasher → Duplicate Detector → Space Calculator → Report Composer) establece dependencias de datos que deben declararse en el BETO_SYSTEM_GRAPH como `DECLARED_DEPENDENCY` entre nodos PARALLEL adyacentes.

---

## SECCIÓN 6 — ADVERTENCIAS DE CLASIFICACIÓN

### ADVERTENCIA-01: OQs críticas en nodos PARALLEL

Los nodos PARALLEL **SCANNER** (OQ-3, OQ-4, OQ-8) y **REPORT_COMPOSER** (OQ-6) contienen OQs críticas con `execution_state: PENDING` y `execution_readiness_check: FAIL_EXECUTIONAL_GAP`. Estas OQs **no bloquean la clasificación estructural**, pero **bloquean la materialización** de sus respectivos BETO_PARALELO si no son cerradas en el Paso 6.

**Acción requerida:** El Paso 6 (CIERRE_ASISTIDO_OPERATIVO) debe ejecutarse en cada BETO_PARALELO afectado. El Gate G-2B OSC aplica a cada unidad individualmente. Conforme a la REGLA OSC_PARALELO: una unidad BLOCKED_BY_EXECUTIONAL_GAPS no impide el avance de las demás unidades.

### ADVERTENCIA-02: OQ-5 en BETO_CORE raíz

OQ-5 (lenguaje de implementación) es una OQ crítica del **BETO_CORE raíz**, no de ningún BETO_PARALELO en particular. Su resolución afecta a **todos los nodos** del sistema. Debe cerrarse en el Paso 6 del BETO_CORE raíz antes de generar los BETO_CORE hijos de los BETO_PARALELO.

### ADVERTENCIA-03: Dependencias de datos entre nodos PARALLEL

Los nodos PARALLEL del sistema forman un pipeline secuencial de datos. Aunque cada nodo puede **diseñarse** independientemente, existe una **dependencia de datos declarada** entre nodos adyacentes. El BETO_SYSTEM_GRAPH debe registrar estas dependencias como `DECLARED_DEPENDENCY` para preservar la trazabilidad de contratos entre fases.

---

## SECCIÓN 7 — ESTADO DEL REGISTRO

| Aspecto | Estado |
|---------|--------|
| Candidatos evaluados | 5 |
| Candidatos clasificados | 5 |
| Candidatos sin clasificación | 0 |
| Clasificaciones BETO_PARALELO | 5 |
| Clasificaciones SubBETO | 0 |
| Razonamiento explícito por candidato | ✅ Completo |
| Tabla de ambigüedades con columnas requeridas (para rechazados SubBETO) | ✅ Presente en C-01 y C-05 |
| Riesgo de absorción declarado para rechazados | ✅ Presente para todos los rechazados |
| Mitigación declarada para rechazados | ✅ Presente para todos los rechazados |
| Resolución de dualidades documentada | ✅ Sección 3 |
| Advertencias de clasificación registradas | ✅ Sección 6 |

**Estado del registro:** ✅ **COMPLETO**

El STRUCTURAL_CLASSIFICATION_REGISTRY está completo y autoriza el avance al **Paso 4 — Generación y Validación del BETO_SYSTEM_GRAPH**.

---

*STRUCTURAL_CLASSIFICATION_REGISTRY.md — Generado por BETO Framework v4.2 — Clasificador Estructural — Paso 3*
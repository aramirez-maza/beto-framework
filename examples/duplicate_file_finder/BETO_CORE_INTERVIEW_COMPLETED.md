# BETO_CORE_INTERVIEW_COMPLETED.md

**Framework:** BETO v4.2
**Artifact:** BETO_CORE_INTERVIEW_COMPLETED
**Source BETO_CORE_DRAFT:** BETO_CORE_DRAFT.md (eligibility: GO)
**Date:** 2025-01-31

---

## SECCIÓN 1 — SYSTEM INTENT

### P1.1 — Propósito fundamental

**¿Qué debe existir cuando este sistema esté resuelto?**

Una herramienta CLI ejecutable que, dado un directorio objetivo, recorra su árbol de archivos recursivamente, calcule el hash de contenido de cada archivo encontrado, identifique grupos de archivos duplicados por hash idéntico, y produzca un reporte que exponga esos grupos, las rutas de archivo correspondientes, y el espacio en disco total recuperable.

**¿Qué problema específico deja de existir?**

La incapacidad del usuario de detectar y cuantificar archivos duplicados dentro de un sistema de archivos local sin recurrir a inspección manual o herramientas externas no controladas.

---

### P1.2 — Criterio de éxito observable

El sistema cumple su objetivo cuando se verifican todas las siguientes capacidades:

1. Dado un directorio, la herramienta produce un reporte que lista correctamente todos los grupos de archivos con contenido idéntico, incluyendo las rutas de cada archivo por grupo.
2. El reporte incluye el espacio total recuperable calculado a partir de las copias redundantes detectadas.
3. El sistema completa la ejecución sin modificar, eliminar ni mover ningún archivo del sistema de archivos escaneado.

---

### P1.3 — Naturaleza del sistema

El sistema produce salidas persistentes reutilizables: el reporte generado es un artefacto que puede consultarse después de la ejecución. El canal de entrega exacto (stdout, archivo, ambos) no está declarado — capturado como OQ-6.

---

## SECCIÓN 2 — SYSTEM BOUNDARIES

### P2.1 — Alcance explícito

Las siguientes funciones están claramente dentro del alcance del sistema:

- Aceptar un directorio objetivo como argumento CLI
- Traversar recursivamente el directorio objetivo
- Computar un hash de contenido para cada archivo descubierto
- Agrupar archivos que comparten hash de contenido idéntico
- Calcular el espacio total recuperable representado por archivos duplicados
- Generar un reporte que contenga grupos de duplicados, rutas de archivo por grupo, y espacio recuperable total

---

### P2.2 — Fuera de alcance explícito

Las siguientes funciones están explícitamente fuera del alcance:

- Eliminación o modificación de cualquier archivo
- Deduplicación o cualquier acción destructiva sobre el sistema de archivos
- Escaneo de rutas remotas o montadas en red (a menos que se declare explícitamente)
- Cualquier comportamiento no directamente implicado por scan, detect y report
- Resolución de enlaces simbólicos o hard links (a menos que se declare explícitamente — ver OQ-4)
- Cualquier ejecución programada, automatizada o en segundo plano

---

### P2.3 — Exclusiones operativas

- Optimización de rendimiento mediante pre-filtrado por tamaño: no declarado (ver OQ-2)
- Edición, inserción o borrado de datos del sistema de archivos: excluido explícitamente
- Simulación física: no aplicable
- Integraciones externas con APIs o servicios remotos: excluidas
- Autenticación o control de acceso: excluidos
- Multiusuario o ejecución concurrente: no declarado
- Soporte de opciones CLI adicionales más allá del directorio objetivo: no declarado (ver OQ-7)

---

## SECCIÓN 3 — INPUTS AND OUTPUTS

### P3.1 — Inputs principales

| # | Input | Origen | Tipo | Forma |
|---|-------|--------|------|-------|
| 1 | Ruta del directorio objetivo | Argumento CLI proporcionado por el usuario | String (ruta del sistema de archivos) | Único argumento posicional en la línea de comandos |
| 2 | Archivos del árbol de directorios | Sistema de archivos local, alcanzados por traversal recursivo | Archivos binarios/texto de contenido arbitrario | Leídos para cómputo de hash; no inspeccionados por estructura interna |

---

### P3.2 — Outputs principales

El sistema produce un reporte que contiene:

1. **Grupos de duplicados**: cada grupo identifica un conjunto de archivos cuyo contenido es idéntico (mismo hash)
2. **Rutas de archivo por grupo**: para cada grupo, la lista completa de rutas de todos los archivos que comparten ese hash
3. **Espacio total recuperable**: la suma del espacio en bytes representado por las copias redundantes en todos los grupos (total de copias menos una, por grupo, multiplicado por el tamaño del archivo)

El formato, estructura y canal de entrega del reporte no están declarados — capturado como OQ-6.

---

### P3.3 — Contrato mínimo del input

El sistema no opera sobre archivos estructurados con encabezado, separador o encoding definido. Los inputs son rutas del sistema de archivos y contenido de archivo arbitrario.

| Aspecto | Estado |
|---------|--------|
| ¿El input tiene encabezado? | No aplicable — el input es un directorio del sistema de archivos, no un archivo estructurado |
| Separador | No aplicable |
| Encoding | No declarado — los archivos pueden tener cualquier encoding; el sistema los trata como bytes para hashing |
| ¿El formato del campo Fecha es estable? | No aplicable |
| ¿Cómo se representan valores vacíos o faltantes? | Archivos de cero bytes: tratamiento no declarado (ver OQ-3) |

---

### P3.4 — Contrato de salida ejecutable

No declarado (ver OQ-6). Las opciones posibles son stdout, archivo local, o ambos. La resolución de OQ-6 determina este contrato.

---

### P3.5 — Persistencia de la salida

No declarado con certeza. El reporte generado es funcionalmente un artefacto persistente reutilizable, pero si el canal de entrega es exclusivamente stdout, no existe persistencia automática entre ejecuciones. La resolución de OQ-6 determina la persistencia efectiva.

---

### P3.6 — Candidatos a Sub-BETO por Inputs (Recursividad Controlada)

**Input 1 — Ruta del directorio objetivo:**

a) ¿Está completamente especificado? **Sí** — es un string de ruta del sistema de archivos, primitivo.
b) Clasificación: **primitivo**
c) Estándar externo: no aplica
d) Candidato Sub-BETO: no generado

**Input 2 — Archivos del árbol de directorios (traversal recursivo):**

a) ¿Está completamente especificado? **No** — el comportamiento ante enlaces simbólicos (OQ-4), archivos de cero bytes (OQ-3), y errores de permisos (OQ-8) no están declarados.
b) Clasificación: **complejo con incertidumbre propia**
c) Estándar externo: no declarado
d) **Candidato Sub-BETO: Traversal de Sistema de Archivos** (Origen: Sección 3)

---

## SECCIÓN 4 — CORE UNIT OF PROCESSING

### P4.1 — Unidad atómica

La unidad mínima que procesa el sistema es una **entrada de archivo descubierto** (File Entry): un registro que representa un único archivo encontrado durante el traversal recursivo del directorio objetivo.

---

### P4.2 — Campos esenciales

Los siguientes campos son imprescindibles para que la unidad pueda procesarse:

| Campo | Propósito |
|-------|-----------|
| `file_path` | Ruta absoluta o relativa del archivo dentro del árbol de directorios escaneado |
| `content_hash` | Valor hash calculado del contenido completo del archivo; es la clave de agrupación para detección de duplicados |
| `file_size` | Tamaño del archivo en bytes; requerido para calcular el espacio recuperable por grupo |

---

### P4.3 — Campos de trazabilidad

Los siguientes campos deben preservarse en todas las fases sin modificación:

- `file_path`: debe preservarse desde el descubrimiento hasta el reporte sin alteración
- `content_hash`: debe estar vinculado al `file_path` exacto desde el cual fue calculado y no puede reasignarse

---

### P4.4 — Unicidad

El campo `file_path` identifica de forma única a cada File Entry dentro del contexto de una ejecución, dado que una ruta de archivo es unívoca dentro de un sistema de archivos local en un momento dado.

---

### P4.5 — Política de duplicados

El sistema **muestra todos** los miembros de cada grupo de duplicados. No consolida ni elimina. Cada File Entry del grupo aparece en el reporte con su ruta individual.

---

### P4.6 — Candidatos a Sub-BETO por Componentes (Recursividad Controlada)

**Campo `file_path`:**
a) ¿Es tipo primitivo? **Sí** — string de ruta del sistema de archivos.
→ No genera candidato Sub-BETO.

**Campo `content_hash`:**
a) ¿Es tipo primitivo? **No** — requiere cómputo mediante un algoritmo de hashing.
b) ¿Existe estándar externo completo? **Sí** — los algoritmos de hashing (SHA-256, BLAKE2b, etc.) son estándares externos completamente especificados.
→ No genera candidato Sub-BETO. La selección del algoritmo está capturada en OQ-1.

**Campo `file_size`:**
a) ¿Es tipo primitivo? **Sí** — entero en bytes, obtenido del sistema de archivos.
→ No genera candidato Sub-BETO.

---

## SECCIÓN 5 — GLOBAL INVARIANTS (BETO RULES)

### P5.1 — Reglas no negociables

Las siguientes reglas no pueden violarse bajo ninguna circunstancia:

1. **No invención de información**: el sistema no puede inferir, asumir ni completar datos ausentes durante la ejecución. Toda ausencia debe reportarse o gestionarse según política declarada.
2. **Ejecución no destructiva**: el sistema no puede modificar, eliminar, mover ni escribir sobre ningún archivo del sistema de archivos escaneado. La única escritura autorizada es el reporte de salida.
3. **Trazabilidad absoluta entre fases**: el `file_path` y el `content_hash` asociado a cada File Entry deben preservarse sin modificación desde la fase de descubrimiento hasta la generación del reporte.
4. **Contratos explícitos entre fases**: cada fase recibe exactamente los campos definidos en la arquitectura de fases (Sección 7) y no puede operar sobre campos no declarados.
5. **Consistencia semántica y epistémica**: toda representación aproximada debe indicarse explícitamente como tal. No se autoriza presentar resultados como exactos cuando exista incertidumbre no resuelta.
6. **Reporte completo**: el reporte debe incluir los tres elementos declarados — grupos de duplicados, rutas por grupo, y espacio total recuperable. La omisión de cualquiera de estos elementos constituye una salida inválida.

---

### P5.2 — Señalización de aproximaciones

Sí. Toda representación aproximada (por ejemplo, espacio recuperable estimado en casos de incertidumbre de tamaño) debe indicarse explícitamente como tal en el reporte.

---

### P5.3 — Invariantes de trazabilidad

Sí. El registro completo de File Entries con sus campos de trazabilidad (`file_path`, `content_hash`) debe estar disponible para consulta durante toda la ejecución del sistema, desde la fase de descubrimiento hasta la generación del reporte.

---

## SECCIÓN 6 — CONCEPTUAL MODEL

### P6.1 — Conceptos principales

| Concepto | Significado mínimo |
|----------|-------------------|
| **CLI Tool** | La herramienta ejecutable en línea de comandos que orquesta todas las fases del sistema. Punto de entrada del usuario. |
| **Target Directory** | El directorio raíz provisto por el usuario desde el cual comienza el traversal recursivo. Define el universo de archivos a analizar. |
| **File Entry** | La unidad atómica de procesamiento. Representa un único archivo descubierto durante el traversal, portando su ruta, tamaño y hash de contenido. |
| **Scanner** | Componente responsable de recorrer el árbol de directorios recursivamente y producir la colección de File Entries con path y tamaño. |
| **Hasher** | Componente responsable de computar el content_hash para cada File Entry a partir del contenido completo del archivo. |
| **Duplicate Detector** | Componente que agrupa File Entries por content_hash idéntico y retiene únicamente los grupos con más de un miembro. |
| **Duplicate Group** | Conjunto de dos o más File Entries que comparten el mismo content_hash. Representa archivos con contenido idéntico. |
| **Space Calculator** | Componente que calcula el espacio recuperable por grupo (tamaño × copias redundantes) y el total acumulado entre todos los grupos. |
| **Report Composer** | Componente que recibe los grupos de duplicados anotados y produce el artefacto de reporte final. |
| **Report** | El artefacto de salida del sistema. Contiene los grupos de duplicados, las rutas por grupo, y el espacio total recuperable. |
| **Recoverable Space** | El espacio en bytes que podría liberarse eliminando todas las copias redundantes de cada grupo (manteniendo exactamente una copia por grupo). |

---

### P6.2 — Definición de interacción

La interacción principal del sistema es la invocación CLI por parte del usuario:

- El usuario provee el directorio objetivo como argumento en la línea de comandos
- El sistema ejecuta las fases en secuencia: Discovery → Hashing → Grouping → Space Calculation → Report Generation
- El sistema emite el reporte al canal de salida declarado (no declarado aún — OQ-6)
- El sistema termina su ejecución sin efecto secundario sobre el sistema de archivos escaneado

No existe interacción iterativa ni interfaz gráfica declarada.

---

### P6.3 — Candidatos a BETO_PARALELO (Independencia Funcional)

Para cada concepto o componente identificado en P6.1:

| Componente | ¿Puede desarrollarse independientemente? | Clasificación |
|------------|------------------------------------------|---------------|
| Scanner | Sí — su propósito, input (target directory path) y output (colección de File Entries con path y tamaño) son completamente definibles sin conocer la lógica del Hasher o el Report Composer | **Candidato BETO_PARALELO: Scanner** (Origen: Sección 6) |
| Hasher | Sí — recibe File Entries con path y tamaño, emite File Entries con content_hash añadido. Su contrato es independiente del Scanner y del Duplicate Detector | **Candidato BETO_PARALELO: Hasher** (Origen: Sección 6) |
| Duplicate Detector | Sí — recibe colección de File Entries con content_hash, emite colección de Duplicate Groups. Lógica de agrupación independiente | **Candidato BETO_PARALELO: Duplicate Detector** (Origen: Sección 6) |
| Space Calculator | Sí — recibe Duplicate Groups con file_size, emite grupos anotados con recoverable_bytes y total. Lógica aritmética independiente | **Candidato BETO_PARALELO: Space Calculator** (Origen: Sección 6) |
| Report Composer | Sí — recibe grupos anotados y total, emite reporte. Su lógica de composición es independiente de cómo se calcularon los grupos | **Candidato BETO_PARALELO: Report Composer** (Origen: Sección 6) |
| CLI Tool (orquestador) | No — el CLI Tool integra todos los componentes y depende de sus contratos combinados. No es independiente. | No genera candidato BETO_PARALELO |
| File Entry | No aplicable — es una estructura de datos, no un componente funcional | No genera candidato BETO_PARALELO |
| Duplicate Group | No aplicable — es una estructura de datos | No genera candidato BETO_PARALELO |

---

### P6.4 — Candidatos a Sub-BETO por Conceptos (Recursividad Controlada)

| Concepto | ¿Definido con precisión operacional suficiente? | Clasificación | Candidato Sub-BETO |
|----------|------------------------------------------------|---------------|-------------------|
| Scanner | No — el comportamiento ante symlinks (OQ-4), permisos (OQ-8), y archivos de cero bytes (OQ-3) no están declarados | Requiere contrato interno | **Candidato Sub-BETO: Scanner / Traversal** (Origen: Sección 6) |
| Hasher | No — el algoritmo de hashing no está declarado (OQ-1) | Definible por estándar externo una vez resuelto OQ-1 | No genera Sub-BETO propio; se resuelve por resolución de OQ-1 |
| Duplicate Detector | Sí — la lógica de agrupación por hash idéntico con cardinalidad > 1 está suficientemente definida | — | No genera candidato Sub-BETO |
| Space Calculator | Sí — la fórmula (tamaño × copias_redundantes, donde copias_redundantes = total − 1) está suficientemente definida | — | No genera candidato Sub-BETO |
| Report Composer | No — formato, estructura y canal de entrega no están declarados (OQ-6) | Requiere contrato interno | **Candidato Sub-BETO: Report Composer** (Origen: Sección 6) |
| Recoverable Space | Sí — definido como bytes = file_size × (count − 1) por grupo | — | No genera candidato Sub-BETO |

---

## SECCIÓN 7 — PHASE ARCHITECTURE

### P7.1 — Fases del sistema

| Fase | Nombre | Propósito | Input | Output |
|-----:|--------|-----------|-------|--------|
| 1 | Discovery | Traversar recursivamente el directorio objetivo y producir el conjunto completo de File Entries con path y tamaño | Target directory path (argumento CLI) | Colección de File Entries (file_path, file_size) |
| 2 | Hashing | Computar el content_hash para cada File Entry a partir del contenido completo del archivo | Colección de File Entries (file_path, file_size) | Colección de File Entries (file_path, file_size, content_hash) |
| 3 | Grouping | Agrupar File Entries por content_hash; retener únicamente grupos con más de un miembro | Colección de File Entries (file_path, file_size, content_hash) | Colección de Duplicate Groups (content_hash, [file_paths], group_size) |
| 4 | Space Calculation | Computar espacio recuperable por grupo y total recuperable entre todos los grupos | Colección de Duplicate Groups | Duplicate Groups anotados con recoverable_bytes; total_recoverable_bytes |
| 5 | Report Generation | Componer y emitir el reporte final a partir de los grupos anotados | Duplicate Groups anotados; total_recoverable_bytes | Artefacto de reporte |

Esta tabla define la arquitectura de fases completa y autoritativa del sistema.

---

### P7.2 — Distribución de capacidades

No aplica en este sistema. El sistema no tiene capacidad de búsqueda interactiva separada de su capacidad de procesamiento. La única interacción es la invocación CLI que desencadena la ejecución completa del pipeline de fases. Todas las fases forman una secuencia única y continua.

---

## SECCIÓN 8 — STABLE TECHNICAL DECISIONS

### P8.1 — Decisiones técnicas confirmadas

| # | Decisión | Estado | Notas |
|---|----------|--------|-------|
| TD-1 | El sistema expone una interfaz de línea de comandos (CLI) que acepta al menos el directorio objetivo como argumento posicional | **Confirmed** | Declarado explícitamente en IDEA_RAW |
| TD-2 | La ejecución del sistema es no destructiva: nunca modifica, elimina ni mueve ningún archivo durante la ejecución | **Confirmed** | Implicado directamente por el intent scan-and-report de IDEA_RAW; elevado a invariante en Sección 5 |
| TD-3 | La detección de duplicados se basa en hash de contenido (no en nombre de archivo, fecha de modificación, ni tamaño aislado) | **Confirmed** | Declarado explícitamente en IDEA_RAW: "detects duplicate files by content hash" |
| TD-4 | El traversal del directorio objetivo es recursivo (no superficial) | **Confirmed** | Declarado explícitamente en IDEA_RAW: "scans a directory recursively" |
| TD-5 | Lenguaje o runtime de implementación | **Proposed** | No declarado en IDEA_RAW — capturado como OQ-5 |
| TD-6 | Algoritmo de hashing para content_hash | **Proposed** | No declarado en IDEA_RAW — capturado como OQ-1 |
| TD-7 | Formato y canal de entrega del reporte | **Proposed** | No declarado en IDEA_RAW — capturado como OQ-6 |

---

### P8.2 — Restricciones de entorno

- **Offline**: el sistema opera exclusivamente sobre el sistema de archivos local. No requiere conectividad de red para su función principal. Esto es una restricción operativa implícita por el scope declarado.
- **Sistema operativo**: no declarado — ningún SO específico está declarado en IDEA_RAW.
- **Regulación**: no declarado.
- **Requisitos de instalación o empaquetado**: no declarado.
- **Requisitos de rendimiento o límites de tamaño de directorio**: no declarado (ver Risk R-3 en Sección 10).

---

## SECCIÓN 9 — CURRENT SYSTEM STATE

### P9.1 — Estado de ejecución requerido

**Phase completed:** 0 (IDEA_RAW procesada y BETO_CORE_DRAFT generado)

**Phase in progress:** 1 (BETO_CORE_INTERVIEW en curso)

**Open Questions activas:**

| ID | Texto | Tipo | Crítica | Estado |
|----|-------|------|---------|--------|
| OQ-1 | ¿Qué algoritmo de hashing debe usarse para computar el content_hash de cada archivo? (ej: MD5, SHA-1, SHA-256, BLAKE2b) | OQ_CONFIG | SÍ | OPEN |
| OQ-2 | ¿Deben pre-filtrarse los archivos por tamaño antes del hashing (skip hashing para archivos con tamaño único en el árbol) para optimizar rendimiento? | OQ_POLICY | NO | OPEN |
| OQ-3 | ¿Los archivos de cero bytes deben incluirse o excluirse del proceso de detección de duplicados? | OQ_POLICY | NO | OPEN |
| OQ-4 | ¿El scanner debe seguir enlaces simbólicos durante el traversal recursivo, o ignorarlos? | OQ_POLICY | SÍ | OPEN |
| OQ-5 | ¿En qué lenguaje de programación o runtime debe implementarse la herramienta CLI? | OQ_CONFIG | SÍ | OPEN |
| OQ-6 | ¿Cuál es el formato de salida y canal de entrega requerido para el reporte? (ej: texto plano a stdout, archivo JSON, archivo CSV, archivo legible por humano). ¿El reporte debe incluir una sección de resumen separada del listado de grupos? | OQ_INTERFACE | SÍ | OPEN |
| OQ-7 | ¿Debe la herramienta soportar opciones CLI adicionales más allá del directorio objetivo? (ej: --output, --min-size, --exclude, --verbose) | OQ_INTERFACE | NO | OPEN |
| OQ-8 | ¿Cómo debe comportarse la herramienta cuando encuentra archivos que no puede leer por errores de permisos durante el traversal o el hashing? (ignorar silenciosamente, ignorar con advertencia, abortar) | OQ_EXCEPTION | SÍ | OPEN |

---

### P9.2 — Política de cierre de incertidumbre

Las incertidumbres no críticas (OQ-2, OQ-3, OQ-7) se registran como OPEN y no bloquean la generación del BETO_CORE. Se resuelven en el Paso 6 (CIERRE_ASISTIDO_OPERATIVO) o se cierran con decisión por defecto declarada explícitamente si el operador así lo autoriza.

Las incertidumbres críticas (OQ-1, OQ-4, OQ-5, OQ-6, OQ-8) deben resolverse antes de proceder al Paso 8 (generación de código). Un BETO_CORE con OQs críticas OPEN no es ejecutable.

---

## SECCIÓN 10 — RISKS AND CONSTRAINTS

### P10.1 — Riesgos conocidos

| ID | Riesgo | Descripción | OQ relacionada |
|----|--------|-------------|----------------|
| R-1 | Errores de permisos durante traversal | El directorio objetivo puede contener archivos o subdirectorios con permisos de lectura restringidos. Si no se manejan, causarán resultados de escaneo incompletos o crashes de la herramienta. | OQ-8 |
| R-2 | Colisión de hash | Todo algoritmo de hashing tiene riesgo teórico de colisión: dos archivos con contenido diferente podrían producir el mismo hash y ser agrupados incorrectamente como duplicados. La severidad depende del algoritmo seleccionado. | OQ-1 |
| R-3 | Árboles de directorios grandes | El escaneo recursivo de un árbol muy grande con cómputo de hash para cada archivo puede resultar en alto uso de memoria y tiempos de ejecución prolongados. No se declaran requisitos de rendimiento ni límites. | — |
| R-4 | Bucles por enlaces simbólicos | Si el traversal sigue enlaces simbólicos (symlinks) sin detección de ciclos, puede entrar en bucles infinitos sobre sistemas de archivos con symlinks circulares. | OQ-4 |

---

### P10.2 — Restricciones conocidas

| ID | Restricción | Tipo |
|----|-------------|------|
| C-1 | El sistema nunca puede modificar, eliminar ni mover ningún archivo | Restricción dura — invariante de ejecución no destructiva |
| C-2 | El traversal debe cubrir el árbol completo del directorio objetivo. El traversal parcial no es ejecución válida | Restricción dura — completitud del alcance |
| C-3 | El reporte debe incluir los tres elementos declarados: grupos de duplicados, rutas por grupo, y espacio total recuperable. La omisión de cualquiera constituye salida inválida | Restricción dura — completitud del output |

---

### P10.3 — Expectativa de usabilidad

El sistema debe mantenerse usable con el volumen esperado de archivos en el directorio objetivo. No se declaran límites numéricos específicos (número de archivos, tamaño máximo de árbol). El riesgo R-3 documenta la ausencia de requisitos de rendimiento.

---

### P10.4 — Estrategias de degradación permitidas

- **Filtrado por tamaño previo al hashing (OQ-2)**: estrategia de degradación de rendimiento permitida condicionalmente — su autorización depende de la resolución de OQ-2.
- **Skip de archivos inaccesibles (OQ-8)**: estrategia de degradación de completitud condicionalmente permitida — su comportamiento exacto (silencioso, con advertencia, o abort) depende de la resolución de OQ-8.
- **Agregación**: no declarada.
- **Paginación de reporte**: no declarada.

---

## SECCIÓN 11 — SUB-BETO GOVERNANCE (DECISIÓN CENTRAL)

### P11.1 — Lista consolidada de candidatos

**Candidatos a SubBETO** (complejidad propia — evaluados en P11.2):

Consolidados de P3.6, P4.6 y P6.4:

1. **Traversal de Sistema de Archivos / Scanner** (Origen: P3.6 + P6.4)
2. **Report Composer** (Origen: P6.4)

**Candidatos a BETO_PARALELO** (independencia funcional — clasificados en Paso 3 del BETO_INSTRUCTIVO):

Consolidados de P6.3:

1. Scanner (Origen: P6.3)
2. Hasher (Origen: P6.3)
3. Duplicate Detector (Origen: P6.3)
4. Space Calculator (Origen: P6.3)
5. Report Composer (Origen: P6.3)

*Nota: La clasificación formal PARALLEL vs SUBBETO ocurre en el Paso 3 del BETO_INSTRUCTIVO mediante la Regla de Clasificación Estructural. Esta sección registra y consolida candidatos.*

---

### P11.2 — Evaluación formal de terminación

---

#### C-01: Traversal de Sistema de Archivos / Scanner

**Condición 1 — No es primitivo:**
Evaluación: ✅
Razón: El traversal de sistema de archivos no es un valor atómico ni un tipo de dato simple. Implica lógica de recorrido recursivo, gestión de estados de traversal, evaluación de cada nodo del árbol, y comportamiento diferencial ante tipos de nodo especiales (directorios, archivos regulares, symlinks, archivos especiales). Su implementación requiere decisiones de diseño no triviales que van más allá de leer un valor.

**Condición 2 — Sin estándar externo completo:**
Evaluación: ✅
Razón: Aunque el concepto de traversal recursivo de directorios existe en los estándares POSIX y en las APIs de los lenguajes de programación (os.walk en Python, filepath.Walk en Go, etc.), no existe un estándar externo único que resuelva el comportamiento específico requerido por este sistema en los puntos de ambigüedad declarados: qué hacer con symlinks en este contexto, cómo tratar archivos de cero bytes, y cómo gestionar errores de permisos. El estándar externo proporciona la mecánica, pero no la política.

**Condición 3 — No implementable directo sin ambigüedad:**
Evaluación: ✅
Ambigüedades evaluadas:

| Ambigüedad identificada | Bloquea diseño estructural | Razón |
|------------------------|---------------------------|-------|
| ¿Se siguen symlinks durante el traversal? (OQ-4) | SÍ | La decisión de seguir o no symlinks cambia qué File Entries produce el Scanner como output. Si se siguen sin detección de ciclos, existe riesgo de bucle infinito (R-4). La estructura del componente Scanner varía materialmente: con symlinks requiere detección de ciclos (conjunto de inodos visitados); sin symlinks, no. Esta decisión no es decorativa sino estructural. |
| ¿Qué hacer con errores de permisos? (OQ-8) | SÍ | El comportamiento de la Fase 1 (Discovery) ante un directorio o archivo inaccesible determina si el Scanner continúa, emite advertencias al canal de salida, o aborta. Las tres opciones tienen contratos de output distintos y afectan el diseño del componente. |
| ¿Se incluyen archivos de cero bytes? (OQ-3) | NO | Esta decisión afecta el conjunto de File Entries producido pero no cambia la estructura del componente Scanner. Es un filtro aplicable como paso adicional sin alterar el diseño del traversal. |

Conclusión Condición 3: El Scanner no es implementable directamente sin ambigüedad. Dos de las tres ambigüedades identificadas (OQ-4 y OQ-8) bloquean decisiones estructurales del componente. La resolución de estas OQs es necesaria para definir el contrato de output del Scanner y la lógica interna de manejo de errores y ciclos.

**Condición 4 — Tiene OQ propia:**
Evaluación: ✅
OQ identificada: OQ-4 (comportamiento ante symlinks), OQ-8 (comportamiento ante errores de permisos), OQ-3 (inclusión de archivos de cero bytes). Estas OQs no son resolubles por el BETO_CORE raíz sin ampliar su scope declarado; requieren un espacio de cierre propio.

**DECISIÓN FINAL: APROBADO**
Razón consolidada: El Scanner / Traversal no es primitivo, no tiene estándar externo que cubra su política específica, tiene al menos dos ambigüedades que bloquean su diseño estructural (OQ-4 y OQ-8), y porta OQs propias que deben cerrarse antes de que el componente pueda implementarse. Cumple las cuatro condiciones de la Regla Canónica de Creación de Sub-BETO.

---

#### C-02: Report Composer

**Condición 1 — No es primitivo:**
Evaluación: ✅
Razón: El Report Composer no es un valor atómico. Es un componente funcional que recibe una colección estructurada de datos (grupos de duplicados anotados con espacio recuperable y total acumulado) y los transforma en un artefacto de salida con formato, estructura y canal de entrega definidos. Esta transformación implica decisiones de diseño de presentación y de contrato de interfaz con el exterior del sistema.

**Condición 2 — Sin estándar externo completo:**
Evaluación: ✅
Razón: No existe un estándar externo que dicte el formato específico, la estructura (secciones, jerarquía, campos expuestos) ni el canal de entrega del reporte de este sistema particular. Existen formatos genéricos (JSON, CSV, texto plano) pero la selección entre ellos, su estructura interna específica, y el canal de entrega (stdout vs archivo vs ambos) son decisiones no declaradas que no están cubiertas por ningún estándar externo aplicable.

**Condición 3 — No implementable directo sin ambigüedad:**
Evaluación: ✅
Ambigüedades evaluadas:

| Ambigüedad identificada | Bloquea diseño estructural | Razón |
|------------------------|---------------------------|-------|
| ¿Cuál es el formato de salida del reporte? (OQ-6 — parte 1) | SÍ | La elección entre texto plano, JSON, CSV u otro formato determina completamente la lógica de serialización del Report Composer. No es una decisión de estilo: cambia la estructura del artefacto producido y los contratos con los consumidores del reporte. |
| ¿Cuál es el canal de entrega? (OQ-6 — parte 2: stdout, archivo, o ambos) | SÍ | Si la salida es stdout, el Report Composer escribe a un stream. Si es un archivo, debe gestionar la ruta del archivo de salida, permisos de escritura, y manejo de errores de escritura. Si es ambos, la arquitectura del componente se bifurca. Estas son diferencias estructurales, no decorativas. |
| ¿El reporte debe incluir una sección de resumen separada del listado de grupos? (OQ-6 — parte 3) | NO | Esta decisión afecta el contenido del reporte pero no cambia la estructura del componente en sí. Una sección de resumen es un bloque de contenido adicional que puede añadirse sin alterar el diseño fundamental del Report Composer. |

Conclusión Condición 3: El Report Composer no es implementable directamente sin ambigüedad. Las dos primeras ambigüedades de OQ-6 (formato y canal) son decisiones estructurales que determinan la arquitectura del componente. Sin su resolución, el componente no puede diseñarse.

**Condición 4 — Tiene OQ propia:**
Evaluación: ✅
OQ identificada: OQ-6 (formato de salida y canal de entrega del reporte). Esta OQ es propia del Report Composer y no puede cerrarse sin definir el contrato completo de salida de este componente.

**DECISIÓN FINAL: APROBADO**
Razón consolidada: El Report Composer no es primitivo, no tiene estándar externo que cubra su contrato específico de formato y canal, tiene ambigüedades que bloquean su diseño estructural (formato y canal de entrega de OQ-6), y porta una OQ propia crítica. Cumple las cuatro condiciones de la Regla Canónica de Creación de Sub-BETO.

---

### P11.3 — Regla canónica de creación de Sub-BETO

Confirmado. Los Sub-BETOs se crean si y solo si:

- No es primitivo ✅
- No tiene estándar externo suficiente ✅
- No es implementable directo sin ambigüedad ✅
- Tiene al menos una Open Question propia ✅

Ambos candidatos evaluados (C-01 y C-02) cumplen las cuatro condiciones.

---

### P11.4 — Registro de Sub-BETOs aprobados

**Sub-BETO 1:**

- **Nombre:** `BETO_CORE_SCANNER`
- **Relación:** Hijo del BETO_CORE principal (BETO_CORE_DUPLICATE_FINDER o equivalente)
- **Alcance:** Cerrar las ambigüedades de comportamiento del traversal recursivo de sistema de archivos: política ante symlinks (OQ-4), política ante errores de permisos (OQ-8), y política ante archivos de cero bytes (OQ-3). No inventar comportamiento no declarado.
- **Entrada definida por el padre:** Target directory path (string de ruta del sistema de archivos, argumento CLI)
- **Salida — contrato completo reutilizable:** Colección de File Entries (file_path, file_size) — colección completa, sin modificaciones al sistema de archivos, con comportamiento ante casos de borde documentado y declarado

**Sub-BETO 2:**

- **Nombre:** `BETO_CORE_REPORT_COMPOSER`
- **Relación:** Hijo del BETO_CORE principal
- **Alcance:** Cerrar las ambigüedades de formato, estructura y canal de entrega del reporte de duplicados. Definir el contrato completo de salida del sistema: formato del artefacto, canal de emisión, estructura de contenido (secciones, campos, representación de grupos y espacio). No inventar formato no declarado.
- **Entrada definida por el padre:** Colección de Duplicate Groups anotados (content_hash, [file_paths], group_size, recoverable_bytes) + total_recoverable_bytes
- **Salida — contrato completo reutilizable:** Artefacto de reporte con formato, estructura y canal de entrega completamente especificados y declarados

---

### P11.5 — Protección contra optimización infinita

**Confirmado.**

- **Suficiencia**: Los Sub-BETOs aprobados cierran exactamente las ambigüedades que bloquean la implementación. No se expanden más allá de lo necesario para hacer el sistema implementable.
- **No perfección**: No se busca la especificación exhaustiva de todos los casos posibles, sino la resolución de los gaps que impiden el diseño estructural de cada componente.
- **Declarativo**: Toda decisión tomada en los Sub-BETOs será declarada explícitamente. Ninguna decisión puede inferirse de convenciones, buenas prácticas, o comportamiento "obvio".

---

*BETO_CORE_INTERVIEW_COMPLETED.md — Secciones 1 a 11 completadas.*
*Pendiente: SECCIÓN 12 — PASE DE CONSISTENCIA y SECCIÓN 13 — CLASIFICACIÓN DE OQs.*

# SECCIÓN 12 — PASE DE CONSISTENCIA

*(No elicita información nueva — verifica coherencia interna de las respuestas de las Secciones 1 a 11)*

---

## P12.1 — Consistencia Scope → Outputs

**Pregunta:** ¿Cada output declarado en P3.2 está justificado por al menos un elemento de P2.1 (In scope)?

**Outputs declarados en P3.2:**

| Output | Justificación en P2.1 | ¿Respaldado? |
|--------|----------------------|-------------|
| Grupos de duplicados | P2.1: "Agrupar archivos que comparten un hash de contenido idéntico" | ✅ |
| Rutas de archivo por grupo | P2.1: "Generar un reporte que contenga grupos de duplicados, rutas de archivo por grupo, y espacio recuperable total" | ✅ |
| Espacio total recuperable | P2.1: "Calcular el espacio total recuperable representado por archivos duplicados" | ✅ |
| Formato y canal de entrega del reporte | P2.1: "Generar un reporte..." — el canal y formato no están declarados en P2.1 pero están capturados como OQ-6; la ausencia es explícita y registrada, no un conflicto de scope | ✅ (ausencia documentada — no conflicto) |

**Resultado P12.1:** ✅ SIN CONFLICTO
Cada output declarado en P3.2 tiene respaldo en al menos un elemento de P2.1. La ausencia de declaración sobre formato y canal de entrega está correctamente capturada como OQ-6 y no representa una contradicción de scope.

---

## P12.2 — Consistencia Inputs → Core Unit

**Pregunta:** ¿La unidad de procesamiento declarada en P4.1 es derivable de los inputs declarados en P3.1?

**Inputs declarados en P3.1:**

| Input | Descripción |
|-------|-------------|
| Input 1 | Ruta del directorio objetivo — string CLI |
| Input 2 | Archivos del árbol de directorios alcanzados por traversal recursivo |

**Core Unit declarada en P4.1:**

> "La unidad mínima que procesa el sistema es una entrada de archivo descubierto (File Entry): un registro que representa un único archivo encontrado durante el traversal recursivo del directorio objetivo."

**Verificación de derivabilidad:**

| Relación | Análisis | ¿Consistente? |
|----------|----------|---------------|
| Input 1 (ruta del directorio) → File Entry | La ruta del directorio es el punto de entrada que origina el traversal. Sin ella no existe traversal y por tanto no existen File Entries. La relación es directa y necesaria. | ✅ |
| Input 2 (archivos del árbol por traversal) → File Entry | Cada archivo descubierto durante el traversal recursivo es exactamente la instancia que materializa un File Entry. La definición de File Entry en P4.1 es la representación directa de cada elemento de Input 2. | ✅ |
| Campos de File Entry (file_path, file_size, content_hash) → derivables de Input 2 | `file_path` y `file_size` son atributos directos de cada archivo del sistema de archivos. `content_hash` se computa a partir del contenido del archivo (Input 2). Los tres campos son derivables de los inputs declarados sin invención. | ✅ |

**Resultado P12.2:** ✅ SIN CONFLICTO
La Core Unit declarada en P4.1 es completamente derivable de los inputs declarados en P3.1. No existe brecha ni contradicción entre ambas secciones.

---

## P12.3 — Consistencia Candidates → Sección 11

**Pregunta:** ¿Todos los candidatos registrados en P3.6, P4.6 y P6.4 aparecen en la lista consolidada de P11.1?

**Candidatos registrados por sección de origen:**

| Sección de origen | Candidato registrado | Tipo declarado |
|-------------------|---------------------|----------------|
| P3.6 | Traversal de Sistema de Archivos | Sub-BETO |
| P4.6 | Ningún candidato generado (`file_path` → primitivo; `content_hash` → estándar externo vía OQ-1; `file_size` → primitivo) | — |
| P6.3 | Scanner | BETO_PARALELO |
| P6.3 | Hasher | BETO_PARALELO |
| P6.3 | Duplicate Detector | BETO_PARALELO |
| P6.3 | Space Calculator | BETO_PARALELO |
| P6.3 | Report Composer | BETO_PARALELO |
| P6.4 | Scanner / Traversal | Sub-BETO |
| P6.4 | Report Composer | Sub-BETO |

**Lista consolidada declarada en P11.1:**

| Candidato en P11.1 | Tipo | ¿Presente en origen? |
|--------------------|------|----------------------|
| Traversal de Sistema de Archivos / Scanner | Sub-BETO | ✅ (P3.6 + P6.4) |
| Report Composer | Sub-BETO | ✅ (P6.4) |
| Scanner | BETO_PARALELO | ✅ (P6.3) |
| Hasher | BETO_PARALELO | ✅ (P6.3) |
| Duplicate Detector | BETO_PARALELO | ✅ (P6.3) |
| Space Calculator | BETO_PARALELO | ✅ (P6.3) |
| Report Composer | BETO_PARALELO | ✅ (P6.3) |

**Verificación de omisiones:**

- P3.6 → "Traversal de Sistema de Archivos": presente en P11.1 como "Traversal de Sistema de Archivos / Scanner". ✅
- P4.6 → ningún candidato generado: consistente con P11.1 donde no aparece ningún candidato originado en P4.6. ✅
- P6.3 → cinco candidatos BETO_PARALELO: todos presentes en P11.1. ✅
- P6.4 → dos candidatos Sub-BETO (Scanner/Traversal y Report Composer): ambos presentes en P11.1. ✅

**Observación sobre consolidación de nombres:**
El candidato "Traversal de Sistema de Archivos" de P3.6 y el candidato "Scanner / Traversal" de P6.4 son el mismo componente referenciado con nomenclatura ligeramente diferente. P11.1 los consolida correctamente bajo el nombre unificado "Traversal de Sistema de Archivos / Scanner". No constituye omisión sino consolidación semántica correcta. El candidato "Report Composer" aparece tanto en P6.3 (como BETO_PARALELO) como en P6.4 (como Sub-BETO). Ambas instancias están presentes en P11.1 en sus categorías correspondientes. ✅

**Resultado P12.3:** ✅ SIN CONFLICTO — SIN OMISIONES
Todos los candidatos registrados en P3.6, P4.6 y P6.4 aparecen en la lista consolidada de P11.1. No se detecta ningún candidato omitido en la consolidación.

---

## P12.4 — Consistencia Phases → Outputs

**Pregunta:** ¿Cada fase declarada en P7.1 contribuye a al menos un output de P3.2?

**Fases declaradas en P7.1 y outputs de P3.2:**

| Fase | Nombre | Output de fase | Contribución a P3.2 | ¿Contribuye? |
|-----:|--------|---------------|---------------------|-------------|
| 1 | Discovery | Colección de File Entries (file_path, file_size) | Produce los File Entries que, tras ser procesados por las fases 2–5, dan origen a los grupos de duplicados y rutas del reporte (P3.2 outputs 1 y 2). Sin Discovery no existe ningún output de P3.2. | ✅ Contribución estructural necesaria |
| 2 | Hashing | Colección de File Entries con content_hash añadido | El content_hash calculado en esta fase es la clave de agrupación que hace posibles los grupos de duplicados (P3.2 output 1). Sin Hashing no existe base para la detección de duplicados. | ✅ Contribución al output 1 (grupos de duplicados) |
| 3 | Grouping | Colección de Duplicate Groups (content_hash, [file_paths], group_size) | Produce directamente los grupos de duplicados y las rutas por grupo (P3.2 outputs 1 y 2). | ✅ Contribución directa a outputs 1 y 2 |
| 4 | Space Calculation | Duplicate Groups anotados con recoverable_bytes + total_recoverable_bytes | Produce directamente el espacio total recuperable (P3.2 output 3). | ✅ Contribución directa al output 3 |
| 5 | Report Generation | Artefacto de reporte | Materializa el artefacto final que contiene los tres outputs de P3.2 (grupos de duplicados, rutas por grupo, espacio total recuperable) en el formato y canal declarados (pendiente OQ-6). | ✅ Contribución directa a los tres outputs de P3.2 |

**Fases sin output asociado:** Ninguna.

**Resultado P12.4:** ✅ SIN CONFLICTO — SIN BETO_GAPs
Cada una de las cinco fases declaradas en P7.1 contribuye a al menos un output de P3.2. Ninguna fase existe sin propósito trazable hacia un output declarado. No se identifica ninguna fase candidata a BETO_GAP.

---

## P12.5 — Consistencia Technical Decisions → Scope

**Pregunta:** ¿Cada decisión técnica de P8.1 tiene respaldo en al menos un elemento de P2.1 (In scope)?

**Decisiones técnicas declaradas en P8.1:**

| ID | Decisión | Estado | Respaldo en P2.1 | ¿Respaldada? |
|----|----------|--------|-----------------|-------------|
| TD-1 | El sistema expone una interfaz CLI que acepta el directorio objetivo como argumento posicional | Confirmed | P2.1: "Aceptar un directorio objetivo como argumento CLI" — coincidencia exacta. | ✅ |
| TD-2 | La ejecución es no destructiva: nunca modifica, elimina ni mueve ningún archivo | Confirmed | P2.2/P2.3: "Eliminación o modificación de cualquier archivo" está explícitamente fuera de scope; P5.1 lo eleva a invariante. El scope declarado en P2.1 es exclusivamente scan-and-report, lo que implica y respalda la no destructividad. | ✅ |
| TD-3 | La detección de duplicados se basa en hash de contenido (no en nombre, fecha ni tamaño aislado) | Confirmed | P2.1: "Computar un hash de contenido para cada archivo descubierto" y "Agrupar archivos que comparten un hash de contenido idéntico" — respaldo directo y explícito. | ✅ |
| TD-4 | El traversal del directorio objetivo es recursivo | Confirmed | P2.1: "Traversar el directorio objetivo recursivamente" — coincidencia exacta. | ✅ |
| TD-5 | Lenguaje o runtime de implementación | Proposed (OQ-5) | El scope de P2.1 no declara restricción de lenguaje, pero tampoco la excluye. TD-5 está en estado Proposed y pendiente de resolución de OQ-5. La ausencia de respaldo en P2.1 es consistente con su estado Proposed: no es una decisión confirmada sin respaldo, sino una decisión pendiente de declaración. No constituye conflicto. | ✅ (Proposed — ausencia de respaldo consistente con estado) |
| TD-6 | Algoritmo de hashing | Proposed (OQ-1) | P2.1 respalda la función de hashing ("Computar un hash de contenido para cada archivo descubierto") pero no especifica el algoritmo. TD-6 está en estado Proposed pendiente de OQ-1. La ausencia de especificación del algoritmo en P2.1 es consistente con su estado Proposed. No constituye conflicto. | ✅ (Proposed — ausencia de especificación consistente con estado) |
| TD-7 | Formato y canal de entrega del reporte | Proposed (OQ-6) | P2.1 respalda la generación del reporte ("Generar un reporte que contenga...") pero no especifica formato ni canal. TD-7 está en estado Proposed pendiente de OQ-6. Consistente con su estado. No constituye conflicto. | ✅ (Proposed — ausencia de especificación consistente con estado) |

**Decisiones técnicas sin respaldo en scope declarado:** Ninguna.

**Resultado P12.5:** ✅ SIN CONFLICTO — SIN BETO_GAPs
Todas las decisiones técnicas confirmadas (TD-1, TD-2, TD-3, TD-4) tienen respaldo directo en P2.1. Las decisiones propuestas (TD-5, TD-6, TD-7) están en estado Proposed precisamente porque su respaldo específico está pendiente de resolución de OQ. Esta condición es semánticamente consistente con el framework BETO: una decisión Proposed sin respaldo completo en scope es una OQ abierta, no un conflicto.

---

## CIERRE DE CONSISTENCIA

| Check | Resultado |
|-------|-----------|
| P12.1 — Scope → Outputs | ✅ Sin conflicto |
| P12.2 — Inputs → Core Unit | ✅ Sin conflicto |
| P12.3 — Candidates → Sección 11 | ✅ Sin conflicto — sin omisiones |
| P12.4 — Phases → Outputs | ✅ Sin conflicto — sin BETO_GAPs |
| P12.5 — Technical Decisions → Scope | ✅ Sin conflicto — sin BETO_GAPs |

**Conflictos detectados:** ninguno

**BETO_GAPs identificados en el pase de consistencia:** ninguno

**Estado del pase:** ✅ CONSISTENCIA VERIFICADA

**Resolución:** Conflictos = 0 → **BETO_CORE_INTERVIEW COMPLETO — proceder al Paso 1.**
# CIERRE_ASISTIDO_OPERATIVO.md

```
BETO Framework v4.3 — Operational Semantic Closure Layer
Artifact: CIERRE_ASISTIDO_OPERATIVO.md
System: Duplicate File Finder CLI
Source BETO_CORE: BETO_CORE_DUPLICATE_FINDER.md
Source graph: BETO_SYSTEM_GRAPH.md
Closure mode: CIERRE_ASISTIDO_OPERATIVO
Timestamp: 2025-01-31T00:00:00Z
```

---

## SECCIÓN 1 — SCOPE DE CIERRE

Este documento opera sobre la única unidad BETO_CORE presente:
`BETO_CORE_DUPLICATE_FINDER.md` (nodo `GRAPH.ROOT`).

El sistema NO contiene nodos PARALLEL con BETO_CORE hijos generados
al momento de este cierre. Los nodos PARALLEL declarados en
`BETO_SYSTEM_GRAPH.md` (GRAPH.SCANNER, GRAPH.HASHER,
GRAPH.DUPLICATE_DETECTOR, GRAPH.SPACE_CALCULATOR,
GRAPH.REPORT_COMPOSER) tienen `Associated BETO_CORE target:
not_generated_yet`. Por lo tanto:

```
Unidades bajo cierre operativo:   1
  - BETO_CORE_DUPLICATE_FINDER (GRAPH.ROOT)

Unidades PARALLEL pendientes de generación:   5
  - GRAPH.SCANNER
  - GRAPH.HASHER
  - GRAPH.DUPLICATE_DETECTOR
  - GRAPH.SPACE_CALCULATOR
  - GRAPH.REPORT_COMPOSER
  → Fuera del alcance de este cierre. Se registran sus
    OQs delegadas como DECLARED_RAW en el padre hasta
    que cada BETO_CORE hijo sea generado y cerrado.
```

Compatibilidad BETO_PARALELO: el cierre operativo es LOCAL
a la unidad BETO_CORE_DUPLICATE_FINDER. Una vez generados
los BETO_CORE hijos, cada uno ejecutará su propio ciclo
CIERRE_ASISTIDO_OPERATIVO independiente.

---

## SECCIÓN 2 — INVENTARIO DE OQs POR TIPO

### OQs CRÍTICAS (subject to EXECUTION_READINESS_CHECK)

```
OQ-1  oq_type: OQ_CONFIG            critical: SÍ
OQ-4  oq_type: OQ_POLICY            critical: SÍ
OQ-5  oq_type: OQ_CONFIG            critical: SÍ
OQ-6  oq_type: OQ_INTERFACE         critical: SÍ
OQ-8  oq_type: OQ_EXCEPTION         critical: SÍ
```

Nota sobre tipos críticos:
OQ-1 y OQ-5 son OQ_CONFIG con critical: SÍ.
OQ_CONFIG no figura en la lista explícita de tipos operativos
(OQ_POLICY, OQ_EXECUTION, OQ_EXCEPTION, OQ_DATA_SEMANTICS),
pero ambas tienen `execution_readiness_check: FAIL_EXECUTIONAL_GAP`
en el BETO_CORE fuente y bloquean la materialización del sistema.
Se procesan bajo el mismo protocolo EXECUTION_READINESS_CHECK
por mandato de criticidad declarada.

OQ-6 es OQ_INTERFACE con critical: SÍ y
`execution_readiness_check: FAIL_EXECUTIONAL_GAP`.
Se procesa bajo el mismo protocolo por mandato de criticidad.

### OQs NO CRÍTICAS (cierre BETO_ASSISTED)

```
OQ-2  oq_type: OQ_POLICY            critical: NO
OQ-3  oq_type: OQ_POLICY            critical: NO
OQ-7  oq_type: OQ_INTERFACE         critical: NO
```

---

## SECCIÓN 3 — EXECUTION_READINESS_CHECK POR OQ CRÍTICA

---

### ERC-OQ-1 — Hashing Algorithm

```
OQ-1: Which hashing algorithm must be used to compute the
      content hash of each file?

EXECUTION_READINESS_CHECK:

  alcance:       Computar un único hash de contenido por archivo
                 durante la Fase 2 (Hashing). Ámbito: todos los
                 archivos incluidos por Phase 1 Discovery.

  trigger:       Inicio de la Fase 2 para cada File Entry recibido
                 de la Fase 1 con file_path y file_size.

  input:         Contenido binario completo del archivo referenciado
                 por file_path.

  output:        Un valor content_hash de longitud fija y formato
                 determinístico vinculado al file_path de origen.

  constraint:    El algoritmo debe ser determinístico, producir
                 salidas de longitud fija y ser aplicable sobre
                 contenido binario arbitrario. No está declarado
                 cuál algoritmo específico usar.

  fallback:      NOT_STATED — no hay algoritmo alternativo
                 declarado si el primario falla.

  exception:     NOT_STATED — comportamiento ante error de lectura
                 de contenido no está declarado aquí (ver OQ-8).

  trazabilidad:  content_hash debe permanecer vinculado a
                 file_path sin reasignación en todas las fases
                 posteriores. DECLARED en Section 4 del
                 BETO_CORE.

DETECCIÓN DE PATRONES BLANDOS: ninguno detectado.

RESULTADO: FAIL_EXECUTIONAL_GAP
  El algoritmo específico (MD5 / SHA-1 / SHA-256 / BLAKE2b /
  otro) no está declarado. Sin esta decisión no es posible
  generar código ejecutable para la Fase 2.

→ DECLARED_RAW + BETO_GAP_EXECUTIONAL activo.

REPREGUNTA TIPADA R1-OQ1 (iteración 1 de max 2):

  TIPO: OQ_CONFIG — decisión de configuración de algoritmo

  ¿Qué algoritmo de hashing debe usar el sistema para computar
  el content_hash de cada archivo?

  Opciones comunes para referencia (no exhaustivas):
    a) SHA-256   — sin colisiones conocidas, ampliamente adoptado
    b) BLAKE2b   — rendimiento superior a SHA-256, sin colisiones
                   conocidas
    c) MD5       — rápido, colisiones conocidas, no recomendado
                   para integridad
    d) SHA-1     — obsoleto, colisiones demostradas
    e) Otro (especificar)

  ¿Debe el algoritmo ser configurable por el usuario en tiempo
  de ejecución, o es una decisión fija de implementación?

  Estado actual: PENDING — ejecución bloqueada hasta respuesta.
```

---

### ERC-OQ-4 — Symbolic Links During Traversal

```
OQ-4: Should the scanner follow symbolic links during
      recursive traversal, or skip them?

EXECUTION_READINESS_CHECK:

  alcance:       Fase 1 (Discovery) — comportamiento del traversal
                 ante cada entrada del sistema de archivos cuyo
                 tipo sea symlink.

  trigger:       Detección de un symbolic link durante el traversal
                 recursivo del directorio objetivo.

  input:         Una entrada del sistema de archivos de tipo
                 symbolic link encontrada durante el traversal.

  output:        Decisión binaria: incluir la entrada resuelta del
                 symlink en la colección de File Entries, O
                 excluir la entrada del symlink sin registrarla.

  constraint:    Seguir symlinks puede generar ciclos infinitos si
                 el symlink apunta a un ancestro del árbol (loop
                 de traversal). Este riesgo no está declarado como
                 manejado. Out of scope del BETO_CORE declara
                 explícitamente: "Resolution of symbolic links,
                 hard links, or special files unless explicitly
                 declared."

  fallback:      NOT_STATED — no hay política de fallback
                 declarada para el caso de symlink circular.

  exception:     NOT_STATED — comportamiento ante symlink
                 circular (loop de traversal) no está declarado.

  trazabilidad:  Si se sigue un symlink, el file_path registrado
                 en el File Entry debe ser el path del symlink o
                 el path resuelto — no está declarado cuál.

DETECCIÓN DE PATRONES BLANDOS: ninguno detectado.

RESULTADO: FAIL_EXECUTIONAL_GAP
  La decisión seguir/no-seguir no está declarada. Además,
  si se decide seguir, existen sub-decisiones sin declarar
  (path a registrar, manejo de loops) que también bloquean
  la implementación.

→ DECLARED_RAW + BETO_GAP_EXECUTIONAL activo.

REPREGUNTA TIPADA R1-OQ4 (iteración 1 de max 2):

  TIPO: OQ_POLICY — política de comportamiento ante entrada
        de tipo symlink

  El sistema declara explícitamente en Section 2 (Out of
  scope) que la resolución de symbolic links está fuera de
  alcance "unless explicitly declared."

  ¿Debe el scanner seguir symbolic links durante el traversal
  recursivo?

  Opciones:
    a) NO seguir — los symlinks se omiten silenciosamente.
       El file_path del symlink no se incluye en la colección.
       (Opción más segura: elimina riesgo de loops y
       duplicación por resolución de path.)
    b) SÍ seguir — el target del symlink se incluye como
       File Entry. Requiere declarar:
         i)  ¿Qué path se registra: el del symlink o el
             path resuelto?
         ii) ¿Cómo se manejan los loops circulares?

  Estado actual: PENDING — ejecución bloqueada hasta respuesta.
```

---

### ERC-OQ-5 — Programming Language / Runtime

```
OQ-5: In which programming language or runtime must the
      CLI tool be implemented?

EXECUTION_READINESS_CHECK:

  alcance:       Global — afecta la totalidad del sistema
                 (todos los nodos PARALLEL, el punto de
                 entrada CLI, el pipeline completo).

  trigger:       Inicio del Paso 8 (materialización) para
                 cualquier nodo del sistema.

  input:         N/A — es una decisión de configuración previa
                 a la generación de cualquier artefacto de código.

  output:        Declaración de lenguaje/runtime con la que se
                 generará todo el código del sistema.

  constraint:    OQ-5 debe cerrarse ANTES de que cualquier nodo
                 avance a materialización (Sección 11 de
                 BETO_SYSTEM_GRAPH: "OQ-5 es una OQ crítica del
                 BETO_CORE raíz que afecta a todos los nodos.
                 Debe cerrarse en el Paso 6 del BETO_CORE raíz
                 antes de que cualquier BETO_CORE hijo avance
                 al Paso 8."). Sin lenguaje declarado no puede
                 generarse ningún artefacto ejecutable.

  fallback:      NOT_STATED.

  exception:     NOT_STATED.

  trazabilidad:  La decisión de lenguaje genera un ID
                 BETO_DUPLICATE_FINDER.SEC8.LANG.<SLUG> que
                 debe registrarse en TRACE_REGISTRY antes del
                 Paso 6.

DETECCIÓN DE PATRONES BLANDOS: ninguno detectado.

RESULTADO: FAIL_EXECUTIONAL_GAP
  No hay lenguaje o runtime declarado. Bloquea la totalidad
  del sistema.

→ DECLARED_RAW + BETO_GAP_EXECUTIONAL activo.

REPREGUNTA TIPADA R1-OQ5 (iteración 1 de max 2):

  TIPO: OQ_CONFIG — decisión de lenguaje de implementación

  ¿En qué lenguaje de programación o runtime debe
  implementarse el CLI tool?

  Ejemplos de referencia (no exhaustivos):
    a) Python 3.x
    b) Go
    c) Rust
    d) Node.js (TypeScript o JavaScript)
    e) Java / Kotlin
    f) C / C++
    g) Otro (especificar)

  ¿Existe algún requisito adicional de versión mínima,
  compatibilidad de plataforma (Linux / macOS / Windows)
  o restricción de dependencias externas?

  Estado actual: PENDING — bloquea materialización global.
```

---

### ERC-OQ-6 — Report Output Format and Delivery Channel

```
OQ-6: What is the required output format and delivery
      channel for the report? Must the report include
      a summary section separate from the group listing?

EXECUTION_READINESS_CHECK:

  alcance:       Fase 5 (Report Generation) — comportamiento
                 completo del nodo GRAPH.REPORT_COMPOSER.
                 Incluye: formato del artefacto, canal de
                 entrega, estructura interna del reporte.

  trigger:       Inicio de la Fase 5 con input: Duplicate Groups
                 anotados con recoverable_bytes +
                 total_recoverable_bytes.

  input:         Duplicate Groups anotados (content_hash,
                 [file_paths], group_size, recoverable_bytes)
                 + escalar total_recoverable_bytes.

  output:        Artefacto de reporte. Contenido mínimo
                 obligatorio DECLARED: grupos de duplicados,
                 rutas por grupo, espacio total recuperable
                 (Section 3 y Constraint C-3 del BETO_CORE).
                 Formato y canal: NOT_STATED.

  constraint:    Constraint C-3 (DECLARED): el reporte DEBE
                 incluir los tres elementos declarados. No puede
                 omitir ninguno. El formato y canal no tienen
                 restricción declarada adicional.

  fallback:      NOT_STATED — qué hacer si el canal de entrega
                 falla (ej: no se puede escribir el archivo de
                 salida).

  exception:     NOT_STATED — comportamiento ante fallo de
                 escritura o formato inválido.

  trazabilidad:  El artefacto de reporte es el output final
                 del sistema. Su existencia está DECLARED en
                 Section 3. Su estructura interna no está
                 trazada hasta que OQ-6 se resuelva.

DETECCIÓN DE PATRONES BLANDOS:
  "human-readable" y "summary section" aparecen como
  ejemplos en la formulación de OQ-6 — requieren validación
  operativa si son parte de la respuesta del operador.

RESULTADO: FAIL_EXECUTIONAL_GAP
  Formato (plain text / JSON / CSV / otro), canal de
  entrega (stdout / archivo / ambos) y estructura
  (sección resumen separada o no) no están declarados.
  Sin estos tres sub-elementos no puede generarse la
  Fase 5.

→ DECLARED_RAW + BETO_GAP_EXECUTIONAL activo.

REPREGUNTA TIPADA R1-OQ6 (iteración 1 de max 2):

  TIPO: OQ_INTERFACE — decisión de contrato de salida
        del sistema

  El reporte debe contener obligatoriamente: grupos de
  duplicados, rutas de archivo por grupo y espacio total
  recuperable (Constraint C-3 DECLARED).

  Se requiere declaración sobre los siguientes tres
  sub-elementos:

  (A) FORMATO del artefacto de reporte:
      Opciones:
        a1) Texto plano legible por humanos (plain text)
        a2) JSON estructurado
        a3) CSV
        a4) Otro (especificar)

  (B) CANAL DE ENTREGA:
      Opciones:
        b1) Solo stdout
        b2) Solo archivo (path especificado por argumento CLI)
        b3) Stdout por defecto, archivo si se provee
            argumento --output
        b4) Otro (especificar)

  (C) ESTRUCTURA INTERNA — ¿debe el reporte incluir una
      sección de resumen separada del listado de grupos?
      Opciones:
        c1) SÍ — sección de resumen separada con
            total_recoverable_bytes y conteo de grupos/archivos
        c2) NO — solo listado de grupos sin sección de resumen
            separada
        c3) Ambas (especificar disposición)

  Estado actual: PENDING — ejecución bloqueada hasta respuesta.
```

---

### ERC-OQ-8 — Behavior on Permission Errors

```
OQ-8: How should the tool behave when it encounters files
      it cannot read due to permission errors during
      traversal or hashing (skip silently, skip with
      warning, abort)?

EXECUTION_READINESS_CHECK:

  alcance:       Fase 1 (Discovery) y Fase 2 (Hashing) —
                 los dos puntos del pipeline donde ocurre
                 acceso efectivo al sistema de archivos y
                 donde pueden surgir errores de permisos.

  trigger:
    - Traversal: intento de listar el contenido de un
      subdirectorio con permisos de lectura denegados.
    - Hashing: intento de leer el contenido de un archivo
      con permisos de lectura denegados.

  input:         Error del sistema operativo de tipo
                 "permission denied" recibido al intentar
                 acceder a una entrada del filesystem.

  output:        Una de las siguientes respuestas:
                 a) Continuar sin registrar la entrada
                    (skip silently)
                 b) Continuar registrando un aviso
                    (skip with warning)
                 c) Detener la ejecución con código de
                    error (abort)
                 — no está declarado cuál.

  constraint:    Risk R-1 (DECLARED en Section 10) reconoce
                 explícitamente que "If unhandled, this will
                 cause incomplete scan results or tool
                 crashes." El comportamiento actual es
                 NOT_STATED. Un error no manejado viola el
                 principio de ejecución no destructiva y puede
                 producir resultados de reporte incompletos sin
                 notificación al usuario.

  fallback:      NOT_STATED.

  exception:     El propio error de permisos es el evento de
                 excepción bajo análisis. El handler no está
                 declarado.

  trazabilidad:  Si se adopta "skip with warning", los archivos
                 omitidos deben ser trazables en alguna forma
                 (stderr, log, sección del reporte) — no
                 declarado.

DETECCIÓN DE PATRONES BLANDOS: ninguno detectado.

RESULTADO: FAIL_EXECUTIONAL_GAP
  El comportamiento ante errores de permisos no está
  declarado. Afecta directamente la integridad del reporte
  (Constraint C-3) y la robustez del pipeline.

→ DECLARED_RAW + BETO_GAP_EXECUTIONAL activo.

REPREGUNTA TIPADA R1-OQ8 (iteración 1 de max 2):

  TIPO: OQ_EXCEPTION — política de manejo de excepción
        de acceso al sistema de archivos

  Durante el traversal (Fase 1) o el hashing (Fase 2), el
  sistema puede encontrar entradas que no puede leer por
  permisos insuficientes.

  ¿Cuál debe ser el comportamiento del sistema en ese caso?

  Opciones:
    a) SKIP SILENTLY — omitir la entrada sin registrar
       ningún aviso. El usuario no es notificado. El reporte
       refleja solo los archivos accesibles.
    b) SKIP WITH WARNING — omitir la entrada y emitir un
       aviso (stderr o sección dedicada en el reporte).
       El usuario es informado de qué entradas fueron
       omitidas. Requiere declarar: ¿dónde se emite el
       aviso (stderr / sección del reporte / ambos)?
    c) ABORT — detener la ejecución con código de error
       distinto de cero al primer error de permisos.

  ¿La misma política aplica tanto a subdirectorios
  inaccesibles (Fase 1) como a archivos individuales
  inaccesibles (Fase 2)?

  Estado actual: PENDING — ejecución bloqueada hasta respuesta.
```

---

## SECCIÓN 4 — CIERRE BETO_ASSISTED PARA OQs NO CRÍTICAS

---

### CIERRE OQ-2 — Pre-filter by File Size Before Hashing

```
OQ-2: Should files be pre-filtered by size before hashing
      (skip hashing for files whose size is unique across
      the tree)?

critical: NO
oq_type: OQ_POLICY

ANÁLISIS BETO_ASSISTED:

  Contexto operativo: Esta optimización no afecta la
  corrección del output del sistema — archivos con tamaño
  único no pueden tener duplicados basados en contenido
  (dado que content_hash de archivos con distinto tamaño
  nunca puede colisionar). La optimización es semánticamente
  segura si se implementa correctamente: omitir el hashing
  de archivos cuyo file_size no tiene otro archivo con el
  mismo file_size en la colección.

  Impacto sobre invariantes: No viola Non-destructive
  processing. No viola Absolute traceability (los archivos
  omitidos nunca serán duplicados). No viola Report
  completeness (C-3) porque los archivos de tamaño único
  no pueden aparecer en ningún Duplicate Group.

  Riesgo de adoptar la optimización sin declararla: bajo.
  Riesgo de NO adoptarla: ninguno para la corrección;
  impacto potencial en rendimiento sobre árboles grandes
  (Risk R-3 del BETO_CORE).

CIERRE BETO_ASSISTED:

  Dado que OQ-2 es no crítica y la optimización es
  semánticamente segura y derivable del SYSTEM INTENT
  (eficiencia de procesamiento, Risk R-3), se cierra con
  la siguiente resolución por defecto:

  RESOLUCIÓN: El sistema DEBE pre-filtrar archivos por
  tamaño antes de ejecutar el hashing. Solo los archivos
  cuyo file_size está presente en más de una File Entry
  de la colección pasan a la Fase 2. Los archivos con
  file_size único se excluyen del hashing y no se incluyen
  en ningún Duplicate Group. Esta optimización es
  transparente para el output y no modifica los invariantes
  del sistema.

  Nota: si el operador prefiere deshabilitar esta
  optimización (ej: para fines de auditoría exhaustiva),
  debe declararlo explícitamente en una revisión del
  BETO_CORE.

execution_state final:  DECLARED_WITH_LIMITS
status final:           CLOSED
source:                 BETO_ASSISTED
```

---

### CIERRE OQ-3 — Zero-byte Files

```
OQ-3: Should zero-byte files be included in the duplicate
      detection process or excluded?

critical: NO
oq_type: OQ_POLICY

ANÁLISIS BETO_ASSISTED:

  Contexto operativo: Todos los archivos de cero bytes
  comparten el mismo content_hash (hash de contenido vacío),
  independientemente del algoritmo seleccionado. Si se
  incluyen, todos los archivos de cero bytes del árbol
  formarán un único Duplicate Group. Esto puede producir
  un reporte con un grupo de "duplicados" compuesto
  exclusivamente por archivos vacíos, lo que puede ser
  ruido semánticamente inútil para el usuario.

  Impacto sobre invariantes: incluirlos no viola ningún
  invariante técnico. Excluirlos tampoco. La decisión
  es semánticamente ambigua solo si el operador tiene un
  caso de uso explícito para archivos de cero bytes.

  Derivabilidad del SYSTEM INTENT: el SYSTEM INTENT
  declara "identifies duplicate files by comparing their
  content hashes." Un archivo de cero bytes es un archivo
  válido con un content_hash válido. No hay base declarada
  para excluirlos automáticamente.

CIERRE BETO_ASSISTED:

  Dado que OQ-3 es no crítica y la inclusión es coherente
  con el SYSTEM INTENT, se cierra con la siguiente
  resolución por defecto:

  RESOLUCIÓN: Los archivos de cero bytes SE INCLUYEN en
  el proceso de detección de duplicados. Si existen dos
  o más archivos de cero bytes en el árbol, forman un
  Duplicate Group válido. El recoverable_bytes de ese
  grupo es 0 (tamaño × (count − 1) = 0 × n = 0), lo que
  es matemáticamente correcto y no distorsiona el cálculo
  de total_recoverable_bytes.

  Nota: si el operador desea excluir archivos de cero bytes
  (ej: para reducir ruido en el reporte), debe declararlo
  explícitamente.

execution_state final:  DECLARED_WITH_LIMITS
status final:           CLOSED
source:                 BETO_ASSISTED
```

---

### CIERRE OQ-7 — Additional CLI Options

```
OQ-7: Should the tool support additional CLI options beyond
      the target directory path?

critical: NO
oq_type: OQ_INTERFACE

ANÁLISIS BETO_ASSISTED:

  Contexto operativo: IDEA_RAW declara explícitamente un
  único argumento CLI: el target directory path. No se
  declaran opciones adicionales. El BETO_CORE Section 2
  (In scope) confirma: "Accept a target directory as input
  from the command line." La invariante de Iniciativa
  Controlada prohíbe agregar capacidades no declaradas.

  Impacto: agregar opciones no declaradas (--output,
  --min-size, --exclude, --verbose) constituiría expansión
  no autorizada del sistema. La resolución de OQ-6 puede
  justificar --output si el canal de entrega así lo
  requiere, pero eso es una consecuencia de OQ-6, no de
  OQ-7 independientemente.

CIERRE BETO_ASSISTED:

  RESOLUCIÓN: El sistema implementa ÚNICAMENTE el argumento
  obligatorio de directorio objetivo, como está DECLARED.
  No se agregan opciones CLI adicionales en esta versión
  del BETO_CORE. Si la resolución de OQ-6 requiere un
  argumento --output, dicho argumento se declara como
  consecuencia directa de OQ-6 en el BETO_CORE_REPORT_COMPOSER
  correspondiente, no como extensión independiente de OQ-7.

  Cualquier opción CLI adicional requiere declaración
  explícita del operador y actualización del BETO_CORE
  antes de ser implementada.

execution_state final:  DECLARED_WITH_LIMITS
status final:           CLOSED
source:                 BETO_ASSISTED
```

---

## SECCIÓN 5 — EXECUTION SUMMARY

```
┌──────┬───────────────────────────────┬──────────────────────┬──────────────────────────────┬─────────────────────────────┐
│ OQ   │ Texto breve                   │ Tipo                 │ Estado final                 │ Gate                        │
├──────┼───────────────────────────────┼──────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ OQ-1 │ Hashing algorithm             │ OQ_CONFIG (crítica)  │ DECLARED_RAW                 │ BETO_GAP_EXECUTIONAL activo │
│      │                               │                      │ FAIL_EXECUTIONAL_GAP         │                             │
├──────┼───────────────────────────────┼──────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ OQ-2 │ Pre-filter by size            │ OQ_POLICY (no crit.) │ DECLARED_WITH_LIMITS         │ CLOSED BETO_ASSISTED        │
├──────┼───────────────────────────────┼──────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ OQ-3 │ Zero-byte files               │ OQ_POLICY (no crit.) │ DECLARED_WITH_LIMITS         │ CLOSED BETO_ASSISTED        │
├──────┼───────────────────────────────┼──────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ OQ-4 │ Symbolic links                │ OQ_POLICY (crítica)  │ DECLARED_RAW                 │ BETO_GAP_EXECUTIONAL activo │
│      │                               │                      │ FAIL_EXECUTIONAL_GAP         │                             │
├──────┼───────────────────────────────┼──────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ OQ-5 │ Programming language/runtime  │ OQ_CONFIG (crítica)  │ DECLARED_RAW                 │ BETO_GAP_EXECUTIONAL activo │
│      │                               │                      │ FAIL_EXECUTIONAL_GAP         │                             │
├──────┼───────────────────────────────┼──────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ OQ-6 │ Report format and channel     │ OQ_INTERFACE (crit.) │ DECLARED_RAW                 │ BETO_GAP_EXECUTIONAL activo │
│      │                               │                      │ FAIL_EXECUTIONAL_GAP         │                             │
├──────┼───────────────────────────────┼──────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ OQ-7 │ Additional CLI options        │ OQ_INTERFACE (no c.) │ DECLARED_WITH_LIMITS         │ CLOSED BETO_ASSISTED        │
├──────┼───────────────────────────────┼──────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ OQ-8 │ Permission error behavior     │ OQ_EXCEPTION (crit.) │ DECLARED_RAW                 │ BETO_GAP_EXECUTIONAL activo │
│      │                               │                      │ FAIL_EXECUTIONAL_GAP         │                             │
└──────┴───────────────────────────────┴──────────────────────┴──────────────────────────────┴─────────────────────────────┘

OQs en DECLARED_RAW:         5  (OQ-1, OQ-4, OQ-5, OQ-6, OQ-8)
OQs en DECLARED_WITH_LIMITS: 3  (OQ-2, OQ-3, OQ-7)
OQs en DECLARED_EXECUTABLE:  0
BETO_GAP_EXECUTIONAL activos: 5
```

---

## SECCIÓN 6 — GATE G-2B — OPERATIONAL READINESS GATE

```
UNIDAD EVALUADA: BETO_CORE_DUPLICATE_FINDER (GRAPH.ROOT)
TIPO DE EVALUACIÓN: LOCAL (compatible BETO_PARALELO)

RESULTADO: BLOCKED_BY_EXECUTIONAL_GAPS

────────────────────────────────────────────────────────────
GAPS BLOQUEANTES ACTIVOS:

  BETO_GAP_EXECUTIONAL-1  OQ-1  Hashing algorithm
    Impacto: bloquea Fase 2 (Hashing) y nodo GRAPH.HASHER.
    Repregunta emitida: R1-OQ1 (iteración 1/2).
    Acción requerida: respuesta del operador.

  BETO_GAP_EXECUTIONAL-2  OQ-4  Symbolic links policy
    Impacto: bloquea Fase 1 (Discovery) y nodo GRAPH.SCANNER.
    Repregunta emitida: R1-OQ4 (iteración 1/2).
    Acción requerida: respuesta del operador.

  BETO_GAP_EXECUTIONAL-3  OQ-5  Programming language/runtime
    Impacto: bloquea la totalidad del sistema (todos los nodos).
    Repregunta emitida: R1-OQ5 (iteración 1/2).
    Acción requerida: respuesta del operador.
    PRIORIDAD MÁXIMA — bloqueo global.

  BETO_GAP_EXECUTIONAL-4  OQ-6  Report format and channel
    Impacto: bloquea Fase 5 (Report Generation) y nodo
    GRAPH.REPORT_COMPOSER. Gate G-2B OSC del Report Composer
    permanece bloqueado.
    Repregunta emitida: R1-OQ6 (iteración 1/2).
    Acción requerida: respuesta del operador.

  BETO_GAP_EXECUTIONAL-5  OQ-8  Permission error behavior
    Impacto: bloquea Fases 1 y 2 (Discovery y Hashing),
    afecta integridad de Report (Constraint C-3).
    Repregunta emitida: R1-OQ8 (iteración 1/2).
    Acción requerida: respuesta del operador.

────────────────────────────────────────────────────────────
ESTADO DE TODOS LOS CHECKS DE GATE:

  Hashing algorithm declared:          FAIL
  Symlink policy declared:             FAIL
  Language/runtime declared:           FAIL
  Report format and channel declared:  FAIL
  Permission error policy declared:    FAIL
  Non-critical OQs closed:             PASS (OQ-2, OQ-3, OQ-7)
  Topology validated:                  PASS (BETO_SYSTEM_GRAPH
                                        Sección 14 — VALIDATED)
  BETO_CORE invariants intact:         PASS

────────────────────────────────────────────────────────────
CONDICIÓN DE DESBLOQUEO:

  El Gate G-2B cambia a APPROVED_WITH_LIMITS o
  APPROVED_EXECUTABLE cuando el operador responde a las
  repreguntas R1-OQ1, R1-OQ4, R1-OQ5, R1-OQ6 y R1-OQ8
  con declaraciones ejecutables (sin patrones blandos
  no resueltos), y el BETO_CORE es actualizado con
  execution_state = DECLARED_EXECUTABLE para cada OQ.

  Si tras la segunda repregunta (iteración 2/2) alguna
  OQ permanece en FAIL_EXECUTIONAL_GAP, se registra como
  DECLARED_RAW permanente y se escala al operador para
  decisión de continuación parcial o suspensión.

────────────────────────────────────────────────────────────
NOTA DE COMPATIBILIDAD BETO_PARALELO:

  Este bloqueo es LOCAL a BETO_CORE_DUPLICATE_FINDER
  (GRAPH.ROOT). Los BETO_CORE hijos aún no generados
  (GRAPH.SCANNER, GRAPH.HASHER, GRAPH.DUPLICATE_DETECTOR,
  GRAPH.SPACE_CALCULATOR, GRAPH.REPORT_COMPOSER) ejecutarán
  sus propios gates G-2B independientes cuando sean
  generados. El bloqueo del ROOT no impide la generación
  de los BETO_CORE hijos, pero sí bloquea el avance de
  cualquier nodo a materialización (Paso 8) hasta que
  OQ-5 sea resuelta, dado su impacto global declarado.
```

---

## SECCIÓN 7 — ACTUALIZACIÓN DE ESTADOS EN BETO_CORE

Los siguientes campos del BETO_CORE_DUPLICATE_FINDER.md
deben actualizarse como resultado de este cierre:

```
OQ-1:
  execution_state: DECLARED_RAW
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP
  (sin cambio — gap activo, repregunta emitida)

OQ-2:
  execution_state: DECLARED_WITH_LIMITS
  status: CLOSED
  resolution: El sistema pre-filtra archivos por tamaño antes
              de hashing. Solo archivos con file_size presente
              en más de una File Entry avanzan a Fase 2.
  source: BETO_ASSISTED
  execution_readiness_check: PASS_WITH_LIMITS

OQ-3:
  execution_state: DECLARED_WITH_LIMITS
  status: CLOSED
  resolution: Los archivos de cero bytes se incluyen en el
              proceso de detección. Su recoverable_bytes es 0.
  source: BETO_ASSISTED
  execution_readiness_check: PASS_WITH_LIMITS

OQ-4:
  execution_state: DECLARED_RAW
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP
  (sin cambio — gap activo, repregunta emitida)

OQ-5:
  execution_state: DECLARED_RAW
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP
  (sin cambio — gap activo, repregunta emitida)

OQ-6:
  execution_state: DECLARED_RAW
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP
  (sin cambio — gap activo, repregunta emitida)

OQ-7:
  execution_state: DECLARED_WITH_LIMITS
  status: CLOSED
  resolution: Solo el argumento de directorio objetivo es
              implementado. Ninguna opción CLI adicional se
              agrega sin declaración explícita del operador.
  source: BETO_ASSISTED
  execution_readiness_check: PASS_WITH_LIMITS

OQ-8:
  execution_state: DECLARED_RAW
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP
  (sin cambio — gap activo, repregunta emitida)

Phase completed:   1 (Cierre Asistido Operativo ejecutado)
Phase in progress: BLOCKED — Gate G-2B en estado
                   BLOCKED_BY_EXECUTIONAL_GAPS
```

Nota sobre SUCCESS_CLOSED:
El BETO_CORE_DUPLICATE_FINDER no puede actualizarse a
SUCCESS_CLOSED en este ciclo porque existen 5 OQs críticas
en DECLARED_RAW con BETO_GAP_EXECUTIONAL activos. El estado
SUCCESS_CLOSED se emitirá cuando Gate G-2B alcance
APPROVED_EXECUTABLE o APPROVED_WITH_LIMITS tras la
resolución de las OQs bloqueantes.

---

## SECCIÓN 8 — REPREGUNTAS PENDIENTES AL OPERADOR

Las siguientes repreguntas requieren respuesta del operador
para continuar la materialización del sistema.

**PRIORIDAD MÁXIMA (bloqueo global):**

```
R1-OQ5: ¿En qué lenguaje de programación o runtime debe
        implementarse el CLI tool? ¿Existe algún requisito
        de versión mínima, compatibilidad de plataforma o
        restricción de dependencias externas?
```

**BLOQUEO DE PIPELINE (requeridas para desblocar fases):**

```
R1-OQ1: ¿Qué algoritmo de hashing debe usar el sistema?
        ¿Debe ser configurable por el usuario o es una
        decisión fija de implementación?

R1-OQ4: ¿Debe el scanner seguir symbolic links?
        Si SÍ: ¿qué path se registra y cómo se manejan
        los loops circulares?

R1-OQ6: (A) ¿Qué formato debe tener el reporte?
        (B) ¿Cuál es el canal de entrega?
        (C) ¿Debe incluir sección de resumen separada?

R1-OQ8: ¿Qué debe hacer el sistema ante errores de
        permisos: skip silently / skip with warning /
        abort? ¿La misma política aplica a subdirectorios
        y a archivos individuales?
```

Todas las repreguntas están en iteración 1 de máximo 2.
Si el operador no responde con especificación ejecutable
tras la iteración 2, las OQs se registran como
DECLARED_RAW permanente y el gap se escala.

---

*Fin del documento CIERRE_ASISTIDO_OPERATIVO.md*
*Gate G-2B: BLOCKED_BY_EXECUTIONAL_GAPS*
*Siguiente acción: respuesta del operador a repreguntas*
*R1-OQ5 (prioridad máxima), R1-OQ1, R1-OQ4, R1-OQ6, R1-OQ8*
```
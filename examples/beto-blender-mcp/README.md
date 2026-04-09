# BETO × Blender MCP — Epistemic Governance over a 3D Pipeline Addon

> **"blenderface-mcp is not a Blender addon that happens to have comments. It is a formally declared system where every class, method, and constant traces back to an operator decision."**

---

## What This Is

**[beto-blender-mcp](https://github.com/aramirez-maza/beto-blender-mcp)** is a Blender 5.1 MCP (Model Context Protocol) addon built for the **blenderface pipeline** — a system that reconstructs a 3D FLAME head mesh from a frontal face photo and generates anatomically-correct 3D hair on it.

The addon was **fully specified and materialized using BETO v4.5** — from a raw idea to a running, tested, published Blender extension — in a single uninterrupted BETO cycle.

**This is a canonical BETO Skill example:** it shows BETO operating not on a simple script, but on a real integration system with threading constraints, a binary framing protocol, Blender's plugin API, and a multi-module pipeline migration.

---

## The Problem It Solved

The pipeline was using **[ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp)** as its Blender connection layer. During a BETO analysis, the following issues were formally identified:

| Problem | Root Cause | BETO Declaration |
|---------|-----------|------------------|
| Incompatible with Blender 5.1 | `bl_info` deprecated since 4.2 | `SEC8.TECH.BLENDER_VERSION` |
| Broken for large payloads | `recv(8192)` with no message framing | `SEC8.TECH.TCP_FRAMING` |
| Unsafe threading | `bpy` accessed from secondary threads | `SEC8.TECH.CONCURRENCY_MODEL` [OPERATOR] |
| Unmaintainable | 2,635-line god-class | `SEC8.TECH.MODULAR_ARCH` |
| API key in source | `RODIN_FREE_TRIAL_KEY = "k9Tc..."` | `SEC8.TECH.NO_EXTERNAL_APIS` |
| No pipeline-specific tools | No FLAME mesh, no Hair Curves, no materials | `SEC3.HANDLER.*` |

The operator declared each constraint explicitly. BETO did not infer any of them.

---

## The BETO Cycle

**Full BETO v4.5 protocol — 11 steps, 3 human gates.**

```
Step 0   Eligibility: GO
Step 1   BETO_CORE_DRAFT — 54 elements declared
         5 OQs resolved [BETO_ASSISTED]
── G-1 ─ Operator: approved + declared concurrency model (threading constraints) [OPERATOR]
Step 2   Structural Interview — 7 PARALLEL candidates, 0 conflicts
Step 3   Classification — 7 PARALLEL nodes, 0 Sub-BETOs
Step 4   System Graph — 8 nodes, 13 edges, 10/10 topology validations PASS
── G-2 ─ Operator: approved + refined TCP_SERVER_CORE execution constraints [OPERATOR]
Step 5   7 child BETO_COREs (one per PARALLEL node)
Step 6   OSC: APPROVED_EXECUTABLE — 0 critical OQs remain open
Step 6B  Product Fit: FIT_APPROVED — 5/5 criteria PASS
Step 7   Phase documents — 8 nodes × declared phases
Step 8   TRACE_REGISTRY — 48 authorized IDs
── G-3 ─ Operator: approved → materialization begins
Step 10  9 files, 69 BETO-TRACE annotations, TRACE_VERIFIED
```

**Traceability stats:**

```
DECLARED [BETO_ASSISTED]:  5 OQ resolutions
DECLARED [OPERATOR]:       2 direct declarations (concurrency model, TCP_SERVER_CORE constraints)
BETO_GAPs:                 0
OQs open at G-3:           0
Product Fit:               FIT_APPROVED (5/5)
OSC:                       APPROVED_EXECUTABLE
BETO-TRACE annotations:    69
Authorized TRACE IDs:      48
Silent completions:        0
```

---

## The Operator-Declared Concurrency Model

This is the most technically significant declaration in this cycle. The operator declared the threading architecture explicitly before G-1, leaving zero ambiguity for the implementation:

> *"El servidor TCP debe ejecutarse fuera del hilo principal de Blender, en un thread dedicado exclusivo para networking. Ninguna operación bpy puede ejecutarse desde threads secundarios. Toda solicitud recibida por socket debe convertirse en un job y encolarse en una queue thread-safe. La ejecución real de handlers que usan bpy debe ocurrir exclusivamente en el hilo principal de Blender, mediante un dispatcher controlado con bpy.app.timers.register()."*

Registered as `SEC8.TECH.CONCURRENCY_MODEL [DECLARED [OPERATOR]]`. Materialized in `server.py`:

```python
# BETO-TRACE: BFMCP.SEC8.TECH.CONCURRENCY_MODEL
# BETO-TRACE: BFMCP.SEC8.TECH.ANTI_PATTERNS

def _net_loop(self) -> None:
    """Dedicated networking thread. Never touches bpy."""
    ...

def _dispatcher_tick(self) -> Optional[float]:
    """Runs exclusively in Blender main thread."""
    ...
```

---

## The BETO-TRACE Pattern

Every element in the generated code carries a `BETO-TRACE` annotation:

```python
# BETO-TRACE: TCPSRV.SEC8.TECH.FRAMING_STRUCT_PACK
@staticmethod
def _send_framed(sock: socket.socket, data: bytes) -> None:
    """Send bytes with 4-byte big-endian length prefix."""
    sock.sendall(struct.pack(">I", len(data)) + data)
```

```python
# BETO-TRACE: HHAIR.SEC8.TECH.VERTEX_READ_FROM_BLENDER
# Reads vertex positions and normals directly from the Blender mesh.
# droop_factor = hair_length * 0.15 (declared in BETO_CORE_HANDLERS_HAIR SEC5)
```

Format: `BETO_<SYSTEM>.SEC<N>.<TYPE>.<ELEMENT>`

Every ID in the code exists in the `TRACE_REGISTRY`. No code element without a declared ID. No declared ID without a code element.

---

## System Graph

```
ROOT: blenderface-mcp addon
│
├─[FUNCTIONAL_BRANCH]─ TCP_SERVER_CORE          (net thread + queue + dispatcher)
├─[FUNCTIONAL_BRANCH]─ HANDLERS_SCENE           (get_scene_info, screenshot, execute_code)
├─[FUNCTIONAL_BRANCH]─ HANDLERS_FLAME           (import_flame_mesh, get_object_info)
├─[FUNCTIONAL_BRANCH]─ HANDLERS_HAIR            (create_hair_curves, particle_hair)
├─[FUNCTIONAL_BRANCH]─ HANDLERS_MATERIAL        (assign_material, set_color)
├─[FUNCTIONAL_BRANCH]─ BLENDER_UI_PANEL         (View3D N-panel)
└─[FUNCTIONAL_BRANCH]─ PIPELINE_MIGRATION       (framing migration in client modules)

8 nodes · 13 edges · 0 Sub-BETOs · 10/10 topology validations PASS
```

---

## Repository

**→ [github.com/aramirez-maza/beto-blender-mcp](https://github.com/aramirez-maza/beto-blender-mcp)**

Includes:
- Full addon source with `blender_manifest.toml`
- 13 domain handlers across 4 modules
- Migrated pipeline clients (`blender_materializer`, `blender_hair_materializer`)
- Complete installation instructions for Blender 5.1 + WSL2/Windows setup
- 69 BETO-TRACE annotations throughout

---

## What Makes This a Good BETO Example

1. **Real complexity** — not a toy script. A Blender addon with threading, binary protocols, platform-specific networking (WSL2/Windows), and Blender's plugin API.

2. **Operator-declared constraints that changed the implementation** — the concurrency model declared at G-1 eliminated an entire class of possible implementations (asyncio, thread-per-handler, direct bpy from threads).

3. **BETO_ASSISTED resolutions that saved gates** — 5 OQs resolved automatically without operator interruption, while flagging the ones that truly needed human judgment.

4. **Protocol migration as a PARALLEL node** — the pipeline client migration was modeled as an independent PARALLEL node (`PIPELINE_MIGRATION`), not as an afterthought, resulting in a clean separate phase.

5. **Zero gaps, zero open OQs at G-3** — the system was fully executable before a single line of code was written.

---

*Generated with BETO v4.5 + Claude Code (claude-sonnet-4-6) · April 2026*

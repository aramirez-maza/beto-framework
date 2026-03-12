"""
Prueba unitaria rápida del TraceInjector.
No requiere LLM ni API — verifica la inyección mecánica con datos sintéticos.

Ejecutar:
    python3 test_injector.py
"""

from motor_codigo.trace_injector import TraceInjector

# — Scaffold típico que genera Claude —
SCAFFOLD = '''"""
BETO-TRACE: BETO_GESTOR.SEC1.INTENT.CICLO_LIFECYCLE
BETO-TRACE: BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_DETECTION
"""

from pathlib import Path


class DuplicateDetector:
    """
    BETO-TRACE: BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_DETECTION
    BETO-TRACE: BETO_GESTOR.SEC4.UNIT.DUPLICATE_DETECTOR
    """

    def __init__(self, cycles_dir: Path):
        """
        BETO-TRACE: BETO_GESTOR.SEC3.INPUT.CYCLES_DIR
        """
        pass  # IMPLEMENT: store cycles_dir

    def detectar(self, idea_raw: str) -> dict:
        """
        BETO-TRACE: BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_DETECTION
        """
        pass  # IMPLEMENT: compute SHA-256, check existing cycles
'''

# — Código que genera qwen-coder (sin BETO-TRACE) —
CODIGO_SIN_TRACES = '''import hashlib
import json
from pathlib import Path


class DuplicateDetector:

    def __init__(self, cycles_dir: Path):
        self.cycles_dir = cycles_dir

    def detectar(self, idea_raw: str) -> dict:
        hash_idea = hashlib.sha256(idea_raw.encode()).hexdigest()
        for ciclo_dir in self.cycles_dir.iterdir():
            meta_path = ciclo_dir / "meta.json"
            if meta_path.exists():
                meta = json.loads(meta_path.read_text())
                if meta.get("idea_hash") == hash_idea:
                    return {"duplicate": meta}
        return {"duplicate": None}
'''

# — Scaffold con markdown fences (caso Claude desobediente) —
SCAFFOLD_CON_FENCES = f"```python\n{SCAFFOLD}\n```"


def test_inyeccion_basica():
    injector = TraceInjector()
    resultado = injector.inject(SCAFFOLD, CODIGO_SIN_TRACES)

    assert "BETO-TRACE:" in resultado, "FALLO: no se inyectaron BETO-TRACE"
    assert "BETO_GESTOR.SEC1.INTENT.CICLO_LIFECYCLE" in resultado, "FALLO: ID de módulo no inyectado"
    assert "BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_DETECTION" in resultado, "FALLO: ID de clase/método no inyectado"
    assert "BETO_GESTOR.SEC4.UNIT.DUPLICATE_DETECTOR" in resultado, "FALLO: ID de clase no inyectado"
    assert "BETO_GESTOR.SEC3.INPUT.CYCLES_DIR" in resultado, "FALLO: ID de __init__ no inyectado"
    assert "hashlib" in resultado, "FALLO: implementación de qwen-coder fue destruida"
    assert "sha256" in resultado, "FALLO: lógica de negocio fue destruida"

    print("OK test_inyeccion_basica")
    return resultado


def test_strip_code_fences():
    injector = TraceInjector()
    resultado = injector.inject(SCAFFOLD_CON_FENCES, CODIGO_SIN_TRACES)

    assert "BETO-TRACE:" in resultado, "FALLO: fences no eliminados del scaffold"
    print("OK test_strip_code_fences")


def test_codigo_ya_tiene_docstring():
    codigo_con_docstring = '''from pathlib import Path


class DuplicateDetector:
    """Detecta ciclos duplicados."""

    def __init__(self, cycles_dir: Path):
        """Inicializa el detector."""
        self.cycles_dir = cycles_dir

    def detectar(self, idea_raw: str) -> dict:
        """Busca duplicados por hash."""
        return {"duplicate": None}
'''
    injector = TraceInjector()
    resultado = injector.inject(SCAFFOLD, codigo_con_docstring)

    assert "BETO-TRACE:" in resultado, "FALLO: no se inyectó en docstring existente"
    assert "Detecta ciclos duplicados" in resultado, "FALLO: docstring existente fue destruido"
    print("OK test_codigo_ya_tiene_docstring")


if __name__ == "__main__":
    print("=" * 50)
    print("Test TraceInjector")
    print("=" * 50)

    resultado = test_inyeccion_basica()
    test_strip_code_fences()
    test_codigo_ya_tiene_docstring()

    print()
    print("=" * 50)
    print("TODOS LOS TESTS PASARON")
    print("=" * 50)
    print()
    print("— Resultado de inyección básica —")
    print(resultado)

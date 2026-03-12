"""
BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION
BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED
"""

import ast
import re
from typing import Optional

BETO_TRACE_PATTERN = re.compile(r"BETO-TRACE:\s*([A-Z][A-Z0-9_]*\.SEC\d+\.\w+\.\w+)")


def _strip_code_fences(text: str) -> str:
    """Elimina markdown code fences. Robusto ante texto explicativo posterior al bloque."""
    text = text.strip()
    if not text.startswith("```"):
        return text
    first_newline = text.index("\n") if "\n" in text else len(text)
    content_start = first_newline + 1
    close_pos = text.find("\n```", content_start)
    if close_pos != -1:
        return text[content_start:close_pos].strip()
    return text[content_start:].strip()


class TraceInjector:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION

    Inyecta determinísticamente las anotaciones BETO-TRACE del scaffold
    en el código final generado por el motor de código.

    No depende del LLM para preservar las anotaciones — las inserta
    por matching de nombre de clase/función via AST.
    """

    def inject(self, scaffold: str, codigo_final: str) -> str:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED

        Inyecta BETO-TRACE del scaffold en codigo_final.
        Primero intenta inyección AST por símbolo; luego safety net para
        IDs que no quedaron capturados (comentarios, SyntaxError, etc.).
        Retorna el código con las anotaciones correctamente inyectadas.
        """
        all_scaffold_ids = set(BETO_TRACE_PATTERN.findall(scaffold))

        # Fast path: si todos los IDs del scaffold ya están en el código, no inyectar
        all_codigo_ids = set(BETO_TRACE_PATTERN.findall(codigo_final))
        if all_scaffold_ids <= all_codigo_ids:
            return codigo_final

        # Paso 1: inyección AST por símbolo
        trace_map = self._build_trace_map(scaffold)
        resultado = self._apply_trace_map(codigo_final, trace_map) if trace_map else codigo_final

        # Paso 2: safety net — inyectar IDs del scaffold que no llegaron al resultado
        all_resultado_ids = set(BETO_TRACE_PATTERN.findall(resultado))
        missing_ids = sorted(all_scaffold_ids - all_resultado_ids)

        if missing_ids:
            resultado = self._inject_module(resultado.split("\n"), missing_ids)
            resultado = "\n".join(resultado) if isinstance(resultado, list) else resultado

        return resultado

    # — Construcción del mapa de trazas —

    def _build_trace_map(self, scaffold: str) -> dict:
        """
        Parsea el scaffold con AST y construye mapa symbol_key → [trace_ids].

        Keys:
          "__module__"         → IDs del docstring de módulo
          "ClassName"          → IDs del docstring de clase
          "ClassName.method"   → IDs del docstring de método
          "function_name"      → IDs del docstring de función de módulo
        """
        trace_map = {}
        # Limpiar markdown code fences si el LLM los incluyó
        scaffold_clean = _strip_code_fences(scaffold)
        try:
            tree = ast.parse(scaffold_clean)
        except SyntaxError:
            print(f"  [TraceInjector] WARN: scaffold con SyntaxError — trace_map vacío")
            print(f"  [TraceInjector] Primeras 200 chars: {scaffold_clean[:200]!r}")
            return {}

        # Módulo
        module_doc = ast.get_docstring(tree)
        if module_doc:
            ids = BETO_TRACE_PATTERN.findall(module_doc)
            if ids:
                trace_map["__module__"] = ids

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                doc = ast.get_docstring(node)
                if doc:
                    ids = BETO_TRACE_PATTERN.findall(doc)
                    if ids:
                        trace_map[node.name] = ids

                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        doc = ast.get_docstring(child)
                        if doc:
                            ids = BETO_TRACE_PATTERN.findall(doc)
                            if ids:
                                trace_map[f"{node.name}.{child.name}"] = ids

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                doc = ast.get_docstring(node)
                if doc:
                    ids = BETO_TRACE_PATTERN.findall(doc)
                    if ids:
                        trace_map[node.name] = ids

        return trace_map

    # — Aplicación del mapa al código final —

    def _apply_trace_map(self, code: str, trace_map: dict) -> str:
        """
        Aplica el trace_map al código final usando AST para ubicar
        líneas de inserción y manipulación de texto para inyectar.
        Las inserciones se hacen de abajo hacia arriba para preservar índices.
        """
        code = _strip_code_fences(code)
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code

        # Recopilar puntos de inyección: (lineno_1indexed, key, col_offset)
        injection_points = []

        # Módulo
        if "__module__" in trace_map:
            injection_points.append((0, "__module__", 0))

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                if node.name in trace_map:
                    injection_points.append((node.lineno, node.name, node.col_offset))

                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        key = f"{node.name}.{child.name}"
                        if key in trace_map:
                            injection_points.append(
                                (child.lineno, key, child.col_offset)
                            )

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name in trace_map:
                    injection_points.append((node.lineno, node.name, node.col_offset))

        # Ordenar de abajo hacia arriba para no desplazar índices
        injection_points.sort(key=lambda x: -x[0])

        lines = code.split("\n")

        for lineno, key, col_offset in injection_points:
            traces = trace_map[key]

            if key == "__module__":
                lines = self._inject_module(lines, traces)
                continue

            # Indent del cuerpo = indent de la def/class + 4
            body_indent = col_offset + 4
            indent_str = " " * body_indent

            # Encontrar el final de la firma (puede ser multilínea)
            # lineno es 1-indexed; convertir a 0-indexed
            j = lineno - 1
            while j < len(lines) and not lines[j].rstrip().endswith(":"):
                j += 1

            body_start = j + 1  # primera línea del cuerpo (0-indexed)
            if body_start >= len(lines):
                continue

            # Saltar líneas en blanco al inicio del cuerpo
            while body_start < len(lines) and not lines[body_start].strip():
                body_start += 1

            if body_start >= len(lines):
                continue

            body_first = lines[body_start].strip()

            if body_first.startswith('"""') or body_first.startswith("'''"):
                quote = '"""' if body_first.startswith('"""') else "'''"
                rest = body_first[3:]

                if rest.endswith(quote) and len(rest) >= len(quote):
                    # Docstring de una línea → expandir a multilínea
                    content = rest[: -len(quote)].strip()
                    new_doc = [f"{indent_str}{quote}"]
                    if content:
                        new_doc.append(f"{indent_str}{content}")
                    for t in traces:
                        new_doc.append(f"{indent_str}BETO-TRACE: {t}")
                    new_doc.append(f"{indent_str}{quote}")
                    lines[body_start : body_start + 1] = new_doc
                else:
                    # Docstring multilínea → inyectar antes del cierre
                    k = body_start + 1
                    while k < len(lines) and quote not in lines[k]:
                        k += 1
                    trace_lines = [f"{indent_str}BETO-TRACE: {t}" for t in traces]
                    lines[k:k] = trace_lines
            else:
                # Sin docstring → insertar uno nuevo
                new_doc = [f"{indent_str}\"\"\""]
                for t in traces:
                    new_doc.append(f"{indent_str}BETO-TRACE: {t}")
                new_doc.append(f"{indent_str}\"\"\"")
                lines[body_start:body_start] = new_doc

        return "\n".join(lines)

    def _inject_module(self, lines: list, traces: list) -> list:
        """
        Inyecta el docstring de módulo al inicio del archivo.
        Si ya existe uno, agrega los IDs antes del cierre.
        """
        # Buscar primera línea no vacía y no comentario
        for j, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if stripped.startswith('"""') or stripped.startswith("'''"):
                quote = '"""' if stripped.startswith('"""') else "'''"
                rest = stripped[3:]

                if rest.endswith(quote) and len(rest) >= len(quote):
                    # Docstring de una línea
                    content = rest[: -len(quote)].strip()
                    new_doc = ['"""']
                    if content:
                        new_doc.append(content)
                    for t in traces:
                        new_doc.append(f"BETO-TRACE: {t}")
                    new_doc.append('"""')
                    return new_doc + lines[j + 1 :]
                else:
                    # Multilínea: inyectar antes del cierre
                    k = j + 1
                    while k < len(lines) and quote not in lines[k]:
                        k += 1
                    trace_lines = [f"BETO-TRACE: {t}" for t in traces]
                    return lines[:k] + trace_lines + lines[k:]

            # No hay docstring de módulo
            break

        # Sin docstring existente → agregar al inicio
        new_doc = ['"""'] + [f"BETO-TRACE: {t}" for t in traces] + ['"""', ""]
        return new_doc + lines

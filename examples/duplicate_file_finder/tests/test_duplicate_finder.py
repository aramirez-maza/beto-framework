"""
Tests for duplicate_file_finder — BETO cycle 14210d80
Generated files: 6 TRACE_VERIFIED source files, 72 authorized IDs, 0 silent completions.

Tests cover:
  - detect_duplicates (duplicate_detector.py)
  - SpaceCalculator (space_calculator.py)
  - ReportComposer (report_composer.py)
  - Scanner (scanner.py)
  - End-to-end pipeline (main.py)
"""

import json
import sys
import os
import pytest
from pathlib import Path

# Add materialized src to path
SRC = Path(__file__).parent.parent / "materialized" / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(SRC / "duplicate_detector"))
sys.path.insert(0, str(SRC / "space_calculator"))
sys.path.insert(0, str(SRC / "report_composer"))
sys.path.insert(0, str(SRC / "scanner"))
sys.path.insert(0, str(SRC / "duplicate_finder"))

from duplicate_detector import FileEntry, DuplicateGroup, detect_duplicates
from space_calculator import SpaceCalculator
from report_composer import ReportComposer
import main as finder_main


# ─── detect_duplicates ────────────────────────────────────────────────────────

class TestDetectDuplicates:

    def test_no_duplicates_returns_empty(self):
        entries = [
            FileEntry("/a/file1.txt", 100, "hash_aaa"),
            FileEntry("/a/file2.txt", 200, "hash_bbb"),
            FileEntry("/a/file3.txt", 300, "hash_ccc"),
        ]
        result = detect_duplicates(entries)
        assert result == []

    def test_single_duplicate_pair_detected(self):
        entries = [
            FileEntry("/a/file1.txt", 100, "hash_same"),
            FileEntry("/b/file2.txt", 100, "hash_same"),
        ]
        result = detect_duplicates(entries)
        assert len(result) == 1
        assert set(result[0].file_paths) == {"/a/file1.txt", "/b/file2.txt"}
        assert result[0].content_hash == "hash_same"
        assert result[0].group_size == 100

    def test_multiple_duplicate_groups(self):
        entries = [
            FileEntry("/a/f1.txt", 50,  "hash_x"),
            FileEntry("/b/f2.txt", 50,  "hash_x"),
            FileEntry("/a/f3.txt", 200, "hash_y"),
            FileEntry("/b/f4.txt", 200, "hash_y"),
            FileEntry("/c/f5.txt", 200, "hash_y"),
        ]
        result = detect_duplicates(entries)
        assert len(result) == 2
        hashes = {g.content_hash for g in result}
        assert hashes == {"hash_x", "hash_y"}

    def test_triplet_detected_as_one_group(self):
        entries = [
            FileEntry("/a/f1.txt", 10, "hash_dup"),
            FileEntry("/b/f2.txt", 10, "hash_dup"),
            FileEntry("/c/f3.txt", 10, "hash_dup"),
        ]
        result = detect_duplicates(entries)
        assert len(result) == 1
        assert len(result[0].file_paths) == 3

    def test_empty_input_returns_empty(self):
        assert detect_duplicates([]) == []

    def test_single_file_not_a_duplicate(self):
        entries = [FileEntry("/a/only.txt", 100, "hash_solo")]
        assert detect_duplicates(entries) == []


# ─── SpaceCalculator ──────────────────────────────────────────────────────────

class TestSpaceCalculator:

    def _make_group(self, file_paths, group_size):
        return {"content_hash": "h", "file_paths": file_paths, "group_size": group_size}

    def test_single_pair_recoverable_space(self):
        calc = SpaceCalculator()
        groups = [self._make_group(["/a/f1.txt", "/b/f2.txt"], 1000)]
        result = calc.calculate_recoverable_space(groups)
        assert result["total_recoverable_bytes"] == 1000

    def test_triplet_recoverable_space(self):
        calc = SpaceCalculator()
        groups = [self._make_group(["/a/f1.txt", "/b/f2.txt", "/c/f3.txt"], 500)]
        result = calc.calculate_recoverable_space(groups)
        assert result["total_recoverable_bytes"] == 1000  # 2 copies recoverable

    def test_multiple_groups_total(self):
        calc = SpaceCalculator()
        groups = [
            self._make_group(["/a/f1.txt", "/b/f2.txt"], 100),
            self._make_group(["/c/f3.txt", "/d/f4.txt"], 200),
        ]
        result = calc.calculate_recoverable_space(groups)
        assert result["total_recoverable_bytes"] == 300

    def test_empty_groups_returns_zero(self):
        calc = SpaceCalculator()
        result = calc.calculate_recoverable_space([])
        assert result["total_recoverable_bytes"] == 0

    def test_recoverable_bytes_added_to_group(self):
        calc = SpaceCalculator()
        groups = [self._make_group(["/a/f1.txt", "/b/f2.txt"], 400)]
        result = calc.calculate_recoverable_space(groups)
        assert result["duplicate_groups"][0]["recoverable_bytes"] == 400


# ─── ReportComposer ───────────────────────────────────────────────────────────

class TestReportComposer:

    def _make_groups(self):
        return [
            {"content_hash": "abc123", "file_paths": ["/a/f1.txt", "/b/f2.txt"], "recoverable_bytes": 1000},
        ]

    def test_json_report_is_valid_json(self):
        composer = ReportComposer(self._make_groups(), 1000)
        report = composer.generate_report(output_format="json")
        data = json.loads(report)
        assert "duplicate_groups" in data
        assert "total_recoverable_bytes" in data

    def test_json_report_total_bytes(self):
        composer = ReportComposer(self._make_groups(), 1000)
        report = composer.generate_report(output_format="json")
        data = json.loads(report)
        assert data["total_recoverable_bytes"] == 1000

    def test_text_report_contains_hash(self):
        composer = ReportComposer(self._make_groups(), 1000)
        report = composer.generate_report(output_format="text")
        assert "abc123" in report

    def test_text_report_contains_file_paths(self):
        composer = ReportComposer(self._make_groups(), 1000)
        report = composer.generate_report(output_format="text")
        assert "/a/f1.txt" in report
        assert "/b/f2.txt" in report

    def test_unsupported_format_raises(self):
        composer = ReportComposer(self._make_groups(), 1000)
        with pytest.raises(ValueError):
            composer.generate_report(output_format="xml")

    def test_report_written_to_file(self, tmp_path):
        out = tmp_path / "report.json"
        composer = ReportComposer(self._make_groups(), 1000)
        composer.generate_report(output_format="json", output_file=str(out))
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["total_recoverable_bytes"] == 1000


# ─── Scanner ──────────────────────────────────────────────────────────────────

class TestScanner:

    def test_scan_empty_directory(self, tmp_path):
        from scanner import Scanner
        s = Scanner(str(tmp_path))
        assert s.scan() == []

    def test_scan_finds_files(self, tmp_path):
        from scanner import Scanner
        (tmp_path / "a.txt").write_text("hello")
        (tmp_path / "b.txt").write_text("world")
        s = Scanner(str(tmp_path))
        entries = s.scan()
        assert len(entries) == 2

    def test_scan_recursive(self, tmp_path):
        from scanner import Scanner
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "root.txt").write_text("root")
        (sub / "nested.txt").write_text("nested")
        s = Scanner(str(tmp_path))
        entries = s.scan()
        assert len(entries) == 2

    def test_identical_files_same_hash(self, tmp_path):
        from scanner import Scanner
        (tmp_path / "f1.txt").write_bytes(b"same content")
        (tmp_path / "f2.txt").write_bytes(b"same content")
        s = Scanner(str(tmp_path))
        entries = s.scan()
        hashes = {e.content_hash for e in entries}
        assert len(hashes) == 1

    def test_different_files_different_hash(self, tmp_path):
        from scanner import Scanner
        (tmp_path / "f1.txt").write_bytes(b"content A")
        (tmp_path / "f2.txt").write_bytes(b"content B")
        s = Scanner(str(tmp_path))
        entries = s.scan()
        hashes = {e.content_hash for e in entries}
        assert len(hashes) == 2


# ─── End-to-end via main.py ───────────────────────────────────────────────────

class TestEndToEnd:

    def test_no_duplicates_full_pipeline(self, tmp_path):
        (tmp_path / "f1.txt").write_bytes(b"unique A")
        (tmp_path / "f2.txt").write_bytes(b"unique B")
        entries = finder_main.scan_directory(str(tmp_path))
        groups = finder_main.detect_duplicates(entries)
        report, total = finder_main.generate_report(groups)
        assert groups == []
        assert report == []
        assert total == 0

    def test_duplicate_detected_full_pipeline(self, tmp_path):
        content = b"identical content"
        (tmp_path / "orig.txt").write_bytes(content)
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "copy.txt").write_bytes(content)
        entries = finder_main.scan_directory(str(tmp_path))
        groups = finder_main.detect_duplicates(entries)
        report, total = finder_main.generate_report(groups)
        assert len(groups) == 1
        assert total == len(content)

    def test_recoverable_space_calculation(self, tmp_path):
        content = b"x" * 1000
        (tmp_path / "f1.txt").write_bytes(content)
        (tmp_path / "f2.txt").write_bytes(content)
        (tmp_path / "f3.txt").write_bytes(content)
        entries = finder_main.scan_directory(str(tmp_path))
        groups = finder_main.detect_duplicates(entries)
        _, total = finder_main.generate_report(groups)
        assert total == 2000  # 3 files — keep 1 — recover 2

    def test_empty_directory(self, tmp_path):
        entries = finder_main.scan_directory(str(tmp_path))
        assert entries == []

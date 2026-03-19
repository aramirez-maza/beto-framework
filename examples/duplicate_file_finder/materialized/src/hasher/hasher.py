"""
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC1.INTENT.CLI_TOOL
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC1.INTENT.TARGET_USERS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C1_NON_DESTRUCTIVE
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C2_RECURSIVE_SCOPE
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C3_REPORT_COMPLETENESS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R1_PERMISSION_ERRORS
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R2_HASH_COLLISION
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R3_LARGE_DIRECTORY_TREES
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.DUPLICATE_DETECTOR
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.FILE_ENTRY
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.LOCAL_FILESYSTEM
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.REPORT_COMPOSER
"""

import os
import hashlib
from typing import List, Dict, Tuple

class FileEntry:
    def __init__(self, file_path: str, file_size: int, content_hash: str):
        self.file_path = file_path
        self.file_size = file_size
        self.content_hash = content_hash

class Hasher:
    def __init__(self, target_directory: str):
        self.target_directory = target_directory

    def scan_directory(self) -> List[FileEntry]:
        file_entries = []
        for root, _, files in os.walk(self.target_directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    content_hash = self.compute_hash(file_path)
                    file_entries.append(FileEntry(file_path, file_size, content_hash))
                except PermissionError:
                    print(f"Permission denied: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
        return file_entries

    def compute_hash(self, file_path: str) -> str:
        hash_algorithm = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_algorithm.update(chunk)
        return hash_algorithm.hexdigest()

# NODO: 
# IMPLEMENT: conservar BETO-TRACE del docstring; implementar lógica real.
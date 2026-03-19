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
BETO-TRACE: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.SCANNER
"""

import os
import hashlib

class FileEntry:
    def __init__(self, file_path, file_size, content_hash):
        self.file_path = file_path
        self.file_size = file_size
        self.content_hash = content_hash

class Scanner:
    def __init__(self, target_directory):
        self.target_directory = target_directory

    def scan(self):
        file_entries = []
        for root, _, files in os.walk(self.target_directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    content_hash = self._compute_content_hash(file_path)
                    file_entries.append(FileEntry(file_path, file_size, content_hash))
                except PermissionError:
                    continue
        return file_entries

    def _compute_content_hash(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
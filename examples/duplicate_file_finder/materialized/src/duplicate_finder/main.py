"""
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC1.INTENT.CLI_TOOL
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC1.INTENT.CONTENT_HASH_DETECTION
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC1.INTENT.DUPLICATE_GROUPS
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC1.INTENT.FILE_PATHS
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC1.INTENT.LOCAL_FILESYSTEM
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC1.INTENT.RECOVERABLE_SPACE
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC1.INTENT.RECURSIVE_SCAN
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC1.INTENT.REPORT_GENERATION
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC10.CONSTRAINT.NON_DESTRUCTIVE
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC10.CONSTRAINT.RECURSIVE_SCOPE
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC10.CONSTRAINT.REPORT_COMPLETENESS
BETO-TRACE: BETO_DUPLICATE_FINDER.SEC10.RISK.HASH_COLLISION
"""

import os
import hashlib
import argparse

class FileEntry:
    def __init__(self, file_path, file_size, content_hash):
        self.file_path = file_path
        self.file_size = file_size
        self.content_hash = content_hash

class DuplicateGroup:
    def __init__(self, content_hash, file_paths, group_size):
        self.content_hash = content_hash
        self.file_paths = file_paths
        self.group_size = group_size

def compute_content_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_directory(target_dir):
    file_entries = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                content_hash = compute_content_hash(file_path)
                file_entries.append(FileEntry(file_path, file_size, content_hash))
            except PermissionError:
                continue
    return file_entries

def detect_duplicates(file_entries):
    candidate_groups = {}
    for entry in file_entries:
        if entry.content_hash not in candidate_groups:
            candidate_groups[entry.content_hash] = []
        candidate_groups[entry.content_hash].append(entry)

    duplicate_groups = []
    for content_hash, entries in candidate_groups.items():
        if len(entries) >= 2:
            file_paths = [entry.file_path for entry in entries]
            group_size = entries[0].file_size
            duplicate_groups.append(DuplicateGroup(content_hash, file_paths, group_size))

    return duplicate_groups

def generate_report(duplicate_groups):
    report = []
    total_recoverable_bytes = 0
    for group in duplicate_groups:
        recoverable_bytes = (len(group.file_paths) - 1) * group.group_size
        total_recoverable_bytes += recoverable_bytes
        report.append({
            'content_hash': group.content_hash,
            'file_paths': group.file_paths,
            'recoverable_bytes': recoverable_bytes
        })
    return report, total_recoverable_bytes

def main():
    parser = argparse.ArgumentParser(description='Duplicate File Finder')
    parser.add_argument('target_dir', help='Path to the target directory')
    args = parser.parse_args()

    file_entries = scan_directory(args.target_dir)
    duplicate_groups = detect_duplicates(file_entries)
    report, total_recoverable_bytes = generate_report(duplicate_groups)

    print("Duplicate Groups Report:")
    for group in report:
        print(f"Content Hash: {group['content_hash']}")
        print("File Paths:")
        for path in group['file_paths']:
            print(f"  {path}")
        print(f"Recoverable Bytes: {group['recoverable_bytes']}\n")

    print(f"Total Recoverable Bytes: {total_recoverable_bytes}")

if __name__ == "__main__":
    main()
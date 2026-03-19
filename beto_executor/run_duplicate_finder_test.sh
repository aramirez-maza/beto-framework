#!/bin/bash
# Modo test: gates aprobados automáticamente — NO usar en producción

cd "$(dirname "$0")/src"

python3 main.py \
  --idea "CLI tool that scans a directory recursively, detects duplicate files by content hash, and generates a report showing duplicate groups, file paths, and total recoverable space" \
  --reasoning-model claude-sonnet-4-6 \
  --code-model qwen-coder \
  --litellm-url http://localhost:8000 \
  --api-key local \
  --cycle-dir ./cycles \
  --templates-dir ../../skills/beto-framework/references \
  --auto-approve

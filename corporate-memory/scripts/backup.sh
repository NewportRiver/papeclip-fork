#!/usr/bin/env bash
set -euo pipefail

DB_PATH="${1:?usage: backup.sh DATABASE_PATH BACKUP_PATH}"
BACKUP_PATH="${2:?usage: backup.sh DATABASE_PATH BACKUP_PATH}"
mkdir -p "$(dirname "$BACKUP_PATH")"
python - "$DB_PATH" "$BACKUP_PATH" <<'PY'
import sqlite3, sys
source, target = sys.argv[1:]
with sqlite3.connect(source) as src, sqlite3.connect(target) as dst:
    src.backup(dst)
    integrity = dst.execute('PRAGMA integrity_check').fetchone()[0]
    if integrity != 'ok':
        raise SystemExit(f'integrity check failed: {integrity}')
print(target)
PY

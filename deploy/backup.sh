#!/usr/bin/env bash
# Backup consistente do SQLite (API de backup online). Mantém 14 dias.
# Instalado em /etc/cron.d/lisa-worksheets-backup (roda como usuário worksheets, 03:15 diariamente).
set -euo pipefail
cd /
umask 077
DIR=/opt/lisa-worksheets/data/backups
mkdir -p "$DIR"
/opt/lisa-worksheets/.venv/bin/python - "$DIR/worksheets-$(date +%Y%m%d-%H%M).db" <<'PY'
import sqlite3, sys
src = sqlite3.connect("/opt/lisa-worksheets/data/worksheets.db")
dst = sqlite3.connect(sys.argv[1])
src.backup(dst)
dst.close(); src.close()
PY
find "$DIR" -name 'worksheets-*.db' -mtime +14 -delete

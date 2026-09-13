#!/usr/bin/env bash
# Roda os comandos de administração no servidor com as variáveis de produção.
# Uso: sudo /opt/lisa-worksheets/deploy/manage.sh create-admin --username X --name "Nome" --email a@b.com
set -euo pipefail
set -a; . /etc/lisa-worksheets.env; set +a
cd /opt/lisa-worksheets
exec runuser -u worksheets -- .venv/bin/python -m app.manage "$@"

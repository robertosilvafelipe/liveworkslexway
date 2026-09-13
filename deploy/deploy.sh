#!/usr/bin/env bash
# Publica a versão local no servidor. Uso: ./deploy/deploy.sh [host-ssh]   (padrão: oracle-lisa)
set -euo pipefail
HOST="${1:-oracle-lisa}"
cd "$(dirname "$0")/.."
PKG="$(mktemp -d)/app.tgz"
tar czf "$PKG" --exclude=__pycache__ --exclude=.venv --exclude=data app deploy requirements.txt
scp -q "$PKG" "$HOST:/tmp/app.tgz"
ssh "$HOST" 'set -e
  sudo -u worksheets /opt/lisa-worksheets/deploy/backup.sh 2>/dev/null || true
  sudo tar xzf /tmp/app.tgz -C /opt/lisa-worksheets
  sudo /opt/lisa-worksheets/.venv/bin/pip -q install -r /opt/lisa-worksheets/requirements.txt
  sudo chown -R worksheets:worksheets /opt/lisa-worksheets
  sudo cp /opt/lisa-worksheets/deploy/lisa-worksheets.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl restart lisa-worksheets
  sleep 3
  systemctl is-active lisa-worksheets
  curl -s -o /dev/null -w "app local: HTTP %{http_code}\n" http://127.0.0.1:8000/login'
echo "Deploy concluído."

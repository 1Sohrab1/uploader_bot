#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$APP_DIR"

if [[ ! -f .env ]]; then
  echo "ERROR: .env not found — create it before deploying." >&2
  exit 1
fi

if [[ -d venv ]]; then
  VENV_DIR=venv
elif [[ -d .venv ]]; then
  VENV_DIR=.venv
else
  VENV_DIR=.venv
  python3 -m venv "$VENV_DIR"
fi

# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"
pip install -q -r requirements.txt

mkdir -p logs

pkill -f "${APP_DIR}/${VENV_DIR}/bin/python main.py" 2>/dev/null || true
pkill -f "${APP_DIR}/main.py" 2>/dev/null || true
pkill -f "python3 main.py" 2>/dev/null || true
sleep 1

nohup "${VENV_DIR}/bin/python" main.py >> logs/bot.log 2>&1 &
disown

echo "Deploy OK"

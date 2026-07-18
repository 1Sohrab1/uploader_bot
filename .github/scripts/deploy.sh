#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
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

mkdir -p logs data

stop_bot() {
  # Kill every process whose cwd/cmdline is this app's main.py.
  # Deploy used to leave orphans → TelegramConflictError + random replies.
  local pids
  pids="$(pgrep -f "[p]ython([0-9.]*)?( .*/)?main\.py" 2>/dev/null || true)"
  if [[ -n "${pids}" ]]; then
    # shellcheck disable=SC2086
    for pid in ${pids}; do
      if [[ -r "/proc/${pid}/cwd" ]] && [[ "$(readlink -f "/proc/${pid}/cwd")" == "${APP_DIR}" ]]; then
        kill "${pid}" 2>/dev/null || true
      fi
    done
  fi

  if [[ -f logs/bot.pid ]]; then
    local old_pid
    old_pid="$(cat logs/bot.pid 2>/dev/null || true)"
    if [[ -n "${old_pid}" ]] && kill -0 "${old_pid}" 2>/dev/null; then
      kill "${old_pid}" 2>/dev/null || true
    fi
    rm -f logs/bot.pid
  fi

  sleep 2

  # Force-kill leftovers still in this directory
  pids="$(pgrep -f "[p]ython([0-9.]*)?( .*/)?main\.py" 2>/dev/null || true)"
  if [[ -n "${pids}" ]]; then
    for pid in ${pids}; do
      if [[ -r "/proc/${pid}/cwd" ]] && [[ "$(readlink -f "/proc/${pid}/cwd")" == "${APP_DIR}" ]]; then
        kill -9 "${pid}" 2>/dev/null || true
      fi
    done
  fi
}

stop_bot

nohup "${VENV_DIR}/bin/python" main.py >> logs/bot.log 2>&1 &
echo $! > logs/bot.pid

echo "Deploy OK — PID $(cat logs/bot.pid)"

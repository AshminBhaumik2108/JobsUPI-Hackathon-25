#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -d "agent-service/.venv" ]; then
  echo "Python venv not found in agent-service/.venv" >&2
  exit 1
fi
source agent-service/.venv/bin/activate
cd agent-service
exec uvicorn app.main:app --reload --port 8001

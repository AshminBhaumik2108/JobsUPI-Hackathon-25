#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
cd core-service
if [ -f package.json ]; then
  npm install
fi
exec npm run dev

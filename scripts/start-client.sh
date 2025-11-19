#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
cd client
if [ -f package.json ]; then
  npm install
fi
exec npm run dev

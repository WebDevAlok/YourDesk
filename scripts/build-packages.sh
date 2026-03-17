#!/usr/bin/env bash
set -euo pipefail

VERSION=${1:-1.0.0}
DIST_DIR=${DIST_DIR:-dist}
mkdir -p "$DIST_DIR"

python -m pip install --upgrade build
python -m build

if command -v fpm >/dev/null 2>&1; then
  fpm -s python -t deb --python-bin python3 --name yourdesk --version "$VERSION" dist/*.whl
  fpm -s python -t rpm --python-bin python3 --name yourdesk --version "$VERSION" dist/*.whl
else
  echo "fpm not found; skipping .deb/.rpm artifact creation" >&2
fi

echo "Package build flow completed."

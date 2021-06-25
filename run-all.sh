#!/usr/bin/env bash

VENV=$(readlink -f "$(poetry env info -p)")

find "$PWD" -path "$VENV" -prune -o \( -type f -a -name \*.py -a -not -name .\* -print \) | while read -r F; do
  grep -q "__main__" "$F" || continue
  relative_path=$(realpath --relative-to="$PWD" "$F")
  module_name=$(dirname "$relative_path" | tr / .).$(basename "$F" .py)
  echo ">>> $module_name"
  poetry run python -m "$module_name"
done

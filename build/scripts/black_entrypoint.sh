#!/bin/sh

set -e

echo "Activating virtual environment..."
. /application_root/.venv/bin/activate

# Evaluating passed CMD
echo "Running black..."
black "$@"

#!/bin/bash

set -e

# Start Gunicorn
echo "Activating virtual environment..."
. /application_root/.venv/bin/activate

exec uvicorn --workers 1 --host 0.0.0.0 --port 8080 app.main:app

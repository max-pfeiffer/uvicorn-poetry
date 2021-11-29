#!/bin/bash

set -e

# Process environment variables for uvicorn options
declare -A ALLOWED_LOG_LEVEL=([critical]='critical'
                              [error]='error'
                              [warning]='warning'
                              [info]='info'
                              [debug]='debug'
                              [trace]='trace')

declare -a OPTIONS_ARRAY=('--workers 1'
                    '--host 0.0.0.0'
                    '--port 80')


if [[ -n $LOG_LEVEL ]]
  then
    if [[ -n "${ALLOWED_LOG_LEVEL[$LOG_LEVEL]}" ]]
      then
        OPTIONS_ARRAY+=("--log-level $LOG_LEVEL")
      else
        echo "Invalid log level!"
        exit 1
    fi
else
  # Default log level
  OPTIONS_ARRAY+=("--log-level ${ALLOWED_LOG_LEVEL[info]}")
fi

if [[ -n $RELOAD ]]
  then
    if [ "$RELOAD" = true ]
      then
        OPTIONS_ARRAY+=("--reload")
    fi
fi

OPTIONS_STRING="${OPTIONS_ARRAY[*]}"

# Start Gunicorn
echo "Activating virtual environment..."
. /application_root/.venv/bin/activate

exec uvicorn $OPTIONS_STRING app.main:app

#!/bin/bash

set -e



echo "Activating virtual environment..."
. /application_root/.venv/bin/activate

declare -A ALLOWED_LOG_LEVEL=([critical]='critical'
                              [error]='error'
                              [warning]='warning'
                              [info]='info'
                              [debug]='debug'
                              [trace]='trace')

declare -a ARGUMENTS=('--workers 1'
                      '--host 0.0.0.0'
                      '--port 80')


if [[ -n $LOG_LEVEL ]]
  then
    if [[ -n "${ALLOWED_LOG_LEVEL[$LOG_LEVEL]}" ]]
      then
        ARGUMENTS+=("--log-level $LOG_LEVEL")
      else
        exit 1
    fi
fi

if [[ -n $RELOAD ]]
  then
    if [ "$RELOAD" = true ]
      then
        ARGUMENTS+=("--reload")
    fi
fi

# Start Gunicorn
exec uvicorn "${ARGUMENTS[@]}" app.main:app

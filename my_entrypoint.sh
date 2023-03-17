#!/bin/bash
set -e

pytest tests
python --version
echo $PROJECT_ID
ls

# Run Airflow's entrypoint with the passed arguments
exec /entrypoint "${@}"

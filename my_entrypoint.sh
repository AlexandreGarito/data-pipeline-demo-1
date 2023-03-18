#!/bin/bash
set -e

pytest tests
python --version
echo $PROJECT_ID
ls
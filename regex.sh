#!/bin/bash
source venv/bin/activate

python3 regex.py "$@"

deactivate

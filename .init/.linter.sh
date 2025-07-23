#!/bin/bash
cd /home/kavia/workspace/code-generation/audiobook-library-55ac5558/backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi


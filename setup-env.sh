#!/bin/bash
set -e

app="${1:-venv}"

if hash virtualenv 2>/dev/null
then
  VENV="virtualenv"
else
  VENV="python -m venv"
fi

$VENV ".venv/$app"

. activate

pip install -U setuptools
pip install -U pip
pip install -r requirements.txt
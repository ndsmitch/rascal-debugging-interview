#!/bin/bash

# Establish a Neurological Linkage to The Rascal:
# source neuralink.sh

if [[ "$VIRTUAL_ENV" != "" ]]
then
  echo "🛠️ Clearing previous neuralink"
  virtualenv --clear venv
  deactivate
fi

echo "🧠 Establishing Neuralink"
PYTHON=$(which python3.8)
eval $PYTHON -m virtualenv venv
source venv/bin/activate

echo "🐍 Enhancing Neuralink"
python -m pip install --upgrade pip
python -m pip install falcon==3.1.1
python -m pip install requests==2.31.0
python -m pip install structlog==23.1.0
python -m pip install pytest==7.4.0
python -m pip install rich==13.5.2

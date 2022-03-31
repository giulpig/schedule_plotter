#!/usr/bin/env bash

set -e
CURRENT=`dirname "$0"`
cd $CURRENT
virtualenv venv
source $CURRENT/venv/bin/activate

pip install $CURRENT

printf "\n\nSuccesfully created virtual environment, now launching example script\n"

python3 $CURRENT/example/example.py

deactivate
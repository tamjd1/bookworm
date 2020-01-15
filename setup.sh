#!/usr/bin/env bash

python -m venv venv
source venv/bin/activate
which python
python --version
pip install --upgrade pip

pip install -r requirements.txt

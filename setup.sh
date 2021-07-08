#!/bin/bash
conda env create --file environment.yml
conda activate gfit
python -m pip install -r requirements.txt
python -m pip install -e .

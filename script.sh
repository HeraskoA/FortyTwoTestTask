#!/bin/bash

TIME=$(date +"%Y-%m-%d")
PYTHON="python"


$PYTHON manage.py mcount 2> $TIME.dat

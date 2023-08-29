#!/bin/sh

# Do all the linting on your machine

flake8 src/client --ignore=E501,W503
pylint src/client --recursive True --rcfile=.pylintrc --reports True --output-format=colorized
mypy src/client --config-file=.mypy.ini
bandit src/client -r

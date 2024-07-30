#!/bin/bash
coverage run --source=../ -m unittest -v
coverage report -m
coverage html
#open htmlcov/index.html
open http://localhost:63342/quantum-network/htmlcov/index.html
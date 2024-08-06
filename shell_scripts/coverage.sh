#!/bin/bash
coverage run --parallel-mode --source=./ -m unittest -v
coverage combine
coverage report -m
coverage html
#open htmlcov/index.html
open http://localhost:63342/quantum-network/htmlcov/index.html
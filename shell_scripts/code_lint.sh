#!/bin/bash
#flake8 --max-line-length=127
#flake8 --max-line-length=127 --statistics
flake8 /opt/project/src/ --max-line-length=127 --exit-zero --statistics --tee --output-file /opt/project/reports/flake/flake8stats.txt
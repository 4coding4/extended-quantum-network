#!/bin/bash
#flake8 --max-line-length=127
#flake8 --max-line-length=127 --statistics
rm /opt/project/reports/flake8/flake8stats.txt
flake8 /opt/project/src/ --max-line-length=127 --exit-zero --statistics --tee --output-file /opt/project/reports/flake8/flake8stats.txt
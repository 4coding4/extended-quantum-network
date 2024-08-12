#!/bin/bash
coverage run --parallel-mode --source=./ -m unittest -v
coverage combine
coverage report
#-m --skip-covered --skip-empty
rm /opt/project/reports/coverage/coverage.xml
coverage xml -o /opt/project/reports/coverage/coverage.xml
coverage html
#--skip-covered --skip-empty
#open htmlcov/index.html
open http://localhost:63342/quantum-network/htmlcov/index.html
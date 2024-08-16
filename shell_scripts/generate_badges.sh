#!/bin/bash
# update all the reports by running the other scripts
/opt/project/shell_scripts/test_all.sh
/opt/project/shell_scripts/coverage.sh
/opt/project/shell_scripts/code_lint.sh

genbadge tests -o '/opt/project/badges/tests-badge.svg'
genbadge coverage -o '/opt/project/badges/coverage-badge.svg'
genbadge flake8 -o '/opt/project/badges/flake8-badge.svg'
#!/bin/bash
genbadge tests -o '/opt/project/badges/tests-badge.svg'
genbadge coverage -o '/opt/project/badges/coverage-badge.svg'
genbadge flake8 -o '/opt/project/badges/flake8-badge.svg'
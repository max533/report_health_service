#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Reload environment for cond
source /app/.env_file

echo "Health Report Date: `date +"%Y-%m-%d"`" > /proc/1/fd/1 2>&1
/usr/local/bin/python /app/report_health.py > /proc/1/fd/1 2>&1
echo
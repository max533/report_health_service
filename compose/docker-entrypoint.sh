#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "Health Report Service start at `date`"
echo

export REFERER_SITE_PATH=/app/$REFERER_SITE_PATH
export USER_AGENT_PATH=/app/$USER_AGENT_PATH

# Provide environment source for health_report_contab.sh
export > /app/.env_file

echo "Health Report Date: `date +"%Y-%m-%d"`"
/usr/local/bin/python /app/report_health.py > /proc/1/fd/1 2>&1
echo

exec "$@"

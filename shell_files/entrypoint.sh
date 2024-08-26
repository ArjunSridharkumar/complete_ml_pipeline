#!/bin/bash
set -e

airflow scheduler &
airflow webserver &

# exec airflow webserver
exec tail -f /dev/null
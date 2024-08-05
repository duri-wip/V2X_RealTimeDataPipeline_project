#!/bin/bash

# airflow scheduler 프로세스 종료
scheduler_pid=$(ps -ef | grep 'airflow-scheduler' | grep -v grep | awk '{print $2}')
if [ -n "$scheduler_pid" ]; then
  echo "Stopping airflow scheduler (PID: $scheduler_pid)..."
  kill $scheduler_pid
  # 프로세스가 완전히 종료될 때까지 기다림
  while kill -0 $scheduler_pid 2>/dev/null; do
    sleep 1
  done
  echo "airflow scheduler stopped."
else
  echo "airflow scheduler is not running."
fi

# airflow webserver 프로세스 종료
webserver_pid=$(ps -ef | grep 'airflow-webserver' | grep -v grep | awk '{print $2}')
if [ -n "$webserver_pid" ]; then
  echo "Stopping airflow webserver (PID: $webserver_pid)..."
  kill $webserver_pid
  # 프로세스가 완전히 종료될 때까지 기다림
  while kill -0 $webserver_pid 2>/dev/null; do
    sleep 1
  done
  echo "airflow webserver stopped."
else
  echo "airflow webserver is not running."
fi

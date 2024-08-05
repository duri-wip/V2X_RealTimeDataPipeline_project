#!/bin/bash

# pyenv가 설치된 디렉토리를 환경 변수로 설정
export PYENV_ROOT="$HOME/.pyenv"

# pyenv가 설치된 디렉토리가 존재하는지 확인하고, PATH에 추가
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"

# pyenv 초기화
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# pyenv-virtualenv 초기화
eval "$(pyenv virtualenv-init -)"

# pyenv로 특정 환경 활성화
pyenv activate py3_11_9

# Airflow 웹 서버와 스케줄러를 백그라운드에서 실행
nohup airflow webserver --port 8880 > ~/app/airflow/logs/webserver.log 2>&1 &
nohup airflow scheduler > ~/app/airflow/logs/scheduler.log 2>&1 &

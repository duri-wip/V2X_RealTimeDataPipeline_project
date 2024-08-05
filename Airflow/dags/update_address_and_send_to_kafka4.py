import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# 현재 파일의 디렉토리를 기준으로 utils 및 tasks 디렉토리를 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'tasks'))

from tasks.fetch_and_update import fetch_and_update_address
from tasks.send_to_kafka import send_to_kafka

# 기본 설정
default_args = {
    'owner': 'DEProjTeam13',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# DAG 정의
dag = DAG(
    'update_address_and_send_to_kafka4',
    default_args=default_args,
    description='Fetch coordinates, update address, and send to Kafka',
    schedule_interval=timedelta(minutes=15),
    start_date=datetime(2024, 7, 23),
    catchup=False,
)

fetch_and_update_task = PythonOperator(
    task_id='fetch_and_update_address',
    python_callable=fetch_and_update_address,
    dag=dag,
)

send_to_kafka_task = PythonOperator(
    task_id='send_to_kafka',
    python_callable=send_to_kafka,
    provide_context=True,
    dag=dag,
)

fetch_and_update_task >> send_to_kafka_task

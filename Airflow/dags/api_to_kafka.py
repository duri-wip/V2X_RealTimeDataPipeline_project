from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from kafka import KafkaProducer
import requests
import json

# 기본 설정
default_args = {
    'owner': 'DEProjTeam13',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
with DAG(
    dag_id='api_to_kafka',
    default_args=default_args,
    description='Fetch data from API and send to Kafka',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 7, 23),
    catchup=False,
) as dag:

    # API 데이터 수집 함수
    def fetch_api_data(**kwargs):
        api_key = Variable.get("tdata_apikey")
        url = f"https://t-data.seoul.go.kr/apig/apiman-gateway/tapi/v2xVehiclePositionInformation/1.0?apikey={api_key}&numOfRows=10"
        response = requests.get(url)
        response.raise_for_status()  # API 호출 실패 시 예외 발생
        data = response.json()
        return data

    # Kafka로 데이터 전송 함수
#    def send_to_kafka(**kwargs):
#        data = kwargs['ti'].xcom_pull(task_ids='fetch_api_data')
#        producer = KafkaProducer(
#            bootstrap_servers='server01:9092,server02:9092,server03:9092',
#            value_serializer=lambda v: json.dumps(v).encode('utf-8')
#        )
#        producer.send('car_info', data)
#        producer.flush()

    def send_to_kafka(**kwargs):
        data = kwargs['ti'].xcom_pull(task_ids='fetch_api_data')
        if isinstance(data, list):
            producer = KafkaProducer(
                bootstrap_servers='server01:9092,server02:9092,server03:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
         )
            for item in data:
                producer.send('car_info', item)
            producer.flush()
        else:
            raise ValueError("Expected list from fetch_api_data, but got: {}".format(type(data)))

    # PythonOperator로 작업 정의
    fetch_api_data_task = PythonOperator(
        task_id='fetch_api_data',
        python_callable=fetch_api_data,
        dag=dag,
    )

    send_to_kafka_task = PythonOperator(
        task_id='send_to_kafka',
        python_callable=send_to_kafka,
        dag=dag,
    )

    # 작업 순서 정의
    fetch_api_data_task >> send_to_kafka_task

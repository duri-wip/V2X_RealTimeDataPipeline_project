from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import aiohttp
import asyncio
from kafka import KafkaProducer
from airflow.models import Variable

# Kafka 설정
KAFKA_BOOTSTRAP_SERVERS = 'server01:9092,server02:9092,server03:9092'
KAFKA_TOPIC = 'car_info'  # Kafka 토픽 이름을 'car_info'로 수정

# API 키 설정 - Airflow 변수에서 가져오기
TDATA_API_KEY = Variable.get("tdata_apikey")
KAKAO_API_KEY = Variable.get("kakao_rest_api_key")

# TDATA URL 설정
tdata_url = f'https://t-data.seoul.go.kr/apig/apiman-gateway/tapi/v2xVehiclePositionInformation/1.0?apikey={TDATA_API_KEY}&numOfRows=1000'

# 기본 설정
default_args = {
    'owner': 'DEProjTeam13',  # 소유자
    'depends_on_past': False,  # 이전 DAG 실행에 의존하지 않음
    'email_on_failure': False,  # 실패 시 이메일 알림 비활성화
    'email_on_retry': False,  # 재시도 시 이메일 알림 비활성화
    'retries': 1,  # 재시도 횟수
    'retry_delay': timedelta(minutes=1),  # 재시도 간격
}

# DAG 정의
dag = DAG(
    'update_address_and_send_to_kafka3',  # DAG ID
    default_args=default_args,  # 기본 설정 적용
    description='Fetch coordinates, update address, and send to Kafka',  # 설명
    schedule_interval=timedelta(minutes=15),  # 15분 간격으로 실행
    start_date=datetime(2024, 7, 23),  # 시작 날짜
    catchup=False,  # 시작 날짜 이후의 미실행 DAG catchup 비활성화
)

async def fetch_address(session, lat, lng, retries=3):
    """
    Kakao API를 사용하여 위도(lat)와 경도(lng)로부터 주소를 가져오는 비동기 함수.
    주어진 재시도(retries) 횟수만큼 시도.
    """
    url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={lng}&y={lat}"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}"
    }
    
    for attempt in range(retries):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:  # 응답 코드가 200일 경우에만 JSON 반환
                return await response.json()
            else:
                print(f"Attempt {attempt + 1} failed for lat: {lat}, lng: {lng}, status: {response.status}")
                await asyncio.sleep(0.5)  # 재요청 전에 잠시 대기

    return {"documents": []}  # 재시도 후에도 실패하면 빈 documents 반환

async def update_address(tdata_json):
    """
    tdata_json 리스트의 각 항목에 대해 주소를 업데이트하는 비동기 함수.
    Kakao API를 사용하여 위도와 경도로부터 주소를 가져오고, 서울특별시가 아닌 경우 데이터를 제거.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []  # 비동기 태스크를 저장할 리스트
        for index, i in enumerate(tdata_json):
            tasks.append(fetch_address(session, i['vhcleLat'], i['vhcleLot']))
            if len(tasks) == 100:  # 100개씩 묶어서 실행
                results = await asyncio.gather(*tasks)
                for idx, result in enumerate(results):
                    if result and result.get('documents') and len(result['documents']) > 1:
                        doc = result['documents'][1]
                        if doc["region_1depth_name"] == "서울특별시":
                            addr = doc.get("region_2depth_name", "주소 없음")
                            tdata_json[index - 99 + idx].update({'addr': addr})
                        else:
                            tdata_json[index - 99 + idx] = None  # 서울특별시가 아니면 None으로 설정
                    else:
                        tdata_json[index - 99 + idx] = None  # 유효하지 않은 결과인 경우 None으로 설정
                tasks = []  # tasks 리스트 초기화
        if tasks:  # 남은 태스크 처리
            results = await asyncio.gather(*tasks)
            for idx, result in enumerate(results):
                if result and result.get('documents') and len(result['documents']) > 1:
                    doc = result['documents'][1]
                    if doc["region_1depth_name"] == "서울특별시":
                        addr = doc.get("region_2depth_name", "주소 없음")
                        tdata_json[len(tdata_json) - len(results) + idx].update({'addr': addr})
                    else:
                        tdata_json[len(tdata_json) - len(results) + idx] = None
                else:
                    tdata_json[len(tdata_json) - len(results) + idx] = None
        # None 값을 제거하여 유효한 데이터만 남김
        tdata_json = [item for item in tdata_json if item is not None]
    return tdata_json

def fetch_and_update_address():
    """
    TDATA API에서 데이터를 가져오고, 주소를 업데이트하는 함수.
    """
    response = requests.get(tdata_url)
    response.raise_for_status()  # API 호출 실패 시 예외 발생
    tdata_json = response.json()  # 응답을 JSON으로 변환
    updated_data = asyncio.run(update_address(tdata_json))  # 주소 업데이트
    return updated_data

def send_to_kafka(**kwargs):
    """
    업데이트된 데이터를 Kafka로 전송하는 함수.
    """
    data = kwargs['ti'].xcom_pull(task_ids='fetch_and_update_address')
    if isinstance(data, list):
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        for item in data:
            producer.send(KAFKA_TOPIC, item)
        producer.flush()
    else:
        raise ValueError("Expected list from fetch_and_update_address, but got: {}".format(type(data)))

# PythonOperator로 작업 정의
fetch_and_update_task = PythonOperator(
    task_id='fetch_and_update_address',
    python_callable=fetch_and_update_address,
    dag=dag,
)

send_to_kafka_task = PythonOperator(
    task_id='send_to_kafka',
    python_callable=send_to_kafka,
    provide_context=True,  # context를 제공하여 kwargs['ti'] 사용 가능
    dag=dag,
)

# 작업 순서 정의
fetch_and_update_task >> send_to_kafka_task

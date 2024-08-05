import requests
from airflow.models import Variable

TDATA_API_KEY = Variable.get("tdata_apikey")
TDATA_URL = f'https://t-data.seoul.go.kr/apig/apiman-gateway/tapi/v2xVehiclePositionInformation/1.0?apikey={TDATA_API_KEY}&numOfRows=1000'

def fetch_tdata():
    """
    TDATA API에서 데이터를 가져오는 함수.
    """
    response = requests.get(TDATA_URL)
    response.raise_for_status()
    return response.json()

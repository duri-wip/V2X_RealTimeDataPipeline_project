import aiohttp
import asyncio
from airflow.models import Variable

KAKAO_API_KEY = Variable.get("kakao_rest_api_key")

async def fetch_address(session, lat, lng, retries=3):
    """
    Kakao API를 사용하여 위도(lat)와 경도(lng)로부터 주소를 가져오는 비동기 함수.
    주어진 재시도(retries) 횟수만큼 시도.
    """
    url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={lng}&y={lat}"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

    for attempt in range(retries):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            await asyncio.sleep(0.5)

    return {"documents": []}

async def update_address(tdata_json):
    """
    tdata_json 리스트의 각 항목에 대해 주소를 업데이트하는 비동기 함수.
    Kakao API를 사용하여 위도와 경도로부터 주소를 가져오고, 서울특별시가 아닌 경우 데이터를 제거.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, i in enumerate(tdata_json):
            tasks.append(fetch_address(session, i['vhcleLat'], i['vhcleLot']))
            if len(tasks) == 100:
                results = await asyncio.gather(*tasks)
                for idx, result in enumerate(results):
                    if (result and 'documents' in result and len(result['documents']) > 1 and
                        result['documents'][1]["region_1depth_name"] == "서울특별시"):
                        doc = result['documents'][1]
                        addr = doc.get("region_2depth_name", "주소 없음")
                        tdata_json[index - 99 + idx].update({'addr': addr})
                    else:
                        tdata_json[index -99 + idx] = None
                tasks = []

        tdata_json = [item for item in tdata_json if item is not None]

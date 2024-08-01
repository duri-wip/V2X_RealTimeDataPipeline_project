import aiohttp
import asyncio
import json
import requests
import time

# 데이터 URL
TDATA_API_KEY = 'API키 입력'
tdata_url = f'https://t-data.seoul.go.kr/apig/apiman-gateway/tapi/v2xVehiclePositionInformation/1.0?apikey={TDATA_API_KEY}&numOfRows=1000'
api_json = requests.get(tdata_url)
tdata_json = json.loads(api_json.text)
KAKAO_API_KEY = 'API키 입력'  # Kakao API 키

async def fetch_address(session, lat, lng, retries=3):
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

async def main(tdata_json):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for index, i in enumerate(tdata_json):
            tasks.append(fetch_address(session, i['vhcleLat'], i['vhcleLot']))

            # 100개 단위로 묶어서 실행
            if len(tasks) == 100:
                results = await asyncio.gather(*tasks)
                # None이 아닌 결과만 필터링
                for idx, result in enumerate(results):
                    if result and result.get('documents'):
                        address_name = result['documents'][0].get('address_name', "주소 없음")  # 기본값 설정
                    else:
                        address_name = "주소 없음"  # 기본값 설정
                    # 원래의 JSON에 address_name 추가
                    tdata_json[index - 99 + idx].update({'address_name': address_name})

                tasks = []  # tasks 리스트 초기화

        # 남은 태스크 처리
        if tasks:
            results = await asyncio.gather(*tasks)
            for idx, result in enumerate(results):
                if result and result.get('documents'):
                    address_name = result['documents'][0].get('address_name', "주소 없음")  # 기본값 설정
                else:
                    address_name = "주소 없음"  # 기본값 설정
                # 원래의 JSON에 address_name 추가
                tdata_json[len(tdata_json) - len(results) + idx].update({'address_name': address_name})

        return json.dumps(tdata_json, ensure_ascii=False)  # JSON 형식으로 반환

# 비동기 함수 실행
if __name__ == "__main__":
    start = time.time()
    addresses_json = await (main(tdata_json))  # 일반 스크립트에서 사용
    end = time.time()
    print(json.loads(addresses_json))  # 최종 결과 출력
    print(f'{end-start} sec')
    
    # 정상입력인지 확인
    addresses_data = json.loads(addresses_json)

    # 총 개수 확인
    total_count = len(addresses_data)
    print(f'Total number of entries: {total_count}')

    # address_name이 있는지 확인
    missing_addresses = []
    for index, entry in enumerate(addresses_data):
        if 'address_name' not in entry:
            missing_addresses.append(index)

    # 결과 출력
    if missing_addresses:
        print(f'Missing address_name in entries: {missing_addresses}, {len(missing_addresses)}개')
    else:
        print('All entries have address_name.')


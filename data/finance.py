import pandas as pd
import json, requests, datetime


def bok_eos_api(code='', counts=10000, date_gap='MM', date_start='20011201', date_end=None, code2="?", code3="?"):

    r"""한국은행 OPENAPI 수집기"""
    if date_end == None: date_end = datetime.date.today().strftime("%Y%m%d") # 오늘날짜
    # Process 1 : api key 값 추출
    # with open('./_keys.json', 'r') as f:
    #     apiKey = json.loads(f.read())['bokey']
    apiKey = "YOWLAS8MI7X427J1231C"

    # API link 주소 생성기
    url = f'http://ecos.bok.or.kr/api/StatisticSearch/{apiKey}/json/kr/1/{counts}/{code}/{date_gap}/{date_start}/{date_end}/{code2}/{code3}'
    response = requests.get(url).content.decode('utf-8')
    response_dict = json.loads(response)
    response_key  = list(response_dict.keys())[0]
    
    # 유효값을 호출한 경우
    if response_key == 'StatisticSearch':
        response_data = response_dict[response_key]['row'] # 유효값 Data 추출하기
        response_dataframe = pd.DataFrame(response_data) 
        response_dataframe['DATA_VALUE'] = list(  # DATA_VALUE 텍스트를 숫자로 변환
            map(lambda x : float(x),  response_dataframe['DATA_VALUE'])) 
       
        # 월간 정보인 경우, 날짜값 추가
        # https://stackoverflow.com/questions/37354105/find-the-end-of-the-month-of-a-pandas-dataframe-series
        if date_gap == 'MM':
            response_dataframe['TIME'] = pd.to_datetime(
                response_dataframe['TIME'], format='%Y%m')
        
        # 내부에 여러개 테이블이 추가되어 있는 경우, 내용 출력하기
        if len(set(response_dataframe['ITEM_CODE1'])) > 1:
            print(f"Code2 items : {sorted(set(response_dataframe['ITEM_CODE1']))}")
        if len(set(response_dataframe['ITEM_CODE2'])) > 1:
            print(f"Code3 items : {sorted(set(response_dataframe['ITEM_CODE2']))}")
        return response_dataframe

    # 오류값이 호출된 경우
    else:
        print(response_dict)
        return None
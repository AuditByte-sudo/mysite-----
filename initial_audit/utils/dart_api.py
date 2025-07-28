import requests
import io
import zipfile
import xmltodict
import pandas as pd
from datetime import datetime, timedelta


DART_API_KEY = '715ad327459d41eb1cf8f574cce7adea607efec2'

def get_corp_code(corp_name):
    '''
    :param corp_name: 기업이름
    :return: 기업의 DART 고유번호를 반환한다.
    '''
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    params = {
        "crtfc_key": DART_API_KEY
    }
    resp = requests.get(url, params=params)

    f = io.BytesIO(resp.content)
    zfile = zipfile.ZipFile(f)
    xml = zfile.read("CORPCODE.xml").decode("utf-8")
    dict_data = xmltodict.parse(xml)

    data = dict_data['result']['list']
    df = pd.DataFrame(data)

    result = df[df['corp_name'] == corp_name]
    corp_code = result['corp_code'].iloc[0] if not result.empty else None

    return corp_code



def get_report(corp_code, period):
    '''
    :param corp_code: 기업의 고유번호
    :param period: 조회기간
    :return: 기업의 최근 사업보고서의 번호를 이용하여 DART의 해당 사업보고서 페이지로 연결되는 url을 반환한다.
    '''
    url = "https://opendart.fss.or.kr/api/list.json"

        # 오늘 날짜 기준으로 시작일은 1년 전
    end_date = datetime.today().strftime('%Y%m%d')
    start_date = (datetime.today() - timedelta(days=365*period)).strftime('%Y%m%d')

    params = {
        'crtfc_key': DART_API_KEY,
        'corp_code': corp_code,
        'bgn_de': start_date,
        'end_de': end_date,
        'last_reprt_at': 'Y',
        'pblntf_detail_ty': 'A001',
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == '000':
        if data['list']:
            return data['list'][0] #'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=' + data['list'][0]['rcept_no']  # 첫 번째 보고서 정보 반환
        else:
            return 1
    else:
        return 2



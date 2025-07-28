import requests
import pandas as pd
import os
from datetime import datetime


DART_API_KEY = '715ad327459d41eb1cf8f574cce7adea607efec2'
REPRT_CODE = "11011"


def get_single_index_pivot(corp_code, period, idx_cl_code):
    '''
    :param corp_code: DART 기업 고유번호
    :param period: 조회기간
    :param idx_cl_code: 지표분류 ex) 수익성지표 : M210000 안정성지표 : M220000 성장성지표 : M230000 활동성지표 : M240000
    :return: 해당 기업의 조회기간 동안 지표값을 데이터프레임으로 반환함.
    '''
    years = [str(datetime.now().year - i) for i in range(period)]
    data = []

    for y in years:
        r = requests.get(
            'https://opendart.fss.or.kr/api/fnlttSinglIndx.json',
            params={
                'crtfc_key': DART_API_KEY,
                'corp_code': corp_code,
                'bsns_year': y,
                'reprt_code': REPRT_CODE,
                'idx_cl_code': idx_cl_code
            }
        ).json()

        data += [{
            '지표명': i.get('idx_nm'),
            '연도': i.get('bsns_year'),
            '값': float(i['idx_val']) if i.get('idx_val', '').replace('.', '', 1).isdigit() else None
        } for i in r.get('list', [])]

    if not data:
        return pd.DataFrame(columns=['지표명'] + years[::-1])

    df = pd.DataFrame(data)
    pivot = df.pivot_table(index='지표명', columns='연도', values='값')

    return pivot.round(2)


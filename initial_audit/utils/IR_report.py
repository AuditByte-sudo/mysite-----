import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

def get_code_html(corp_name):
    '''
    :param corp_name: 기업명
    :return: KIND에서 기업명에 따른 종목코드를 구하기 위해 해당 검색화면의 html을 파싱하여 BeautifulSoup 객체를 반환한다.
    '''
    url = "https://kind.krx.co.kr/common/corpList.do"  # F12 → Network 탭에서 실제 요청 URL 복사

    data = {
        'method': 'searchCorpList',
        'forward': 'corpList',
        'pageIndex': '1',
        'beginIndex': '',
        'currentPageSize': '10',
        'delistFlag': 'Y',
        'sub': '',
        'kwd': '',
        'searchCorp': '',
        'corpName': corp_name,
        'corpNameTmp': corp_name,
        'marketType': 'all',
        }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    encoded_data = urlencode(data).encode('utf-8')

    response = requests.post(url, headers=headers, data=encoded_data)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def get_code(soup, corp_name):
    '''
    :param soup:파싱된 soup 객체. 종목코드에 대한 정보가 들어있다.
    :param corp_name:기업명
    :return:기업명과 정확히 일치하는 기업의 종목코드를 반환한다.
    '''
    for tr in soup.find_all('tr'):
        a_tag = tr.find('a', id='CorpInfo')
        if a_tag:
            a_text = a_tag.get_text(strip=True)
            if a_text == corp_name:
                td = tr.find('td', class_='first txc')
                if td:
                    return td.get_text(strip=True)
    return None


def get_ir_html(corp_code, corp_name):
    '''
    :param corp_code: KIND 에서 IR자료 검색을 위한 종목코드
    :param corp_name: 기업명
    :return: IR자료실에서 입력받은 종목코드에 해당되는 기업의 IR자료가 담긴 html파일을 파싱하여 BeautifulSoup 객체로 저장한다.
    '''

    url = "https://kind.krx.co.kr/corpgeneral/irschedule.do"  # 실제 POST 요청 URL로 바꿔야 함

    data = {
        'method': 'searchIRMaterialsSub',
        'paxreq': '',
        'outsvcno': '',
        'currentPageSize': '15',
        'pageIndex': '',
        'searchCodeType': 'char',
        'repIsuSrtCd': 'A' + corp_code,  # A + 종목코드
        'irSeq': '',
        'forward': 'searchirmaterials_sub',
        'searchCorpName': corp_name, #회사명
        'resoroomType': '',
        'searchFromDate': '1999-01-01',
        'searchToDate': '2025-08-26',
        'marketType': '',
        'searchName': corp_name, #회사명
        'kosdaqSegment': '',
        'title': '',
        'fromDate': '1999-01-01',
        'toDate': '2025-08-26',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.post(url, data=data, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


def get_ir_report(soup, corp_name):
    '''
    :param soup: IR자료의 pdf 주소가 담긴 soup 객체
    :param corp_name: 기업명
    :return: IR자료의 pdf를 반환한다.
    '''
    for row in soup.select('tbody tr'):
        a = row.select_one('a[onclick^="companysummary_open"]')
        if a and a.text.strip() == corp_name:
            return row.select_one('a.btn.attach_file')['href']
    return None

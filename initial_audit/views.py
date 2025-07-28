from django.shortcuts import render
from django.http import HttpResponse
from .utils.dart_api import get_corp_code, get_report
from .utils.IR_report import get_code_html, get_code, get_ir_html, get_ir_report
from .utils.fs_indicator import get_single_index_pivot


# Create your views here.
def index(request):
    '''
    첫 화면을 보여준다.
    '''
    return render(request,'initial_audit/initial_audit_manual.html')


def corp_view(request):
    '''
    조회 버튼을 클릭한 후 연결되는 화편을 보여준다.
    '''
    if request.method == 'GET':
        corp_name = request.GET.get('corp_name')
        period = int(request.GET.get('period'))


        #1. 사업보고서
        corp_code = get_corp_code(corp_name)
        report = get_report(corp_code, period)
        if not corp_code:
            return render(request, 'initial_audit/initial_audit_result.html', {'corp_name': corp_name,
            'period': period,
            'corp_code': '기업이름을 찾을 수 없습니다.',})


        #2. IR자료
        soup = get_code_html(corp_name)
        stock_code = get_code(soup, corp_name)
        soup2 = get_ir_html(stock_code, corp_name)
        url_detail = get_ir_report(soup2, corp_name)

        if url_detail:
            ir_url = "https://kind.krx.co.kr" + url_detail
        else:
            ir_url = "KIND의 IR자료가 존재하지 않습니다."


        #3. 최근 n년간 주요 재무지표
        index_types = {
            '수익성지표': 'M210000',
            '안정성지표': 'M220000',
            '성장성지표': 'M230000',
            '활동성지표': 'M240000',
        }

        tables = {}

        for name, index_code in index_types.items():
            df = get_single_index_pivot(corp_code, period, index_code)
            tables[name] = df.to_html(classes='table', index=True)

        return render(request, 'initial_audit/initial_audit_result.html', {
            'corp_name': corp_name,
            'period': period,
            'corp_code': corp_code,
            'report_nm' : report['report_nm'],
            'rcept_dt' : report['rcept_dt'],
            'report_url' : 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=' + report['rcept_no'],
            'ir_url' : ir_url,
            'tables': tables,
        })

    return render(request, 'initial_audit/initial_audit_manual.html')
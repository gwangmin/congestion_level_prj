from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse
import time
from django.core.paginator import Paginator
import math
from .models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

template_dir = 'cctv/'

def paging(models, page_num):
    '''
    Paging

    models: entire models
    page_num: current page_num string. e.g. req.GET.get('page', '1')

    return: current page, page_range
    '''
    # get current page
    # 한 페이지당 10개
    paginator = Paginator(models, 10) # invalid page number를 자동으로 처리함
    page = paginator.get_page(page_num)
    # calc page range
    # 1~10, 11~20, ... 이런 식으로 페이지 버튼 구성
    page_num = int(page_num)
    max_page = math.ceil(len(models) / 10)
    min_ = 1
    max_ = 10
    while True:
        if min_ <= page_num <= max_:
            if max_ <= max_page:
                page_range = range(min_, max_ + 1)
            else:
                page_range = range(min_, max_page + 1)
            break
        else:
            min_ += 10
            max_ += 10
    return page, page_range

# Create your views here.
def index(req):
    '''
    main(first) page
    '''
    return render(req, template_dir + 'index.html')

def search(req):
    '''
    facility search

    TODO: 나중에 완성
    '''
    q = req.GET.get('q', '')
    facilities = Facility.objects.all()
    if q:
        pass

@csrf_exempt
def connection_test(req):
    '''
    # test
    '''
    return HttpResponse(req)

def show_congestion(req, building_id):
    '''
    building_id: building id
    '''
    def get_congestion():
        '''
        yield current congestion level every 5 seconds
        '''
        while True:
            # get current congestion level
            building = get_object_or_404(Building, pk=building_id)
            congest_lv = building.congest_lv
            yield congest_lv.encode('utf-8')
            time.sleep(5)
    response = StreamingHttpResponse(get_congestion(), content_type='text/plain')
    return response

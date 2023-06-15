from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse
import time
from django.core.paginator import Paginator
import math
from .models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json

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
    q = req.GET.get('q', '')
    return render(req, template_dir + 'index.html', {'q': q})

def search(req):
    '''
    facility search
    '''
    q = req.GET.get('q', '')
    if q == '': return HttpResponse('require keyword')

    facilities = Facility.objects.all()
    buildings = Building.objects.all()
    facilities = facilities.filter(
        Q(name__icontains=q) |
        Q(intro__icontains=q) |
        Q(addr__icontains=q) |
        Q(web_addr__icontains=q) |
        Q(phone_num__icontains=q)
    ).distinct()
    buildings = buildings.filter(
        Q(name__icontains=q) |
        Q(intro__icontains=q)
    ).distinct()

    facilities = set(facilities)
    for building in buildings:
        facilities.add(building.facility)

    return render(req, template_dir + 'search_result.html', {'facilities': facilities, 'q': q})

@csrf_exempt
def connection_test(req):
    '''
    # test
    '''
    return HttpResponse(req)

def show_congestion(req, building_id):
    '''
    Show congestion level
    
    building_id: building id
    '''
    building = get_object_or_404(Building, pk=building_id)
    
    context = {'building': building, 'facility': building.facility}
    return render(req, template_dir + 'congest_viewer.html', context)

def get_congest(req, building_id):
    '''
    get current congestion level
    '''
    building = get_object_or_404(Building, pk=building_id)
    congest_lv = building.congest_lv
    return HttpResponse(congest_lv)

def update_congest(req):
    '''
    Receive congestion level from http post json.
    And save it to db

    TODO
    '''
    if req.method == 'POST':
        recv_json = json.loads(req.body)
        # retrieve data

        # building = cctv.building
        # building.congest_lv = retrieved_congest_lv
        # building.save()

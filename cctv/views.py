from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
import math
import json
import datetime
from .models import *
from .forms import *

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

@csrf_exempt
def update_congest(req):
    '''
    Receive congestion level from http post json.
    And save it to db

    TODO
    '''
    if req.method == 'POST':
        recv_json = json.loads(req.body)
        '''
        - json -
        fname: facility name, nametag: id string, value: float [0,1], timestamp
        '''
        # get cctv from nametag, facility
        cctv = CCTV.objects.get(pk=int(recv_json['nametag']))
        # parse congestion level from value
        congest_lv = float(recv_json['value'])
        if congest_lv < .25:
            congest_label = '여유 ' + str(congest_lv)
        elif congest_lv < .5:
            congest_label = '보통 ' + str(congest_lv)
        elif congest_lv < .75:
            congest_label = '혼잡 ' + str(congest_lv)
        else:
            congest_label = '매우혼잡 ' + str(congest_lv)
        # save Statistics using value, timestamp
        stat = Statistics(building=cctv.building, congest_lv=congest_lv)
        stat.time = datetime.datetime.fromtimestamp(float(recv_json['timestamp']))
        stat.save()

        # save congestion level for user:
        building = cctv.building
        building.congest_lv = congest_label
        building.save()

        return HttpResponse('ok')

def get_facility(req):
    '''
    Request with fname by GET param, send facility info as json.
    {
        facility1_name:{
            'intro':'...',
            'addr':'...',
            'web_addr':'...',
            'phone_num':'...',
            'buildings':{
                building1_name:{
                    'intro':'...',
                    'base':'...',
                    'congest_lv':<congestion level value>,
                    'cctvs':{
                        cctv1_id:{
                            'rtsp_url':'...',
                            'rt_base':'...',
                        },
                        cctv2_id...
                    }
                },
                building2_name...
            }
        },
        facility2_name...
    }
    '''
    if req.method == 'GET':
        # get fname
        facility_name = req.GET.get('fname', '')
        if facility_name == '':
            return HttpResponse('fname required')
        # get list
        data = {}
        facilities = Facility.objects.filter(name__icontains=facility_name)
        for facility in facilities:
            data[facility.name] = {'intro':facility.intro, 'addr':facility.addr, 'web_addr':facility.web_addr,
                                   'phone_num':facility.phone_num, 'buildings':{}}
            for building in facility.building_set.all():
                data[facility.name]['buildings'][building.name] = {'intro':building.intro, 'base':building.base,
                                                                   'congest_lv':building.congest_lv, 'cctvs':{}}
                for i, cctv in enumerate(building.cctv_set.all()):
                    data[facility.name]['buildings'][building.name]['cctvs'][cctv.id] = {'rtsp_url': cctv.rtsp_url,
                                                                                         'rt_base': cctv.rt_base}
        return HttpResponse(json.dumps(data))


@login_required(login_url='accounts:login')
def edit_facility(req):
    '''
    Edit facility info
    '''
    facility = req.user.facility
    if req.method == 'GET':
        form = FacilityForm(instance=facility)
    elif req.method == 'POST':
        form = FacilityForm(req.POST, instance=facility)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/')
    return render(req, template_dir + 'edit_form.html', {'form': form})


@login_required(login_url='accounts:login')
def add_building(req):
    '''
    Add new building in my facility
    '''
    if req.method == 'GET':
        form = BuildingForm()
    elif req.method == 'POST':
        form = BuildingForm(req.POST)
        if form.is_valid():
            b = form.save(commit=False)
            b.facility = req.user.facility
            b.save()
            return redirect('cctv:show_buildings')
    return render(req, template_dir + 'edit_form.html', {'form': form})

@login_required(login_url='accounts:login')
def edit_building(req, building_id):
    '''
    Edit specified building
    '''
    building = get_object_or_404(Building, pk=building_id)
    if req.user.facility != building.facility:
        messages.error(req, '적절한 권한이 없습니다.')
        return redirect('/')
    if req.method == 'GET':
        form = BuildingForm(instance=building)
    elif req.method == 'POST':
        form = BuildingForm(req.POST, instance=building)
        if form.is_valid():
            form.save(commit=True)
            return redirect('cctv:show_buildings')
    return render(req, template_dir + 'edit_form.html', {'form': form})

@login_required(login_url='accounts:login')
def show_buildings(req):
    '''
    Show buildings in my facility
    '''
    building_list = req.user.facility.building_set.all()
    return render(req, template_dir + 'building_list.html', {'building_list': building_list})

@login_required(login_url='accounts:login')
def remove_building(req, building_id):
    '''
    Remove specified building
    '''
    building = get_object_or_404(Building, pk=building_id)
    if building.facility != req.user.facility:
        messages.error(req, '삭제권한이 없습니다.')
        return redirect('/')
    building.delete()
    return redirect('cctv:show_buildings')


@login_required(login_url='accounts:login')
def add_cctv(req):
    '''
    Add new cctv
    '''
    if req.method == 'GET':
        form = CCTVForm()
    elif req.method == 'POST':
        form = CCTVForm(req.POST)
        if form.is_valid():
            cctv = form.save(commit=False)
            cctv.save()
            messages.info(req, '방금 추가한 CCTV의 id는 ' + str(cctv.id) + '입니다.')
            return redirect('cctv:show_cctvs')
    return render(req, template_dir + 'edit_form.html', {'form': form})

@login_required(login_url='accounts:login')
def edit_cctv(req, cctv_id):
    '''
    Edit specified cctv
    '''
    cctv = get_object_or_404(CCTV, pk=cctv_id)
    if cctv.building.facility != req.user.facility:
        messages.error(req, '적절한 권한이 없습니다.')
        return redirect('/')
    if req.method == 'GET':
        form = CCTVForm(instance=cctv)
    elif req.method == 'POST':
        form = CCTVForm(req.POST, instance=cctv)
        if form.is_valid():
            form.save(commit=True)
            return redirect('cctv:show_cctvs')
    return render(req, template_dir + 'edit_form.html', {'form': form})

@login_required(login_url='accounts:login')
def show_cctvs(req):
    '''
    show my cctv list
    '''
    cctv_list = []
    for building in req.user.facility.building_set.all():
        cctv_list.extend(list(building.cctv_set.all()))
    return render(req, template_dir + 'cctv_list.html', {'cctv_list': cctv_list})

@login_required(login_url='accounts:login')
def remove_cctv(req, cctv_id):
    '''
    Remove specified cctv
    '''
    cctv = get_object_or_404(CCTV, pk=cctv_id)
    if cctv.building.facility != req.user.facility:
        messages.error(req, '적절한 권한이 없습니다.')
        return redirect('/')
    cctv.delete()
    return redirect('cctv:show_cctvs')

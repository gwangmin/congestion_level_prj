from django.urls import path
from . import views

app_name = 'cctv'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('view/<int:building_id>/', views.show_congestion, name='view'),
    path('get/<int:building_id>/', views.get_congest, name='get_congest'),

    path('update_congest/', views.update_congest, name='update_congest'),
    path('set_base/', views.set_base, name='set_base'),

    path('edit/facility/', views.edit_facility, name='edit_facility'),

    path('add/building/', views.add_building, name='add_building'),
    path('show/buildings/', views.show_buildings, name='show_buildings'),
    path('edit/building/<int:building_id>/', views.edit_building, name='edit_building'),
    path('remove/building/<int:building_id>/', views.remove_building, name='remove_building'),

    path('add/cctv/', views.add_cctv, name='add_cctv'),
    path('show/cctvs/', views.show_cctvs, name='show_cctvs'),
    path('edit/cctv/<int:cctv_id>/', views.edit_cctv, name='edit_cctv'),
    path('remove/cctv/<int:cctv_id>/', views.remove_cctv, name='remove_cctv'),

    path('connection_test/', views.connection_test, name='connection_test'),
    path('get/info/facility/', views.get_facility, name='get_facility_info'),
]

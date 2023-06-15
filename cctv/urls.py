from django.urls import path
from . import views

app_name = 'cctv'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('view/<int:building_id>/', views.show_congestion, name='view'),
    path('get/<int:building_id>/', views.get_congest, name='get_congest'),

    path('connection_test/', views.connection_test, name='connection_test'),
]

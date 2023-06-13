from django.urls import path
from . import views

app_name = 'cctv'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('show/<int:building_id>/', views.show_congestion, name='show'),

    path('connection_test/', views.connection_test, name='connection_test'),
]

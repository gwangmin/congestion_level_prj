from django.urls import path
from . import views

app_name = 'cctv'

urlpatterns = [
    path('', views.HelloView, name='hello')
]

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def HelloView(req):
    return HttpResponse('hello')

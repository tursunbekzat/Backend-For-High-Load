from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def basic_view(request):
    return HttpResponse("Hello, Blog!")

from django.http import HttpResponse
from django.shortcuts import render
#mysite = receiptRecognition
#polls = shopperHelper

def index(request):
    return HttpResponse("Hello World!")

from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import user, item
from .forms import loginForm

from django.shortcuts import render
#mysite = receiptRecognition
#polls = shopperHelper

def index(request):
    return HttpResponse("Hello World!")

def login(request):
    if request.session.has_key('currentUser'):
        return render(request, 'shopperHelper/login.html')
        #redirect('/shopperHelper/landing')
    else:
        if request.method == 'POST':
            loginFormData = loginForm(request.POST)
            if loginFormData.is_valid():
                rawLoginData = loginFormData.cleaned_data[login_form_data]
                
                #loginFormData.save()
                return render(request, 'shopperHelper/login.html')
            else:
                return HttpResponseRedirect('/shopperHelper/login')
        else:
            loginFormData = loginForm()
            args = {'loginForm': loginForm}
            return render(request, 'shopperHelper/login.html', args)

def landing(request):
    return render(request, 'shopperHelper/landing.html')

def createGroup(request):
    return render(request, 'shopperHelper/create_group.html')

def addReceipt(request):
    return render(request, 'shopperHelper/addReceipt.html')

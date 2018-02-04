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
    if request.session.has_key('polyCardData'):
        return render(request, 'shopperHelper/login.html')
    else:
        if request.method == 'POST':
            loginFormData = studentLoginForm(request.POST)
            if loginForms.is_valid():
                return render(request, 'shopperHelper/login.html')
        else:
            loginFormInput = loginForm()
            args = {'loginForm': loginFormInput}
            return render(request, 'shopperHelper/login.html', args)

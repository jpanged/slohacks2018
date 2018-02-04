from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Item, Receipt
from .forms import loginForm,createGroupForm, addReceiptForm

from django.shortcuts import render
#mysite = receiptRecognition
#polls = shopperHelper

import cv2

def index(request):
    return HttpResponse("Hello World!")

def login(request):

    if request.session.has_key('currentUser'):
        #return render(request, 'shopperHelper/login.html')
        redirect('/shopperHelper/landing')

        if request.method == 'POST':
            form = loginForm(request.POST or None)

            if form.is_valid():
                raw_Phone_Data = int(form.cleaned_data['login_form_data'])
                registeredStatus = None

                all_Users = list(User.objects.all())

                model_Attribute = 'phone'

                i = 0
                while i < len(all_Users):
                    userPhoneNumber = int(User.objects.values(model_Attribute)[i][model_Attribute])

                    if userPhoneNumber == raw_Phone_Data:
                        registeredStatus = True
                        break
                    i += 1

                if registeredStatus == True:
                    request.session['currentUser'] = str(raw_Phone_Data)
                    return HttpResponseRedirect('/shopperHelper/landing')
                else:
                    return HttpResponseRedirect('/shopperHelper/register')

                #loginFormData.save()
                return render(request, 'shopperHelper/login.html')
            else:
                return HttpResponseRedirect('/shopperHelper/login')
        else:
            form = loginForm()
            args = {'form': form}
            return render(request, 'shopperHelper/login.html', args)

def landing(request):
    return render(request, 'shopperHelper/landing.html')

def createGroup(request):
    GroupForm = createGroupForm()
    args = {'groupForm': GroupForm}
    return render(request, 'shopperHelper/create_group.html', args)

def addReceipt(request):

    if request.method == 'POST':
        form = addReceiptForm(request.POST, request.FILES)
        if form.is_valid():

            newReceipt = Receipt(image=form.cleaned_data['image'])
            # m = ExampleModel.objects.get(pk=course_id)
            # m.model_pic = form.cleaned_data['image']
            newReceipt.save()
            print(form.cleaned_data['image'])
            imageLocation = Receipt.objects.filter(image=form.cleaned_data['image'])
            print(imageLocation)
            image = cv2.imread("receipt_images/{}".format(form.cleaned_data['image']))
            cv2.imshow("test", image)
            cv2.waitKey(0)

            return HttpResponse('image upload success')
        else:
            return HttpResponse(':(')
    else:
        addReceiptFormData = addReceiptForm()
        args = {'receiptForm': addReceiptFormData}
        return render(request, 'shopperHelper/addReceipt.html', args)

def register(request):
    return render(request, 'shopperHelper/register.html')

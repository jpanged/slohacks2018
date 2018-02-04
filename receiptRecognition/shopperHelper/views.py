from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import forms
from django.core.exceptions import ObjectDoesNotExist
import time
from .models import User, Item, Receipt
from .forms import loginForm,createGroupForm, addReceiptForm

from django.shortcuts import render

import cv2
import os

import io
import json
import re
# import file

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from google.oauth2 import service_account

def getJSONofCurrentUser(sessionData):
    currentUserData = User.objects.get(phone=sessionData).__dict__
    return currentUserData

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

                print(registeredStatus)



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
    if request.session.has_key('currentUser'):
        userData = getJSONofCurrentUser(request.session['currentUser'])
        args = {'userFirstName': userData['first_Name']}
        return render(request, 'shopperHelper/landing.html',args)
    else:
        return redirect('/app_Transaction/')

def createGroup(request):
    if request.session.has_key('currentUser'):
        GroupForm = createGroupForm()
        args = {'groupForm': GroupForm}
        return render(request, 'shopperHelper/create_group.html', args)
    else:
       return redirect('/app_Transaction/')

def addReceipt(request):
    if request.session.has_key('currentUser'):
        if request.method == 'POST':
            form = addReceiptForm(request.POST, request.FILES)
            if form.is_valid():
                receiptID = time.time()
                newReceipt = Receipt(image=form.cleaned_data['image'],owner=User.objects.get(phone=request.session['currentUser']))
                # m = ExampleModel.objects.get(pk=course_id)
                # m.model_pic = form.cleaned_data['image']
                newReceipt.save()
                print(form.cleaned_data['image'])
                imageLocation = Receipt.objects.filter(image=form.cleaned_data['image'])
                print(imageLocation)
                image = cv2.imread("media/receipt_images/{}".format(form.cleaned_data['image']))
                cv2.imshow("test", image)
                cv2.waitKey(0)


                credentials = service_account.Credentials.from_service_account_file("..//..//slohacks-feb4bf79b42b.json")

                # Instantiates a client
                client = vision.ImageAnnotatorClient(credentials=credentials)

                file_name = os.path.join(os.path.dirname(__file__), "media/receipt_images/{}")

                with io.open(file_name, 'rb') as image_file:
                    content = image_file.read()

                image = types.Image(content=content)

                response = client.text_detection(image=image)
                document = response.full_text_annotation
                texts = response.text_annotations
                blockBounds.write(str(response))

                t = response.text_annotations[0].description

                r = re.search('([0-9]|\s]*)[0-9|\s]*-[0-9|\s]*', t)
                i = r.end(0)

                t = t[i+1:]

                r = re.search('\n[S]*[U]*[B]*[T]*[O]*[T]*[A]*[L]*\n', t)
                i = r.start(0)

                t = t[:i]

                r = re.findall('\n[0-9]+\s.+', t) # might need to remove \n for other OS in deployment

                no_and_names = []
                for p in r:
                    no_and_names.append(p)

                item_prices = []
                r = re.findall('[0-9]+\.[0-9]+', t)
                for p in r:
                    item_prices.append(p)


                item_nos = []
                item_names = []
                for element in no_and_names:
                    i = element.find(' ')
                    item_nos.append(element[1:i])
                    item_names.append(element[i + 1:])

                item_nos.extend(['0', '0', '0'])
                item_names.extend(['SUBTOTAL', 'TAX', 'TOTAL'])

                master_list = []
                min_length = min([len(item_nos), len(item_names), len(item_prices)])
                for i in range(0, min_length):
                    master_list.append((item_nos[i], item_names[i], item_prices[i]))

                for val in master_list:
                    item = Item(val[0], val[1], val[2])
                    item.save()

                return HttpResponse('image upload success')
            else:
                return HttpResponse(':(')
        else:
            addReceiptFormData = addReceiptForm()
            userData = getJSONofCurrentUser(request.session['currentUser'])
            args = {'receiptForm': addReceiptFormData, 'userFirstName': userData['first_Name']}
            return render(request, 'shopperHelper/addReceipt.html', args)
    else:
        return redirect('/app_Transaction')

def register(request):
    if request.session.has_key('currentUser'):
        return render(request, 'shopperHelper/register.html')
    else:
       return redirect('/app_Transaction/')

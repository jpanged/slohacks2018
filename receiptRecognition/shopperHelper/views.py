from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import forms
from django.core.exceptions import ObjectDoesNotExist
import time
from .models import User, Item, Receipt, Group
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

#Declare global variables
global master_list


def getJSONofCurrentUser(sessionData):
    currentUserData = User.objects.get(phone=sessionData).__dict__
    return currentUserData

def index(request):
    return HttpResponse("Hello World!")

def login(request):

    if request.session.has_key('currentUser'):
        #return render(request, 'shopperHelper/login.html')
        return redirect('/shopperHelper/landing')
    else:
        if request.method == 'POST':
            form = loginForm(request.POST or None)
            print(form.errors)
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
        return redirect('/shopperHelper/')

def createGroup(request):
    if request.session.has_key('currentUser'):
        if request.method == 'POST':
            form = createGroupForm(request.POST or None)
            groupName = form.cleaned_data['group_name']
            group_members = form.cleaned_data['group_members']
            print(group_members)
        else:
            GroupForm = createGroupForm()
            args = {'groupForm': GroupForm}
            return render(request, 'shopperHelper/create_group.html', args)
    else:
       return redirect('/shopperHelper/')

def addReceipt(request):
    if request.session.has_key('currentUser'):
        if request.method == 'POST':
            form = addReceiptForm(request.POST, request.FILES)
            if form.is_valid():
                receiptIDText = time.time()
                newReceipt = Receipt(image=form.cleaned_data['image'],owner=User.objects.get(phone=request.session['currentUser']),groupAssigned=Group.objects.get(name=form.cleaned_data['group_Assigned']),receiptID=receiptIDText)
                newReceipt.save()
                request.session['receiptID'] = newReceipt.receiptID
                #print(form.cleaned_data['image'])
                imageLocation = Receipt.objects.filter(image=form.cleaned_data['image'])
                #print("#########################################\###########################")
                #print(imageLocation)
                image = cv2.imread("media/receipt_images/{}".format(form.cleaned_data['image']))
                # --SHOWS IMAGE USING OPENCV--
                #cv2.imshow("imageLocation", image)
                #cv2.waitKey(0)

                credentials = service_account.Credentials.from_service_account_file("..//slohacks-servicekey.json")

                # Instantiates a client
                client = vision.ImageAnnotatorClient(credentials=credentials)

                file_name =  "media/receipt_images/{}".format(form.cleaned_data['image'])

                with io.open(file_name, 'rb') as image_file:
                    content = image_file.read()

                image = types.Image(content=content)

                response = client.text_detection(image=image)
                document = response.full_text_annotation
                texts = response.text_annotations
                # blockBounds.write(str(response))

                t = response.text_annotations[0].description

                #print (t)

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

                ##MAKE LIST GLOBAL TO ACCESS IN DIFFERENT VIEW##
                master_list = []
                min_length = min([len(item_nos), len(item_names), len(item_prices)])
                for i in range(0, min_length):
                    master_list.append((item_nos[i], item_names[i], item_prices[i]))

                print (master_list)

                for val in master_list:
                    #print(val)
                    itemT = Item(number = val[0], name = val[1], price = val[2])
                    itemT.save()
                    #print(newReceipt)
                    newReceipt.items.add(itemT)
                    newReceipt.save()
                    # b = Item.objects.filter(number=val[0], name=val[1], price=val[2]).exists()
                    # if b == False:
                    #     print(val)
                    #     itemT = Item(number = val[0], name = val[1], price = val[2])
                    #     itemT.save()
                    #     newReceipt(item=itemT)
                    #     newReceipt.save()

                #return HttpResponse('image upload success')
                #return redirect('/shopperHelper/checkBoxPage/')
                args = {'masterList': master_list}
                return redirect('/shopperHelper/select_items/', args)
            else:
                return HttpResponse(':(')
        else:
            addReceiptFormData = addReceiptForm()
            userData = getJSONofCurrentUser(request.session['currentUser'])
            args = {'receiptForm': addReceiptFormData, 'userFirstName': userData['first_Name']}
            return render(request, 'shopperHelper/addReceipt.html', args)
    else:
        return redirect('/shopperHelper')

def checkBoxPage(request):
    if request.session.has_key('currentUser'):
        return render(request, 'shopperHelper/checkBoxPage.html')
    else:
        return redirect('/shopperHelper/')

def register(request):
    if request.session.has_key('currentUser'):
        return render(request, 'shopperHelper/register.html')
    else:
       return redirect('/shopperHelper/')

def selectItems(request):
    if request.session.has_key('currentUser'):
        items_on_receipt_list = []
        print (master_list)
        '''
        all_items = Receipt.objects.get(receiptID=request.session['receiptID'])


        for i in range(len(list(all_items.items.all())    )):
            number = all_items[i].items.number
            name = all_items[i].items.name
            price = all_items[i].items.price
            # partData = {"PartName": part, "PartQty": partQty}
            registered_Items_inner = [number, name, price]
            items_on_receipt_list.append(registered_Items_inner)
        args = {'items_on_receipt': items_on_receipt_list}
        return render(request, 'shopperHelper/selectItems.html', args)
        '''
        return render(request, 'shopperHelper/selectItems.html')


    else:
        return redirect('/shopperHelper/')

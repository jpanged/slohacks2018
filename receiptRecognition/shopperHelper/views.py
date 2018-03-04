from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import forms
from django.core.exceptions import ObjectDoesNotExist
import time
from .models import User, Item, Receipt, Group
from .forms import loginForm,createGroupForm, addReceiptForm, registrationForm

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
                    print ('You should be redirected now')
                    return HttpResponseRedirect('/shopperHelper/register')
            else:
                return HttpResponseRedirect('/shopperHelper/login')
        else:
            form = loginForm()
            args = {'form': form}
            return render(request, 'shopperHelper/login.html', args)


def landing(request):
    if request.session.has_key('currentUser'):
        userData = getJSONofCurrentUser(request.session['currentUser'])
        args = {'userFirstName': userData['first_Name'], 'createGroupSuccessFlag' : "True"}
        return render(request, 'shopperHelper/landing.html',args)
    else:
        return redirect('/shopperHelper/')

def createGroup(request):
    if request.session.has_key('currentUser'):
        if request.method == 'POST':
            form = createGroupForm(request.POST or None)
            #print (form.errors) --for debugging purposes
            if form.is_valid():

                # groupName = form.cleaned_data['group_name']
                # group_members = form.cleaned_data['group_members']
                groupName = form.cleaned_data['name']
                group_members = form.cleaned_data['members']
                form.save()
                return redirect('/shopperHelper/landing/?createGroupSuccessFlag=True')
            else:
                return HttpResponseRedirect('/shopperHelper/create_group')
        else:
            GroupForm = createGroupForm()
            userData = getJSONofCurrentUser(request.session['currentUser'])
            args = {'groupForm': GroupForm, 'userFirstName': userData['first_Name']}
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
                print ('--------------------------------------')

                currentGroup = newReceipt.groupAssigned
                request.session['group'] = str(currentGroup)
                #members = Group.objects.filter(name=currentGroup)

                members_qs = Group.objects.filter(name=currentGroup).values_list('members', flat = True).order_by('id')

                membersList= []

                for item in members_qs:
                    phoneNumber = User.objects.get(pk = item)
                    membersList.append(phoneNumber)

                phoneNumberOfGroupMembersList = []
                for number in membersList:
                    phoneNumberOfGroupMembersList.append(str(number))
                # print (type(nameOfGroupMembers))
                # print (nameOfGroupMembers[0])
                # print (type(nameOfGroupMembers[0]))
                # print (str(nameOfGroupMembers[0]))
                print (phoneNumberOfGroupMembersList)

                print (type(phoneNumberOfGroupMembersList[0]))

                request.session['phoneNumberOfGroupMembersList'] = phoneNumberOfGroupMembersList

                newReceipt.save()

                request.session['receiptID'] = newReceipt.receiptID
                imageLocation = Receipt.objects.filter(image=form.cleaned_data['image'])
                image = cv2.imread("media/receipt_images/{}".format(form.cleaned_data['image']))

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

                t = response.text_annotations[0].description

                r = re.search('([0-9]|\s]*)[0-9|\s]*-[0-9|\s]*', t)
                #Trying to implment regex for member numbers
                #r = re.search('[0-9]*[A-Z]*[\s]*[M]*[e]*[m]*[b]*[e]*[r]*[\s]*[0-9|\s]*', t)
                #r = re.search('[a-zA-Z0-9_|\s]*[M]*[e]*[m]*[b]*[e]*[r]*[\s]*[0-9|\s]*', t)
                #r = re.search('[a-zA-Z0-9|\s]*[Member\s]*[\d{12}*', t)
                #r = re.search('[0-9]\w+\s]*[Member\s]*\d{12}', t)

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

                print (master_list)
                item_list = master_list[:-2]
                print (item_list)

                itemNumList = []
                itemPriceList = []
                for item in item_list:
                    itemNumList.append(item[0])
                    itemPriceList.append((item[2]))

                print (itemNumList)
                print ('########################################')
                itemFloatPriceList = []
                # for item in itemPriceList:
                for i in range(0, len(itemPriceList)):
                    item = float(itemPriceList[i])
                    itemFloatPriceList.append(item)
                print (itemPriceList)

                request.session['itemNumList'] = itemNumList
                request.session['itemFloatPriceList'] = itemFloatPriceList


                #request.session['master_list'] = master_list
                request.session['list'] = item_list



                for val in master_list:

                    itemT = Item(number = val[0], name = val[1], price = val[2])
                    itemT.save()
                    newReceipt.items.add(itemT)
                    newReceipt.save()

                return redirect('/shopperHelper/select_items/?imageUploadSuccessFlag=True')
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
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            form.save()
            args = {'logoutFlag' : "True"}
            return redirect('/shopperHelper/login/?registerFlag=True', args)
    else:
        form = registrationForm()
        args = {'form': form}
        return render(request, 'shopperHelper/register.html', args)

def selectItems(request):
    if request.session.has_key('currentUser'):
        if request.method == 'POST':
            itemData = json.loads(request.POST['itemData'])
            print (itemData)
            receiptList = []
            for name, item in itemData.items():
                print ('------------------------------------')
                print (item)
                print (item.items()) #{'assigned': True, 'userAssigned': '9253535156', 'item': '1'}
                elements = (item['assigned'], item['userAssigned'], item['item'])
                receiptList.append(elements)

                for key, value in item.items():
                    print('{} - {}'.format(key,value))
                    # y=(key,value)
                    # x.append(y)
            print (receiptList)
            receiptList.sort()
            print (receiptList)
            for item in receiptList:
                if item[0] == False:
                    receiptList.remove(item)
            print (receiptList)

            phoneNumberOfGroupMembersList = request.session['phoneNumberOfGroupMembersList']
            itemNumList = request.session['itemNumList']
            itemFloatPriceList = request.session['itemFloatPriceList']

            print (itemFloatPriceList)

            tempList = []
            masterList = []
            print('Start Loop')
            print (len(itemNumList))
            print (len(receiptList))
            print (len(phoneNumberOfGroupMembersList))

            #For 1 user
            dummyList = []
            for k in range(0, len(itemNumList)+1):
                dummyList.append(0)
            masterList.append(dummyList)
            for h in range(0, len(phoneNumberOfGroupMembersList)):
                tempList.append(phoneNumberOfGroupMembersList[h])
                for i in range(0, len(itemNumList)):
                    j = 0
                    while 1:
                        if itemNumList[i] == receiptList[j][2] and phoneNumberOfGroupMembersList[h] == receiptList[j][1]:
                            if receiptList[j][0] == True:
                                tempList.append(1)
                                break
                            else:
                                tempList.append(0)
                                break
                        else:
                            j += 1
                            if j > len(itemNumList):
                                tempList.append(0)
                                break
                masterList.append(tempList)
                tempList = []
            print ('Finish Loop')
            print (masterList)

            itemizedList = []
            itemizedList.append(calc_totals(masterList, itemFloatPriceList))

            print (itemizedList)

            '''
            print (receiptList) #[(True, '5108610831', '1'), (True, '9253535156', '1'), (True, '8189394534', '1')]
                                #[(True, '9253535156', '1'), (True, '5108610831', '1'), (True, '8189394534', '1')]
            receiptList.sort()
            print (receiptList)


            itemNumList = request.session['itemNumList']
            phoneNumberOfGroupMembersList = request.session['phoneNumberOfGroupMembersList']
            print ('-------------------------------------------')
            print (itemNumList) #['1', '44004', '287783', '30669', '18600']
            print (phoneNumberOfGroupMembersList) #['5108610831', '9253535156', '8189394534']

            masterArray = []
            for member in phoneNumberOfGroupMembersList:
                tempArray = []
                for receipt in receiptList:
                    print (receipt[0])
                    if receipt[0] == True:
                        for itemNum in itemNumList:
                            print (receipt[1], receipt[2], itemNum)
                            if receipt[1] == member and receipt[2] == itemNum:
                                tempArray.append('1')
                    else:
                        tempArray.append('0')
                print (tempArray)




            masterArray = []
            i = 0
            for stdTuple in receiptList:
                if stdTuple[0] == True:
                    while i < len(receiptList):
                        tempArray = []
                        if phoneNumberOfGroupMembersList[i] == stdTuple[1]:
                            tempTuple = (stdTuple[1], stdTuple[2])
                            tempArray.append(tempTuple)
                            masterArray.append(tempArray)
                        i += 1
                else:
                    pass

            print (masterArray)
            masterArray.sort()
            print (masterArray)
            # return redirect("/shopperHelper/summary/")
            '''
            return HttpResponse("Hello")
        else:
            item_list = request.session['list'] #takes masterList data from addReceiptView
            phoneNumberOfGroupMembersList = request.session['phoneNumberOfGroupMembersList']
            #print (master_list)
            print (item_list)
            userData = getJSONofCurrentUser(request.session['currentUser'])
            args = {'item_list': item_list, 'userFirstName': userData['first_Name'], 'imageUploadSuccessFlag' : "True", 'phoneNumberOfGroupMembersList' : phoneNumberOfGroupMembersList,}
            return render(request, 'shopperHelper/selectItems.html', args)

    else:
        return redirect('/shopperHelper/')

'''
def summary(request):
    if request.session.has_key('currentUser'):
        # if request.method == 'POST':
        return render(request, 'shopperHelper/summary.html')
        # else:
        #     return render(request, 'shopperHelper/summary.html')

    else:
        return redirect('/shopperHelper/')
'''

# class Item:
#     def __init__(self, price):
#         self.price = price
#
#     def __eq__(self, other):
#         return ((type(other) == Item)
#           and self.price == other.price
#         )
#
#     def __repr__(self):
#         return ("Item({!r})".format(self.price))

def calc_totals(list1, items):
    print("list1: " + str(list1))
    print("item prices: " + str(items))
    list2 = []
    list3 = []
    i = 0
    j = 0
    for j in range(1, len(list1[i])):
        list2.append(0)
        for i in range(1, len(list1)):
            list2[j-1] += list1[i][j]
            #print(list2[j-1])
        #print(list2)
    i = 0
    for i in range(0, len(list2)):
        list2[i] = items[i]/list2[i]
    print("split price per item: " + str(list2))
    i = 0
    j = 0
    for i in range(1, len(list1)):
        list3.append([list1[i][0], 0])
        for j in range(0, len(list2)):
            list3[i-1][1] += list1[i][j+1]*list2[j]
        list3[i-1][1] = round(list3[i-1][1], 2)
    return list3

# list1 = [[0, "i1", "i2", "i3"],["dom", 1, 1, 0],["russ", 1, 1, 1],["alex", 1, 0, 0]]
# item1 = Item(2.99)
# item2 = Item(5.99)
# item3 = Item(9.99)
# items = [item1, item2, item3]
# print("total per person: " + str(calc_totals(list1, items)))

def logout(request):
    try:
        del request.session['currentUser']
    except:
        print("Fail")
        pass
    args = {'logoutFlag' : "True"}
    return redirect('/shopperHelper/login/?logoutFlag=True', args)

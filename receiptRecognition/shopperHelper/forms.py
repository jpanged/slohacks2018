from django import forms
from django.db import models

from .models import User, Item, Group, Receipt


print(list(User.objects.all()))
ALL_MEMBERS = []
for i in range(len(list(User.objects.all()))):
    userC = User.objects.values('phone')[i]['phone']
    ALL_MEMBERS.append(('{}'.format(userC), '{}'.format(userC)))
print(ALL_MEMBERS)

print(list(Group.objects.all()))
ALL_GROUPS = []
for i in range(len(list(Group.objects.all()))):
    groupC = Group.objects.values('name')[i]['name']
    ALL_GROUPS.append(('{}'.format(groupC), '{}'.format(groupC)))
print(ALL_GROUPS)

class loginForm(forms.ModelForm):
    login_form_data = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loginUserInput'}))

    class Meta:
        model = User
        fields = ('phone',)

class registrationForm(forms.ModelForm):
    # r_fname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'r_fname'}))
    # r_lname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'r_lname'}))
    # r_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'r_email'}))
    # r_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'r_phone'}))

    class Meta:
        model = User
        fields = ('first_Name',
                  'last_Name',
                  'email',
                  'phone',)

class createGroupForm(forms.ModelForm):

    #group_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'group_name'}))
    #group_members = forms.CharField(widget=forms.Select(choices=ALL_MEMBERS, attrs={'class': 'form-control', 'id': 'member_name'}))

    class Meta:
        model = Group
        fields = ('name',
                  'members',)
        exclude = ('groupOwner',)

class addReceiptForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn-primary', 'id': 'selectedFile', 'style':"display: none"}))
    # group_Assigned = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'group_assigned'}))
    group_Assigned = forms.CharField(widget=forms.Select(choices=ALL_GROUPS, attrs={'class': 'form-control', 'id': 'group_assigned'}))

    class Meta:
        model = Receipt
        fields = ('image',
                  'groupAssigned',)
        exclude = ('items','owner',)

# class itemSelectForm(forms):

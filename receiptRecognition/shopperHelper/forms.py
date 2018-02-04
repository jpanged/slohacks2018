from django import forms
from django.db import models

from .models import User, Item, Group


class loginForm(forms.ModelForm):
    login_form_data = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loginUserInput'}))

    class Meta:
        model = User
        fields = ('phone',)
'''
class createGroupForm(forms.ModelForm):

    ALL_MEMBERS = sorted(list(user.objects.all()))

    group_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'group_name'}))
    group_members = forms.CharField(widget=forms.Select(choices=ALL_MEMBERS, attrs={'class': 'form-control', 'id': 'partQty'}))

    class Meta:
        model = group
        fields = ('name',
                  'members',)
'''

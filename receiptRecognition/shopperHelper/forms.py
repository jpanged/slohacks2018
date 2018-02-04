from django import forms
from django.db import models

from .models import user, item


class loginForm(forms.ModelForm):
    login_form_data = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'loginUserInput'}))

    class Meta:
        model = user
        fields = ('phone',)

# class createGroupForm(forms.ModelForm):
#

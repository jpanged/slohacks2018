from django import forms
from django.db import models

from .models import user, item


class loginForm(forms.ModelForm):
    login_form_data = forms.CharField(attrs={'class': 'form-control', 'id': 'loginUserInput'},required=True)

    class Meta:
        model = User
        fields = ('phone',)

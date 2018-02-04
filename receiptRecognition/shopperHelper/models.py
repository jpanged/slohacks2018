from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class item(models.Model):
    number = models.CharField(null=True, max_length=200)
    name = models.CharField(null=True, max_length=200)
    price = models.IntegerField(null=True,)
    displayName = models.CharField(null=True, max_length=200)

    def __str__(self):
        return displayName

class user(models.Model):
    first_Name = models.CharField(max_length=100, blank = True)
    last_Name = models.CharField(max_length=100, blank = True)
    #user_Type = models.CharField(max_length=100, default="STUDENT")
    email = models.EmailField(null=True, max_length=100, blank = True)
    #phone = PhoneNumberField()
    phone = models.IntegerField(null=True)

    def __str__(self):
        return phone

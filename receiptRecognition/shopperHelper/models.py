from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Item(models.Model):
    number = models.CharField(null=True, max_length=200)
    name = models.CharField(null=True, max_length=200)
    price = models.IntegerField(null=True,)
    displayName = models.CharField(null=True, max_length=200)

    def __str__(self):
        return self.displayName

class User(models.Model):
    first_Name = models.CharField(max_length=100)
    last_Name = models.CharField(max_length=100)
    # user_Type = models.CharField(max_length=100, default="STUDENT")
    email = models.EmailField(null=True, max_length=100)
    #phone = models.CharField(null=False,max_length=10)
    phone = models.CharField(default = None, blank = True, max_length=10)

    def __str__(self):
        return "{} {}".format(self.first_Name, self.last_Name)

class Group(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    groupOwner = models.ForeignKey('user', null=True, related_name='groupOwner', on_delete=models.CASCADE)

class Receipt(models.Model):
    image = models.ImageField(upload_to = 'receipt_images/', default = 'receipt_images/None/no-image.jpg')
    items = models.ManyToManyField(Item)
    groupAssigned = models.ForeignKey('group', null=True, related_name='groupAssigned', on_delete=models.CASCADE, blank=True)
    owner = models.ForeignKey('user', null=True, related_name='owner', on_delete=models.CASCADE, blank=True)
    receiptID = models.CharField(blank=True,max_length=200)

class ItemOnReceipt(models.Model):
    item = models.ForeignKey('item', null=True, related_name='item', on_delete=models.CASCADE)
    receiptMaster = models.ForeignKey('receipt', null=True, related_name='receiptMaster', on_delete=models.CASCADE)
    usersToSplit = models.ManyToManyField(User)

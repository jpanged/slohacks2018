from django.contrib import admin

# Register your models here.

from .models import Item, User, Group, Receipt, ItemOnReceipt

admin.site.register(Item)
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Receipt)
admin.site.register(ItemOnReceipt)

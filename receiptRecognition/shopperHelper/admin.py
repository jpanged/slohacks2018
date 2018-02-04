from django.contrib import admin

# Register your models here.

from .models import item, user, group, receipt, itemOnReceipt

admin.site.register(item)
admin.site.register(user)
admin.site.register(group)
admin.site.register(receipt)
admin.site.register(itemOnReceipt)

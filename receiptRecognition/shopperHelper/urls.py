from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                    views.login,   name='login'),
    url(r'^login/$',      views.login,      name='studentLogin'),
    url(r'^landing/$',      views.landing,      name='landing'),
    url(r'^create_group/$',      views.createGroup,      name='createGroup'),
    url(r'^addReceipt/$',      views.addReceipt,      name='addReceipt'),
]

from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                    views.login,   name='login'),
    url(r'^login/$',      views.login,      name='studentLogin'),
    url(r'^logout/$',      views.logout,      name='studentLogout'),
    url(r'^landing/$',      views.landing,      name='landing'),
    url(r'^create_group/$',      views.createGroup,      name='createGroup'),
    url(r'^checkBoxPage/$',      views.checkBoxPage,      name='checkBoxPage'),
    url(r'^addReceipt/$',      views.addReceipt,      name='addReceipt'),
    url(r'^register/$',      views.register,      name='register'),
    url(r'^select_items/$',      views.selectItems,      name='selectItems'),
    # url(r'^summary/$',      views.summary,      name='summary'),
]

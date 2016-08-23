from django.conf.urls import url
from . import views

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^locate$',views.locateMobile,name='locate_mobile'),
    url(r'^infopage$',views.infoPage,name='info_page'),
    url(r'^register/$',views.register, name='register')

]

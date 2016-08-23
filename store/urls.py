from django.conf.urls import url
from . import views

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^store$',views.storeArea,name='store_area'),
    url(r'^redraw$',views.redrawArea,name='redraw_area'),

]

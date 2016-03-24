from django.conf.urls import url

from . import views

app_name = 'diplomas'
urlpatterns = [
    url(r'^geoloto$', views.geoloto, name='geoloto'),
    url(r'^azbuka$', views.azbuka, name='azbuka'),
    url(r'^regions$', views.regions, name='regions'),
    url(r'^$', views.index, name='index'),
]
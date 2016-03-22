from django.conf.urls import url

from . import views

app_name = 'diplomas'
urlpatterns = [
    url(r'^geoloto$', views.geoloto, name='geoloto'),
    url(r'^', views.index, name='index'),
]
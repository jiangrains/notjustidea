from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login.json$', views.login),
]
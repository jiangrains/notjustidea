from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login.json$', views.login),
    url(r'^signup$', views.signup),
    url(r'^signin$', views.signin),
    #url(r'^checktoken$', views.checktoken),
    #url(r'^activate$', views.activate),
    #url(r'^exists$', views.exists),
    #url(r'^retrieve$', views.retrieve),
    #url(r'^resetpsw$', views.resetpsw),
]

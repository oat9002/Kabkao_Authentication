from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.authentication, name='authentication'),
    url(r'^verify$', views.verify_account, name='verify_account'),
]
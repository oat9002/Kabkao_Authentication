from django.conf.urls import url
from . import views

app_name = 'authen'

urlpatterns = [
    # url(r'^$', views.authentication),
    # url(r'^verify$', views.verify_account, name='verify_account'),
    url(r'^login', views.Authentication.as_view(), name='authenticate'),
    url(r'^sign_up', views.SignUp.as_view(), name='sign_up'),
]
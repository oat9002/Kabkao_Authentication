from django.conf.urls import url
from . import views

app_name = 'authen'

urlpatterns = [
    # url(r'^$', views.authentication),
    # url(r'^verify$', views.verify_account, name='verify_account'),
    url(r'^login$', views.Login.as_view(), name='authenticate'),
    url(r'^logout$', views.Logout.as_view(), name='authenticate'),
    url(r'^sign_up$', views.SignUp.as_view(), name='sign_up'),
    url(r'^user', views.UserInfo.as_view(), name='user_info'),
    url(r'^check_permission$', views.CheckPermission.as_view(), name='check_permisson'),
    # url(r'^test_permission$', views.test_permission),
]
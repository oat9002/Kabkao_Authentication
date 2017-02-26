from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomPermission
from authentication.serializer import FullAccountSerializer, BasicAccountSerializer
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


import ErrorCode
import ResponseFormat


class SignUp(APIView):

    @staticmethod
    def get(request):
        return render(request, 'sign_up.html')

    def post(self, request):
        try:
            if User.objects.filter(email=request.data['email']).exists():
                raise Exception
            group = PermissionManagement().get_standard_user_group()
            user = User.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
            user.groups.add(group)
            self.setExtraPermissions(user)
            Token.objects.create(user=user)
            return Response({'success': True,
                         'payload': {
                             'token': Token.objects.get(user=user).key,
                             'user_data': FullAccountSerializer(user).data
                         }})
        except Exception as ex:
            return Response(ResponseFormat.error(ErrorCode.USERNAME_OR_EMAIL_ALREADY_EXISTS, "Username or email may already exist. Please use another one."), status=status.HTTP_406_NOT_ACCEPTABLE)

    def setExtraPermissions(self, user):
        assign_perm('change_user', user, user)
        assign_perm('delete_user', user, user)


class Authentication(APIView):

    @staticmethod
    def get(request):
        return render(request, 'login.html')

    @staticmethod
    def post(request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            return Response(ResponseFormat.success({
                                 'token': Token.objects.get(user=user).key,
                                 'user_data': FullAccountSerializer(user).data
                             }))
        return Response(ResponseFormat.error(ErrorCode.USERNAME_OR_PASSWORD_INCORRECT, "Username or password is incorrect. Please try again."), status=status.HTTP_404_NOT_FOUND)


class UserInfo(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            user_obj = User.objects.get(pk=request.query_params['id'])
            user_data = self.get_serializer_class(user_obj)(user_obj).data
            return Response(ResponseFormat.success({'user_data': user_data}))
        except Exception:
            return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "User data not found."), status=status.HTTP_404_NOT_FOUND)

    def get_serializer_class(self, user_obj):
        user = self.request.user
        if user.has_perm('change_user', user_obj):
            return FullAccountSerializer
        return BasicAccountSerializer


# def test_permission(request):
#     # PermissionManagement().update_standard_user_group_permission()
#     user = User.objects.get(pk=7)
#     # perm_shortcut = Permission.objects.get
#     # content_type = ContentType.objects.get_for_model(User)
#     # user.user_permissions.set([perm_shortcut(content_type=content_type, codename='view_user'),])
#     # user2 = User.objects.get(pk=5)
#     # assign_perm('view_user', user, user2)
#     print user.has_perm('delete_user', user)
#     # return Response(user.has_perm('add_user'))
#     return HttpResponse('success')


class PermissionManagement():

    def get_standard_user_group(self):
        group = Group.objects.get_or_create(name='standard_users')
        return group[0]

    def update_standard_user_group_permission(self):
        content_type = ContentType.objects.get_for_model(User)
        perm_shortcut = Permission.objects.get
        user_permissions = [perm_shortcut(content_type=content_type, codename='view_user'),]

        content_type = ContentType.objects.get_for_model(CustomPermission)
        menu_permissions = [perm_shortcut(content_type=content_type, codename='view_menu'),]
        order_permissions = [perm_shortcut(content_type=content_type, codename='add_order'),
                             perm_shortcut(content_type=content_type, codename='view_order'),
                             perm_shortcut(content_type=content_type, codename='delete_order'),]
        group = self.get_standard_user_group()
        group.permissions.set(user_permissions + menu_permissions + order_permissions)
        group.save()
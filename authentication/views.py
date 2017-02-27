from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
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
        user = None
        try:
            if not request.user.is_anonymous():
                return Response(ResponseFormat.error(ErrorCode.REQUIRE_ANONYMOUS, "Cannot sign up while staying logged in."))
            if User.objects.filter(email=request.data['email']).exists():
                raise Exception
            group = PermissionManagement().get_standard_user_group()
            user = User.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
            user.groups.add(group)
            self.setExtraPermissions(user)
            Token.objects.create(user=user)
            # login(request, user)
            return Response({'success': True,
                         'payload': {
                             'token': Token.objects.get(user=user).key,
                             'user_data': FullAccountSerializer(user).data
                         }})
        except Exception as ex:
            if user and not user.is_anonymous:
                user.delete()
            return Response(ResponseFormat.error(ErrorCode.USERNAME_OR_EMAIL_ALREADY_EXISTS, "Username or email may already exist. Please use another one."), status=status.HTTP_406_NOT_ACCEPTABLE)

    def setExtraPermissions(self, user):
        assign_perm('change_user', user, user)
        assign_perm('delete_user', user, user)


class Login(APIView):

    @staticmethod
    def get(request):
        return render(request, 'login.html')

    @staticmethod
    def post(request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            # login(request, user)
            return Response(ResponseFormat.success({
                                 'token': Token.objects.get(user=user).key,
                                 'user_data': FullAccountSerializer(user).data
                             }))
        return Response(ResponseFormat.error(ErrorCode.USERNAME_OR_PASSWORD_INCORRECT, "Username or password is incorrect. Please try again."), status=status.HTTP_404_NOT_FOUND)


class Logout(APIView):

    @staticmethod
    def post(request):
        try:
            logout(request)
            return Response(ResponseFormat.success())
        except Exception:
            return Response(ResponseFormat.error(ErrorCode.INTERNAL_SERVER_ERROR, "Logout failed."))


class UserInfo(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            user_obj = User.objects.get(pk=request.query_params['id'])
            user_data = self.get_serializer_class(user_obj)(user_obj).data
            return Response(ResponseFormat.success({'user_data': user_data}))
        except Exception:
            return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "User data not found."), status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def put(request):
        try:
            user = User.objects.get(pk=request.data['id'])
            if request.user.has_perm('change_user', user):
                serializer = FullAccountSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    user = serializer.save()
                    return Response(ResponseFormat.success({"user_data": FullAccountSerializer(user).data}))
                return Response(ResponseFormat.error(ErrorCode.INPUT_DATA_INVALID, "Input data is invalid. Please correct and try again.", status.HTTP_406_NOT_ACCEPTABLE))
            return Response(ResponseFormat.error(ErrorCode.FORBIDDEN, "Permission not allowed."))
        except Exception:
            return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "User data not found."))

    @staticmethod
    def delete(request):
        try:
            user = User.objects.get(pk=request.data['id'])
            if request.user.has_perm('delete_user', user):
                user.delete()
                return Response(ResponseFormat.success())
            return Response(ResponseFormat.error(ErrorCode.FORBIDDEN, "Permission not allowed."), status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response(ResponseFormat.error(ErrorCode.INTERNAL_SERVER_ERROR, "Delete failed."))

    def get_serializer_class(self, user_obj):
        user = self.request.user
        if user.has_perm('change_user', user_obj):
            return FullAccountSerializer
        return BasicAccountSerializer


# def test_permission(request):
#         if not request.user.is_staff():
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


class CheckPermission(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):
        try:
            user = request.user
            permission = request.query_params['permission']
            if user.has_perm(permission, user) or user.has_perm('authentication.' + permission):
                return Response(ResponseFormat.success({'is_allowed': True}))
            return Response(ResponseFormat.success({'is_allowed': False}))
        except Exception:
            return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "Permission not found. Please try again."))


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
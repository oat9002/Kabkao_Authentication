from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializer import FullAccountSerializer, BasicAccountSerializer
from guardian.shortcuts import assign_perm


import ErrorCode
import ResponseFormat


class SignUp(APIView):

    @staticmethod
    def get(request):
        return render(request, 'sign_up.html')

    @staticmethod
    def post(request):
        try:
            if User.objects.filter(email=request.data['email']).exists():
                raise Exception
            user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
            Token.objects.create(user=user)
            return Response({'success': True,
                         'payload': {
                             'token': Token.objects.get(user=user).key,
                             'user_data': FullAccountSerializer(user).data
                         }})
        except Exception as ex:
            return Response(ResponseFormat.error(ErrorCode.USERNAME_OR_EMAIL_ALREADY_EXISTS, "Username or email may already exist. Please use another one."), status=status.HTTP_406_NOT_ACCEPTABLE)


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
            user_data = self.get_serializer_class()(user_obj).data
            return Response(ResponseFormat.success({'user_data': user_data}))
        except Exception:
            return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "User data not found."), status=status.HTTP_404_NOT_FOUND)

    # def post(self, request):


    def get_serializer_class(self):
        request = self.request
        user = request.user
        if user.is_staff or user.id == request.query_params['id']:
            return FullAccountSerializer
        return BasicAccountSerializer


# def test_permission(request):
#     user = User.objects.get(pk=1)
#     user2 = User.objects.get(pk=5)
#     # assign_perm('view_user', user, user2)
#     print user.has_perm('view_user', user2)
#     return Response(user.has_perm('add_user'))
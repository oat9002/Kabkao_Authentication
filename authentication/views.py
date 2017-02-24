from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
# import pyrebase
from rest_framework.response import Response
from rest_framework.views import APIView

import ErrorCode
import ResponseFormat
from authentication.permissions import IsAdmin

# config = {
#     'apiKey': "AIzaSyAGPTJC14nFrWJE0e7348YftzcYkUkEhG0",
#     'authDomain': "kabkao-fc139.firebaseapp.com",
#     'databaseURL': "https://kabkao-fc139.firebaseio.com",
#     'storageBucket': "kabkao-fc139.appspot.com",
#     'messagingSenderId': "279221787005"
# }
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
#
# def authentication(request):
#     user = auth.sign_in_with_email_and_password(request.GET['email'], request.GET['password'])
#     return HttpResponse(user['idToken'])

# def verify_account(request):
#     try:
#         verification = auth.get_account_info(request.GET['idToken'])
#     except:
#         return HttpResponse('not verify')
#     return HttpResponse('verify')
# Create your views here.
from authentication.serializer import FullAccountSerializer


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
            return Response(ResponseFormat.error(ErrorCode.USERNAME_OR_EMAIL_ALREADY_EXISTS, "Username or email may already exist. Please use another one."))


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
        return Response(ResponseFormat.error(ErrorCode.USERNAME_OR_PASSWORD_INCORRECT, "Username or password is incorrect. Please try again."))
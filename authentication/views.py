from django.shortcuts import render
from django.http import HttpResponse
import pyrebase

config = {
    'apiKey': "AIzaSyAGPTJC14nFrWJE0e7348YftzcYkUkEhG0",
    'authDomain': "kabkao-fc139.firebaseapp.com",
    'databaseURL': "https://kabkao-fc139.firebaseio.com",
    'storageBucket': "kabkao-fc139.appspot.com",
    'messagingSenderId': "279221787005"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def authentication(request):
    user = auth.sign_in_with_email_and_password(request.GET['email'], request.GET['password'])
    return HttpResponse(user['idToken'])

def verify_account(request):
    try:
        verification = auth.get_account_info(request.GET['idToken'])
    except:
        return HttpResponse('not verify')
    return HttpResponse('verify')
# Create your views here.

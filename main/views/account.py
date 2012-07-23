from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import email_re
from django.template import loader, Context
from django.core.mail import send_mail
from main.models.account import *



@csrf_exempt
def login_action(request):
    """Need to figure out why csrf_token is not set"""
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('main.views.index.index')             
    else:
        return HttpResponse('{"code":"1","msg":"Username or password incorrect."}')

def logout_view(request):
    logout(request)
    return redirect('main.views.index.index')


    
    
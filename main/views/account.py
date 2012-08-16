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
from main.utils.form_check import *
from main.utils.misc import generate_random_string



def login_action(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('main.views.index.index')             
    else:
        messages.error(request, 'Incorrect username or password. Please try again.')
        return redirect('main.views.index.index') 

@login_required
def logout_view(request):
    logout(request)
    return redirect('main.views.index.index')

def forgot_password(request):
    return render_to_response('forgot.htm',{}, context_instance=RequestContext(request)) 

def forgot_password_action(request):
    username = request.POST['username']
    email = request.POST['email']
    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request, 'This username does not exist')
        return redirect('main.views.account.forgot_password')
    profile = Profile.objects.get(user=user)
    if profile.email != email:
        messages.error(request, 'Email does match.')
        return redirect('main.views.account.forgot_password')
    new_password = generate_random_string(10)
    user.set_password(new_password)
    t = loader.get_template('forgot_password.txt')
    c = Context({
        'url': settings.APP_URL,
        'new_password': new_password 
    })
    send_mail('Your new password at QuantMD', t.render(c), 'service@quant.md', (email,), fail_silently=False)
    
    messages.info(request, 'Your new password has been sent to your email')
    return redirect('main.views.account.forgot_password')

@login_required
def change_password_view(request):
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.role == 1:
        return render_to_response('referring/change-password.htm', {},
                              context_instance=RequestContext(request))
    elif profile.role == 2:
        return render_to_response('receptionist/change-password.htm', {},
                              context_instance=RequestContext(request))
    elif profile.role == 3:
        return render_to_response('broker/change-password.htm', {},
                              context_instance=RequestContext(request))
    elif profile.role == 4:
        return render_to_response('cardiologist/change-password.htm', {},
                              context_instance=RequestContext(request))
    elif profile.role == 0:
        return render_to_response('quantmd/change-password.htm', {},
                              context_instance=RequestContext(request))

@login_required
def change_password(request):
    password = request.POST['old']
    new_password = request.POST['new']
    confirm_password = request.POST['confirm']
    
    if not password.strip():
        messages.error(request, 'Password is empty or does not match')
        return redirect('main.views.account.change_password_view')
    
    if not new_password.strip() or new_password != confirm_password:
        messages.error(request, 'New password is empty or does not match')
        return redirect('main.views.account.change_password_view')
        
    user = authenticate(username=request.user.username, password=password)
    
    if user is None:
        messages.error(request, 'Current password is incorrect')
        return redirect('main.views.account.change_password_view')
    
    
    user = request.user
    user.set_password(new_password)
    user.save()
    
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.role == 1:
        return render_to_response('referring/change-password-confirm.htm', {},
                              context_instance=RequestContext(request))
    elif profile.role == 2:
        return render_to_response('receptionist/change-password-confirm.htm', {},
                              context_instance=RequestContext(request))
    elif profile.role == 3:
        return render_to_response('broker/change-password-confirm.htm', {},
                              context_instance=RequestContext(request))
    elif profile.role == 4:
        return render_to_response('cardiologist/change-password-confirm.htm', {},
                              context_instance=RequestContext(request))
    elif profile.role == 0:
        return render_to_response('quantmd/change-password-confirm.htm', {},
                              context_instance=RequestContext(request))
        


    
    
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
        return HttpResponse('{"code":"1","msg":"Username or password incorrect."}')

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
    send_mail('Your new password at QuantMD', t.render(c), 'support@xifenfen.com', (email,), fail_silently=False)
    
    messages.info(request, 'Your new password has been sent to your email')
    return redirect('main.views.account.forgot_password')

def change_password_view(request):
    if request.user.is_authenticated():
        return render_to_response('changePassword.htm', {},
                              context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))


def change_password(request):
    print "haha"
    if request.user.is_authenticated():
        password = request.POST['password']
        new_password = request.POST['new-password']
        confirm_password = request.POST['confirm-password']
        
        error = []
        
        if IsEmpty(password):
            error.append("Please enter current password")
        if IsEmpty(new_password):
            error.append("Please enter new password")
        if new_password != confirm_password:
            error.append("new password is inconsistent")
            
        user = authenticate(username=request.user.user_name, password=password)
         
        if user is None:
            error.append("Current password is incorrect")
        
        
        if len(error) != 0:
             return render_to_response('changePassword.htm', {},
                              context_instance=RequestContext(request))
        
        user = request.user
        user.set_password(new_password)
        user.save()
        print "success"
        return redirect('main.views.index.index')
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    


    
    
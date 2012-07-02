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

def login_view(request):
    orgs = Organization.objects.all()
    return render_to_response('main/account/login.html', {'orgs':orgs},
                              context_instance=RequestContext(request))

@csrf_exempt
def login_action(request):
    """Need to figure out why csrf_token is not set"""
    email_prefix = request.POST['email_prefix']
    password = request.POST['password']
    domain = request.POST['domain']
    user = authenticate(username=email_prefix+'@'+domain, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse('{"code":"0","msg":"Logged in."}')
        else:
            return HttpResponse('{"code":"1","msg":"User is not activated."}')
            
    else:
        return HttpResponse('{"code":"1","msg":"Username or password incorrect."}')

def logout_view(request):
    logout(request)
    return redirect('main.views.index.index')

@csrf_exempt
def register_action(request):
    if request.user.is_authenticated():
        logout(request)
    email_prefix = request.POST['email_prefix']
    domain = request.POST['domain']
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']
    email = email_prefix + '@' + domain
    
    if not email_re.match(email):
        return HttpResponse('{"code":"1","msg":"Email format not correct"}')
    if password != password_confirm:
        return HttpResponse('{"code":"1","msg":"Two passwords do not match!"}')
    if len(password) < 6 or len(password) > 20:
        return HttpResponse('{"code":"1","msg":"Password should have length between 6 to 20 characters."}')
    if password[0] == ' ' or password[-1] == ' ':
        return HttpResponse('{"code":"1","msg":"Password should not have space at the two ends."}')
    if User.objects.filter(email=email).exists():
        return HttpResponse('{"code":"1","msg":"This email is already registered."}')
    
    user = User.objects.create_user(email, email, password)
    user.is_active = False
    user.save()
    
    #TODO: create Profile object here
    
    try:
        org = Organization.objects.get(domain=domain)
        org.user_count += 1
        org.save()
    except:
        pass
    
    from main.utils.misc import generate_random_string
    random_code = generate_random_string(length=10)
    v = EmailValidation(user=user, email=email, code=random_code)
    v.save()
    t = loader.get_template('main/account/validate_email.txt')
    c = Context({
        'url': settings.APP_URL + 'account/validate_email/' + random_code,
    })
    send_mail('Welcome to StartAhead', t.render(c), 'service@xifenfen.com', (email,), fail_silently=False)
    
    return HttpResponse('{"code":"0","msg":"success. email sent."}')

    
def validate_email(request, code):
    try:
        v = EmailValidation.objects.get(code=code)
    except:
        return render_to_response('main/account/validate_result.html', {'error':'URL incorrect!'},
                              context_instance=RequestContext(request)) 
    v.validated = True
    v.save()
    user = v.user
    user.is_active = True
    user.save()
    return render_to_response('main/account/validate_result.html', {},
                              context_instance=RequestContext(request)) 
    
    
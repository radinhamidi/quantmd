from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.account import Profile
from main.models.message import Message
from django.db.models import Q

def message(request):
    """The base layout"""
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.role == 1:
        template = 'referring/message.htm'
    else: #role == 3
        template = 'cardiologist/message.htm'
    return render_to_response(template, {},
                                  context_instance=RequestContext(request))

def message_list(request):
    """
    Display all messages in reverse order of case number
    Need to resolve the problem that messages are already ranked in backend by not shown
    in order in frontend
    """
    user_id = request.user.pk
    q = Q(sender__pk=user_id) | Q(receiver__pk=user_id)    
    messages = Message.objects.filter(q).order_by('-id')
    for m in messages:
        print m.pk
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.role == 1:
        template = 'referring/message-list.htm'
    else: #role == 3
        template = 'cardiologist/message-list.htm'
    return render_to_response(template, {'messages':messages},
                                  context_instance=RequestContext(request))

def message_dialog(request, case_id, is_sys, message_id):
    """Display the dialog of message, and also allow user to reply"""
    user_id = request.user.pk
    message = Message.objects.get(pk=message_id)
    message.is_read = True
    message.save()
    is_sys = 1 if is_sys == 'True' else 0
    if is_sys:
        q = Q(case__pk=case_id) & Q(is_sys=True) & Q(receiver__pk=user_id)    
    else:
        q = Q(case__pk=case_id) & Q(is_sys=False) &(Q(sender__pk=user_id) | Q(receiver__pk=user_id))    
    messages = Message.objects.filter(q).order_by('id')
    sender_id = 0
    if not is_sys:
        for m in messages:
            if m.sender_id != user_id:
                sender_id = m.sender_id
                break
    profile = Profile.objects.get(pk=request.user.pk)
    if profile.role == 1:
        template = 'referring/message-dialog.htm'
    else: #role == 3
        template = 'cardiologist/message-dialog.htm'
    
    return render_to_response(template, {'messages':messages, 
                                  'sender_id':sender_id, 'is_sys':is_sys},
                                  context_instance=RequestContext(request))

def send(request):
    receiver_id = int(request.POST['receiver_id'])
    case_id = int(request.POST['case_id'])
    content = request.POST['content']
    message = Message(is_sys=False)
    message.sender_id = request.user.pk
    message.receiver_id = receiver_id
    message.case_id = case_id
    message.content = content
    message.save()
    return redirect('main.views.message.message_dialog', case_id, 'False')




    
    
    
    
    
    
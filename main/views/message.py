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
    return render_to_response('referring/message.htm', {},
                                  context_instance=RequestContext(request))

def message_list(request):
    """Display all messages reverse order of case number"""
    user_id = request.user.pk
    q = Q(sender__pk=user_id) | Q(receiver__pk=user_id)    
    messages = Message.objects.filter(q).order_by('-id')
    for m in messages:
        print m.pk
    return render_to_response('referring/message-list.htm', {'messages':messages},
                                  context_instance=RequestContext(request))

def message_dialog(request, case_id, is_sys):
    """Display the dialog of message, and also allow user to reply"""
    user_id = request.user.pk
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
    return render_to_response('referring/message-dialog.htm', {'messages':messages, 
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


    
    
    
    
    
    
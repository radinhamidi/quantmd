from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.account import *
from main.models.case import *
from main.models.data import *
from main.models.report import Report
from main.models.message import Message
from main.models.appointment import Appointment 

def case(request):
    cases = Case.objects.filter(status=4, cardiologist__pk=request.user.pk)
    if len(cases) == 0:
        has_pending_case = 0
        case = None #No use
    else:
        has_pending_case = 1
        case = cases[0]
    return render_to_response('cardiologist/case.htm', {'has_pending_case':has_pending_case,
                                                        'case':case},
                                  context_instance=RequestContext(request))

def accept_case(request):
    """ Need to change query status to 3 in production """
    cases = Case.objects.filter(status=4, cardiologist__pk=request.user.pk)
    if len(cases) != 0:
        messages.error(request, 'You can only accept one case at a time')
        return redirect('main.views.cardiologist.case')
    
    cases = Case.objects.filter(status=2).order_by('id')
    if len(cases) == 0:
        messages.error(request, 'No pending cases to review.')
        return redirect('main.views.cardiologist.case')
    else:
        case = cases[0]
        case.status = 4
        case.cardiologist_id = request.user.pk
        case.save()
        return redirect('main.views.cardiologist.case')

def submit_report(request):
    """Need to generate PDF report"""
    profile = Profile.objects.get(pk=request.user.pk)
    diagnosis = request.POST['diagnosis']
        
    report = Report(content=diagnosis)
    report.save()
    
    case_id = request.POST['case_id']
    case = Case.objects.get(pk=case_id)
    case.status = 5
    case.report = report
    case.save()
    
    apt = Appointment.objects.get(case=case)
    
    message = Message(is_sys=False, receiver=apt.doctor, case=case)
    message.sender_id = request.user.pk
    message.title = 'Report uploaded for Case #' + case_id
    message.content = 'Report is uploaded for Case #' + case_id + \
                      'from cardiologist ' + profile.first_name + ' ' + profile.last_name + ': '\
                      + diagnosis
    message.save()
    messages.info(request, 'Report submited and sent a message to referring doctor')
    return redirect('main.views.cardiologist.case')


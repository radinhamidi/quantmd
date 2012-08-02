from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from main.models.account import *
from main.models.patient import *
from main.models.appointment import *
from main.models.mri import *
from main.utils.form_check import *
from main.models.case import *
from main.models.data import *
from django.utils.datetime_safe import datetime


def accept_case_view(request):
    if request.user.is_authenticated():
        return render_to_response('cardiologist/accept.htm', {},
                                context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
def accept_case_action(request):
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        if Case.objects.filter(cardiologist = profile).filter(status=3).exists():
            error  = "You already got one case, please finish that case first"
            return render_to_response('cardiologist/accept.htm', {'error':error},
                                context_instance=RequestContext(request))
            
        if Case.objects.filter(status = 2).exists():
            case = Case.objects.filter(status = 2)[0]
            case.status = 3
            case.cardiologist = Profile.objects.get(user = request.user)
            case.assigned_time = datetime.now()
            case.save()
            return redirect('main.views.index.index')
        else:
            error = "No case available for now"
            return render_to_response('cardiologist/accept.htm', {'error':error},
                                context_instance=RequestContext(request))
        
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))

def case_view(request):
    print "case view"
    if request.user.is_authenticated():
        profile = Profile.objects.get(user = request.user)
        print "right"
        if Case.objects.filter(cardiologist = profile).filter(status=3).exists():
            case = Case.objects.filter(cardiologist = profile).filter(status=3)[0]
            return render_to_response('cardiologist/case.htm', {'case':case},
                                context_instance=RequestContext(request))
        else:
            print "error"
            error = "You need to accept case first"
            return render_to_response('cardiologist/case.htm', {'error':error},
                                context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
  
    
def handin_report(request, case_id):
    
    if request.user.is_authenticated():
        diagnosis = request.POST['diagnosis']
        error = []
        if len(diagnosis) == 0:
            error.append("diagnosis cannot be empty")
                
        if not Case.objects.filter(id=case_id).exists():
            error.append("Case is not exist") 
        
        if len(error) != 0:    
            return render_to_response('cardiologist/case.htm', {'error': error},
                                context_instance=RequestContext(request))
        
        case = Case.objects.get(id=case_id)
        case.status = 4
        report = Report.objects.create(content = diagnosis)
        case.report = report
        report.save()
        case.save()
        return redirect('main.views.cardiologist.case_view')
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def diagnosis_list(request):
    print "aaa"
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        cases = Case.objects.filter(cardiologist = profile).filter(status = 4)
        return render_to_response('cardiologist/completed.htm', {'cases': cases},
                                context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
def view_report(request, case_id):
    if request.user.is_authenticated():
        if Case.objects.filter(id=case_id).exists():
            case = Case.objects.get(id=case_id)
            return render_to_response('cardiologist/report.htm', {'case': case},
                                      context_instance=RequestContext(request))
        else:
            error = "case is not exist"
            return render_to_response('cardiologist/report.htm', {'error': error},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('login.htm',{}, context_instance=RequestContext(request))
    
    
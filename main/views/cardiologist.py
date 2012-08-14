from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from main.models.account import *
from main.models.case import *
from main.models.data import *
from main.models.report import Report
from main.models.message import Message
from main.models.appointment import Appointment 
from main.utils.pdf_generator import Report2PDF
from os import listdir, makedirs, rename
from os.path import isfile, join
from datetime import datetime

def case(request):
    cases = Case.objects.filter(status=4, cardiologist__pk=request.user.pk)
    if len(cases) == 0:
        has_pending_case = 0
        case = None #No use
        data = None
        image_objs = []
        anal_videos = []
        anal_images = []
    else:
        has_pending_case = 1
        case = cases[0]
        data = case.data
        image_objs = []
        sequences = DataSequence.objects.filter(data=data)
        for i in xrange(data.image_count):
            index = i + 1
            for s in sequences:
                if index >= s.image_start and index <= s.image_end:
                    image_objs.append((index, str(index)+'.dcm.png', s.name))
                    break #found service name, continue to next image
        
        #Get analysis media
        directory = settings.MEDIA_ROOT + 'dicom/' + data.name + '/analysis'
        file_names = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
        anal_videos = []
        anal_images = []
        for fn in file_names:
            if fn.lower().endswith('.mp4'):
                anal_videos.append(fn)
            else:
                anal_images.append(fn)
        
          
    return render_to_response('cardiologist/case.htm', {'has_pending_case':has_pending_case,
                                                        'case':case, 'data':data, 'image_objs':image_objs,
                                                        'anal_videos':anal_videos, 'anal_images':anal_images},
                                  context_instance=RequestContext(request))

def accept_case(request):
    """ Need to change query status to 3 in production """
    cases = Case.objects.filter(status=4, cardiologist__pk=request.user.pk)
    if len(cases) != 0:
        messages.error(request, 'You can only accept one case at a time')
        return redirect('main.views.cardiologist.case')
    
    cases = Case.objects.filter(status=3).order_by('id')
    if len(cases) == 0:
        messages.error(request, 'No pending cases to review.')
        return redirect('main.views.cardiologist.case')
    else:
        case = cases[0]
        case.status = 4
        case.cardiologist_id = request.user.pk
        case.assigned_time = datetime.now()
        case.save()
        return redirect('main.views.cardiologist.case')

@csrf_exempt
def submit_report(request):
    profile = Profile.objects.get(pk=request.user.pk)
    diagnosis = request.POST['diagnosis']
    comments = (request.POST['comments']).split('!#!')
    
    case_id = request.POST['case_id']
    case = Case.objects.get(pk=case_id)
    data = case.data
    
    image_list = []
    comments_list = [] #list of string
    for c in comments:
        split_index = c.find(':')
        image_index = int(c[:split_index])        
        content = c[split_index+1:] if split_index != len(c) - 1 else ''
        cinstance = Comment(data=data, image_index=image_index, content=content)
        cinstance.save()
        comments_list.append(content)
        image_list.append(str(image_index)+'.dcm.png')
    
    
    #Generate PDF report
    identifier = data.name
    directory = settings.MEDIA_ROOT + 'dicom/' + identifier
    pdf_path = settings.MEDIA_ROOT + 'dicom/' + identifier + '/' + identifier + '.pdf'
    patient_dob_str = case.patient.birthday.strftime("%m/%d/%Y")
    patient_gender = 'Male' if case.patient.gender else 'Female'
    Report2PDF(profile.first_name, profile.last_name, case.patient.first_name, case.patient.last_name,
               patient_gender, patient_dob_str, directory, image_list, comments_list, pdf_path, diagnosis)
    report = Report(content=diagnosis)
    report.file = 'dicom/' + identifier + '/' + identifier + '.pdf'  
    report.save()
    
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
    return HttpResponse('{"code":"0", "msg":"Success"}')

def logs(request):
    cases = Case.objects.filter(status__gte=5, cardiologist__pk=request.user.pk)
    return render_to_response('cardiologist/logs.htm', {'cases':cases},
                                  context_instance=RequestContext(request))


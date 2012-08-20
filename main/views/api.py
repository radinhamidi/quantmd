from django.conf import settings
from django.http import HttpResponse
from main.models.account import Profile
from main.models.case import Case
from main.models.mri import Schedule
from main.models.analysis import Analysis
import json
from datetime import datetime, time


def dicom_zip(request, case_id):
    """Get the zipped dicom files of a case"""
    try:
        try:
            case = Case.objects.get(pk=case_id)
        except:
            d = {'code':1, 'error_msg':'No such case'}
            return HttpResponse(json.dumps(d))
        if not case.data:
            d = {'code':1, 'error_msg':'This case has no uploaded data'}
            return HttpResponse(json.dumps(d)) 
        name = case.data.name
        d = {}
        d['code'] = 0
        d['dicom_zip_url'] = settings.MEDIA_URL + 'dicom/' + name + '/' + name + '.zip'
        return HttpResponse(json.dumps(d))
    except:
        d = {'code':1, 'error_msg':'API system has an error when processing your request.'}
        return HttpResponse(json.dumps(d)) 

def upload_analysis(request, case_id, admin_id):
    try:
        try:
            case = Case.objects.get(pk=case_id)
        except:
            d = {'code':1, 'error_msg':'No such case'}
            return HttpResponse(json.dumps(d))
        try:
            admin = Profile.objects.get(pk=admin_id, role=0)
        except:
            d = {'code':1, 'error_msg':'No such user or this user is not admin'}
            return HttpResponse(json.dumps(d))
        analysis = Analysis(admin=admin, content='Analysis files uploaded.')
        analysis.save()
        case.status = 3
        case.save()
        d = {'code':0}
        return HttpResponse(json.dumps(d)) 
    except:
        d = {'code':1, 'error_msg':'API system has an error when processing your request.'}
        return HttpResponse(json.dumps(d)) 

def get_schedule_by_day(request, mri_id, date_str):
    """
    The date should be of format 2012-1-1 or 2012-01-01
    Return code:1 if there is an error, and no more other fields
    Return code:0 if success; If there is slots, slots field is set
    """
    try:
        date_list = date_str.split('-')
        date = datetime(int(date_list[0].strip('0')), int(date_list[1].strip('0')), int(date_list[2].strip('0'))) 
        schedules = Schedule.objects.filter(mri=int(mri_id), date=date, is_cancelled=False).order_by('start_time')
        d = {}
        d['code'] = 0
        d['num_slots'] = len(schedules)
        if len(schedules) != 0:
            d['slots'] = [] 
            for s in schedules:
                d['slots'].append({'schedule_id':s.pk, 'is_available':s.is_available, 'start_time':str(s.start_time)})
        return HttpResponse(json.dumps(d))
    except:
        d = {'code':1, 'error_msg':'API system has an error when processing your request.'}
        return HttpResponse(json.dumps(d)) 

def add_slot(request, mri_id, date_str, time_str):
    """
    The date should be of format 2012-1-1 or 2012-01-01
    The time should be of format 12:00:00 or 12:0:0
    Return code:1 if there is an error
    Return code:0 if success;
    """
    try:
        date_list = date_str.split('-')
        date = datetime(int(date_list[0].strip('0')), int(date_list[1].strip('0')), int(date_list[2].strip('0')))
        t_list = time_str.split(':')
        t0_str = t_list[0].strip('0')
        t0 = 0 if not t0_str else int(t0_str)
        t1_str = t_list[1].strip('0')
        t1 = 0 if not t1_str else int(t1_str)
        t2_str = t_list[2].strip('0')
        t2 = 0 if not t2_str else int(t2_str)
        t = time(t0, t1, t2)
        try:
            schedule = Schedule.objects.get(mri=int(mri_id), date=date, start_time=t)
            #slot already exist, return error
            d = {'code':1, 'error_msg':'This slot already exists!'}
            return HttpResponse(json.dumps(d)) 
        except:
            pass 
        schedule = Schedule(date=date, is_cancelled=False, is_available=True)
        schedule.mri_id = int(mri_id)
        schedule.start_time = t
        schedule.end_time = t
        schedule.save()
        d = {}
        d['code'] = 0
        return HttpResponse(json.dumps(d))
    except:
        d = {'code':1, 'error_msg':'API system has an error when processing your request.'}
        return HttpResponse(json.dumps(d)) 
    
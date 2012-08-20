from django.conf import settings
from django.http import HttpResponse
from main.models.case import Case
import json


def dicom_zip(request, case_id):
    case = Case.objects.get(pk=case_id)
    d = {}
    d['code'] = '0'
    d['dicom_zip_']
    

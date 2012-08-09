from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from main.models.account import *
from main.models.appointment import Appointment 
from main.models.case import Case
from main.models.patient import Patient
from main.models.data import MRIData
from main.models.message import Message
from main.utils.misc import generate_random_string
from os import listdir, makedirs, rename
from os.path import isfile, join
from subprocess import call
from zipfile import ZipFile
import sys

def cardiologist(request):
    """Show lists of cardiologist"""
    
    
    return render_to_response('quantmd/cardilogist.htm', {},
                                  context_instance=RequestContext(request))

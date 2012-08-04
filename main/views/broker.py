from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template import loader, Context
from django.views.decorators.csrf import csrf_exempt
from main.models.account import *
from main.utils.misc import generate_random_string



def upload(request):
    return render_to_response('broker/upload.htm', {},
                                  context_instance=RequestContext(request))
@csrf_exempt   
def upload_action(request):
    file = request.FILES['fileToUpload']
    path = settings.MEDIA_ROOT + 'dicom/' + generate_random_string() + '.dcm'
    f = open(path, 'w')
    f.write(file.read())
    f.close()
    return HttpResponse('{"code":"0", "msg":"success"}')

    
    
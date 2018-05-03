# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import *
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader
from django.db.models import *
from .models import *
import time
import csv
from django.utils import timezone
from django.utils.encoding import *
import hashlib
from celery.result import AsyncResult
from celery.task.control import *
from celery import task, current_task,current_app
import os
import codecs
import json
from celery import Celery
from django.conf import settings
from anyjson import serialize
import uuid
from os import listdir
from os.path import isfile, join
from django import template
import messages as MESSAGE
import settings
# Create your views here.
siteurl=settings.siteurl
data={}
@csrf_exempt
@ensure_csrf_cookie
def index(request):
    if request.method == "GET":
        if "HTTP_X_AP_SIGNATURE" not in request.META:
            data['message']="invalid signature"
        if "HTTP_X_NL_API_VERSION" not in request.META:
            data['message']="unknown api version"
        if "HTTP_VERSION" not in request.META:
            data['message']="unknown app version"
        if "HTTP_X_NL_KEY" not in request.META:
            data['message']="invalid key"
        return JsonResponse(data)
    else:
        return JsonResponse(data)















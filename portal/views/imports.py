# -*- coding: utf-8 -*-
import math
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.db.models import *
from api.models import *
import time
import csv
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.utils.encoding import *
import hashlib
from celery.result import AsyncResult
from celery.task.control import *
from celery import task, current_task,current_app
import os
import codecs
from celery import Celery
from django.conf import settings
from anyjson import serialize
import uuid
from api.models import *
from os import listdir
from os.path import isfile, join
from django import template
from datetime import datetime, timedelta
import json
import random, string
import messages as MESSAGE
# Create your views here.
from smsgateway import *
import settings
# Create your views here.
siteurl=settings.siteurl
data={"sitename":settings.sitename}

def verifySignature(req):
    request=req
    sig_verify={}
    if "HTTP_X_AP_SIGNATURE" not in request.META:
        sig_verify['status']="invalid signature"
    elif "HTTP_X_NL_API_VERSION" not in request.META:
        sig_verify['status']="unknown api version"
    elif "HTTP_VERSION" not in request.META:
        sig_verify['status']="unknown app version"
    elif "HTTP_X_NL_KEY" not in request.META:
        sig_verify['status']="invalid key"
    else:
        sig_verify['status']="ok"
    if sig_verify['status']!="ok":
        data={}
        data['status']="failed"
        data['message']=sig_verify['status']
    else:
        data={}
        data['status']="ok"
    data['status']="ok"
    return data

from imports import *
#register new account
#@csrf_protect
@csrf_exempt
def registeruser(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        username=request.POST.get("username")
        passwd=request.POST.get("password")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        secret=hashlib.md5(passwd).hexdigest()
        password=hashlib.sha256(passwd).hexdigest()
        verifyuser={"username":None}
        verifyprofile={"email":None,"phone":None}
        balance=0.0
        try:
            userobject=User.objects.filter(Q(username=username)).get()
            verifyuser['username']=userobject.username
        except Exception as ex:
            print ex
        try:
            profileobject=Profile.objects.filter(Q(email=email) | Q(phone=phone)).get()
            verifyprofile['email']=profileobject.email
            verifyprofile['phone']=profileobject.phone
        except Exception as ex:
            print ex
        print verifyprofile
        print verifyuser
        if verifyprofile['email']!=None and verifyprofile['email']==email:
            data={}
            data['message']=MESSAGE.EMAIL_EXISTS
            data['status']="failed"
        elif verifyprofile['phone']!=None and verifyprofile['phone']==phone:
            data={}
            data['message']=MESSAGE.PHONE_EXISTS
            data['status']="failed"
        elif verifyuser['username']==None:
            user=User.objects.create(username=username,password=password,secret=secret,createdate=timezone.now())
            if user.id!=None:
                uid=user.id
                profile=Profile.objects.create(uid=uid,email=email,phone=phone,createdate=timezone.now())
                renewdate = datetime.now() - timedelta(days=1)
                uservalidity=UserValidity.objects.create(uid=uid,lastrenewdate=renewdate,nextrenewdate=renewdate)
                data={}
                data['uid']=uid
                data['username']=username
                data['status']="ok"
                if settings.requires2fa:
                    data['verify']="1"
                else:
                    data['verify']="0"
                data['message']=MESSAGE.CREATE_USER_SUCCESS
                recipient=profile.phone
                code=get2FACode()
                request.session['uid']=uid
                request.session['2fa']=code
                sendMessage(recipient,code)
            else:
                data={}
                data['message']=MESSAGE.UNABLE_TO_CREATE
                data['status']="failed"
        else:
            data={}
            data['message']=MESSAGE.USER_EXISTS
            data['status']="failed"

        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        return JsonResponse(data)

@csrf_exempt
def verifydevice(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        code=request.POST.get("code")
        print "Code sent is "+code
        securecode=request.session['2fa']
        print "Session saved code is "+str(securecode)
        if str(securecode)==code:
            if "uid" in request.session:
                uid=request.session['uid']
                user=User.objects.get(id=uid)
                user.isphoneverified=1
                user.save()
            data={}
            data['message']=MESSAGE.VERIFY_OK
            data['status']="ok"
            data['uid']=uid
            return JsonResponse(data)
        else:
            data={}
            data['message']=MESSAGE.VERIFY_FAILED_INVALIDCODE
            data['status']="failed"
            return JsonResponse(data)

    else:
        data={}
        data['message']=MESSAGE.VERIFY_FAILED
        data['status']="failed"
        return JsonResponse(data)

#verify account
#@csrf_protect
@csrf_exempt
def verify(request):
    if request.session.get('isloggedin', False):

        return JsonResponse(data)
    else:
        return JsonResponse(data)


#confirm account
#@csrf_protect
@csrf_exempt
def confirm(request):
    if request.session.get('isloggedin', False):

        return JsonResponse(data)
    else:
        return JsonResponse(data)

def get2FACode():
    n=6
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def sendMessage(recipient,code):
    url="http://www.estoresms.com"
    username="biddyweb"
    password="googleboy234"
    s=SMSGateway(url,username,password)
    method="GET"
    endpoint="smsapi.php"
    params={}
    params['username']=username
    params['password']=password
    params['sender']=settings.sitename
    params['recipient']=recipient
    params['message']="Thank you for signing up for "+settings.sitenameshort+". Your verification token is: "+str(code)
    s.sendMessage(method,endpoint,params)

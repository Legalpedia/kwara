from imports import *


def signup(request):
    template = loader.get_template('portal_signup.html')
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))


def registeruser(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        username=request.POST.get("username")
        passwd=request.POST.get("password")
        passwd2=request.POST.get("password2")
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
                data['requiresphoneverify']=1
                data['message']=MESSAGE.CREATE_USER_SUCCESS
            else:
                data={}
                data['message']=MESSAGE.UNABLE_TO_CREATE
                data['status']="failed"
            user=User.objects.get(username=username)
            request.session['uid']=user.id
        else:
            data={}
            data['message']=MESSAGE.USER_EXISTS
            data['status']="failed"

        request.session['data']=data
        if settings.enable2fa:
            code=get2FACode()
            request.session['2fa']=code
            send2FACode(code,phone)
            return HttpResponseRedirect("verify")
        else:
            return HttpResponseRedirect("login")
    else:
        data={}
        data['message']=MESSAGE.USER_EXISTS
        data['status']="failed"
        request.session['data']=data
        return HttpResponseRedirect("login")



def verify(request):
    template = loader.get_template('portal_verify.html')
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))


def verifycode(request):
    print "2FA Verification"
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
                user.is2faverified=1
                user.save()
            request.session['message']="Please login"
            return HttpResponseRedirect("login")
        else:
            request.session['message']="Invalid verification token"
            return HttpResponseRedirect("verify")


from random import randint

def get2FACode():
    n=6
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def send2FACode(code,receipient):
    url="http://www.estoresms.com"
    username="biddyweb"
    password="googleboy234"
    s=SMSGateway(url,username,password)
    method="GET"
    endpoint="smsapi.php"
    params={}
    params['username']=username
    params['password']=password
    params['sender']=settings.sitenameshort
    params['recipient']=str(receipient)
    params['message']="Welcome to "+settings.sitename+" online. Your validation token is: "+str(code)
    s.sendMessage(method,endpoint,params)





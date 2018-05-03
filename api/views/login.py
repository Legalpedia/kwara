from imports import *



#authenticate user
#@csrf_protect
@csrf_exempt
def auth(request):
    if request.method == "POST":
        response=verifySignature(request)
        if response['status']=="failed":
            return JsonResponse(response)
        username=request.POST.get("username")
        passwd=request.POST.get("password")
        password=hashlib.sha256(passwd).hexdigest()
        currentuser={}
        try:
            userobject=User.objects.filter(Q(username=username) &Q(password=password)).get()
            if userobject.username==username:
                #check if device type has permission
                currentuser['uid']=userobject.id
                currentuser['username']=userobject.username
                currentuser['secret']=userobject.secret
                profileobject=Profile.objects.filter(Q(uid=currentuser['uid'])).get()
                currentuser['firstname']=profileobject.firstname
                currentuser['lastname']=profileobject.lastname
                currentuser['email']=profileobject.email
                currentuser['phone']=profileobject.phone
                currentuser['pid']=profileobject.id
                data={}
                data['message']=MESSAGE.LOGIN_SUCCESS
                data['requiresupdate']=0
                data['status']="ok"
                data['user']=currentuser
                request.session['isloggedin'] =True
                request.session['uid'] =userobject.id
                #request.session['sessionhash'] =uid:
            else:
                data={}
                data['message']=MESSAGE.LOGIN_FAIL
                data['status']="failed"
        except Exception as ex:
            print ex
            data={}
            data['message']=MESSAGE.LOGIN_FAIL
            data['status']="failed"

        return JsonResponse(data)
    else:
        data={}
        data['message']=MESSAGE.INVALID_REQUEST_POST
        data['status']="failed"
        return JsonResponse(data)
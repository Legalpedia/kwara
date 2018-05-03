from imports import *

def login(request):
    template = loader.get_template('portal_login.html')
    data['message']=None
    if "message" in request.session:
        data['message']=request.session['message']
        del request.session['message']
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))

def logout(request):
    	for key in request.session.keys():
		del request.session[key]
	request.session.modified = True
	return HttpResponseRedirect("/login")


def forgotpasswd(request):
    template = loader.get_template('portal_forgotpasswd.html')
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))


def auth(request):
    if request.method == "POST":
            username=request.POST.get("username")
            passwd=request.POST.get("password")
            password=hashlib.sha256(passwd).hexdigest()
            try:
                user=User.objects.filter(Q(username=username) & Q(password=password)).get()
                print user
                if user.username!=None:
                    #check if device type has permission
                    data={}
                    request.session['isloggedin']=True
                    request.session['username']=username
                    request.session['uid']=user.id
                    return HttpResponseRedirect("/portal")

                else:
                    if user.username==username and user.password!=password:
                        request.session['message']="Invalid password. Please check your password"
                    else:
                        request.session['message']="Invalid username/password pair"
                    return HttpResponseRedirect("login")
            except Exception as ex:
                request.session['message']="Invalid username/password pair"
                request.session['isloggedin']=False
                return HttpResponseRedirect("login")



    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

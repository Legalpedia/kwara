from imports import *

def activity(request):
    if request.session.get('isloggedin', False):
        template = loader.get_template('portal_activity.html')
        uid=str(request.session.get("uid"))
        data['message']=None
        if "message" in request.session:
            data['message']=request.session['message']
            del request.session['message']
        user=User.objects.raw("SELECT a.id as id,a.username,a.status as status,b.firstname as firstname,b.uid as uid,b.lastname as lastname,b.email as email,b.phone as phone,b.skype as skype,b.city as city,b.country as country,b.address1 as address1,b.address2 as address2,b.town as town from api_user a,api_profile b WHERE a.id=b.uid AND a.id="+uid)
        data['user']=user[0]
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def profile(request):
    if request.session.get('isloggedin', False):
        template = loader.get_template('portal_profile.html')
        uid=str(request.session.get("uid"))
        data['message']=None
        if "message" in request.session:
            data['message']=request.session['message']
            del request.session['message']
        user=User.objects.raw("SELECT a.id as id,a.username,a.status as status,b.firstname as firstname,b.uid as uid,b.lastname as lastname,b.email as email,b.phone as phone,b.skype as skype,b.city as city,b.country as country,b.address1 as address1,b.address2 as address2,b.town as town from api_user a,api_profile b WHERE a.id=b.uid AND a.id="+uid)
        data['user']=user[0]
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def updateprofile(request):
    if request.session.get('isloggedin', False):
        try:
            uid=request.POST.get("id")
            firstname=request.POST.get("surname").strip()
            lastname=request.POST.get("lastname").strip()
            telephone=str(request.POST.get("telephone")).strip()
            email=request.POST.get("email").strip()
            skype=str(request.POST.get("skype")).strip()
            address1=str(request.POST.get("address1")).strip()
            address2=str(request.POST.get("address2")).strip()
            city=str(request.POST.get("city"))
            town=str(request.POST.get("town"))
            state=str(request.POST.get("state"))
            country=str(request.POST.get("country"))
            checkuser=User.objects.raw("SELECT * FROM api_user,api_profile where api_user.id=api_profile.uid AND (api_user.id='"+uid+"' OR api_profile.email='"+email+"' OR api_profile.phone='"+telephone+"')")
            if len(list(checkuser))>0:
                profile=Profile.objects.get(uid=uid)
                print profile
                profile.email=email
                profile.firstname=firstname
                profile.lastname=lastname
                profile.phone=telephone
                profile.skype=skype
                profile.address1=address1
                profile.address2=address2
                #profile.city=city
                #profile.town=town
                #profile.state=state
                #profile.country=country
                profile.save()
        except Exception as ex:
            print ex
        return HttpResponseRedirect("../profile")
    else:
        return HttpResponseRedirect("login")

def updatepassword(request):
    pass
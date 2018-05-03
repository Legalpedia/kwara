from imports import *


def package(request):
    template = loader.get_template('manager_packages.html')
    context = {
    'data': data
    }
    return HttpResponse(template.render(context, request))


def createpackage(request):
    if request.session.get('ismanagerloggedin', False):
        data={}
        name=request.POST['name']
        try:
            package=Package.objects.create(name=name)
            data['status']="ok"
            data['message']="successfully created package"
        except Exception as ex:
            data['status']="failed"
            data['message']="unable to create package"
        return HttpResponseRedirect("../package")
    else:
        request.session['isloggedin']=False
        data={}
        data['status']="failed"
        data['message']="requires authentication"
        return HttpResponseRedirect("login")

def deletepackage(request):
    if request.session.get('ismanagerloggedin', False):
        data={}
        id=request.GET.get('id','')
        package=Package.objects.get(id=id)
        package.delete()
        data['status']="ok"
        data['message']="successfully deleted"
        return HttpResponseRedirect("../package")
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")


#list package
def listpackage(request):
    if request.session.get('ismanagerloggedin', False):
        data={}
        if request.method == "GET":
            #response=verifySignature(request)
            #if response['status']=="failed":
            #    return JsonResponse(response)
            try:

                offset=request.GET['offset']
                limit=request.GET['limit']
                pager="LIMIT "+offset+","+limit
                package=Package.objects.raw("SELECT * from api_package "+pager)
                listdata=getPackageDict(package)
                data={}
                data['rows']=listdata
                data['total']=len(list(Package.objects.raw("SELECT * from api_package")))
            except Exception as ex:
                data={}
                data['status']="failed"
                data['message']="failed"
            return JsonResponse(data)
        else:
            data['status']="failed"
            data['message']="invalid request"
            return JsonResponse(data)
    else:
        data={}
        data['status']="failed"
        data['message']="invalid session"
        return JsonResponse(data)




def updatepackage(request):
    if request.session.get('ismanagerloggedin', False):
        data={}
        id=request.POST['id']
        name=request.POST['name']
        package=Package.objects.get(id=id)
        package.id=id
        package.name=name
        package.save()
        return HttpResponseRedirect("../package")
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

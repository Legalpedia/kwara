from imports import *


def index(request):
    if request.session.get('isloggedin', False):
        template = loader.get_template('portal_dashboard.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")



def indexmain(request):
    if request.session.get('isloggedin', False):
        template = loader.get_template('portal_dashboard.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")




def noteview(request):
    if request.session.get('isloggedin', False):
        template = loader.get_template('portal_noteview.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def searchview(request):
    if request.session.get('isloggedin', False):
        template = loader.get_template('portal_search.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def profile(request):
    pass










from imports import *



#checkupdates
#@csrf_protect
@csrf_exempt
def checkupdates(request):
    if request.session.get('isloggedin', False):

        return JsonResponse(data)
    else:
        return JsonResponse(data)


#fetchupdates
#@csrf_protect
@csrf_exempt
def fetchupdates(request):
    if request.session.get('isloggedin', False):

        return JsonResponse(data)
    else:
        return JsonResponse(data)
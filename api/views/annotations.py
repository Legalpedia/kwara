from imports import *




@csrf_exempt
def addannotation(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            case_id=request.POST.get("id")
            title=request.POST.get("title")
            uid=request.POST.get("uid")
            position=request.POST.get("position")
            comment=request.POST.get("comment")

            annotation=Annotations.objects.create(case_id=case_id,ratio_title=title,uid=uid,position=position,comment=comment,createdate=timezone.now())
            if annotation.id!=None:
                data={}
                data['status']="ok"
                data['message']="annotation added successfully"
            else:
                data={}
                data['message']="unable to create annotation"
                data['status']="failed"
            context = {
                'data': data
                }
            return JsonResponse(context)
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return JsonResponse(context)

    else:
        data={}
        data['message']="user not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return JsonResponse(context)

@csrf_exempt
def listannotations(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        uid=request.session.get("uid",0)
        annotation=Annotations.objects.raw("SELECT * from api_annotations WHERE uid="+str(uid)+" "+pager)
        data={}
        data['total']= Annotations.objects.count()
        data['rows']=annotationToJson(annotation)
        return JsonResponse(data)
    else:
        data={}
        data['message']="user not loggedin"
        data['status']="failed"
        return JsonResponse(data)

@csrf_exempt
def deleteannotation(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            annotationid=request.GET['id']
        else:
            annotationid=id

        try:
            annotation=Annotations.objects.get(id=annotationid)
            annotation.delete()
            data={}
            data['status']="ok"
            data['message']="annotation deleted successfully"
        except Exception as ex:
            data={}
            data['message']="unable to delete annotation"
            data['status']="failed"
        return JsonResponse(data)
    else:
        data={}
        data['message']="user not loggedin"
        data['status']="failed"
        return JsonResponse(data)



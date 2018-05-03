from imports import *

@csrf_exempt
def addnote(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            case_id=request.POST.get("id")
            title=request.POST.get("title")
            uid=request.POST.get("uid")
            position=request.POST.get("position")
            comment=request.POST.get("comment")

            note=Notes.objects.create(case_id=case_id,ratio_title=title,uid=uid,position=position,comment=comment,createdate=timezone.now())
            if note.id!=None:
                data={}
                data['status']="ok"
                data['message']="note added successfully"
            else:
                data={}
                data['message']="unable to create note"
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
def listnotes(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        uid=request.session.get("uid",0)
        note=Notes.objects.raw("SELECT * from api_notes  WHERE uid="+str(uid)+" "+pager)
        data={}
        data['total']= Notes.objects.count()
        data['rows']=notesToJson(note)
        return JsonResponse(data)
    else:
        data={}
        data['message']="user not loggedin"
        data['status']="failed"
        return JsonResponse(data)

@csrf_exempt
def deletenote(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            noteid=request.GET['id']
        else:
            noteid=id
        try:
            note=Notes.objects.get(id=noteid)
            note.delete()
            data={}
            data['status']="ok"
            data['message']="note deleted successfully"
        except Exception as ex:
            data={}
            data['message']="unable to delete note"
            data['status']="failed"
        return JsonResponse(data)
    else:
        data={}
        data['message']="user not loggedin"
        data['status']="failed"
        return JsonResponse(data)
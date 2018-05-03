from imports import *

@csrf_exempt
def listsections(request,sectionid):
    data={}
    data['status']="ok"
    sections=Sections.objects.filter(lawid=sectionid).order_by('title').all()
    datalist=sectionsToJson(sectionid,sections)
    return HttpResponse(serialize(datalist), content_type='application/json')

@csrf_exempt
def getsection(request):
    laws=Laws.objects.order_by('title').all()
    datalist=lawsToJson(laws)
    return HttpResponse(serialize(datalist), content_type='application/json')

@csrf_exempt
def getlawdetail(request,sectionid):
    data={}
    data['status']="ok"
    sections=Sections.objects.get(id=sectionid)
    datalist=sectionDetailToJson(sections)
    return HttpResponse(serialize(datalist), content_type='application/json')

@csrf_exempt
def getlaw(request,lawid):
    data={}
    data['status']="ok"
    law=Laws.objects.get(id=lawid)
    datalist=lawfullToJson(law)
    return HttpResponse(serialize(datalist), content_type='application/json')

@csrf_exempt
def search(request):
    query=request.GET.get("query")
    data={}
    data['status']="ok"
    sqlquery="select a.id as id,b.id as sectionid,a.title as lawtitle,b.title as sectiontitle from api_laws a,api_sections b where a.title like '%%"+query+"' or b.title like '%%"+query+"' or a.description like '%%"+query+"' or b.body like '%%"+query+"' limit 10"
    print sqlquery
    result=Sections.objects.raw(sqlquery)
    searchresult=searchResultToJson(result)
    return HttpResponse(serialize(searchresult), content_type='application/json')
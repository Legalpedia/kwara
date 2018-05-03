from imports import *

def billing(request):
    if request.session.get('isloggedin', False):
        template = loader.get_template('portal_billing.html')
        data['duration'] = range(1, 25)
        data['paymentoptions']=PackageInfo.objects.all()
        data['message']=None
        if "message" in request.session:
            data['message']=request.session['message']
            del request.session['message']
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")

def listpayments(request):
    if request.session.get('isloggedin', False):
        uid=str(request.session.get("uid"))
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        transaction=Transactions.objects.raw("SELECT  a.id as id,b.username as username,amount,tax,description,commission,a.status,a.createdate as paymentdate from api_transactions a,api_user b WHERE a.uid=b.id AND a.uid="+uid+" "+pager)
        data={}
        data['total']= len(list(Transactions.objects.raw("SELECT  a.id as id,b.username as username,amount,tax,description,commission,a.status,a.createdate as paymentdate from api_transactions a,api_user b WHERE a.uid=b.id AND a.uid="+uid)))
        data['rows']=transactionsToJson(transaction)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")


def payment(request):
    if request.session.get('isloggedin', False):
        template = loader.get_template('portal_payment.html')
        pid=request.POST.get("pinfo")
        duration=request.POST.get("duration")
        pinfo=PackageInfo.objects.get(id=pid)
        uid=request.session.get("uid")
        profile=Profile.objects.get(uid=uid)
        data['payment_gateway']="paystack"#"kongapay"
        data['merchantid']="pk_test_294b393b858f07d85789bc1d0029a482568cf605" #"testmerchant"
        data['merchantname']="Kwara Law"
        data['phone']=profile.phone
        data['callbackurl']="http://k1.mobilipia.com/completed"
        data['amount']=str(int(pinfo.price) * int(duration))
        data['email']=profile.email
        genuuid=uuid.uuid4()
        data['transid']=genuuid.hex.upper()
        data['description']="Payment for "+pinfo.name
        try:
            transaction=Transactions.objects.create(packageinfo=pid,duration=duration,uid=uid,tax=0.0,commission=0.0,voucher_code="",amount=data['amount'],reference=data['transid'],otherref="",description=data['description'],status=0,createdate=timezone.now())
            data['transactionid']=transaction.id
        except Exception as ex:
            print ex
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("/portal/login")


def paymentcompleted(request):
    if request.session.get('isloggedin', False):
        url="https://api.paystack.co/transaction/verify/"
        txnref=request.GET.get('reference','Not Available')
        transactionid=request.GET.get('transactionid',0)
        fullurl=url+txnref
        secret_key="sk_test_b9ffbfbaf3f29559d8945aed1b11b8b7d1db708a"
        headers={"Authorization":"Bearer "+secret_key}
        res=requests.get(fullurl,headers=headers)
        response=json.loads(res.content)
        status=response['data']['status']
        amountgateway=response['data']['amount']
        reason=response['data']['gateway_response']
        transaction=Transactions.objects.get(id=transactionid)
        pid=transaction.packageinfo
        duration=transaction.duration * 30
        amounttrans=transaction.amount*100
        pinfo=PackageInfo.objects.get(id=pid)
        uid=request.session.get("uid")
        data={}
        if transaction.status==1:
            data['message']="Successfully renewed subscription"
        elif status and transaction.status==0:

            if amountgateway==amounttrans:
                transaction.status=1
                transaction.otherref=txnref
                transaction.save()
                uservalidity=UserValidity.objects.get(uid=uid)
                lastrenewdate=datetime.strptime(uservalidity.nextrenewdate.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                renewdate = lastrenewdate + timedelta(days=duration)
                currentdate=datetime.now()
                uservalidity.lastnewdate=currentdate.strftime("%Y-%m-%d %H:%M:%S")
                uservalidity.nextrenewdate=renewdate.strftime("%Y-%m-%d %H:%M:%S")
                uservalidity.save()
                data['message']="Successfully renewed subscription"
            else:
                data['message']="Amount does not match"
        else:
            data['message']="Unable to complete payment ("+reason+")"

        template = loader.get_template('portal_paymentcompleted.html')
        context = {
            'data': data
            }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("/portal/login")
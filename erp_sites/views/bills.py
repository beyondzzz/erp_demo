#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getPackage,getBills,isValid
import traceback
from erp_sites.models import Bills,BillsSub,PackageOrTeardownOrder
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def billInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            bills_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            bills_code = 'AP-' + bills_date[0:10] + '-'
            if 'customerSupplierID' in json2Dict:
                if isValid(json2Dict['customerSupplierID']):
                    customer_supplier_id = int(json2Dict['customerSupplierID'])
                else:
                    customer_supplier_id = 0
            else:
                customer_supplier_id = 0
            if 'billsType' in json2Dict:
                if isValid(json2Dict['billsType']):
                    bills_type = json2Dict['billsType']
                else:
                    bills_type = 0
            else:
                bills_type = None
            if 'bank' in json2Dict:
                if isValid(json2Dict['bank']):
                    bank = json2Dict['bank']
                else:
                    bank = None
            else:
                bank = None
            if 'bankAccount' in json2Dict:
                if isValid(json2Dict['bankAccount']):
                    bank_account = json2Dict['bankAccount']
                else:
                    bank_account = None
            else:
                bank_account = None
            if 'payment' in json2Dict:
                if isValid(json2Dict['payment']):
                    payment = int(json2Dict['payment'])
                else:
                    payment = 0
            else:
                payment = 0
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                else:
                    originator = None
            else:
                originator = None
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                else:
                    person_id = 0
            else:
                person_id = 0
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                else:
                    summary = None
            else:
                summary = None
            if 'remark' in json2Dict:
                if isValid(json2Dict['remark']):
                    remark = json2Dict['remark']
                else:
                    remark = None
            else:
                remark = None
            if 'money' in json2Dict:
                if isValid(json2Dict['money']):
                    money = atof(json2Dict['money'])
                else:
                    money = 0
            else:
                money = 0
            if 'ticketNo' in json2Dict:
                if isValid(json2Dict['ticketNo']):
                    ticket_no = json2Dict['ticketNo']
                else:
                    ticket_no = None
            else:
                ticket_no = None
            if 'branch' in json2Dict:
                if isValid(json2Dict['branch']):
                    branch = json2Dict['branch']
                else:
                    branch = None
            else:
                branch = None
            if 'balance' in json2Dict:
                if isValid(json2Dict['balance']):
                    balance = atof(json2Dict['balance'])
                else:
                    balance = 0
            else:
                balance = 0
            if 'account' in json2Dict:
                if isValid(json2Dict['account']):
                    account = json2Dict['account']
                else:
                    account = None
            else:
                account = None
            if 'orderType' in json2Dict:
                if isValid(json2Dict['orderType']):
                    order_type = json2Dict['orderType']
                else:
                    order_type = None
            else:
                order_type = None
            bill = Bills(None,bills_code,customer_supplier_id,bills_type,bills_date,bank,bank_account,payment,originator,person_id,summary,remark,money,ticket_no,branch,balance,account,order_type)
            bill.save()
            bill.bills_code = bills_code + str(bill.id)
            bill.save()
            if 'billsSubs' in json2Dict:
                billsSubs = json2Dict['billsSubs']
                for billsSub in billsSubs:
                    bills_id = bill.id
                    if 'procureSalesID' in billsSub:
                        if isValid(billsSub['procureSalesID']):
                            procure_sales_id = int(billsSub['procureSalesID'])
                        else:
                            procure_sales_id = 0
                    else:
                        procure_sales_id = 0
                    if 'clearingMoney' in billsSub:
                        if isValid(billsSub['clearingMoney']):
                            clearing_money = atof(billsSub['clearingMoney'])
                        else:
                            clearing_money = 0
                    else:
                        clearing_money = 0
                    if 'stayMoney' in billsSub:
                        if isValid(billsSub['stayMoney']):
                            stay_money = atof(billsSub['stayMoney'])
                        else:
                            stay_money = 0
                    else:
                        stay_money = 0
                    if 'theMoeny' in billsSub:
                        if isValid(billsSub['theMoeny']):
                            the_moeny = atof(billsSub['theMoeny'])
                        else:
                            the_moeny = 0
                    else:
                        the_moeny = 0
                    if 'actualMoney' in billsSub:
                        if isValid(billsSub['actualMoney']):
                            actual_money = atof(billsSub['actualMoney'])
                        else:
                            actual_money = 0
                    else:
                        actual_money = 0
                    if 'rebateMoney' in billsSub:
                        if isValid(billsSub['rebateMoney']):
                            rebate_money = atof(billsSub['rebateMoney'])
                        else:
                            rebate_money = 0
                    else:
                        rebate_money = 0
                    if 'isPayment' in billsSub:
                        if isValid(billsSub['isPayment']):
                            is_payment = billsSub['isPayment']
                        else:
                            is_payment = None
                    else:
                        is_payment = None
                    if 'rebate' in billsSub:
                        if isValid(billsSub['rebate']):
                            rebate = int(billsSub['rebate'])
                        else:
                            rebate = 0
                    else:
                        rebate = 0
                    if 'remark' in billsSub:
                        if isValid(billsSub['remark']):
                            remark = billsSub['remark']
                        else:
                            remark = None
                    else:
                        remark = None
                    if 'payMoney' in billsSub:
                        if isValid(billsSub['payMoney']):
                            pay_money = atof(billsSub['payMoney'])
                        else:
                            pay_money = 0
                    else:
                        pay_money = 0
                    billsSubObj = BillsSub(None,bills_id,procure_sales_id,clearing_money,stay_money,the_moeny,actual_money,rebate_money,is_payment,rebate,remark,pay_money)
                    billsSubObj.save()
            billsJSON = getBills(bill)
            billInsert = setStatus(200,billsJSON)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        billInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(billInsert), content_type='application/json')


def singleBillSelect(request):
    try:
        if isTokenExpired(request):
            billsCode = request.GET['billsCode']
            bills = Bills.objects.filter(bills_code=billsCode)
            if len(bills) > 0:
                bill = bills[0]
                singleBillSelect = getBills(bill)
            else:
                singleBillSelect = setStatus(300, {})
                return HttpResponse(json.dumps(singleBillSelect), content_type='application/json')
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        singleBillSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(singleBillSelect), content_type='application/json')


def multiBillSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                condition = {}
                selectType = {}
                if 'billsType' in request.GET and isValid(request.GET['billsType']):
                    condition['bills_type'] = int(request.GET['billsType'])
                if 'queryTime' in request.GET:
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                multiBillSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                multiBillSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        multiBillSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(multiBillSelect), content_type='application/json')



def paging(request, ONE_PAGE_OF_DATA, condition, selectType):
    logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    allPage = 1
    if condition == None:
        basicsCount = Bills.objects.all().count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = PackageOrTeardownOrder.objects.filter(
                Q(**condition) & Q(bills_date__gte=timeFrom) & Q(bills_date__lte=timeTo)).count()
        else:
            basicsCount = Bills.objects.filter(**condition).count()
    if basicsCount != 0:
        if basicsCount % ONE_PAGE_OF_DATA == 0:
            allPage = basicsCount / ONE_PAGE_OF_DATA
        else:
            allPage = basicsCount / ONE_PAGE_OF_DATA + 1
    else:
        allPage = 1
    if curPage == 1:
        if condition == None:
            basicObjs = Bills.objects.all()[0:ONE_PAGE_OF_DATA]
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = Bills.objects.filter(
                    Q(**condition) & Q(bills_date__gte=timeFrom) & Q(bills_date__lte=timeTo))[0:ONE_PAGE_OF_DATA]
            else:
                basicObjs = Bills.objects.filter(**condition)[0:ONE_PAGE_OF_DATA]
        for basicObj in basicObjs:
            basicJSON = getBills(basicObj)
            datasJSON.append(basicJSON)
    else:
        if curPage > allPage or curPage < 1:
            pagingSelect['code'] = 300
            pagingSelect['curPage'] = curPage
            pagingSelect['allPage'] = allPage
            pagingSelect['data'] = 'curPage is invalid !'
            return pagingSelect
        startPos = (curPage - 1) * ONE_PAGE_OF_DATA
        endPos = startPos + ONE_PAGE_OF_DATA
        if condition == None:
            basicObjs = Bills.objects.all()[startPos:endPos]
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = Bills.objects.filter(
                    Q(**condition) & Q(bills_date__gte=timeFrom) & Q(bills_date__lte=timeTo))[startPos:endPos]
            else:
                basicObjs = PackageOrTeardownOrder.objects.filter(**condition)[startPos:endPos]
        for basicObj in basicObjs:
            basicJSON = getBills(basicObj)
            datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
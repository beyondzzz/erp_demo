#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getPackage,getWriteoff,isValid
import traceback
from erp_sites.models import Writeoff,WriteoffSub
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def writeoffInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            writeoff_code = 'AT-' + create_date[0:10] + '-'
            if 'writeoffType' in json2Dict:
                if isValid(json2Dict['writeoffType']):
                    writeoff_type = json2Dict['writeoffType']
                else:
                    writeoff_type = None
            else:
                writeoff_type = None
            if 'companyOne' in json2Dict:
                if isValid(json2Dict['companyOne']):
                    company_one = int(json2Dict['companyOne'])
                else:
                    company_one = 0
            else:
                company_one = 0
            if 'companyTwo' in json2Dict:
                if isValid(json2Dict['companyTwo']):
                    company_two = int(json2Dict['companyTwo'])
                else:
                    company_two = 0
            else:
                company_two = 0
            if 'money' in json2Dict:
                if isValid(json2Dict['money']):
                    money = atof(json2Dict['money'])
                else:
                    money = 0
            else:
                money = 0
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
            if 'voucherNo' in json2Dict:
                if isValid(json2Dict['voucherNo']):
                    voucher_no = json2Dict['voucherNo']
                else:
                    voucher_no = None
            else:
                voucher_no = None
            if 'branch' in json2Dict:
                if isValid(json2Dict['branch']):
                    branch = json2Dict['branch']
                else:
                    branch = None
            else:
                branch = None
            writeoff = Writeoff(None,writeoff_code,writeoff_type,company_one,company_two,money,create_date,originator,person_id,summary,remark,voucher_no,branch)
            writeoff.save()
            writeoff.writeoff_code = writeoff_code + str(writeoff.id)
            writeoff.save()
            if 'writeOffSubs' in json2Dict:
                writeOffSubs = json2Dict['writeOffSubs']
                for writeOffSub in writeOffSubs:
                    writeoff_id = writeoff.id
                    if 'procureSalesID' in writeOffSub:
                        if isValid(writeOffSub['procureSalesID']):
                            procure_sales_id = int(writeOffSub['procureSalesID'])
                        else:
                            procure_sales_id = 0
                    else:
                        procure_sales_id = 0
                    if 'clearMoney' in writeOffSub:
                        if isValid(writeOffSub['clearMoney']):
                            clear_money = atof(writeOffSub['clearMoney'])
                        else:
                            clear_money = 0
                    else:
                        clear_money = 0
                    if 'stayMoney' in writeOffSub:
                        if isValid(writeOffSub['stayMoney']):
                            stay_money = atof(writeOffSub['stayMoney'])
                        else:
                            stay_money = 0
                    else:
                        stay_money = 0
                    if 'theMoney' in writeOffSub:
                        if isValid(writeOffSub['theMoney']):
                            the_money = int(writeOffSub['theMoney'])
                        else:
                            the_money = 0
                    else:
                        the_money = 0
                    if 'isWriteoff' in writeOffSub:
                        if isValid(writeOffSub['isWriteoff']):
                            is_writeoff = writeOffSub['isWriteoff']
                        else:
                            is_writeoff = None
                    else:
                        is_writeoff = None
                    if 'isProcureSales' in writeOffSub:
                        if isValid(writeOffSub['isProcureSales']):
                            is_procure_sales = int(writeOffSub['isProcureSales'])
                        else:
                            is_procure_sales = 0
                    else:
                        is_procure_sales = 0
                    if 'remark' in writeOffSub:
                        if isValid(writeOffSub['remark']):
                            remark = writeOffSub['remark']
                        else:
                            remark = None
                    else:
                        remark = None
                    writeoffSubObj = WriteoffSub(None,writeoff_id,procure_sales_id,clear_money,stay_money,the_money,is_writeoff,is_procure_sales,remark)
                    writeoffSubObj.save()
            writeoffJSON = getWriteoff(writeoff)
            writeoffInsert = setStatus(200,writeoffJSON)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        writeoffInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(writeoffInsert), content_type='application/json')


def singleWriteoffSelect(request):
    try:
        if isTokenExpired(request):
            writeoff_code = request.GET['writeoffCode']
            writeoffs = Writeoff.objects.filter(writeoff_code=writeoff_code)
            if len(writeoffs) > 0:
                writeoff = writeoffs[0]
                singleWriteoffSelect = getWriteoff(writeoff)
            else:
                singleWriteoffSelect = setStatus(300, {})
                return HttpResponse(json.dumps(singleWriteoffSelect), content_type='application/json')
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        singleWriteoffSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(singleWriteoffSelect), content_type='application/json')


def multiWriteoffSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                condition = {}
                selectType = {}
                if 'writeoffType' in request.GET and isValid(request.GET['writeoffType']):
                    condition['writeoff_type'] = int(request.GET['writeoffType'])
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                multiWriteoffSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                multiWriteoffSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        multiWriteoffSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(multiWriteoffSelect), content_type='application/json')



def paging(request, ONE_PAGE_OF_DATA, condition, selectType):
    logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    if 'sizePage' in request.GET:
        ONE_PAGE_OF_DATA = int(request.GET['sizePage'])
    allPage = 1
    if condition == None:
        basicsCount = Writeoff.objects.all().count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = Writeoff.objects.filter(
                Q(**condition) & Q(create_date__gte=timeFrom) & Q(create_date__lte=timeTo)).count()
        else:
            basicsCount = Writeoff.objects.filter(**condition).count()
    if basicsCount != 0:
        if basicsCount % ONE_PAGE_OF_DATA == 0:
            allPage = basicsCount / ONE_PAGE_OF_DATA
        else:
            allPage = basicsCount / ONE_PAGE_OF_DATA + 1
    else:
        allPage = 1
    
    if curPage > allPage or curPage < 1:
        pagingSelect['code'] = 300
        pagingSelect['curPage'] = curPage
        pagingSelect['allPage'] = allPage
        pagingSelect['data'] = 'curPage is invalid !'
        return pagingSelect
    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    if condition == None:
        basicObjs = Writeoff.objects.all()[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = Writeoff.objects.filter(
                    Q(**condition) & Q(create_date__gte=timeFrom) & Q(create_date__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = Writeoff.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getWriteoff(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getBreakage,isValid
import traceback
from erp_sites.models import BreakageOrder,BreakageOrderCommodity
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def breakageInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            breakage_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'BO-' + breakage_date[0:10] + '-'
            if 'warehouseID' in json2Dict:
                if isValid(json2Dict['warehouseID']):
                    warehouse_id = int(json2Dict['warehouseID'])
                else:
                    warehouse_id = 0
            else:
                warehouse_id = 0
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                else:
                    person_id = 0
            else:
                person_id = 0
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                else:
                    originator = None
            else:
                originator = None
            if 'reviewer' in json2Dict:
                if isValid(json2Dict['reviewer']):
                    reviewer = json2Dict['reviewer']
                else:
                    reviewer = None
            else:
                reviewer = None
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                else:
                    summary = None
            else:
                summary = None
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                else:
                    state = 0
            else:
                state = 0
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                else:
                    print_num = 0
            else:
                print_num = 0
            is_delete = 0
            breakage = BreakageOrder(None,breakage_date,identifier,warehouse_id,person_id,originator,reviewer,summary,state,print_num,is_delete)
            breakage.save()
            breakage.identifier = identifier + str(breakage.id)
            breakage.save()
            if 'breakageCommodities' in json2Dict:
                breakageCommodities = json2Dict['breakageCommodities']
                for breakageCommodity in breakageCommodities:
                    breakage_order_id = breakage.id
                    if 'commoditySpecificationID' in breakageCommodity:
                        if isValid(json2Dict['commoditySpecificationID']):
                            commodity_specification_id = int(breakageCommodity['commoditySpecificationID'])
                        else:
                            commodity_specification_id = 0
                    else:
                        commodity_specification_id = 0
                    if 'number' in breakageCommodity:
                        if isValid(json2Dict['number']):
                            number = int(breakageCommodity['number'])
                        else:
                            number = 0
                    else:
                        number = 0
                    if 'unitPrice' in breakageCommodity:
                        if isValid(json2Dict['unitPrice']):
                            unit_price = atof(breakageCommodity['unitPrice'])
                        else:
                            unit_price = 0
                    else:
                        unit_price = 0
                    if 'money' in breakageCommodity:
                        if isValid(json2Dict['money']):
                            money = atof(breakageCommodity['money'])
                        else:
                            money = 0
                    else:
                        money = 0
                    breakageCommodityObj = BreakageOrderCommodity(None,breakage_order_id,commodity_specification_id,number,unit_price,money)
                    breakageCommodityObj.save()
            breakageJSON = getBreakage(breakage)
            breakageInsert = setStatus(200,breakageJSON)
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        breakageInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(breakageInsert), content_type='application/json')


def breakageDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                breakages = BreakageOrder.objects.filter(id=identifier)
                if len(breakages) > 0:
                    breakage = breakages[0]
                    breakage.is_delete = 1
                    breakage.save()
                    breakageDelete = setStatus(200,{})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    breakageDelete = setStatus(300, errorIDs)
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        breakageDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(breakageDelete), content_type='application/json')


def breakageUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            breakages = BreakageOrder.objects.filter(identifier=identifier)
            if len(breakages) > 0:
                breakage = breakages[0]
            else:
                breakageUpdate = setStatus(300,{})
                return HttpResponse(json.dumps(breakageUpdate), content_type='application/json')
            if 'warehouseID' in json2Dict:
                if isValid(json2Dict['warehouseID']):
                    warehouse_id = int(json2Dict['warehouseID'])
                    breakage.warehouse_id = warehouse_id
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                    breakage.person_id = person_id
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                    breakage.originator = originator
            if 'reviewer' in json2Dict:
                if isValid(json2Dict['reviewer']):
                    reviewer = json2Dict['reviewer']
                    breakage.reviewer = reviewer
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                    breakage.summary = summary
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                    breakage.state = state
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                    breakage.print_num = print_num
            breakage.save()
            if 'breakageOrderCommodities' in json2Dict:
                breakageCommodities = json2Dict['breakageCommodities']
                for breakageCommodity in breakageCommodities:
                    if 'breakageCommodityID' in breakageCommodity:
                        breakageCommodityID = breakageCommodity['breakageCommodityID']
                        breakageCommodityObjs = BreakageOrderCommodity.objects.filter(id=breakageCommodityID)
                        if len(breakageCommodityObjs) > 0:
                            breakageCommodityObj = breakageCommodityObjs[0]
                        else:
                            breakageUpdate = setStatus(300,{})
                            return HttpResponse(json.dumps(breakageUpdate), content_type='application/json')
                    else:
                        continue
                    if 'commoditySpecificationID' in breakageCommodity:
                        if isValid(breakageCommodity['commoditySpecificationID']):
                            commodity_specification_id = int(breakageCommodity['commoditySpecificationID'])
                            breakageCommodityObj.commodity_specification_id = commodity_specification_id
                    if 'number' in breakageCommodity:
                        if isValid(breakageCommodity['number']):
                            number = int(breakageCommodity['number'])
                            breakageCommodityObj.number = number
                    if 'unitPrice' in breakageCommodity:
                        if isValid(breakageCommodity['unitPrice']):
                            unit_price = atof(breakageCommodity['unitPrice'])
                            breakageCommodityObj.unit_price = unit_price
                    if 'money' in breakageCommodity:
                        if isValid(breakageCommodity['money']):
                            money = atof(breakageCommodity['money'])
                            breakageCommodityObj.money = money
                    breakageCommodityObj.save()
            breakageJSON = getBreakage(breakage)
            breakageUpdate = setStatus(200,breakageJSON)
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        breakageUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(breakageUpdate), content_type='application/json')


def breakageSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                condition = {}
                selectType = {}
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'warehouseID' in request.GET and isValid(request.GET['warehouseID']):
                    condition['warehouse_id'] = int(request.GET['warehouseID'])
                if 'personID' in request.GET and isValid(request.GET['personID']):
                    condition['person_id'] = int(request.GET['personID'])
                if 'state' in request.GET and isValid(request.GET['state']):
                    condition['state'] = int(request.GET['state'])
                condition['is_delete'] = 0
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                breakageSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                breakageSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        breakageSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(breakageSelect), content_type='application/json')


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
        basicsCount = BreakageOrder.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = BreakageOrder.objects.filter(
                Q(**condition) & Q(breakage_date__gte=timeFrom) & Q(breakage_date__lte=timeTo)).count()
        else:
            basicsCount = BreakageOrder.objects.filter(**condition).count()
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
        basicObjs = BreakageOrder.objects.filter(is_delete=0)[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = BreakageOrder.objects.filter(
                    Q(**condition) & Q(breakage_date__gte=timeFrom) & Q(breakage_date__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = BreakageOrder.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getBreakage(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
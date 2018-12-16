#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getPackage,isValid
import traceback
from erp_sites.models import PackageOrTeardownOrder,PackageOrTeardownOrderCommodity
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def packageOrTeardownInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            package_or_teardown_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'PAK-' + package_or_teardown_date[0:10] + '-'
            order_type = int(json2Dict['orderType'])
            if 'warehouseID' in json2Dict:
                if isValid(json2Dict['warehouseID']):
                    warehouse_id = int(json2Dict['warehouseID'])
                else:
                    warehouse_id = 0
            else:
                warehouse_id = 0
            if 'commoditySpecificationID' in json2Dict:
                if isValid(json2Dict['commoditySpecificationID']):
                    commodity_specification_id = int(json2Dict['commoditySpecificationID'])
                else:
                    commodity_specification_id = 0
            else:
                commodity_specification_id = 0
            if 'packageOrTeardownNum' in json2Dict:
                if isValid(json2Dict['packageOrTeardownNum']):
                    package_or_teardown_num = int(json2Dict['packageOrTeardownNum'])
                else:
                    package_or_teardown_num = 0
            else:
                package_or_teardown_num = 0
            if 'unitPrice' in json2Dict:
                if isValid(json2Dict['unitPrice']):
                    unit_price = atof(json2Dict['unitPrice'])
                else:
                    unit_price = 0
            else:
                unit_price = 0
            if 'totalMoney' in json2Dict:
                if isValid(json2Dict['totalMoney']):
                    total_money = atof(json2Dict['totalMoney'])
                else:
                    total_money = 0
            else:
                total_money = 0
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
            package = PackageOrTeardownOrder(None,order_type,package_or_teardown_date,identifier,warehouse_id,commodity_specification_id,package_or_teardown_num,unit_price,total_money,person_id,originator,reviewer,summary,state,print_num,is_delete)
            package.save()
            package.identifier = identifier + str(package.id)
            package.save()
            if 'packageCommodities' in json2Dict:
                packageCommodities = json2Dict['packageCommodities']
                for packageCommodity in packageCommodities:
                    package_or_teardown_order_id = package.id
                    if 'commoditySpecificationID' in packageCommodity:
                        if isValid(packageCommodity['number']):
                            commodity_specification_id = int(packageCommodity['commoditySpecificationID'])
                        else:
                            commodity_specification_id = 0
                    else:
                        commodity_specification_id = 0
                    if 'number' in packageCommodity:
                        if isValid(packageCommodity['number']):
                            number = int(packageCommodity['number'])
                        else:
                           number = 0 
                    else:
                        number = 0
                    if 'unitPrice' in packageCommodity:
                        if isValid(packageCommodity['unitPrice']):
                            unit_price = atof(packageCommodity['unitPrice'])
                        else:
                            unit_price = 0
                    else:
                        unit_price = 0
                    if 'money' in packageCommodity:
                        if isValid(packageCommodity['money']):
                            money = atof(packageCommodity['money'])
                        else:
                            money = 0
                    else:
                        money = 0
                    packageCommodityObj = PackageOrTeardownOrderCommodity(None,package_or_teardown_order_id,commodity_specification_id,number,unit_price,money)
                    packageCommodityObj.save()
            packageCommodityJSON = getPackage(package)
            packageOrTeardownInsert = setStatus(200,packageCommodityJSON)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        packageOrTeardownInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(packageOrTeardownInsert), content_type='application/json')


def packageOrTeardownDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                packages = PackageOrTeardownOrder.objects.filter(id=identifier)
                if len(packages) > 0:
                    package = packages[0]
                    package.is_delete = 1
                    package.save()
                    packageOrTeardownDelete = setStatus(200, {})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    packageOrTeardownDelete = setStatus(300, errorIDs)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        packageOrTeardownDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(packageOrTeardownDelete), content_type='application/json')


def packageOrTeardownUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            packages = PackageOrTeardownOrder.objects.filter(identifier=identifier)
            if len(packages) > 0:
                package = packages[0]
            else:
                packageOrTeardownUpdate = setStatus(300,{})
                return HttpResponse(json.dumps(packageOrTeardownUpdate), content_type='application/json')
            if 'orderType' in json2Dict:
                if isValid(json2Dict['orderType']):
                    order_type = int(json2Dict['orderType'])
                    package.order_type = order_type
            if 'warehouseID' in json2Dict:
                if isValid(json2Dict['warehouseID']):
                    warehouse_id = int(json2Dict['warehouseID'])
                    package.warehouse_id = warehouse_id
            if 'commoditySpecificationID' in json2Dict:
                if isValid(json2Dict['commoditySpecificationID']):
                    commodity_specification_id = int(json2Dict['commoditySpecificationID'])
                    package.commodity_specification_id = commodity_specification_id
            if 'packageOrTeardownNum' in json2Dict:
                if isValid(json2Dict['packageOrTeardownNum']):
                    package_or_teardown_num = int(json2Dict['packageOrTeardownNum'])
                    package.package_or_teardown_num = package_or_teardown_num
            if 'unitPrice' in json2Dict:
                if isValid(json2Dict['unitPrice']):
                    unit_price = atof(json2Dict['unitPrice'])
                    package.unit_price = unit_price
            if 'totalMoney' in json2Dict:
                if isValid(json2Dict['totalMoney']):
                    total_money = atof(json2Dict['totalMoney'])
                    package.total_money = total_money
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                    package.person_id = person_id
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                    package.originator = originator
            if 'reviewer' in json2Dict:
                if isValid(json2Dict['reviewer']):
                    reviewer = json2Dict['reviewer']
                    package.reviewer = reviewer
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                    package.summary = summary
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                    package.state = state
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                    package.print_num = print_num
            package.save()
            if 'packageCommodities' in json2Dict:
                packageCommodities = json2Dict['packageCommodities']
                for packageCommodity in packageCommodities:
                    if 'packageCommodityID' in packageCommodity:
                        packageCommodityID = int(packageCommodity['packageCommodityID'])
                        packageCommodityObjs = PackageOrTeardownOrderCommodity.objects.filter(id=packageCommodityID)
                        if len(packageCommodityObjs) > 0:
                            packageCommodityObj = packageCommodityObjs[0]
                        else:
                            packageOrTeardownUpdate = setStatus(300, {})
                            return HttpResponse(json.dumps(packageOrTeardownUpdate), content_type='application/json')
                    else:
                        continue
                    if 'commoditySpecificationID' in packageCommodity:
                        if isValid(packageCommodity['commoditySpecificationID']):
                            commodity_specification_id = int(packageCommodity['commoditySpecificationID'])
                            packageCommodityObj.commodity_specification_id = commodity_specification_id
                    if 'number' in packageCommodity:
                        if isValid(packageCommodity['number']):
                            number = int(packageCommodity['number'])
                            packageCommodityObj.number = number
                    if 'unitPrice' in packageCommodity:
                        if isValid(packageCommodity['unitPrice']):
                            unit_price = atof(packageCommodity['unitPrice'])
                            packageCommodityObj.unit_price = unit_price
                    if 'money' in packageCommodity:
                        if isValid(packageCommodity['money']):
                            money = atof(packageCommodity['money'])
                            packageCommodityObj.money = money
                    packageCommodityObj.save()
            packageJSON = getPackage(package)
            packageOrTeardownUpdate = setStatus(200,packageJSON)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        packageOrTeardownUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(packageOrTeardownUpdate), content_type='application/json')


def packageOrTeardownSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                if 'identifier' in request.GET:
                    identifier = request.GET['identifier']
                    packages = PackageOrTeardownOrder.objects.filter(identifier=identifier,is_delete=0)
                    if len(packages) > 0:
                        package = packages[0]
                        packageOrTeardownSelect = getPackage(package)
                    else:
                        packageOrTeardownSelect = setStatus(300, {})
                        return HttpResponse(json.dumps(packageOrTeardownSelect), content_type='application/json')
                else:
                    condition = {}
                    selectType = {}
                    if 'warehouseID' in request.GET and isValid(request.GET['warehouseID']):
                        condition['warehouse_id'] = int(request.GET['warehouseID'])
                    if 'personID' in request.GET and isValid(request.GET['personID']):
                        condition['person_id'] = int(request.GET['personID'])
                    if 'orderType' in request.GET and isValid(request.GET['orderType']):
                        condition['order_type'] = int(request.GET['orderType'])
                    if 'state' in request.GET and isValid(request.GET['state']):
                        condition['state'] = int(request.GET['state'])
                    condition['is_delete'] = 0
                    if 'queryTime' in request.GET:
                        queryTime = request.GET['queryTime']
                        timeFrom = queryTime.split('~')[0].strip()
                        timeTo = queryTime.split('~')[1].strip()
                        selectType['timeFrom'] = timeFrom + ' 00:00:00'
                        selectType['timeTo'] = timeTo + ' 23:59:59'
                    packageOrTeardownSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                packageOrTeardownSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        packageOrTeardownSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(packageOrTeardownSelect), content_type='application/json')


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
        basicsCount = PackageOrTeardownOrder.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = PackageOrTeardownOrder.objects.filter(
                Q(**condition) & Q(package_or_teardown_date__gte=timeFrom) & Q(package_or_teardown_date__lte=timeTo)).count()
        else:
            basicsCount = PackageOrTeardownOrder.objects.filter(**condition).count()
    if basicsCount != 0:
        if basicsCount % ONE_PAGE_OF_DATA == 0:
            allPage = basicsCount / ONE_PAGE_OF_DATA
        else:
            allPage = basicsCount / ONE_PAGE_OF_DATA + 1
    else:
        allPage = 1
    if curPage == 1:
        if condition == None:
            basicObjs = PackageOrTeardownOrder.objects.filter(is_delete=0)[0:ONE_PAGE_OF_DATA]
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = PackageOrTeardownOrder.objects.filter(
                    Q(**condition) & Q(package_or_teardown_date__gte=timeFrom) & Q(package_or_teardown_date__lte=timeTo))[0:ONE_PAGE_OF_DATA]
            else:
                basicObjs = PackageOrTeardownOrder.objects.filter(**condition)[0:ONE_PAGE_OF_DATA]
        for basicObj in basicObjs:
            basicJSON = getPackage(basicObj)
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
            basicObjs = PackageOrTeardownOrder.objects.filter(is_delete=0)[startPos:endPos]
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = PackageOrTeardownOrder.objects.filter(
                    Q(**condition) & Q(package_or_teardown_date__gte=timeFrom) & Q(package_or_teardown_date__lte=timeTo))[startPos:endPos]
            else:
                basicObjs = PackageOrTeardownOrder.objects.filter(**condition)[startPos:endPos]
        for basicObj in basicObjs:
            basicJSON = getPackage(basicObj)
            datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
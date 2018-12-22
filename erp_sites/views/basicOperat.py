#!usr/bin/python#coding=utf-8

import json,sys,time
from string import upper, atof, atoi
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,isValid
import traceback
from erp_sites.models import ShippingMode,SettlementType,Department,Warehouse
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def basicInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            tableName = json2Dict['tableName']
            operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            name = json2Dict['name']
            operator_identifier = json2Dict['operatorIdentifier']
            is_delete = 0
            if tableName == 'shippingMode':
                identifier = 'SHIP-' + operator_time[0:10] + '-'
                shippingMode = ShippingMode(None,name,operator_identifier,operator_time,is_delete,identifier)
                shippingMode.save()
                shippingMode.identifier = identifier + str(shippingMode.id)
                shippingMode.save()
                basicJSON = getBasicJSON(shippingMode,tableName)
            elif tableName == 'settlementType':
                identifier = 'SET_TYP-' + operator_time[0:10] + '-'
                settlementType = SettlementType(None,name,identifier,operator_identifier,operator_time,is_delete)
                settlementType.save()
                settlementType.identifier = identifier + str(settlementType.id)
                settlementType.save()
                basicJSON = getBasicJSON(settlementType,tableName)
            elif tableName == 'department':
                identifier = 'DEP-' + operator_time[0:10] + '-'
                department = Department(None,name,operator_identifier,operator_time,identifier,is_delete)
                department.save()
                department.identifier = identifier + str(department.id)
                department.save()
                basicJSON = getBasicJSON(department,tableName)
            elif tableName == 'warehouse':
                identifier = 'WAH-' + operator_time[0:10] + '-'
                position = json2Dict['position']
                warehouse = Warehouse(None,name,position,operator_identifier,operator_time,identifier,is_delete)
                warehouse.save()
                warehouse.identifier = identifier + str(warehouse.id)
                warehouse.save()
                basicJSON = getBasicJSON(warehouse,tableName)
            else:
                basicInsert = setStatus(300, {})
                return HttpResponse(json.dumps(basicInsert), content_type='application/json')
            basicInsert = setStatus(200,basicJSON)
            return HttpResponse(json.dumps(basicInsert), content_type='application/json')
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        basicInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(basicInsert), content_type='application/json')


def basicDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            tableName = json2Dict['tableName']
            identifiers = json2Dict['id']
            errorIDs = []
            if tableName == 'shippingMode':
                for identifier in identifiers:
                    identifier = int(identifier)
                    shippingModes = ShippingMode.objects.filter(id=identifier)
                    if len(shippingModes) > 0:
                        shippingMode = shippingModes[0]
                        shippingMode.is_delete = 1
                        shippingMode.save()
                        basicDelete = setStatus(200,{})
                    else:
                        errorIDs.append(identifier)
                    if len(errorIDs) > 0:
                        basicDelete = setStatus(300, errorIDs)
            elif tableName == 'settlementType':
                for identifier in identifiers:
                    identifier = int(identifier)
                    settlementTypes = SettlementType.objects.filter(id=identifier)
                    if len(settlementTypes) > 0:
                        settlementType = settlementTypes[0]
                        settlementType.is_delete = 1
                        settlementType.save()
                        basicDelete = setStatus(200,{})
                    else:
                        errorIDs.append(identifier)
                    if len(errorIDs) > 0:
                        basicDelete = setStatus(300, errorIDs)
            elif tableName == 'department':
                for identifier in identifiers:
                    identifier = int(identifier)
                    departments = Department.objects.filter(id=identifier)
                    if len(departments) > 0:
                        department = departments[0]
                        department.is_delete = 1
                        department.save()
                        basicDelete = setStatus(200,{})
                    else:
                        errorIDs.append(identifier)
                    if len(errorIDs) > 0:
                        basicDelete = setStatus(300, errorIDs)
            elif tableName == 'warehouse':
                for identifier in identifiers:
                    identifier = int(identifier)
                    warehouses = Warehouse.objects.filter(id=identifier)
                    if len(warehouses) > 0:
                        warehouse = warehouses[0]
                        warehouse.is_delete = 1
                        warehouse.save()
                        basicDelete = setStatus(200,{})
                    else:
                        errorIDs.append(identifier)
                    if len(errorIDs) > 0:
                        basicDelete = setStatus(300, errorIDs)
            else:
                basicDelete = setStatus(300, {})
                return HttpResponse(json.dumps(basicDelete), content_type='application/json')
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        basicDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(basicDelete), content_type='application/json')


def basicUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            tableName = json2Dict['tableName']
            operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if tableName == 'shippingMode':
                identifier = json2Dict['identifier']
                shippingModes = ShippingMode.objects.filter(identifier=identifier)
                if len(shippingModes) > 0:
                    shippingMode = shippingModes[0]
                    if 'name' in json2Dict:
                        if isValid(json2Dict['name']):
                            name = json2Dict['name']
                            shippingMode.name = name
                    if 'operatorIdentifier' in json2Dict:
                        if isValid(json2Dict['operatorIdentifier']):
                            operator_identifier = json2Dict['operatorIdentifier']
                            shippingMode.operator_identifier = operator_identifier
                    shippingMode.save()
                else:
                    basicUpdate = setStatus(300, {})
                    return HttpResponse(json.dumps(basicUpdate), content_type='application/json')
                basicJSON = getBasicJSON(shippingMode, tableName)
            elif tableName == 'settlementType':
                identifier = json2Dict['identifier']
                settlementTypes = SettlementType.objects.filter(identifier=identifier)
                if len(settlementTypes) > 0:
                    settlementType = settlementTypes[0]
                    if 'name' in json2Dict:
                        if isValid(json2Dict['name']):
                            name = json2Dict['name']
                            settlementType.name = name
                    if 'operatorIdentifier' in json2Dict:
                        if isValid(json2Dict['operatorIdentifier']):
                            operator_identifier = json2Dict['operatorIdentifier']
                            settlementType.operator_identifier = operator_identifier
                    settlementType.save()
                else:
                    basicUpdate = setStatus(300, {})
                    return HttpResponse(json.dumps(basicUpdate), content_type='application/json')
                basicJSON = getBasicJSON(settlementType, tableName)
            elif tableName == 'department':
                identifier = json2Dict['identifier']
                departments = Department.objects.filter(identifier=identifier)
                if len(departments) > 0:
                    department = departments[0]
                    if 'name' in json2Dict:
                        if isValid(json2Dict['name']):
                            name = json2Dict['name']
                            department.name = name
                    if 'operatorIdentifier' in json2Dict:
                        if isValid(json2Dict['operatorIdentifier']):
                            operator_identifier = json2Dict['operatorIdentifier']
                            department.operator_identifier = operator_identifier
                    department.save()
                else:
                    basicUpdate = setStatus(300, {})
                    return HttpResponse(json.dumps(basicUpdate), content_type='application/json')
                basicJSON = getBasicJSON(department, tableName)
            elif tableName == 'warehouse':
                identifier = json2Dict['identifier']
                warehouses = Warehouse.objects.filter(identifier=identifier)
                if len(warehouses) > 0:
                    warehouse = warehouses[0]
                    if 'name' in json2Dict:
                        if isValid(json2Dict['name']):
                            name = json2Dict['name']
                            warehouse.name = name
                    if 'operatorIdentifier' in json2Dict:
                        if isValid(json2Dict['operatorIdentifier']):
                            operator_identifier = json2Dict['operatorIdentifier']
                            warehouse.operator_identifier = operator_identifier
                    if 'position' in json2Dict:
                        if isValid(json2Dict['position']):
                            position = json2Dict['position']
                            warehouse.position = position
                    warehouse.save()
                else:
                    basicUpdate = setStatus(300, {})
                    return HttpResponse(json.dumps(basicUpdate), content_type='application/json')
                basicJSON = getBasicJSON(warehouse, tableName)
            else:
                basicUpdate = setStatus(300, {})
                return HttpResponse(json.dumps(basicUpdate), content_type='application/json')
            basicUpdate = setStatus(200,basicJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        basicUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(basicUpdate), content_type='application/json')


def basicSelect(request):
    try:
        if isTokenExpired(request):
            tableName = request.GET['tableName']
            if tableName == 'shippingMode':
                condition = {}
                selectType = {}
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'name' in request.GET and isValid(request.GET['name']):
                    condition['name'] = request.GET['name']
                if 'operatorIdentifier' in request.GET and isValid(request.GET['operatorIdentifier']):
                    condition['operator_identifier'] = request.GET['operatorIdentifier']
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                condition['is_delete'] = 0
                if 'noPaging' in request.GET and request.GET['noPaging'] == "true":
                    basicSelect = conditionSelect(tableName, condition, selectType)
                else:
                    basicSelect = paging4ShippingMode(request, ONE_PAGE_OF_DATA,tableName, condition, selectType)
            elif tableName == 'settlementType':
                condition = {}
                selectType = {}
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'name' in request.GET and isValid(request.GET['name']):
                    condition['name'] = request.GET['name']
                if 'operatorIdentifier' in request.GET and isValid(request.GET['operatorIdentifier']):
                    condition['operator_identifier'] = request.GET['operatorIdentifier']
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                condition['is_delete'] = 0
                if 'noPaging' in request.GET and request.GET['noPaging'] == "true":
                    basicSelect = conditionSelect(tableName, condition, selectType)
                else:
                    basicSelect = paging4SettlementType(request, ONE_PAGE_OF_DATA,tableName, condition, selectType)
            elif tableName == 'department':
                condition = {}
                selectType = {}
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'name' in request.GET and isValid(request.GET['name']):
                    condition['name'] = request.GET['name']
                if 'operatorIdentifier' in request.GET and isValid(request.GET['operatorIdentifier']):
                    condition['operator_identifier'] = request.GET['operatorIdentifier']
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                condition['is_delete'] = 0
                if 'noPaging' in request.GET and request.GET['noPaging'] == "true":
                    basicSelect = conditionSelect(tableName, condition, selectType)
                else:
                    basicSelect = paging4Department(request, ONE_PAGE_OF_DATA,tableName, condition, selectType)
            elif tableName == 'warehouse':
                condition = {}
                selectType = {}
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'name' in request.GET and isValid(request.GET['name']):
                    condition['name'] = request.GET['name']
                if 'operatorIdentifier' in request.GET and isValid(request.GET['operatorIdentifier']):
                    condition['operator_identifier'] = request.GET['operatorIdentifier']
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                condition['is_delete'] = 0
                if 'noPaging' in request.GET and request.GET['noPaging'] == "true":
                    basicSelect = conditionSelect(tableName, condition, selectType)
                else:
                    basicSelect = paging4Warehouse(request, ONE_PAGE_OF_DATA,tableName, condition, selectType)
            else:
                basicSelect = setStatus(300, {})
            return HttpResponse(json.dumps(basicSelect), content_type='application/json')
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        basicSelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(basicSelete), content_type='application/json')


def paging4ShippingMode(request, ONE_PAGE_OF_DATA,tableName, condition, selectType):
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
        basicsCount = ShippingMode.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = ShippingMode.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
        else:
            basicsCount = ShippingMode.objects.filter(**condition).count()
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
        basicObjs = ShippingMode.objects.filter(is_delete=0)[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = ShippingMode.objects.filter(
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = ShippingMode.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getBasicJSON(basicObj,tableName)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect


def paging4SettlementType(request, ONE_PAGE_OF_DATA,tableName, condition, selectType):
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
        basicsCount = SettlementType.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = SettlementType.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
        else:
            basicsCount = SettlementType.objects.filter(**condition).count()
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
        basicObjs = SettlementType.objects.filter(is_delete=0)[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = SettlementType.objects.filter(
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = SettlementType.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getBasicJSON(basicObj,tableName)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect


def paging4Department(request, ONE_PAGE_OF_DATA,tableName, condition, selectType):
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
        basicsCount = Department.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = Department.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
        else:
            basicsCount = Department.objects.filter(**condition).count()
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
        basicObjs = Department.objects.filter(is_delete=0)[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = Department.objects.filter(
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = Department.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getBasicJSON(basicObj,tableName)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect


def paging4Warehouse(request, ONE_PAGE_OF_DATA,tableName, condition, selectType):
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
        basicsCount = Warehouse.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = Warehouse.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
        else:
            basicsCount = Warehouse.objects.filter(**condition).count()
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
        basicObjs = Warehouse.objects.filter(is_delete=0)[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = Warehouse.objects.filter(
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = Warehouse.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getBasicJSON(basicObj,tableName)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect


def conditionSelect(tableName, condition, selectType):
    pagingSelect = {}
    datasJSON = []
    curPage = 1
    allPage = 1
    if tableName == 'shippingMode':
        if condition == None:
            basicsCount = ShippingMode.objects.filter(is_delete=0).count()
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicsCount = ShippingMode.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            else:
                basicsCount = ShippingMode.objects.filter(**condition).count()
        if curPage > allPage or curPage < 1:
            pagingSelect['code'] = 300
            pagingSelect['curPage'] = curPage
            pagingSelect['allPage'] = allPage
            pagingSelect['data'] = 'curPage is invalid !'
            return pagingSelect
        if condition == None:
            basicObjs = ShippingMode.objects.filter(is_delete=0)
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = ShippingMode.objects.filter(
                        Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))
            else:
                basicObjs = ShippingMode.objects.filter(**condition)
        for basicObj in basicObjs:
            basicJSON = getBasicJSON(basicObj,tableName)
            datasJSON.append(basicJSON)
        pagingSelect['code'] = 200
        dataJSON = {}
        dataJSON['curPage'] = curPage
        dataJSON['allPage'] = allPage
        dataJSON['total'] = basicsCount
        dataJSON['datas'] = datasJSON
        pagingSelect['data'] = dataJSON
    elif tableName == 'settlementType':
        if condition == None:
            basicsCount = SettlementType.objects.filter(is_delete=0).count()
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicsCount = SettlementType.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            else:
                basicsCount = SettlementType.objects.filter(**condition).count()
        if curPage > allPage or curPage < 1:
            pagingSelect['code'] = 300
            pagingSelect['curPage'] = curPage
            pagingSelect['allPage'] = allPage
            pagingSelect['data'] = 'curPage is invalid !'
            return pagingSelect
        if condition == None:
            basicObjs = SettlementType.objects.filter(is_delete=0)
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = SettlementType.objects.filter(
                        Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))
            else:
                basicObjs = SettlementType.objects.filter(**condition)
        for basicObj in basicObjs:
            basicJSON = getBasicJSON(basicObj,tableName)
            datasJSON.append(basicJSON)
        pagingSelect['code'] = 200
        dataJSON = {}
        dataJSON['curPage'] = curPage
        dataJSON['allPage'] = allPage
        dataJSON['total'] = basicsCount
        dataJSON['datas'] = datasJSON
        pagingSelect['data'] = dataJSON
    elif tableName == 'department':
        if condition == None:
            basicsCount = Department.objects.filter(is_delete=0).count()
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicsCount = Department.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            else:
                basicsCount = Department.objects.filter(**condition).count()
        if curPage > allPage or curPage < 1:
            pagingSelect['code'] = 300
            pagingSelect['curPage'] = curPage
            pagingSelect['allPage'] = allPage
            pagingSelect['data'] = 'curPage is invalid !'
            return pagingSelect
        if condition == None:
            basicObjs = Department.objects.filter(is_delete=0)
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = Department.objects.filter(
                        Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))
            else:
                basicObjs = Department.objects.filter(**condition)
        for basicObj in basicObjs:
            basicJSON = getBasicJSON(basicObj,tableName)
            datasJSON.append(basicJSON)
        pagingSelect['code'] = 200
        dataJSON = {}
        dataJSON['curPage'] = curPage
        dataJSON['allPage'] = allPage
        dataJSON['total'] = basicsCount
        dataJSON['datas'] = datasJSON
        pagingSelect['data'] = dataJSON
    elif tableName == 'warehouse':
        if condition == None:
            basicsCount = Warehouse.objects.filter(is_delete=0).count()
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicsCount = Warehouse.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            else:
                basicsCount = Warehouse.objects.filter(**condition).count()
        if curPage > allPage or curPage < 1:
            pagingSelect['code'] = 300
            pagingSelect['curPage'] = curPage
            pagingSelect['allPage'] = allPage
            pagingSelect['data'] = 'curPage is invalid !'
            return pagingSelect
        if condition == None:
            basicObjs = Warehouse.objects.filter(is_delete=0)
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = Warehouse.objects.filter(
                        Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))
            else:
                basicObjs = Warehouse.objects.filter(**condition)
        for basicObj in basicObjs:
            basicJSON = getBasicJSON(basicObj,tableName)
            datasJSON.append(basicJSON)
        pagingSelect['code'] = 200
        dataJSON = {}
        dataJSON['curPage'] = curPage
        dataJSON['allPage'] = allPage
        dataJSON['total'] = basicsCount
        dataJSON['datas'] = datasJSON
        pagingSelect['data'] = dataJSON
    else:
        pagingSelect['code'] = 300
        dataJSON['curPage'] = curPage
        dataJSON['allPage'] = allPage
        dataJSON['total'] = 0
        dataJSON['datas'] = "invalid 'tableName'"
    return pagingSelect

def getBasicJSON(basicObj,tableName):
    basicJSON = {}
    basicJSON['basicID'] = basicObj.id
    basicJSON['name'] = basicObj.name
    basicJSON['identifier'] = basicObj.identifier
    if tableName == 'warehouse':
        basicJSON['position'] = basicObj.position
    basicJSON['operatorIdentifier'] = basicObj.operator_identifier
    basicJSON['operatorTime'] = str(basicObj.operator_time)
    basicJSON['isDelete'] = basicObj.is_delete
    return basicJSON

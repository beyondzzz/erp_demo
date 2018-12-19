#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getDepartment,isValid
import traceback
from erp_sites.models import Department
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def departmentInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            if 'name' in json2Dict:
                if isValid(json2Dict['name']):
                    name = json2Dict['name']
                else:
                    name = None
            else:
                name = None
            if 'operatorIdentifier' in json2Dict:
                if isValid(json2Dict['operatorIdentifier']):
                    operator_identifier = json2Dict['operatorIdentifier']
                else:
                    operator_identifier = None
            else:
                operator_identifier = None
            operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'DEP-' + operator_time[0:10] + '-'
            is_delete = 0
            department = Department(None,name,operator_identifier,operator_time,identifier,is_delete)
            department.save()
            department.identifier = identifier + str(department.id)
            department.save()
            departmentJSON = getDepartment(department)
            departmentInsert = setStatus(200,departmentJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        departmentInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(departmentInsert), content_type='application/json')


def departmentDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                departments = Department.objects.filter(id=identifier)
                if len(departments) > 0:
                    department = departments[0]
                    department.is_delete = 1
                    department.save()
                    departmentDelete = setStatus(200,{})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    departmentDelete = setStatus(300, errorIDs)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        departmentDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(departmentDelete), content_type='application/json')


def departmentUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            departments = Department.objects.filter(identifier=identifier)
            if len(departments) > 0:
                department = departments[0]
            else:
                departmentUpdate = setStatus(300,{})
                return HttpResponse(json.dumps(departmentUpdate), content_type='application/json')
            if 'name' in json2Dict:
                if isValid(json2Dict['name']):
                    name = json2Dict['name']
                    department.name = name
            if 'operatorIdentifier' in json2Dict:
                if isValid(json2Dict['operatorIdentifier']):
                    operator_identifier = json2Dict['operatorIdentifier']
                    department.operator_identifier = operator_identifier
            department.save()
            departmentJSON = getDepartment(department)
            departmentUpdate = setStatus(200,departmentJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        departmentUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(departmentUpdate), content_type='application/json')


def departmentSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                if 'identifier' in request.GET:
                    identifier = request.GET['identifier']
                    departments = Department.objects.filter(identifier=identifier,is_delete=0)
                    if len(departments) > 0:
                        department = departments[0]
                        departmentSelect = getDepartment(department)
                    else:
                        departmentSelect = setStatus(300, {})
                        return HttpResponse(json.dumps(departmentSelect), content_type='application/json')
                else:
                    condition = {}
                    selectType = {}
                    if 'name' in request.GET and isValid(request.GET['name']):
                        condition['name'] = request.GET['name']
                    if 'operatorIdentifier' in request.GET and isValid(request.GET['operatorIdentifier']):
                        condition['operator_identifier'] = request.GET['operatorIdentifier']
                    condition['is_delete'] = 0
                    if 'queryTime' in request.GET:
                        queryTime = request.GET['queryTime']
                        timeFrom = queryTime.split('~')[0].strip()
                        timeTo = queryTime.split('~')[1].strip()
                        selectType['timeFrom'] = timeFrom + ' 00:00:00'
                        selectType['timeTo'] = timeTo + ' 23:59:59'
                    departmentSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                departmentSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        departmentSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(departmentSelect), content_type='application/json')


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
        basicsCount = Department.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = Department.objects.filter(
                Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
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
        basicJSON = getDepartment(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getLog,isValid
import traceback
from erp_sites.models import Log,Person
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def getLogMsg(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                condition = {}
                selectType = {}
                if 'operateType' in request.GET and isValid(request.GET['operateType']):
                    condition['operate_type'] = int(request.GET['operateType'])
                if 'operatorIdentifier' in request.GET and isValid(request.GET['operatorIdentifier']):
                    condition['operator_identifier'] = request.GET['operatorIdentifier']
                if 'departmentID' in request.GET and isValid(request.GET['departmentID']):
                    departmentID = int(request.GET['departmentID'])
                else:
                    departmentID = None
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                getLogMsg = paging(request, ONE_PAGE_OF_DATA, condition, selectType, departmentID)
            else:
                getLogMsg = paging(request, ONE_PAGE_OF_DATA, None, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        getLogMsg = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(getLogMsg), content_type='application/json')


def paging(request, ONE_PAGE_OF_DATA, condition, selectType, departmentID):
    logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    allPage = 1
    personIDList = []
    if departmentID != None:
        persons = Person.objects.filter(department_id=departmentID)
        for person in persons:
            personIDList.append(person.identifier)
    if condition == None:
        basicsCount = Log.objects.all().count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            if len(personIDList) > 0:
                basicsCount = Log.objects.filter(Q(operator_identifier__in=personIDList) & Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            else:
                basicsCount = Log.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
        else:
            if len(personIDList) > 0:
                basicsCount = Log.objects.filter(Q(operator_identifier__in=personIDList) & Q(**condition)).count()
            else:
                basicsCount = Log.objects.filter(**condition).count()
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
        basicObjs = Log.objects.all()[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            if len(personIDList) > 0:
                basicObjs = Log.objects.filter(Q(operator_identifier__in=personIDList) & Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
            else:
                basicObjs = Log.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
        else:
            if len(personIDList) > 0:
                basicObjs = Log.objects.filter(Q(operator_identifier__in=personIDList) & Q(**condition))[startPos:endPos]
            else:
                basicObjs = Log.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getLog(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
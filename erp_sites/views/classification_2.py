#!usr/bin/python#coding=utf-8

import json,sys,time
from string import upper, atof, atoi
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,isValid
import traceback
from erp_sites.models import Classification,Person
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def firstClassificationInsert(request):
    try:
        if isTokenExpired(request):
            logRecord = basic_log.Logger('record')
            firstClassificationInsert = {}

            logRecord.log("input: " + str(request.body))
            json2Dict = json.loads(request.body)
            if 'name' in json2Dict:
                if isValid(json2Dict['name']):
                    name = json2Dict['name']
                else:
                    name = None
            else:
                name = None
            if 'keyWord' in json2Dict:
                if isValid(json2Dict['keyWord']):
                    key_word = json2Dict['keyWord']
                else:
                    key_word = None
            else:
                key_word = None
            if 'operator' in json2Dict:
                if isValid(json2Dict['operator']):
                    operator_identifier = json2Dict['operator']
                else:
                    operator_identifier = None
            else:
                operator_identifier = None
            if 'type' in json2Dict:
                if isValid(json2Dict['type']):
                    type = int(json2Dict['type'])
                else:
                    type = 0
            else:
                type = 0
            is_delete = 0
            parent_id = 0
            operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'PO-' + operator_time[0:10] + '-'
            firstClassification = Classification(None,identifier,name,parent_id,key_word,operator_identifier,operator_time,type,is_delete)
            firstClassification.save()
            firstClassification.identifier = identifier + str(firstClassification.id)
            firstClassification.save()
            rData = getClassification(firstClassification)
            firstClassificationInsert = setStatus(200,rData)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        firstClassificationInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(firstClassificationInsert), content_type='application/json')


def firstClassificationDelete(request):
    try:
        if isTokenExpired(request):
            logRecord = basic_log.Logger('record')
            firstClassificationDelete = {}
            identifier = request.GET['identifier']
            classifications = Classification.objects.filter(identifier=identifier,parent_id=0)
            if len(classifications) > 0:
                classification = classifications[0]
                classification.is_delete = 1
                children = Classification.objects.filter(parent_id=classification.id)
                for child in children:
                    child.is_delete = 1
                    child.save()
                classification.save()
                firstClassificationDelete = setStatus(200,{})
            else:
                firstClassificationDelete = setStatus(300, {})
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        firstClassificationDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(firstClassificationDelete), content_type='application/json')


def firstClassificationUpdate(request):
    try:
        if isTokenExpired(request):
            logRecord = basic_log.Logger('record')
            firstClassificationUpdate = {}
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            classifications = Classification.objects.filter(identifier=identifier)
            if len(classifications) > 0:
                classification = classifications[0]
                isAdd = 0
                if 'name' in json2Dict:
                    if isValid(json2Dict['name']):
                        name = json2Dict['name']
                        classification.name = name
                        isAdd += 1
                if 'keyWord' in json2Dict:
                    if isValid(json2Dict['keyWord']):
                        key_word = json2Dict['keyWord']
                        classification.key_word = key_word
                        isAdd += 1
                if 'operator' in json2Dict:
                    if isValid(json2Dict['operator']):
                        operator_identifier = json2Dict['operator']
                        classification.operator_identifier = operator_identifier
                        isAdd += 1
                if 'type' in json2Dict:
                    if isValid(json2Dict['type']):
                        type = int(json2Dict['type'])
                        classification.type = type
                        isAdd += 1
                if isAdd > 0:
                    operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    classification.operator_time = operator_time
                    classification.save()
                    rData = getClassification(classification)
                    firstClassificationUpdate = setStatus(200,rData)
            else:
                firstClassificationUpdate = setStatus(300,{})
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        firstClassificationUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(firstClassificationUpdate), content_type='application/json')


def firstClassificationSelect(request):
    try:
        if isTokenExpired(request):
            logRecord = basic_log.Logger('record')
            firstClassificationSelect = {}
            if len(request.GET) > 0:
                if 'identifier' in request.GET and request.GET['identifier']!="":
                    identifier = request.GET['identifier']
                    classifications = Classification.objects.filter(identifier=identifier)
                    if len(classifications) > 0:
                        classification = classifications[0]
                        classificationJSON = getClassification(classification)
                        firstClassificationSelect = setStatus(200,classificationJSON)
                    else:
                        firstClassificationSelect = setStatus(300, {})
                    return HttpResponse(json.dumps(firstClassificationSelect), content_type='application/json')
                else:
                    condition = {}
                    selectType = {}
                    if 'type' in request.GET and request.GET['type']!="":
                        if isValid(request.GET['type']):
                            condition['type'] = int(request.GET['type'])
                    if 'keyWord' in request.GET and request.GET['keyWord']!="":
                        if isValid(request.GET['keyWord']):
                            condition['key_word'] = request.GET['keyWord']
                    if 'name' in request.GET and request.GET['name']!="":
                        if isValid(request.GET['name']):
                            condition['name'] = request.GET['name']
                    if 'operator' in request.GET and request.GET['operator']!="":
                        if isValid(request.GET['operator']):
                            condition['operator'] = request.GET['operator']
                    if 'queryTime' in request.GET and request.GET['queryTime']!="":
                        queryTime = request.GET['queryTime']
                        timeFrom = queryTime.split('~')[0].strip()
                        timeTo = queryTime.split('~')[1].strip()
                        selectType['timeFrom'] = timeFrom + ' 00:00:00'
                        selectType['timeTo'] = timeTo + ' 23:59:59'
                    condition['is_delete'] = 0
                    condition['parent_id'] = 0
                    logRecord.log("condition: " + str(condition))
                    firstClassificationSelect = paging(request, ONE_PAGE_OF_DATA, condition,  selectType)
                    logRecord.log("return: " + str(firstClassificationSelect))

            else:
                firstClassificationSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        firstClassificationSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(firstClassificationSelect), content_type='application/json')


def secondClassificationInsert(request):
    try:
        if isTokenExpired(request):
            logRecord = basic_log.Logger('record')
            secondClassificationInsert = {}
            json2Dict = json.loads(request.body)
            parent_id = int(json2Dict['parentID'])
            if 'name' in json2Dict:
                if isValid(json2Dict['name']):
                    name = json2Dict['name']
                else:
                    name = None
            else:
                name = None
            if 'keyWord' in json2Dict:
                if isValid(json2Dict['keyWord']):
                    key_word = json2Dict['keyWord']
                else:
                    key_word = None
            else:
                key_word = None
            if 'operator' in json2Dict:
                if isValid(json2Dict['operator']):
                    operator_identifier = json2Dict['operator']
                else:
                    operator_identifier = None
            else:
                operator_identifier = None
            if 'type' in json2Dict:
                if isValid(json2Dict['type']):
                    type = int(json2Dict['type'])
                else:
                    type = 0
            else:
                type = 0
            is_delete = 0
            operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'PO-' + operator_time[0:10] + '-'
            secondClassification = Classification(None, identifier, name, parent_id, key_word, operator_identifier,
                                                 operator_time, type, is_delete)
            secondClassification.save()
            secondClassification.identifier = identifier + str(secondClassification.id)
            secondClassification.save()
            rData = getClassification(secondClassification)
            secondClassificationInsert = setStatus(200, rData)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        secondClassificationInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(secondClassificationInsert), content_type='application/json')


def secondClassificationDelete(request):
    try:
        if isTokenExpired(request):
            logRecord = basic_log.Logger('record')
            secondClassificationDelete = {}
            identifier = request.GET['identifier']
            classifications = Classification.objects.filter(identifier=identifier,parent_id__gt=0)
            if len(classifications) > 0:
                classification = classifications[0]
                classification.is_delete = 1
                classification.save()
                secondClassificationDelete = setStatus(200,{})
            else:
                secondClassificationDelete = setStatus(300, {})
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        secondClassificationDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(secondClassificationDelete), content_type='application/json')


def secondClassificationUpdate(request):
    try:
        if isTokenExpired(request):
            logRecord = basic_log.Logger('record')
            secondClassificationUpdate = {}
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            classifications = Classification.objects.filter(identifier=identifier)
            if len(classifications) > 0:
                classification = classifications[0]
                isAdd = 0
                if 'parentID' in json2Dict:
                    if isValid(json2Dict['parentID']):
                        parent_id = json2Dict['parentID']
                        classification.parent_id = parent_id
                        isAdd += 1
                if 'name' in json2Dict:
                    if isValid(json2Dict['name']):
                        name = json2Dict['name']
                        classification.name = name
                        isAdd += 1
                if 'keyWord' in json2Dict:
                    if isValid(json2Dict['keyWord']):
                        key_word = json2Dict['keyWord']
                        classification.key_word = key_word
                        isAdd += 1
                if 'operator' in json2Dict:
                    if isValid(json2Dict['operator']):
                        operator_identifier = json2Dict['operator']
                        classification.operator_identifier = operator_identifier
                        isAdd += 1
                if 'type' in json2Dict:
                    if isValid(json2Dict['type']):
                        type = int(json2Dict['type'])
                        classification.type = type
                        isAdd += 1
                if isAdd > 0:
                    operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    classification.operator_time = operator_time
                    classification.save()
                    rData = getClassification(classification)
                    secondClassificationUpdate = setStatus(200, rData)
            else:
                secondClassificationUpdate = setStatus(300, {})
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        secondClassificationUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(secondClassificationUpdate), content_type='application/json')


def secondClassificationSelect(request):
    try:
        if isTokenExpired(request):
            logRecord = basic_log.Logger('record')
            secondClassificationSelect = {}
            if len(request.GET) > 0:
                if 'identifier' in request.GET:
                    identifier = request.GET['identifier']
                    classifications = Classification.objects.filter(identifier=identifier)
                    if len(classifications) > 0:
                        classification = classifications[0]
                        classificationJSON = getClassification(classification)
                        secondClassificationSelect = setStatus(200, classificationJSON)
                    else:
                        secondClassificationSelect = setStatus(300, {})
                    return HttpResponse(json.dumps(secondClassificationSelect), content_type='application/json')
                else:
                    condition = {}
                    selectType = {}
                    if 'firstClassIdentifer' in request.GET:
                        if isValid(request.GET['firstClassIdentifer']):
                            firstClassIdentifer = int(request.GET['firstClassIdentifer'])
                            condition['parent_id'] = firstClassIdentifer
                        '''
                        parents = Classification.objects.filter(identifier=firstClassIdentifer)
                        parents = Classification.objects.filter(parent_id=firstClassIdentifer)
                        if len(parents) > 0:
                            parent = parents[0]
                            condition['parent_id'] = parent.id
                        else:
                            secondClassificationSelect = setStatus(300, {})
                            return HttpResponse(json.dumps(secondClassificationSelect), content_type='application/json')
                        '''
                    if 'type' in request.GET:
                        if isValid(request.GET['type']):
                            condition['type'] = int(request.GET['type'])
                    if 'keyWord' in request.GET:
                        if isValid(request.GET['keyWord']):
                            condition['key_word'] = request.GET['keyWord']
                    if 'name' in request.GET:
                        if isValid(request.GET['name']):
                            condition['name'] = request.GET['name']
                    if 'operator' in request.GET:
                        if isValid(request.GET['operator']):
                            selectType['operator'] = request.GET['operator']
                    if 'queryTime' in request.GET:
                        queryTime = request.GET['queryTime']
                        timeFrom = queryTime.split('~')[0].strip()
                        timeTo = queryTime.split('~')[1].strip()
                        selectType['timeFrom'] = timeFrom + ' 00:00:00'
                        selectType['timeTo'] = timeTo + ' 23:59:59'
                    condition['is_delete'] = 0
                    secondClassificationSelect = paging(request, ONE_PAGE_OF_DATA, condition,  selectType)
            else:
                secondClassificationSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        secondClassificationSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(secondClassificationSelect), content_type='application/json')


def paging(request,ONE_PAGE_OF_DATA,condition,selectType):
    logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    allPage = 1
    if selectType:
        if condition == None:
            basicsCount = Classification.objects.filter(is_delete=0).count()
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' not in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicsCount = Classification.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            elif 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                operator = selectType['operator']
                persons = Person.objects.filter(name__icontains=operator)
                personIdentifierList = []
                for person in persons:
                    personIdentifierList.append(person.identifier)
                basicsCount = Classification.objects.filter(Q(operator_identifier__in=personIdentifierList) & Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            elif 'timeFrom' not in selectType and 'timeTo' not in selectType and 'operator' in selectType:
                operator = selectType['operator']
                persons = Person.objects.filter(name__icontains=operator)
                personIdentifierList = []
                for person in persons:
                    personIdentifierList.append(person.identifier)
                basicsCount = Classification.objects.filter(Q(operator_identifier__in=personIdentifierList) & Q(**condition)).count()
            else:
                basicsCount = Classification.objects.filter(**condition).count()
        if basicsCount != 0:
            if basicsCount % ONE_PAGE_OF_DATA == 0:
                allPage = basicsCount / ONE_PAGE_OF_DATA
            else:
                allPage = basicsCount / ONE_PAGE_OF_DATA + 1
        else:
            allPage = 1
        if curPage == 1:
            if condition == None:
                basicObjs = Classification.objects.filter(is_delete=0)[0:ONE_PAGE_OF_DATA]
            else:
                if 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' not in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    basicObjs = Classification.objects.filter(
                        Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[0:ONE_PAGE_OF_DATA]
                elif 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    operator = selectType['operator']
                    persons = Person.objects.filter(name__icontains=operator)
                    personIdentifierList = []
                    for person in persons:
                        personIdentifierList.append(person.identifier)
                    basicObjs = Classification.objects.filter(
                        Q(operator_identifier__in=personIdentifierList) & Q(**condition) & Q(
                            operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[0:ONE_PAGE_OF_DATA]
                elif 'timeFrom' not in selectType and 'timeTo' not in selectType and 'operator' in selectType:
                    operator = selectType['operator']
                    persons = Person.objects.filter(name__icontains=operator)
                    personIdentifierList = []
                    for person in persons:
                        personIdentifierList.append(person.identifier)
                    basicObjs = Classification.objects.filter(
                        Q(operator_identifier__in=personIdentifierList) & Q(**condition))[0:ONE_PAGE_OF_DATA]
                else:
                    basicObjs = Classification.objects.filter(**condition)[0:ONE_PAGE_OF_DATA]
            for basicObj in basicObjs:
                basicObjJSON = getClassification(basicObj)
                childrenJSON = []
                children = Classification.objects.filter(parent_id=basicObj.id,is_delete=0)
                for child in children:
                    childJSON = getClassification(child)
                    childrenJSON.append(childJSON)
                basicObjJSON['children'] = childrenJSON
                datasJSON.append(basicObjJSON)
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
                basicObjs = Classification.objects.filter(is_delete=0)[startPos:endPos]
            else:
                if 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' not in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    basicObjs = Classification.objects.filter(
                        Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
                elif 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    operator = selectType['operator']
                    persons = Person.objects.filter(name__icontains=operator)
                    personIdentifierList = []
                    for person in persons:
                        personIdentifierList.append(person.identifier)
                    basicObjs = Classification.objects.filter(
                            Q(operator_identifier__in=personIdentifierList) & Q(**condition) & Q(
                                operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
                elif 'timeFrom' not in selectType and 'timeTo' not in selectType and 'operator' in selectType:
                    operator = selectType['operator']
                    persons = Person.objects.filter(name__icontains=operator)
                    personIdentifierList = []
                    for person in persons:
                        personIdentifierList.append(person.identifier)
                    basicObjs = Classification.objects.filter(
                            Q(operator_identifier__in=personIdentifierList) & Q(**condition))[startPos:endPos]
                else:
                    basicObjs = Classification.objects.filter(**condition)[startPos:endPos]
            for basicObj in basicObjs:
                basicObjJSON = getClassification(basicObj)
                childrenJSON = []
                children = Classification.objects.filter(parent_id=basicObj.id,is_delete=0)
                for child in children:
                    childJSON = getClassification(child)
                    childrenJSON.append(childJSON)
                basicObjJSON['children'] = childrenJSON
                datasJSON.append(basicObjJSON)
    else:
        if condition == None:
            basicsCount = Classification.objects.filter(is_delete=0,parent_id__gt=0).count()
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' not in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicsCount = Classification.objects.filter(Q (parent_id__gt=0) &
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            elif 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                operator = selectType['operator']
                persons = Person.objects.filter(name__icontains=operator)
                personIdentifierList = []
                for person in persons:
                    personIdentifierList.append(person.identifier)
                basicsCount = Classification.objects.filter(Q (parent_id__gt=0) &
                    Q(operator_identifier__in=personIdentifierList) & Q(**condition) & Q(
                        operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            elif 'timeFrom' not in selectType and 'timeTo' not in selectType and 'operator' in selectType:
                operator = selectType['operator']
                persons = Person.objects.filter(name__icontains=operator)
                personIdentifierList = []
                for person in persons:
                    personIdentifierList.append(person.identifier)
                basicsCount = Classification.objects.filter(Q (parent_id__gt=0) &
                    Q(operator_identifier__in=personIdentifierList) & Q(**condition)).count()
            else:
                basicsCount = Classification.objects.filter(Q (parent_id__gt=0) & Q(**condition)).count()
        if basicsCount != 0:
            if basicsCount % ONE_PAGE_OF_DATA == 0:
                allPage = basicsCount / ONE_PAGE_OF_DATA
            else:
                allPage = basicsCount / ONE_PAGE_OF_DATA + 1
        else:
            allPage = 1
        if curPage == 1:
            if condition == None:
                basicObjs = Classification.objects.filter(is_delete=0,parent_id__gt=0)[0:ONE_PAGE_OF_DATA]
            else:
                if 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' not in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    basicObjs = Classification.objects.filter(Q(parent_id__gt=0) &
                                                                Q(**condition) & Q(operator_time__gte=timeFrom) & Q(
                        operator_time__lte=timeTo))[0:ONE_PAGE_OF_DATA]
                elif 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    operator = selectType['operator']
                    persons = Person.objects.filter(name__icontains=operator)
                    personIdentifierList = []
                    for person in persons:
                        personIdentifierList.append(person.identifier)
                    basicObjs = Classification.objects.filter(Q(parent_id__gt=0) &
                                                                Q(operator_identifier__in=personIdentifierList) & Q(
                        **condition) & Q(
                        operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[0:ONE_PAGE_OF_DATA]
                elif 'timeFrom' not in selectType and 'timeTo' not in selectType and 'operator' in selectType:
                    operator = selectType['operator']
                    persons = Person.objects.filter(name__icontains=operator)
                    personIdentifierList = []
                    for person in persons:
                        personIdentifierList.append(person.identifier)
                    basicObjs = Classification.objects.filter(Q(parent_id__gt=0) &
                                                                Q(operator_identifier__in=personIdentifierList) & Q(
                        **condition))[0:ONE_PAGE_OF_DATA]
                else:
                    basicObjs = Classification.objects.filter(Q(parent_id__gt=0) & Q(**condition))[0:ONE_PAGE_OF_DATA]
            for basicObj in basicObjs:
                basicObjJSON = getClassification(basicObj)
                datasJSON.append(basicObjJSON)
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
                basicObjs = Classification.objects.filter(is_delete=0,parent_id__gt=0)[startPos:endPos]
            else:
                if 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' not in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    basicObjs = Classification.objects.filter(Q(parent_id__gt=0) &
                                                              Q(**condition) & Q(operator_time__gte=timeFrom) & Q(
                        operator_time__lte=timeTo))[startPos:endPos]
                elif 'timeFrom' in selectType and 'timeTo' in selectType and 'operator' in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    operator = selectType['operator']
                    persons = Person.objects.filter(name__icontains=operator)
                    personIdentifierList = []
                    for person in persons:
                        personIdentifierList.append(person.identifier)
                    basicObjs = Classification.objects.filter(Q(parent_id__gt=0) &
                                                              Q(operator_identifier__in=personIdentifierList) & Q(
                        **condition) & Q(
                        operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
                elif 'timeFrom' not in selectType and 'timeTo' not in selectType and 'operator' in selectType:
                    operator = selectType['operator']
                    persons = Person.objects.filter(name__icontains=operator)
                    personIdentifierList = []
                    for person in persons:
                        personIdentifierList.append(person.identifier)
                    basicObjs = Classification.objects.filter(Q(parent_id__gt=0) &
                                                              Q(operator_identifier__in=personIdentifierList) & Q(
                        **condition))[startPos:endPos]
                else:
                    basicObjs = Classification.objects.filter(Q(parent_id__gt=0) & Q(**condition))[startPos:endPos]
            for basicObj in basicObjs:
                basicObjJSON = getClassification(basicObj)
                datasJSON.append(basicObjJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect


def getClassification(classification):
    classificationJSON = {}
    classificationJSON['classificationID'] = classification.id
    classificationJSON['identifier'] = classification.identifier
    classificationJSON['name'] = classification.name
    classificationJSON['parentID'] = classification.parent_id
    classificationJSON['keyWord'] = classification.key_word
    classificationJSON['operator'] = classification.operator_identifier
    classificationJSON['operatorTime'] = str(classification.operator_time)
    classificationJSON['type'] = classification.type
    classificationJSON['isDelete'] = classification.is_delete
    if classification.parent_id == 0:
        classificationJSON['parentName'] = None
        childrenJSON = []
        children = Classification.objects.filter(parent_id=classification.id,is_delete=0)
        for child in children:
            childJSON = getClassification(child)
            childrenJSON.append(childJSON)
        classificationJSON['children'] = childrenJSON
    else:
        parents = Classification.objects.filter(id=classification.parent_id,is_delete=0)
        if len(parents) > 0:
            parent = parents[0]
            classificationJSON['parentName'] = parent.name
        else:
            classificationJSON['parentName'] = None
    return classificationJSON

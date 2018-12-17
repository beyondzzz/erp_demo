#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof, atoi
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getPersonObj,isValid
import traceback
from erp_sites.models import Person,Permission,PersonToken
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def personInsert(request):
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
            if 'type' in json2Dict:
                if isValid(json2Dict['type']):
                    type = json2Dict['type']
                else:
                    type = None
            else:
                type = None
            if 'departmentID' in json2Dict:
                if isValid(json2Dict['departmentID']):
                    department_id = int(json2Dict['departmentID'])
                else:
                    department_id = 0
            else:
                department_id = 0
            if 'entryTime' in json2Dict:
                if isValid(json2Dict['entryTime']):
                    entryTimeStr = json2Dict['entryTime']
                    entry_time = time.strptime(entryTimeStr, '%Y-%m-%d')
                    entry_time = datetime.datetime(*entry_time[:3]).date()
                else:
                    entry_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            else:
                entry_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            if 'duties' in json2Dict:
                if isValid(json2Dict['duties']):
                    duties = json2Dict['duties']
                else:
                    duties = None
            else:
                duties = None
            if 'education' in json2Dict:
                if isValid(json2Dict['education']):
                    education = json2Dict['education']
                else:
                    education = None
            else:
                education = None
            if 'sex' in json2Dict:
                if isValid(json2Dict['sex']):
                    sex = json2Dict['sex']
                else:
                    sex = None
            else:
                sex = None
            if 'birthTime' in json2Dict:
                if isValid(json2Dict['birthTime']):
                    birthTimeStr = json2Dict['birthTime']
                    birth_time = time.strptime(birthTimeStr, '%Y-%m-%d')
                    birth_time = datetime.datetime(*birth_time[:3]).date()
                else:
                    birth_time = None
            else:
                birth_time = None
            if 'nativePlace' in json2Dict:
                if isValid(json2Dict['nativePlace']):
                    native_place = json2Dict['nativePlace']
                else:
                    native_place = None
            else:
                native_place = None
            if 'phone' in json2Dict:
                if isValid(json2Dict['phone']):
                    phone = json2Dict['phone']
                else:
                    phone = None
            else:
                phone = None
            if 'homePhone' in json2Dict:
                if isValid(json2Dict['homePhone']):
                    home_phone = json2Dict['homePhone']
                else:
                    home_phone = None
            else:
                home_phone = None
            if 'commonPhone' in json2Dict:
                if isValid(json2Dict['commonPhone']):
                    common_phone = json2Dict['commonPhone']
                else:
                    common_phone = None
            else:
                common_phone = None
            if 'reservePhone' in json2Dict:
                if isValid(json2Dict['reservePhone']):
                    reserve_phone = json2Dict['reservePhone']
                else:
                    reserve_phone = None
            else:
                reserve_phone = None
            if 'postcode' in json2Dict:
                if isValid(json2Dict['postcode']):
                    postcode = json2Dict['postcode']
                else:
                    postcode = None
            else:
                postcode = None
            if 'homeAddress' in json2Dict:
                if isValid(json2Dict['homeAddress']):
                    home_address = json2Dict['homeAddress']
                else:
                    home_address = None
            else:
                home_address = None
            if 'mailbox' in json2Dict:
                if isValid(json2Dict['mailbox']):
                    mailbox = json2Dict['mailbox']
                else:
                    mailbox = None
            else:
                mailbox = None
            quit_time = None
            if 'business' in json2Dict:
                if isValid(json2Dict['business']):
                    business = int(json2Dict['business'])
                else:
                    business = 0
            else:
                business = 0
            if 'quite' in json2Dict:
                if isValid(json2Dict['quite']):
                    quite = int(json2Dict['quite'])
                else:
                    quite = 0
            else:
                quite = 0
            if 'operatorIdentifier' in json2Dict:
                if isValid(json2Dict['operatorIdentifier']):
                    operator_identifier = json2Dict['operatorIdentifier']
                else:
                    operator_identifier = ''
            else:
                operator_identifier = ''
            operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if 'remark' in json2Dict:
                if isValid(json2Dict['remark']):
                    remark = json2Dict['remark']
                else:
                    remark = None
            else:
                remark = None
            if 'idNumber' in json2Dict:
                if isValid(json2Dict['idNumber']):
                    id_number = json2Dict['idNumber']
                else:
                    id_number = None
            else:
                id_number = None
            identifier = 'PPL-' + operator_time[0:10] + '-'
            if 'loginName' in json2Dict:
                if isValid(json2Dict['loginName']):
                    login_name = json2Dict['loginName']
                    personCount = Person.objects.filter(login_name=login_name).count()
                    if personCount > 0:
                        personInsert = setStatus(300, "the 'loginName' is exists ! ")
                        return HttpResponse(json.dumps(personInsert), content_type='application/json')
                else:
                    login_name = None
            else:
                login_name = None
            if 'password' in json2Dict:
                if isValid(json2Dict['password']):
                    password = json2Dict['password']
                    password = base64.b64encode(password)
                else:
                    password = base64.b64encode('1')
            else:
                password = base64.b64encode('1')
            if 'warehouseID' in json2Dict:
                if isValid(json2Dict['warehouseID']):
                    warehouse_id = int(json2Dict['warehouseID'])
                else:
                    warehouse_id = 0
            else:
                warehouse_id = 0
            if 'place' in json2Dict:
                if isValid(json2Dict['place']):
                    place = json2Dict['place']
                else:
                    place = None
            else:
                place = None
            is_delete = 0
            person = Person(None,name,type,department_id,entry_time,duties,education,sex,birth_time,native_place,phone,home_phone,common_phone,reserve_phone,postcode,home_address,mailbox,quit_time,business,quite,operator_identifier,operator_time,remark,id_number,identifier,login_name,password,warehouse_id,place,is_delete)
            person.save()
            person.identifier = identifier + str(person.id)
            person.save()
            personToken = PersonToken(None,person.id,None,None,None)
            personToken.save()
            if 'resIDs' in json2Dict:
                create_time = operator_time
                resIds = json2Dict['resIDs']
                user_id = person.id
                operator_identifier = person.identifier
                for resId in resIds:
                    menu_id = resId
                    permission = Permission(None,user_id,menu_id,operator_identifier,create_time)
                    permission.save()
            person.save()
            personJSON = getPersonObj(person)
            personInsert = setStatus(200,personJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        personInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(personInsert), content_type='application/json')


def personDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                persons = Person.objects.filter(id=identifier)
                if len(persons) > 0:
                    person = persons[0]
                    person.is_delete = 1
                    person.quit_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    person.save()
                    personDelete = setStatus(200,{})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    personDelete = setStatus(300, errorIDs)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        personDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(personDelete), content_type='application/json')


def personUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            persons = Person.objects.filter(identifier=identifier)
            if len(persons) > 0:
                person = persons[0]
            else:
                personUpdate = setStatus(300,{})
                return HttpResponse(json.dumps(personUpdate), content_type='application/json')
            if 'name' in json2Dict:
                if isValid(json2Dict['name']):
                    name = json2Dict['name']
                    person.name = name
            if 'type' in json2Dict:
                if isValid(json2Dict['type']):
                    type = json2Dict['type']
                    person.type = type
            if 'departmentID' in json2Dict:
                if isValid(json2Dict['departmentID']):
                    department_id = int(json2Dict['departmentID'])
                    person.department_id = department_id
            if 'entryTime' in json2Dict:
                if isValid(json2Dict['entryTime']):
                    entryTimeStr = json2Dict['entryTime']
                    entry_time = time.strptime(entryTimeStr, '%Y-%m-%d')
                    person.entry_time = datetime.datetime(*entry_time[:3]).date()
            if 'duties' in json2Dict:
                if isValid(json2Dict['duties']):
                    duties = json2Dict['duties']
                    person.duties = duties
            if 'education' in json2Dict:
                if isValid(json2Dict['education']):
                    education = json2Dict['education']
                    person.education = education
            if 'sex' in json2Dict:
                if isValid(json2Dict['sex']):
                    sex = json2Dict['sex']
                    person.sex = sex
            if 'birthTime' in json2Dict:
                if isValid(json2Dict['birthTime']):
                    birthTimeStr = json2Dict['birthTime']
                    birth_time = time.strptime(birthTimeStr, '%Y-%m-%d')
                    birth_time = datetime.datetime(*birth_time[:3]).date()
                    person.birth_time = birth_time
            if 'nativePlace' in json2Dict:
                if isValid(json2Dict['nativePlace']):
                    native_place = json2Dict['nativePlace']
                    person.native_place = native_place
            if 'phone' in json2Dict:
                if isValid(json2Dict['phone']):
                    phone = json2Dict['phone']
                    person.phone = phone
            if 'homePhone' in json2Dict:
                if isValid(json2Dict['homePhone']):
                    home_phone = json2Dict['homePhone']
                    person.home_phone = home_phone
            if 'commonPhone' in json2Dict:
                if isValid(json2Dict['commonPhone']):
                    common_phone = json2Dict['commonPhone']
                    person.common_phone = common_phone
            if 'reservePhone' in json2Dict:
                if isValid(json2Dict['reservePhone']):
                    reserve_phone = json2Dict['reservePhone']
                    person.reserve_phone = reserve_phone
            if 'postcode' in json2Dict:
                if isValid(json2Dict['postcode']):
                    postcode = json2Dict['postcode']
                    person.postcode = postcode
            if 'homeAddress' in json2Dict:
                if isValid(json2Dict['homeAddress']):
                    home_address = json2Dict['homeAddress']
                    person.home_address = home_address
            if 'mailbox' in json2Dict:
                if isValid(json2Dict['mailbox']):
                    mailbox = json2Dict['mailbox']
                    person.mailbox = mailbox
            if 'quitTime' in json2Dict:
                if isValid(json2Dict['quitTime']):
                    quit_time = json2Dict['quitTime']
                    person.quit_time = quit_time
            if 'business' in json2Dict:
                if isValid(json2Dict['business']):
                    business = int(json2Dict['business'])
                    person.business = business
            if 'quite' in json2Dict:
                if isValid(json2Dict['quite']):
                    quite = int(json2Dict['quite'])
                    person.quite = quite
            if 'operatorIdentifier' in json2Dict:
                if isValid(json2Dict['operatorIdentifier']):
                    operator_identifier = json2Dict['operatorIdentifier']
                    person.operator_identifier = operator_identifier
            operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if 'remark' in json2Dict:
                if isValid(json2Dict['remark']):
                    remark = json2Dict['remark']
                    person.remark = remark
            if 'idNumber' in json2Dict:
                if isValid(json2Dict['idNumber']):
                    id_number = json2Dict['idNumber']
                    person.id_number = id_number
            if 'loginName' in json2Dict:
                if isValid(json2Dict['loginName']):
                    login_name = json2Dict['loginName']
                    personCount = Person.objects.filter(login_name=login_name).count()
                    if personCount > 0 and login_name != person.login_name:
                        personUpdate = setStatus(300, "the 'loginName' is exists ! ")
                        return HttpResponse(json.dumps(personUpdate), content_type='application/json')
                    person.login_name = login_name
            if 'password' in json2Dict:
                if isValid(json2Dict['password']):
                    password = json2Dict['password']
                    person.password = base64.b64encode(password)
            if 'warehouseID' in json2Dict:
                if isValid(json2Dict['warehouseID']):
                    warehouse_id = int(json2Dict['warehouseID'])
                    person.warehouse_id = warehouse_id
            if 'place' in json2Dict:
                if isValid(json2Dict['place']):
                    place = json2Dict['place']
                    person.place = place
            if 'resIDs' in json2Dict:
                user_id = person.id
                permissions = Permission.objects.filter(user_id=user_id)
                for permission in permissions:
                    permission.delete()
                create_time = operator_time
                resIDs = json2Dict['resIDs']
                for resID in resIDs:
                    menu_id = resID
                    permission = Permission(None,user_id,menu_id,person.identifier,create_time)
                    permission.save()
            person.save()
            personJSON = getPersonObj(person)
            personUpdate = setStatus(200,personJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        personUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(personUpdate), content_type='application/json')


def personSelect(request):
    try:
        if isTokenExpired(request):
            personSelect = {}
            if len(request.GET) > 0:
                if 'identifier' in request.GET:
                    identifier = request.GET['identifier']
                    persons = Person.objects.filter(identifier=identifier,is_delete=0)
                    if len(persons) > 0:
                        person = persons[0]
                        personJSON = getPersonObj(person)
                        personSelect = setStatus(200,personJSON)
                    else:
                        personSelect = setStatus(300,{})
                        return HttpResponse(json.dumps(personSelect), content_type='application/json')
                else:
                    condition = {}
                    selectType = {}
                    if 'name' in request.GET and isValid(request.GET['name']):
                        name = request.GET['name']
                        condition['name'] = name
                    if 'placce' in request.GET and isValid(request.GET['placce']):
                        placce = request.GET['placce']
                        condition['placce'] = placce
                    if 'deparmentID' in request.GET and isValid(request.GET['deparmentID']):
                        deparment_id = int(request.GET['deparmentID'])
                        condition['deparment_id'] = deparment_id
                    if 'queryTime' in request.GET:
                        queryTime = request.GET['queryTime']
                        timeFrom = queryTime.split('~')[0].strip()
                        timeTo = queryTime.split('~')[1].strip()
                        selectType['timeFrom'] = timeFrom + ' 00:00:00'
                        selectType['timeTo'] = timeTo + ' 23:59:59'
                    condition['is_delete'] = 0
                    personSelect = paging(request,ONE_PAGE_OF_DATA,condition,selectType)
            else:
                personSelect = paging(request,ONE_PAGE_OF_DATA,None,None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        personSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(personSelect), content_type='application/json')


def updatePwdByID(request):
    try:
        if isTokenExpired(request):
            updatePwdByID = {}
            identifier = request.GET['identifier']
            person = Person.objects.filter(identifier=identifier)
            password = base64.b64encode('1')
            person.password = password
            person.save()
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        updatePwdByID = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(updatePwdByID), content_type='application/json')



def paging(request,ONE_PAGE_OF_DATA,condition,selectType):
    logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    allPage = 1
    if condition == None:
        basicsCount = Person.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = Person.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
        else:
            basicsCount = Person.objects.filter(**condition).count()
    if basicsCount != 0:
        if basicsCount % ONE_PAGE_OF_DATA == 0:
            allPage = basicsCount / ONE_PAGE_OF_DATA
        else:
            allPage = basicsCount / ONE_PAGE_OF_DATA + 1
    else:
        allPage = 1
    if curPage == 1:
        if condition == None:
            basicObjs = Person.objects.filter(is_delete=0)[0:ONE_PAGE_OF_DATA]
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = Person.objects.filter(
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[
                          0:ONE_PAGE_OF_DATA]
            else:
                basicObjs = Person.objects.filter(**condition)[0:ONE_PAGE_OF_DATA]
        for basicObj in basicObjs:
            basicJSON = getPersonObj(basicObj)
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
            basicObjs = Person.objects.filter(is_delete=0)[startPos:endPos]
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = Person.objects.filter(
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
            else:
                basicObjs = Person.objects.filter(**condition)[startPos:endPos]
        for basicObj in basicObjs:
            basicJSON = getPersonObj(basicObj)
            datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect

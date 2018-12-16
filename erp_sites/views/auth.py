#!usr/bin/python#coding=utf-8

import base64,datetime,json,sys
import traceback
from django.http import HttpResponse,StreamingHttpResponse
from erp_sites import basic_log
from erp_sites.models import Person,PersonToken
from erp_sites.public import makeCaptcha

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 2
import importlib
import os
#project_settings = os.environ['DJANGO_SETTINGS_MODULE']
#settings_ = importlib.import_module(project_settings)
#CORS = getattr(settings_, 'CORS')


'''Token方法，开始'''

def checkUserPassword(loginName, password):
    # Read the employee info by email.
    employeeInfo = Person.objects.filter(login_name=loginName)

    # Convert it into dict type.
    employeeDict = employeeInfo.values()

    # Check the result is empty.
    if len(employeeDict) == 0:
        return False
    userID = employeeDict[0]['id']

    # Search it by user ID
    if employeeDict[0]['password'] == password:
        return True
    return False

def generateToken(username, password):
    currentTime = str(datetime.datetime.now())
    expriedTime = str(datetime.datetime.now() + datetime.timedelta(minutes=120))  # 120 minutes valid
    token = base64.b64encode(str(username) + ":" + str(password) + ":" + currentTime)
    return [token, expriedTime]


def generatePOSToken(username, password):
    currentTime = str(datetime.datetime.now())
    expriedTime = str(datetime.datetime.now() + datetime.timedelta(minutes=120))  # 720 minutes valid
    token = base64.b64encode(str(username) + ":" + str(password) + ":" + currentTime)
    return [token, expriedTime]


def passwordGenerator():
    import random
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mypw = ""
    for i in range(8):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]
    return mypw


def loginPost(request):
    try:
        logRecord = basic_log.Logger('record')
        postMethod = {}
        postMethod['data'] = {}
        # Check the parameter:
        json2Dict = json.loads(request.body)
        if 'loginName' not in json2Dict or 'password' not in json2Dict:
            postMethod['status'] = 404
            postMethod['data']['message']= 'Miss loginName or password.'
            return HttpResponse(json.dumps(postMethod), content_type='application/json')
        loginName = json2Dict['loginName']
        password = json2Dict['password']
        password = base64.b64encode(password)
        if checkUserPassword(loginName, password)== False:
                postMethod['status'] = 406
                postMethod['data']['message'] = 'User password are wrong.'
                return HttpResponse(json.dumps(postMethod), content_type='application/json')
        [tokenValue, expiredTime] = generateToken(loginName, password)
        #request = addCookieAndEpTime(request, tokenValue, expiredTime)

        personTable = Person.objects.filter(login_name=loginName)
        userID = personTable.values()[0]['id']
        name = personTable.values()[0]['name']
        identifier = personTable.values()[0]['identifier']
        PersonToken.objects.filter(person_id=userID).update(token=tokenValue,end_time=expiredTime )
        postMethod['status'] = 200
        postMethod['data']['message'] = 'login Successful.'
        postMethod['data']['identifier'] = identifier
        postMethod['data']['name'] = name
        postMethod['data']['token'] = tokenValue

        #If password type is new, it need to be changed on the next login.
        
        #response = HttpResponse(json.dumps(postMethod),content_type='application/json')
        response = HttpResponse(json.dumps(postMethod),content_type='application/x-www-form-urlencoded')
        response["Access-Control-Allow-Origin"] = "127.0.0.1:62448"
        response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
        response["hahahahahahha"] = "Content-Type, X-Requested-With"
        response.__setitem__("Access-Control-Allow-Origin", "http://127.0.0.1:62448")
        response.__setitem__("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.__setitem__("Access-Control-Allow-Credentials", "true")
        response.__setitem__("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")
        #response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
        #response["Access-Control-Allow-Credentials"] = "true"
        #response["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
        #response["Content-Type"] = "application/x-www-form-urlencoded"
        #response.set_cookie(key='Cookie', value=tokenValue, max_age=1800, expires=expiredTime)
        return response
    except Exception, e:
        postMethod = {}
        postMethod['status'] = 404
        postMethod['data'] = traceback.format_exc()
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        return HttpResponse(json.dumps(postMethod), content_type='application/json')


def getCaptcha(request):
    text, img = makeCaptcha()
    # 设置头信息
    response = StreamingHttpResponse(img)
    response['Content-Type'] = 'image/jpg'
    #response['Content-Disposition'] = 'attachment;filename="{0}"'.format(text)
    return response
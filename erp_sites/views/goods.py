#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getGoods,isValid
import traceback
from erp_sites.models import Goods
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def goodsInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            if 'stock' in json2Dict:
                if isValid(json2Dict['stock']):
                    stock = int(json2Dict['stock'])
                else:
                    stock = 0
            else:
                stock = 0
            if 'purchase' in json2Dict:
                if isValid(json2Dict['purchase']):
                    purchase = atof(json2Dict['purchase'])
                else:
                    purchase = 0
            else:
                purchase = 0
            if 'brand' in json2Dict:
                if isValid(json2Dict['brand']):
                    brand = json2Dict['brand']
                else:
                    brand = None
            else:
                brand = None
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                else:
                    state = 0
            else:
                state = 0
            goods = Goods(None,stock,purchase,brand,state)
            goods.save()
            goodsJSON = getGoods(goods)
            goodsInsert = setStatus(200,goodsJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        goodsInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(goodsInsert), content_type='application/json')


def goodsDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                goodsID = int(identifier)
                goodses = Goods.objects.filter(id=goodsID)
                if len(goodses) > 0:
                    goods = goodses[0]
                    goods.delete()
                    goodsDelete = setStatus(200,{})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    goodsDelete = setStatus(300, errorIDs)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        goodsDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(goodsDelete), content_type='application/json')


def goodsUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            goodsID = json2Dict['goodsID']
            goodses = Goods.objects.filter(id=goodsID)
            if len(goodses) > 0:
                goods = goodses[0]
            else:
                goodsUpdate = setStatus(300,{})
                return HttpResponse(json.dumps(goodsUpdate), content_type='application/json')
            if 'stock' in json2Dict:
                if isValid(json2Dict['stock']):
                    stock = int(json2Dict['stock'])
                    goods.stock = stock
            if 'purchase' in json2Dict:
                if isValid(json2Dict['purchase']):
                    purchase = atof(json2Dict['purchase'])
                    goods.purchase = purchase
            if 'brand' in json2Dict:
                if isValid(json2Dict['brand']):
                    brand = json2Dict['brand']
                    goods.brand = brand
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                    goods.state = state
            goods.save()
            goodsJSON = getGoods(goods)
            goodsUpdate = setStatus(200,goodsJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        goodsUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(goodsUpdate), content_type='application/json')


def goodsSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                if 'goodsID' in request.GET:
                    goodsID = request.GET['goodsID']
                    goodses = Goods.objects.filter(id=goodsID)
                    if len(goodses) > 0:
                        goods = goodses[0]
                        goodsSelect = getGoods(goods)
                    else:
                        goodsSelect = setStatus(300, {})
                        return HttpResponse(json.dumps(goodsSelect), content_type='application/json')
                else:
                    condition = {}
                    selectType = {}
                    if 'stock' in request.GET and isValid(request.GET['stock']):
                        condition['stock'] = int(request.GET['stock'])
                    if 'purchase' in request.GET and isValid(request.GET['purchase']):
                        condition['purchase'] = atof(request.GET['purchase'])
                    if 'brand' in request.GET and isValid(request.GET['brand']):
                        condition['brand'] = request.GET['brand']
                    if 'state' in request.GET and isValid(request.GET['state']):
                        condition['state'] = int(request.GET['state'])
                    goodsSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                goodsSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        goodsSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(goodsSelect), content_type='application/json')


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
        basicsCount = Goods.objects.all().count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = Goods.objects.filter(
                Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
        else:
            basicsCount = Goods.objects.filter(**condition).count()
    if basicsCount != 0:
        if basicsCount % ONE_PAGE_OF_DATA == 0:
            allPage = basicsCount / ONE_PAGE_OF_DATA
        else:
            allPage = basicsCount / ONE_PAGE_OF_DATA + 1
    else:
        allPage = 1
    if curPage == 1:
        if condition == None:
            basicObjs = Goods.objects.all()[0:ONE_PAGE_OF_DATA]
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = Goods.objects.filter(
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[
                            0:ONE_PAGE_OF_DATA]
            else:
                basicObjs = Goods.objects.filter(**condition)[0:ONE_PAGE_OF_DATA]
        for basicObj in basicObjs:
            basicJSON = getGoods(basicObj)
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
            basicObjs = Goods.objects.all()[startPos:endPos]
        else:
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicObjs = Goods.objects.filter(
                    Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
            else:
                basicObjs = Goods.objects.filter(**condition)[startPos:endPos]
        for basicObj in basicObjs:
            basicJSON = getGoods(basicObj)
            datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
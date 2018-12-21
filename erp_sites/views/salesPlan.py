#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getSalesPlanOrder,isValid
import traceback
from erp_sites.models import SalesPlanOrder,SalesPlanOrderCommodity
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def salesPlanInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'SP-' + create_time[0:10] + '-'
            if 'endTime' in json2Dict:
                if isValid(json2Dict['endTime']):
                    end_time_str = json2Dict['endTime']
                    end_time = time.strptime(end_time_str, '%Y-%m-%d')
                    end_time = datetime.datetime(*end_time[:3]).date()
                else:
                    end_time = None
            else:
                end_time = None
            if 'currency' in json2Dict:
                if isValid(json2Dict['currency']):
                    currency = int(json2Dict['currency'])
                else:
                    currency = 0
            else:
                currency = 0
            if 'branch' in json2Dict:
                if isValid(json2Dict['branch']):
                    branch = json2Dict['branch']
                else:
                    branch = None
            else:
                branch = None
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                else:
                    originator = None
            else:
                originator = None
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                else:
                    summary = None
            else:
                summary = None
            if 'supctoID' in json2Dict:
                if isValid(json2Dict['supctoID']):
                    supcto_id = int(json2Dict['supctoID'])
                else:
                    supcto_id = 0
            else:
                supcto_id = 0
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                else:
                    person_id = 0
            else:
                person_id = 0
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                else:
                    state = 0
            else:
                state = 0
            if 'isAppOrder' in json2Dict:
                if isValid(json2Dict['isAppOrder']):
                    is_app_order = int(json2Dict['isAppOrder'])
                else:
                    is_app_order = 0
            else:
                is_app_order = 0
            if 'appConsigneeName' in json2Dict:
                if isValid(json2Dict['appConsigneeName']):
                    app_consignee_name = json2Dict['appConsigneeName']
                else:
                    app_consignee_name = None
            else:
                app_consignee_name = None
            if 'appConsigneePhone' in json2Dict:
                if isValid(json2Dict['appConsigneePhone']):
                    app_consignee_phone = json2Dict['appConsigneePhone']
                else:
                    app_consignee_phone = None
            else:
                app_consignee_phone = None
            if 'appConsigneeAddress' in json2Dict:
                if isValid(json2Dict['appConsigneeAddress']):
                    app_consignee_address = json2Dict['appConsigneeAddress']
                else:
                    app_consignee_address = None
            else:
                app_consignee_address = None
            if 'missOrderID' in json2Dict:
                if isValid(json2Dict['missOrderID']):
                    miss_order_id = int(json2Dict['missOrderID'])
                else:
                    miss_order_id = 0
            else:
                miss_order_id = 0
            if 'activityID' in json2Dict:
                if isValid(json2Dict['activityID']):
                    activity_id = int(json2Dict['activityID'])
                else:
                    activity_id = 0
            else:
                activity_id = 0
            if 'fax' in json2Dict:
                if isValid(json2Dict['fax']):
                    fax = json2Dict['fax']
                else:
                    fax = None
            else:
                fax = None
            if 'shippingModeID' in json2Dict:
                if isValid(json2Dict['shippingModeID']):
                    shipping_mode_id = int(json2Dict['shippingModeID'])
                else:
                    shipping_mode_id = 0
            else:
                shipping_mode_id = 0
            if 'phone' in json2Dict:
                if isValid(json2Dict['phone']):
                    phone = json2Dict['phone']
                else:
                    phone = None
            else:
                phone = None
            if 'deliverGoodsPlace' in json2Dict:
                if isValid(json2Dict['deliverGoodsPlace']):
                    deliver_goods_place = json2Dict['deliverGoodsPlace']
                else:
                    deliver_goods_place = None
            else:
                deliver_goods_place = None
            if 'orderer' in json2Dict:
                if isValid(json2Dict['orderer']):
                    orderer = json2Dict['orderer']
                else:
                    orderer = None
            else:
                orderer = None
            salesPlanOrder = SalesPlanOrder(None,identifier,create_time,end_time,currency,branch,originator,summary,supcto_id,person_id,state,is_app_order,app_consignee_name,app_consignee_phone,app_consignee_address,miss_order_id,activity_id,fax,shipping_mode_id,phone,deliver_goods_place,orderer)
            salesPlanOrder.save()
            salesPlanOrder.identifier = identifier + str(salesPlanOrder.id)
            salesPlanOrder.save()
            if 'salesPlanOrderCommodities' in json2Dict:
                salesPlanOrderCommodities = json2Dict['salesPlanOrderCommodities']
                for salesPlanOrderCommodity in salesPlanOrderCommodities:
                    sales_plan_order_id = salesPlanOrder.id
                    if 'commoditiespecificationID' in salesPlanOrderCommodity:
                        if isValid(json2Dict['commoditiespecificationID']):
                            commodity_specification_id = int(salesPlanOrderCommodity['commoditiespecificationID'])
                        else:
                            commodity_specification_id = 0
                    else:
                        commodity_specification_id = 0
                    if 'number' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['number']):
                            number = int(salesPlanOrderCommodity['number'])
                        else:
                            number = 0
                    else:
                        number = 0
                    if 'unitPrice' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['unitPrice']):
                            unit_price = int(salesPlanOrderCommodity['unitPrice'])
                        else:
                            unit_price = 0
                    else:
                        unit_price = 0
                    if 'money' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['money']):
                            money = atof(salesPlanOrderCommodity['money'])
                        else:
                            money = 0
                    else:
                        money = 0
                    if 'remark' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['remark']):
                            remark = salesPlanOrderCommodity['remark']
                        else:
                            remark = None
                    else:
                        remark = None
                    salesPlanOrderCommodity = SalesPlanOrderCommodity(None,sales_plan_order_id,commodity_specification_id,number,unit_price,money,remark)
                    salesPlanOrderCommodity.save()
            salesPlanOrderJSON = getSalesPlanOrder(salesPlanOrder)
            salesPlanInsert = setStatus(200,salesPlanOrderJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        salesPlanInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(salesPlanInsert), content_type='application/json')


def salesPlanDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                salesPlanOrders = SalesPlanOrder.objects.filter(id=identifier)
                if len(salesPlanOrders) > 0:
                    salesPlanOrder = salesPlanOrders[0]
                    salesPlanOrderCommodities = SalesPlanOrderCommodity.objects.filter(sales_plan_order_id=salesPlanOrder.id)
                    for salesPlanOrderCommodity in salesPlanOrderCommodities:
                        salesPlanOrderCommodity.delete()
                    salesPlanOrder.delete()
                    salesPlanDelete = setStatus(200,{})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    salesPlanDelete = setStatus(300, errorIDs)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        salesPlanDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(salesPlanDelete), content_type='application/json')


def salesPlanUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            salesPlanOrders = SalesPlanOrder.objects.filter(identifier=identifier)
            if len(salesPlanOrders) > 0:
                salesPlanOrder = salesPlanOrders[0]
            else:
                salesPlanUpdate = setStatus(300,{})
                return HttpResponse(json.dumps(salesPlanUpdate), content_type='application/json')
            if 'endTime' in json2Dict:
                if isValid(json2Dict['endTime']):
                    end_time_str = json2Dict['endTime']
                    end_time = time.strptime(end_time_str, '%Y-%m-%d')
                    end_time = datetime.datetime(*end_time[:3]).date()
                    salesPlanOrder.end_time = end_time
            if 'currency' in json2Dict:
                if isValid(json2Dict['currency']):
                    currency = int(json2Dict['currency'])
                    salesPlanOrder.currency = currency
            if 'branch' in json2Dict:
                if isValid(json2Dict['branch']):
                    branch = json2Dict['branch']
                    salesPlanOrder.branch = branch
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                    salesPlanOrder.originator = originator
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                    salesPlanOrder.summary = summary
            if 'supctoID' in json2Dict:
                if isValid(json2Dict['supctoID']):
                    supcto_id = int(json2Dict['supctoID'])
                    salesPlanOrder.supcto_id = supcto_id
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                    salesPlanOrder.person_id = person_id
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                    salesPlanOrder.state = state
            if 'isAppOrder' in json2Dict:
                if isValid(json2Dict['isAppOrder']):
                    is_app_order = int(json2Dict['isAppOrder'])
                    salesPlanOrder.is_app_order = is_app_order
            if 'appConsigneeName' in json2Dict:
                if isValid(json2Dict['appConsigneeName']):
                    app_consignee_name = json2Dict['appConsigneeName']
                    salesPlanOrder.app_consignee_name = app_consignee_name
            if 'appConsigneePhone' in json2Dict:
                if isValid(json2Dict['appConsigneePhone']):
                    app_consignee_phone = json2Dict['appConsigneePhone']
                    salesPlanOrder.app_consignee_phone = app_consignee_phone
            if 'appConsigneeAddress' in json2Dict:
                if isValid(json2Dict['appConsigneeAddress']):
                    app_consignee_address = json2Dict['appConsigneeAddress']
                    salesPlanOrder.app_consignee_address = app_consignee_address
            if 'missOrderID' in json2Dict:
                if isValid(json2Dict['missOrderID']):
                    miss_order_id = int(json2Dict['missOrderID'])
                    salesPlanOrder.miss_order_id = miss_order_id
            if 'activityID' in json2Dict:
                if isValid(json2Dict['activityID']):
                    activity_id = int(json2Dict['activityID'])
                    salesPlanOrder.activity_id = activity_id
            if 'fax' in json2Dict:
                if isValid(json2Dict['fax']):
                    fax = json2Dict['fax']
                    salesPlanOrder.fax = fax
            if 'shippingModeID' in json2Dict:
                if isValid(json2Dict['shippingModeID']):
                    shipping_mode_id = int(json2Dict['shippingModeID'])
                    salesPlanOrder.shipping_mode_id = shipping_mode_id
            if 'phone' in json2Dict:
                if isValid(json2Dict['phone']):
                    phone = json2Dict['phone']
                    salesPlanOrder.phone = phone
            if 'deliverGoodsPlace' in json2Dict:
                if isValid(json2Dict['deliverGoodsPlace']):
                    deliver_goods_place = json2Dict['deliverGoodsPlace']
                    salesPlanOrder.deliver_goods_place = deliver_goods_place
            if 'orderer' in json2Dict:
                if isValid(json2Dict['orderer']):
                    orderer = json2Dict['orderer']
                    salesPlanOrder.orderer = orderer
            salesPlanOrder.save()
            if 'salesPlanOrderCommodities' in json2Dict:
                salesPlanOrderCommodities = json2Dict['salesPlanOrderCommodities']
                for salesPlanOrderCommodity in salesPlanOrderCommodities:
                    if 'slesPlanOrderCommodityID' in salesPlanOrderCommodity:
                        slesPlanOrderCommodityID = salesPlanOrderCommodity['slesPlanOrderCommodityID']
                        spocs = SalesPlanOrderCommodity.objects.filter(id=slesPlanOrderCommodityID)
                        if len(spocs) > 0:
                            spoc = spocs[0]
                        else:
                            salesPlanUpdate = setStatus(300,{})
                            return HttpResponse(json.dumps(salesPlanUpdate), content_type='application/json')
                    else:
                        continue
                    if 'commoditySpecificationID' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['commoditySpecificationID']):
                            commodity_specification_id = int(salesPlanOrderCommodity['commoditySpecificationID'])
                            spoc.commodity_specification_id = commodity_specification_id
                    else:
                        commodity_specification_id = 0
                    if 'number' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['number']):
                            number = int(salesPlanOrderCommodity['number'])
                            spoc.number = number
                    else:
                        number = 0
                    if 'unitPrice' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['unitPrice']):
                            unit_price = int(salesPlanOrderCommodity['unitPrice'])
                            spoc.unit_price = unit_price
                    else:
                        unit_price = 0
                    if 'money' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['money']):
                            money = atof(salesPlanOrderCommodity['money'])
                            spoc.money = money
                    else:
                        money = 0
                    if 'remark' in salesPlanOrderCommodity:
                        if isValid(salesPlanOrderCommodity['remark']):
                            remark = salesPlanOrderCommodity['remark']
                            spoc.remark = remark
                    else:
                        remark = None
                    spoc.save()
            salesPlanOrderJSON = getSalesPlanOrder(salesPlanOrder)
            salesPlanUpdate = setStatus(200,salesPlanOrderJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        salesPlanUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(salesPlanUpdate), content_type='application/json')


def salesPlanSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                condition = {}
                selectType = {}
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'commodityID' in request.GET and isValid(request.GET['commodityID']):
                    commodityID = int(request.GET['commodityID'])
                else:
                    commodityID = 0
                if 'personID' in request.GET and isValid(request.GET['personID']):
                    condition['person_id'] = request.GET['personID']
                if 'state' in request.GET and isValid(request.GET['state']):
                        condition['state'] = int(request.GET['state'])
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                salesPlanSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType, commodityID)
            else:
                salesPlanSelect = paging(request, ONE_PAGE_OF_DATA, None, None, 0)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        salesPlanSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(salesPlanSelect), content_type='application/json')

def orderPlanToNormal(request):
    try:
        if isTokenExpired(request):
            identifier = request.GET['identifier']
            #这个api是将计划销售单，转换成正式销售单，⽣成新的单⼦
        else:
            return notTokenExpired()
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        orderPlanToNormal = setStatus(500, traceback.format_exc())
    return HttpResponse(json.dumps(orderPlanToNormal), content_type='application/json')


def paging(request, ONE_PAGE_OF_DATA, condition, selectType,commodityID):
    logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    allPage = 1
    if condition == None:
        basicsCount = SalesPlanOrder.objects.all().count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            spocs = SalesPlanOrderCommodity.objects.filter(commodity_specification_id=commodityID)
            if len(spocs) > 0:
                spoc_id_list = []
                for spoc in spocs:
                    spoc_id_list.append(spoc.sales_plan_order_id)
                basicsCount = SalesPlanOrder.objects.filter(Q(id__in=spoc_id_list) & Q(**condition) & Q(create_time__gte=timeFrom) & Q(create_time__lte=timeTo)).count()
            else:
                basicsCount = SalesPlanOrder.objects.filter(Q(**condition) & Q(create_time__gte=timeFrom) & Q(create_time__lte=timeTo)).count()
        else:
            basicsCount = SalesPlanOrder.objects.filter(**condition).count()
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
        basicObjs = SalesPlanOrder.objects.all()[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            spocs = SalesPlanOrderCommodity.objects.filter(commodity_specification_id=commodityID)
            if len(spocs) > 0:
                spoc_id_list = []
                for spoc in spocs:
                    spoc_id_list.append(spoc.sales_plan_order_id)
                basicObjs = SalesPlanOrder.objects.filter(
                        Q(id__in=spoc_id_list) & Q(**condition) & Q(create_time__gte=timeFrom) & Q(create_time__lte=timeTo))[startPos:endPos]
            else:
                basicObjs = SalesPlanOrder.objects.filter(
                    Q(**condition) & Q(create_time__gte=timeFrom) & Q(create_time__lte=timeTo))[startPos:endPos]
        else:
                basicObjs = SalesPlanOrder.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getSalesPlanOrder(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
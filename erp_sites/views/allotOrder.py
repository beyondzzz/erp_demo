#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getAllot,isValid
import traceback
from erp_sites.models import AllotOrder,AllotOrderCommodity
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def allotInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            allot_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'ALO-' + allot_date[0:10] + '-'
            if 'exportWarehouseID' in json2Dict:
                if isValid(json2Dict['exportWarehouseID']):
                    export_warehouse_id = int(json2Dict['exportWarehouseID'])
                else:
                    export_warehouse_id = 0
            else:
                export_warehouse_id = 0
            if 'importWarehouseID' in json2Dict:
                if isValid(json2Dict['importWarehouseID']):
                    import_warehouse_id = int(json2Dict['importWarehouseID'])
                else:
                    import_warehouse_id = 0
            else:
                import_warehouse_id = 0
            if 'shippingModeID' in json2Dict:
                if isValid(json2Dict['shippingModeID']):
                    shipping_mode_id = int(json2Dict['shippingModeID'])
                else:
                    shipping_mode_id = 0
            else:
                shipping_mode_id = 0
            if 'importBranch' in json2Dict:
                if isValid(json2Dict['importBranch']):
                    import_branch = json2Dict['importBranch']
                else:
                    import_branch = None
            else:
                import_branch = None
            if 'adjustSubject' in json2Dict:
                if isValid(json2Dict['adjustSubject']):
                    adjust_subject = json2Dict['adjustSubject']
                else:
                    adjust_subject = None
            else:
                adjust_subject = None
            if 'sendGoodsPlace' in json2Dict:
                if isValid(json2Dict['sendGoodsPlace']):
                    send_goods_place = json2Dict['sendGoodsPlace']
                else:
                    send_goods_place = None
            else:
                send_goods_place = None
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
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                else:
                    summary = None
            else:
                summary = None
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                else:
                    print_num = 0
            else:
                print_num = 0
            if 'makePerson' in json2Dict:
                if isValid(json2Dict['makePerson']):
                    make_person = json2Dict['makePerson']
                else:
                    make_person = None
            else:
                make_person = None
            if 'description' in json2Dict:
                if isValid(json2Dict['description']):
                    description = json2Dict['description']
                else:
                    description = None
            else:
                description = None
            if 'exportName' in json2Dict:
                if isValid(json2Dict['exportName']):
                    export_name = json2Dict['exportName']
                else:
                    export_name = None
            else:
                export_name = None
            if 'importName' in json2Dict:
                if isValid(json2Dict['importName']):
                    import_name = json2Dict['importName']
                else:
                    import_name = None
            else:
                import_name = None
            allot = AllotOrder(None,allot_date,identifier,export_warehouse_id,import_warehouse_id,shipping_mode_id,import_branch,adjust_subject,send_goods_place,person_id,originator,summary,print_num,make_person,description,export_name,import_name)
            allot.save()
            allot.identifier = identifier + str(allot.id)
            allot.save()
            if 'allotCommodities' in json2Dict:
                allotCommodities = json2Dict['allotCommodities']
                for allotCommodity in allotCommodities:
                    allot_order_id = allot.id
                    if 'commoditySpecificationID' in allotCommodity:
                        commodity_specification_id = int(allotCommodity['commoditySpecificationID'])
                    else:
                        commodity_specification_id = 0
                    if 'number' in allotCommodity:
                        number = int(allotCommodity['number'])
                    else:
                        number = 0
                    if 'exportUnitPrice' in allotCommodity:
                        export_unit_price = atof(allotCommodity['exportUnitPrice'])
                    else:
                        export_unit_price = 0
                    if 'importUnitPrice' in allotCommodity:
                        import_unit_price = atof(allotCommodity['importUnitPrice'])
                    else:
                        import_unit_price = 0
                    if 'importMoney' in allotCommodity:
                        import_money = atof(allotCommodity['importMoney'])
                    else:
                        import_money = 0
                    allotCommodityObj = AllotOrderCommodity(None,allot_order_id,commodity_specification_id,number,export_unit_price,import_unit_price,import_money)
                    allotCommodityObj.save()
            alltoJSON = getAllot(allot)
            allotInsert = setStatus(200,alltoJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        allotInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(allotInsert), content_type='application/json')


def allotDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                allots = AllotOrder.objects.filter(id=identifier)
                if len(allots) > 0:
                    allot = allots[0]
                    allotCommodities = AllotOrderCommodity.objects.filter(allot_order_id=allot.id)
                    for allotCommodity in allotCommodities:
                        allotCommodity.delete()
                    allot.delete()
                    allotDelete = setStatus(200,{})
                else:
                    errorIDs.append(identifier)
            if len(errorIDs) > 0:
                allotDelete = setStatus(300,errorIDs)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        allotDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(allotDelete), content_type='application/json')


def allotUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            allots = AllotOrder.objects.filter(identifier=identifier)
            if len(allots) > 0:
                allot = allots[0]
            else:
                allotUpdate = setStatus(300,{})
                return HttpResponse(json.dumps(allotUpdate), content_type='application/json')
            if 'exportWarehouseID' in json2Dict:
                if isValid(json2Dict['exportWarehouseID']):
                    export_warehouse_id = int(json2Dict['exportWarehouseID'])
                    allot.export_warehouse_id = export_warehouse_id
            if 'importWarehouseID' in json2Dict:
                if isValid(json2Dict['importWarehouseID']):
                    import_warehouse_id = int(json2Dict['importWarehouseID'])
                    allot.import_warehouse_id = import_warehouse_id
            if 'shippingModeID' in json2Dict:
                if isValid(json2Dict['shippingModeID']):
                    shipping_mode_id = int(json2Dict['shippingModeID'])
                    allot.shipping_mode_id = shipping_mode_id
            if 'importBranch' in json2Dict:
                if isValid(json2Dict['importBranch']):
                    import_branch = json2Dict['importBranch']
                    allot.import_branch = import_branch
            if 'adjustSubject' in json2Dict:
                if isValid(json2Dict['adjustSubject']):
                    adjust_subject = json2Dict['adjustSubject']
                    allot.adjust_subject = adjust_subject
            if 'sendGoodsPlace' in json2Dict:
                if isValid(json2Dict['sendGoodsPlace']):
                    send_goods_place = json2Dict['sendGoodsPlace']
                    allot.send_goods_place = send_goods_place
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                    allot.person_id = person_id
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                    allot.originator = originator
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                    allot.summary = summary
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                    allot.print_num = print_num
            if 'makePerson' in json2Dict:
                if isValid(json2Dict['makePerson']):
                    make_person = json2Dict['makePerson']
                    allot.make_person = make_person
            if 'description' in json2Dict:
                if isValid(json2Dict['description']):
                    description = json2Dict['description']
                    allot.description = description
            if 'exportName' in json2Dict:
                if isValid(json2Dict['exportName']):
                    export_name = json2Dict['exportName']
                    allot.export_name = export_name
            if 'importName' in json2Dict:
                if isValid(json2Dict['importName']):
                    import_name = json2Dict['importName']
                    allot.import_name = import_name
            allot.save()
            if 'allotCommodities' in json2Dict:
                allotCommodities = json2Dict['allotCommodities']
                for allotCommodity in allotCommodities:
                    if 'allotCommodityID' in allotCommodity:
                        allotCommodityID = int(allotCommodity['allotCommodityID'])
                        allotCommodityObjs = AllotOrderCommodity.objects.filter(id=allotCommodityID)
                        if len(allotCommodityObjs) > 0:
                            allotCommodityObj = allotCommodityObjs[0]
                        else:
                            allotUpdate = setStatus(300,{})
                            return HttpResponse(json.dumps(allotUpdate), content_type='application/json')
                    else:
                        continue
                    if 'commoditySpecificationID' in allotCommodity:
                        if isValid(allotCommodity['commoditySpecificationID']):
                            commodity_specification_id = int(allotCommodity['commoditySpecificationID'])
                            allotCommodityObj.commodity_specification_id = commodity_specification_id
                    if 'number' in allotCommodity:
                        if isValid(allotCommodity['number']):
                            number = int(allotCommodity['number'])
                            allotCommodityObj.number = number
                    if 'exportUnitPrice' in allotCommodity:
                        if isValid(allotCommodity['exportUnitPrice']):
                            export_unit_price = atof(allotCommodity['exportUnitPrice'])
                            allotCommodityObj.export_unit_price = export_unit_price
                    if 'importUnitPrice' in allotCommodity:
                        if isValid(allotCommodity['importUnitPrice']):
                            import_unit_price = atof(allotCommodity['importUnitPrice'])
                            allotCommodityObj.import_unit_price = import_unit_price
                    if 'importMoney' in allotCommodity:
                        if isValid(allotCommodity['importMoney']):
                            import_money = atof(allotCommodity['importMoney'])
                            allotCommodityObj.import_money = import_money
                    allotCommodityObj.save()
            alltoJSON = getAllot(allot)
            allotUpdate = setStatus(200,alltoJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        allotUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(allotUpdate), content_type='application/json')


def allotSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                condition = {}
                selectType = {}
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'makePerson' in request.GET and isValid(request.GET['makePerson']):
                    condition['make_person'] = request.GET['makePerson']
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                allotSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                allotSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        allotSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(allotSelect), content_type='application/json')


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
        basicsCount = AllotOrder.objects.all().count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = AllotOrder.objects.filter(Q(**condition) & Q(allot_date__gte=timeFrom) & Q(allot_date__lte=timeTo)).count()
        else:
            basicsCount = AllotOrder.objects.filter(**condition).count()
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
        basicObjs = AllotOrder.objects.all()[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = AllotOrder.objects.filter(Q(**condition) & Q(allot_date__gte=timeFrom) & Q(allot_date__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = AllotOrder.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getAllot(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
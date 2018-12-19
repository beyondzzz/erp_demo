#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getStock,isValid
import traceback
from erp_sites.models import TakeStockOrder,TakeStockOrderCommodity
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def stockCheckInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            take_stock_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'TSO-' + take_stock_date[0:10] + '-'
            if 'warehouseID' in json2Dict:
                if isValid(json2Dict['warehouseID']):
                    warehouse_id = int(json2Dict['warehouseID'])
                else:
                    warehouse_id = 0
            else:
                warehouse_id = 0
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
                warehouse_id = None
            if 'financeReviewer' in json2Dict:
                if isValid(json2Dict['financeReviewer']):
                    finance_reviewer = json2Dict['financeReviewer']
                else:
                    finance_reviewer = None
            else:
                finance_reviewer = None
            if 'managerReviewer' in json2Dict:
                if isValid(json2Dict['managerReviewer']):
                    manager_reviewer = json2Dict['managerReviewer']
                else:
                    manager_reviewer = None
            else:
                manager_reviewer = None
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
            stock = TakeStockOrder(None,take_stock_date,identifier,warehouse_id,person_id,originator,finance_reviewer,manager_reviewer,summary,state,print_num,is_delete)
            stock.save()
            stock.identifier = identifier + str(stock.id)
            stock.save()
            if 'stockCommodities' in json2Dict:
                stockCommodities = json2Dict['stockCommodities']
                for stockCommodity in stockCommodities:
                    take_stock_order_id = stock.id
                    if 'commoditySpecificationID' in stockCommodity:
                        if isValid(stockCommodity['commoditySpecificationID']):
                            commodity_specification_id = int(stockCommodity['commoditySpecificationID'])
                        else:
                            commodity_specification_id = 0
                    else:
                        commodity_specification_id = 0
                    if 'inventoryNum' in stockCommodity:
                        if isValid(stockCommodity['inventoryNum']):
                            inventory_num = int(stockCommodity['inventoryNum'])
                        else:
                            inventory_num = 0
                    else:
                        inventory_num = 0
                    if 'realNum' in stockCommodity:
                        if isValid(stockCommodity['realNum']):
                            real_num = int(stockCommodity['realNum'])
                        else:
                            real_num = 0
                    else:
                        real_num = 0
                    if 'profitOrLossNum' in stockCommodity:
                        if isValid(stockCommodity['profitOrLossNum']):
                            profit_or_loss_num = int(stockCommodity['profitOrLossNum'])
                        else:
                            profit_or_loss_num = 0
                    else:
                        profit_or_loss_num = 0
                    if 'unitPrice' in stockCommodity:
                        if isValid(stockCommodity['unitPrice']):
                            unit_price = atof(stockCommodity['unitPrice'])
                        else:
                            unit_price = 0
                    else:
                        unit_price = 0
                    if 'money' in stockCommodity:
                        if isValid(stockCommodity['money']):
                            money = atof(stockCommodity['money'])
                        else:
                            money = 0
                    else:
                        money = 0
                    stockCommoditiObj = TakeStockOrderCommodity(None,take_stock_order_id,commodity_specification_id,inventory_num,real_num,profit_or_loss_num,unit_price,money)
                    stockCommoditiObj.save()
            stockJSON = getStock(stock)
            stockCheckInsert = setStatus(200,stockJSON)
        else:
                return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        stockCheckInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(stockCheckInsert), content_type='application/json')


def stockCheckDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                stocks = TakeStockOrder.objects.filter(id=identifier)
                if len(stocks) > 0:
                    stock = stocks[0]
                    stock.is_delete = 1
                    stock.save()
                    stockCheckDelete = setStatus(200, {})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    stockCheckDelete = setStatus(300, errorIDs)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        stockCheckDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(stockCheckDelete), content_type='application/json')


def stockCheckUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            stocks = TakeStockOrder.objects.filter(identifier=identifier)
            if len(stocks) > 0:
                stock = stocks[0]
            else:
                stockUpdate = setStatus(300, {})
                return HttpResponse(json.dumps(stockUpdate), content_type='application/json')
            if 'warehouseID' in json2Dict:
                if isValid(json2Dict['warehouseID']):
                    warehouse_id = int(json2Dict['warehouseID'])
                    stock.warehouse_id = warehouse_id
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                    stock.person_id = person_id
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                    stock.originator = originator
            if 'financeReviewer' in json2Dict:
                if isValid(json2Dict['financeReviewer']):
                    finance_reviewer = json2Dict['financeReviewer']
                    stock.finance_reviewer = finance_reviewer
            if 'managerReviewer' in json2Dict:
                if isValid(json2Dict['managerReviewer']):
                    manager_reviewer = json2Dict['managerReviewer']
                    stock.manager_reviewer = manager_reviewer
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                    stock.summary = summary
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                    stock.state = state
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                    stock.print_num = print_num
            stock.save()
            if 'stockCommodities' in json2Dict:
                stockCommodities = json2Dict['stockCommodities']
                for stockCommodity in stockCommodities:
                    if 'stockCommoditiyID' in stockCommodity:
                        stockCommoditiyID = stockCommodity['stockCommoditiyID']
                        stockCommodityObjs =TakeStockOrderCommodity.objects.filter(id=stockCommoditiyID)
                        if len(stockCommodityObjs) > 0:
                            stockCommodityObj = stockCommodityObjs[0]
                        else:
                            stockUpdate = setStatus(300, {})
                            return HttpResponse(json.dumps(stockUpdate), content_type='application/json')
                    else:
                        continue
                    if 'commoditySpecificationID' in stockCommodity:
                        if isValid(stockCommodity['commoditySpecificationID']):
                            commodity_specification_id = int(stockCommodity['commoditySpecificationID'])
                            stockCommodityObj.commodity_specification_id = commodity_specification_id
                    if 'inventoryNum' in stockCommodity:
                        if isValid(stockCommodity['inventoryNum']):
                            inventory_num = int(stockCommodity['inventoryNum'])
                            stockCommodityObj.inventory_num = inventory_num
                    if 'realNum' in stockCommodity:
                        if isValid(stockCommodity['realNum']):
                            real_num = int(stockCommodity['realNum'])
                            stockCommodityObj.real_num = real_num
                    if 'profitOrLossNum' in stockCommodity:
                        if isValid(stockCommodity['profitOrLossNum']):
                            profit_or_loss_num = int(stockCommodity['profitOrLossNum'])
                            stockCommodityObj.profit_or_loss_num = profit_or_loss_num
                    if 'advanceMoney' in stockCommodity:
                        if isValid(stockCommodity['advanceMoney']):
                            unit_price = atof(stockCommodity['advanceMoney'])
                            stockCommodityObj.unit_price = unit_price
                    if 'money' in stockCommodity:
                        if isValid(stockCommodity['money']):
                            money = atof(stockCommodity['money'])
                            stockCommodityObj.money = money
                    stockCommodityObj.save()
            stockJSON = getStock(stock)
            stockCheckUpdate = setStatus(200, stockJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        stockCheckUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(stockCheckUpdate), content_type='application/json')


def stockCheckSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                if 'identifier' in request.GET:
                    identifier = request.GET['identifier']
                    stocks = TakeStockOrder.objects.filter(identifier=identifier,is_delete=0)
                    if len(stocks) > 0:
                        stock = stocks[0]
                        stockCheckSelect = getStock(stock)
                    else:
                        stockCheckSelect = setStatus(300, {})
                        return HttpResponse(json.dumps(stockCheckSelect), content_type='application/json')
                else:
                    condition = {}
                    selectType = {}
                    if 'warehouseID' in request.GET and isValid(request.GET['warehouseID']):
                        condition['warehouse_id'] = int(request.GET['warehouseID'])
                    if 'personID' in request.GET and isValid(request.GET['personID']):
                        condition['person_id'] = int(request.GET['personID'])
                    if 'state' in request.GET and isValid(request.GET['state']):
                        condition['state'] = int(request.GET['state'])
                    condition['is_delete'] = 0
                    if 'queryTime' in request.GET:
                        queryTime = request.GET['queryTime']
                        timeFrom = queryTime.split('~')[0].strip()
                        timeTo = queryTime.split('~')[1].strip()
                        selectType['timeFrom'] = timeFrom + ' 00:00:00'
                        selectType['timeTo'] = timeTo + ' 23:59:59'
                    stockCheckSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                stockCheckSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        stockCheckSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(stockCheckSelect), content_type='application/json')


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
        basicsCount = TakeStockOrder.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = TakeStockOrder.objects.filter(
                Q(**condition) & Q(take_stock_date__gte=timeFrom) & Q(take_stock_date__lte=timeTo)).count()
        else:
            basicsCount = TakeStockOrder.objects.filter(**condition).count()
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
        basicObjs = TakeStockOrder.objects.filter(is_delete=0)[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = TakeStockOrder.objects.filter(
                    Q(**condition) & Q(take_stock_date__gte=timeFrom) & Q(take_stock_date__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = TakeStockOrder.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getStock(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
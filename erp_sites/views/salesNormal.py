#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getSalesOrder,isValid
import traceback
from erp_sites.models import SalesOrder,SalesOrderCommodity,Supcto
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def salesNormalInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            if 'parentID' in json2Dict:
                parent_id = int(json2Dict['parentID'])
            else:
                parent_id = 0
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'SON-' + create_time[0:10] + '-'
            if 'breakCode' in json2Dict:
                if isValid(json2Dict['breakCode']):
                    break_code = json2Dict['breakCode']
                else:
                    break_code = None
            else:
                break_code = None
            if 'payment' in json2Dict:
                if isValid(json2Dict['payment']):
                    payment = int(json2Dict['payment'])
                else:
                    payment = 0
            else:
                payment = 0
            if 'orderType' in json2Dict:
                if isValid(json2Dict['orderType']):
                    order_type = int(json2Dict['orderType'])
                else:
                    order_type = 0
            else:
                order_type = 0
            if 'endValidityTime' in json2Dict:
                if isValid(json2Dict['endValidityTime']):
                    end_validity_time_str = json2Dict['endValidityTime']
                    end_validity_time = time.strptime(end_validity_time_str, '%Y-%m-%d')
                    end_validity_time = datetime.datetime(*end_validity_time[:3]).date()
                else:
                    end_validity_time = None
            else:
                end_validity_time = None
            if 'deliverGoodsPlace' in json2Dict:
                if isValid(json2Dict['deliverGoodsPlace']):
                    deliver_goods_place = json2Dict['deliverGoodsPlace']
                else:
                    deliver_goods_place = None
            else:
                deliver_goods_place = None
            if 'receiptGoodsPlace' in json2Dict:
                if isValid(json2Dict['receiptGoodsPlace']):
                    receipt_goods_place = json2Dict['receiptGoodsPlace']
                else:
                    receipt_goods_place = None
            else:
                receipt_goods_place = None
            if 'consignee' in json2Dict:
                if isValid(json2Dict['consignee']):
                    consignee = json2Dict['consignee']
                else:
                    consignee = None
            else:
                consignee = None
            if 'phone' in json2Dict:
                if isValid(json2Dict['phone']):
                    phone = json2Dict['phone']
                else:
                    phone = None
            else:
                phone = None
            if 'fax' in json2Dict:
                if isValid(json2Dict['fax']):
                    fax = json2Dict['fax']
                else:
                    fax = None
            else:
                fax = None
            if 'orderer' in json2Dict:
                if isValid(json2Dict['orderer']):
                    orderer = json2Dict['orderer']
                else:
                    orderer = None
            else:
                orderer = None
            if 'advanceScale' in json2Dict:
                if isValid(json2Dict['advanceScale']):
                    advance_scale = atof(json2Dict['advanceScale'])
                else:
                    advance_scale = 0
            else:
                advance_scale = 0
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
            if 'branch' in json2Dict:
                if isValid(json2Dict['branch']):
                    branch = json2Dict[ 'branch']
                else:
                    branch = None
            else:
                branch = None
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                else:
                    state = 0
            else:
                state = 0
            if 'isSpecimen' in json2Dict:
                if isValid(json2Dict['isSpecimen']):
                    is_specimen = int(json2Dict['isSpecimen'])
                else:
                    is_specimen = 0
            else:
                is_specimen = 0
            if 'supctoID' in json2Dict:
                if isValid(json2Dict['supctoID']):
                    supcto_id = int(json2Dict['supctoID'])
                else:
                    supcto_id = 0
            else:
                supcto_id = 0
            if 'shippingModeID' in json2Dict:
                if isValid(json2Dict['shippingModeID']):
                    shipping_mode_id = int(json2Dict['shippingModeID'])
                else:
                    shipping_mode_id = 0
            else:
                shipping_mode_id = 0
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                else:
                    person_id = 0
            else:
                person_id = 0
            if 'salesPlanOrderID' in json2Dict:
                if isValid(json2Dict['salesPlanOrderID']):
                    sales_plan_order_id = int(json2Dict['salesPlanOrderID'])
                else:
                    sales_plan_order_id = 0
            else:
                sales_plan_order_id = 0
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                else:
                    print_num = 0
            else:
                print_num = 0
            if 'isShow' in json2Dict:
                if isValid(json2Dict['isShow']):
                    is_show = int(json2Dict['isShow'])
                else:
                    is_show = 0
            else:
                is_show = 0
            if 'isVerification' in json2Dict:
                if isValid(json2Dict['isVerification']):
                    is_verification = json2Dict['isVerification']
                else:
                    is_verification = None
            else:
                is_verification = None
            if 'missOrderID' in json2Dict:
                if isValid(json2Dict['missOrderID']):
                    miss_order_id = json2Dict['missOrderID']
                else:
                    miss_order_id = None
            else:
                miss_order_id = None
            if 'activityID' in json2Dict:
                if isValid(json2Dict['activityID']):
                    activity_id = json2Dict['activityID']
                else:
                    activity_id = None
            else:
                activity_id = None
            if 'isAppOrder' in json2Dict:
                if isValid(json2Dict['isAppOrder']):
                    is_app_order = json2Dict['isAppOrder']
                else:
                    is_app_order = None
            else:
                is_app_order = None
            if 'isReturnGoods' in json2Dict:
                if isValid(json2Dict['isReturnGoods']):
                    is_return_goods = int(json2Dict['isReturnGoods'])
                else:
                    is_return_goods = 0
            else:
                is_return_goods = 0
            if 'appOrderIdentifier' in json2Dict:
                if isValid(json2Dict['appOrderIdentifier']):
                    app_order_identifier = json2Dict['appOrderIdentifier']
                else:
                    app_order_identifier = None
            else:
                app_order_identifier = None
            if 'appSendTime' in json2Dict:
                if isValid(json2Dict['appSendTime']):
                    app_send_time = json2Dict['appSendTime']
                else:
                    app_send_time = None
            else:
                app_send_time = None
            if 'isCreateStockOrder' in json2Dict:
                if isValid(json2Dict['isCreateStockOrder']):
                    is_create_stock_order = json2Dict['isCreateStockOrder']
                else:
                    is_create_stock_order = None
            else:
                is_create_stock_order = None
            salesOrder = SalesOrder(None,parent_id,identifier,break_code,payment,order_type,create_time,end_validity_time,deliver_goods_place,receipt_goods_place,consignee,phone,fax,orderer,advance_scale,originator,summary,branch,state,is_specimen,supcto_id,shipping_mode_id,person_id,sales_plan_order_id,print_num,is_show,is_verification,miss_order_id,activity_id,is_app_order,is_return_goods,app_order_identifier,app_send_time,is_create_stock_order)
            salesOrder.save()
            salesOrder.identifier = identifier + str(salesOrder.id)
            salesOrder.save()
            if 'salesOrderCommodities' in json2Dict:
                salesOrderCommodities = json2Dict['salesOrderCommodities']
                for salesOrderCommodity in salesOrderCommodities:
                    sales_order_id = salesOrder.id
                    if 'commoditySpecificationID' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['commoditySpecificationID']):
                            commodity_specification_id = int(salesOrderCommodity['commoditySpecificationID'])
                        else:
                            commodity_specification_id = 0
                    else:
                        commodity_specification_id = 0
                    if 'deliverGoodsMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['deliverGoodsMoney']):
                            deliver_goods_money = atof(salesOrderCommodity['deliverGoodsMoney'])
                        else:
                            deliver_goods_money = 0
                    else:
                        deliver_goods_money = 0
                    if 'deliverGoodsNum' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['deliverGoodsNum']):
                            deliver_goods_num = int(salesOrderCommodity['deliverGoodsNum'])
                        else:
                            deliver_goods_num = 0
                    else:
                        deliver_goods_num = 0
                    if 'returnGoodsNum' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['returnGoodsNum']):
                            return_goods_num = int(salesOrderCommodity['returnGoodsNum'])
                        else:
                            return_goods_num = 0
                    else:
                        return_goods_num = 0
                    if 'receivingGoodsMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['receivingGoodsMoney']):
                            receiving_goods_money = atof(salesOrderCommodity['receivingGoodsMoney'])
                        else:
                            receiving_goods_money = 0
                    else:
                        receiving_goods_money = 0
                    if 'receivingGoodsNum' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['receivingGoodsNum']):
                            receiving_goods_num = int(salesOrderCommodity['receivingGoodsNum'])
                        else:
                            receiving_goods_num = 0
                    else:
                        receiving_goods_num = 0
                    if 'damageNum' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['damageNum']):
                            damage_num = int(salesOrderCommodity['damageNum'])
                        else:
                            damage_num = 0
                    else:
                        damage_num = 0
                    if 'damageMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['damageMoney']):
                            damage_money = atof(salesOrderCommodity['damageMoney'])
                        else:
                            damage_money = 0
                    else:
                        damage_money = 0
                    if 'discount' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['discount']):
                            discount = atof(salesOrderCommodity['discount'])
                        else:
                            discount = 0
                    else:
                        discount = 0
                    if 'unitPrice' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['unitPrice']):
                            unit_price = atof(salesOrderCommodity['unitPrice'])
                        else:
                            unit_price = 0
                    else:
                        unit_price = 0
                    if 'taxesMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['taxesMoney']):
                            taxes_money = atof(salesOrderCommodity['taxesMoney'])
                        else:
                            taxes_money = 0
                    else:
                        taxes_money = 0
                    if 'taxes' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['taxes']):
                            taxes = atof(salesOrderCommodity['taxes'])
                        else:
                            taxes = 0
                    else:
                        taxes = 0
                    if 'batchNumber' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['batchNumber']):
                            batch_number = salesOrderCommodity['batchNumber']
                        else:
                            batch_number = None
                    else:
                        batch_number = None
                    if 'remark' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['remark']):
                            remark = salesOrderCommodity['remark']
                        else:
                            remark = None
                    else:
                        remark = None
                    if 'isSpecialOffer' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['isSpecialOffer']):
                            is_special_offer = int(salesOrderCommodity['isSpecialOffer'])
                        else:
                            is_special_offer = 0
                    else:
                        is_special_offer = 0
                    if 'warehouseID' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['warehouseID']):
                            warehouse_id = int(salesOrderCommodity['warehouseID'])
                        else:
                            warehouse_id = 0
                    else:
                        warehouse_id = 0
                    if 'appAmountMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['appAmountMoney']):
                            app_amountMoney = atof(salesOrderCommodity['appAmountMoney'])
                        else:
                            app_amountMoney = 0
                    else:
                        app_amountMoney = 0
                    soc = SalesOrderCommodity(None,sales_order_id,commodity_specification_id,deliver_goods_money,deliver_goods_num,return_goods_num,receiving_goods_money,receiving_goods_num,damage_num,damage_money,discount,unit_price,taxes_money,taxes,batch_number,remark,is_special_offer,warehouse_id,app_amountMoney)
                    soc.save()
            salesOrderJSON = getSalesOrder(salesOrder)
            salesNormalInsert = setStatus(200,salesOrderJSON)
        else:
            return notTokenExpired()
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        salesNormalInsert = setStatus(500, traceback.format_exc())
    return HttpResponse(json.dumps(salesNormalInsert), content_type='application/json')


def salesNormalDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                salesOrders = SalesOrder.objects.filter(id=identifier)
                if len(salesOrders) > 0:
                    salesOrder = salesOrders[0]
                    salesOrderCommodities = SalesOrderCommodity.objects.filter(sales_order_id=salesOrder.id)
                    for salesOrderCommodity in salesOrderCommodities:
                        salesOrderCommodity.delete()
                    salesNormalDelete = setStatus(200, {})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    salesNormalDelete = setStatus(300, errorIDs)
        else:
            return notTokenExpired()
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        salesNormalDelete = setStatus(500, traceback.format_exc())
    return HttpResponse(json.dumps(salesNormalDelete), content_type='application/json')


def salesNormalUpdate(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            salesOrders = SalesOrder.objects.filter(identifier=identifier)
            if len(salesOrders) > 0:
                salesOrder = salesOrders[0]
            else:
                salesNormalUpdate = setStatus(300, {})
                return HttpResponse(json.dumps(salesNormalUpdate), content_type='application/json')
            if 'parentID' in json2Dict:
                if isValid(json2Dict['parentID']):
                    parent_id = int(json2Dict['parentID'])
                    salesOrder.parent_id = parent_id
            if 'breakCode' in json2Dict:
                if isValid(json2Dict['breakCode']):
                    break_code = json2Dict['breakCode']
                    salesOrder.break_code = break_code
            if 'payment' in json2Dict:
                if isValid(json2Dict['payment']):
                    payment = int(json2Dict['payment'])
                    salesOrder.payment = payment
            if 'orderType' in json2Dict:
                if isValid(json2Dict['orderType']):
                    order_type = int(json2Dict['orderType'])
                    salesOrder.order_type = order_type
            if 'endValidityTime' in json2Dict:
                if isValid(json2Dict['endValidityTime']):
                    end_validity_time_str = json2Dict['endValidityTime']
                    end_validity_time = time.strptime(end_validity_time_str, '%Y-%m-%d')
                    end_validity_time = datetime.datetime(*end_validity_time[:3]).date()
                    salesOrder.end_validity_time = end_validity_time
            if 'deliverGoodsPlace' in json2Dict:
                if isValid(json2Dict['deliverGoodsPlace']):
                    deliver_goods_place = json2Dict['deliverGoodsPlace']
                    salesOrder.deliver_goods_place = deliver_goods_place
            if 'receiptGoodsPlace' in json2Dict:
                if isValid(json2Dict['receiptGoodsPlace']):
                    receipt_goods_place = json2Dict['receiptGoodsPlace']
                    salesOrder.receipt_goods_place = receipt_goods_place
            if 'consignee' in json2Dict:
                if isValid(json2Dict['consignee']):
                    consignee = json2Dict['consignee']
                    salesOrder.consignee = consignee
            if 'phone' in json2Dict:
                if isValid(json2Dict['phone']):
                    phone = json2Dict['phone']
                    salesOrder.phone = phone
            if 'fax' in json2Dict:
                if isValid(json2Dict['fax']):
                    fax = json2Dict['fax']
                    salesOrder.fax = fax
            if 'orderer' in json2Dict:
                if isValid(json2Dict['orderer']):
                    orderer = json2Dict['orderer']
                    salesOrder.orderer = orderer
            if 'advanceScale' in json2Dict:
                if isValid(json2Dict['advanceScale']):
                    advance_scale = atof(json2Dict['advanceScale'])
                    salesOrder.advance_scale = advance_scale
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                    salesOrder.originator = originator
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                    salesOrder.summary = summary
            if 'branch' in json2Dict:
                if isValid(json2Dict['branch']):
                    branch = json2Dict['branch']
                    salesOrder.branch = branch
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                    salesOrder.state = state
            if 'isSpecimen' in json2Dict:
                if isValid(json2Dict['isSpecimen']):
                    is_specimen = int(json2Dict['isSpecimen'])
                    salesOrder.is_specimen = is_specimen
            if 'supctoID' in json2Dict:
                if isValid(json2Dict['supctoID']):
                    supcto_id = int(json2Dict['supctoID'])
                    salesOrder.supcto_id = supcto_id
            if 'shippingModeID' in json2Dict:
                if isValid(json2Dict['shippingModeID']):
                    shipping_mode_id = int(json2Dict['shippingModeID'])
                    salesOrder.shipping_mode_id = shipping_mode_id
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                    salesOrder.person_id = person_id
            if 'salesPlanOrderID' in json2Dict:
                if isValid(json2Dict['salesPlanOrderID']):
                    sales_plan_order_id = int(json2Dict['salesPlanOrderID'])
                    salesOrder.sales_plan_order_id = sales_plan_order_id
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                    salesOrder.print_num = print_num
            if 'isShow' in json2Dict:
                if isValid(json2Dict['isShow']):
                    is_show = int(json2Dict['isShow'])
                    salesOrder.is_show = is_show
            if 'isVerification' in json2Dict:
                if isValid(json2Dict['isVerification']):
                    is_verification = json2Dict['isVerification']
                    salesOrder.is_verification = is_verification
            if 'missOrderID' in json2Dict:
                if isValid(json2Dict['missOrderID']):
                    miss_order_id = json2Dict['missOrderID']
                    salesOrder.miss_order_id = miss_order_id
            if 'activityID' in json2Dict:
                if isValid(json2Dict['activityID']):
                    activity_id = json2Dict['activityID']
                    salesOrder.activity_id = activity_id
            if 'isAppOrder' in json2Dict:
                if isValid(json2Dict['isAppOrder']):
                    is_app_order = json2Dict['isAppOrder']
                    salesOrder.is_app_order = is_app_order
            if 'isReturnGoods' in json2Dict:
                if isValid(json2Dict['isReturnGoods']):
                    is_return_goods = int(json2Dict['isReturnGoods'])
                    salesOrder.is_return_goods = is_return_goods
            if 'appOrderIdentifier' in json2Dict:
                if isValid(json2Dict['appOrderIdentifier']):
                    app_order_identifier = json2Dict['appOrderIdentifier']
                    salesOrder.app_order_identifier = app_order_identifier
            if 'appSendTime' in json2Dict:
                if isValid(json2Dict['appSendTime']):
                    app_send_time = json2Dict['appSendTime']
                    salesOrder.app_send_time = app_send_time
            if 'isCreateStockOrder' in json2Dict:
                if isValid(json2Dict['isCreateStockOrder']):
                    is_create_stock_order = json2Dict['isCreateStockOrder']
                    salesOrder.is_create_stock_order = is_create_stock_order
            salesOrder.save()
            if 'salesOrderCommodities' in json2Dict:
                salesOrderCommodities = json2Dict['salesOrderCommodities']
                for salesOrderCommodity in salesOrderCommodities:
                    if 'salesOrderCommodityID' in salesOrderCommodity:
                        salesOrderCommodityID = int(salesOrderCommodity['salesOrderCommodityID'])
                        salesOrderCommodities = SalesOrderCommodity.objects.filter(id=salesOrderCommodityID)
                        if len(salesOrderCommodities) > 0:
                            soc = salesOrderCommodities[0]
                        else:
                            salesNormalUpdate = setStatus(300, {})
                            return HttpResponse(json.dumps(salesNormalUpdate), content_type='application/json')
                    else:
                        continue
                    if 'commoditySpecificationID' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['commoditySpecificationID']):
                            commodity_specification_id = int(salesOrderCommodity['commoditySpecificationID'])
                            soc.commodity_specification_id = commodity_specification_id
                    if 'deliverGoodsMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['deliverGoodsMoney']):
                            deliver_goods_money = atof(salesOrderCommodity['deliverGoodsMoney'])
                            soc.deliver_goods_money = deliver_goods_money
                    if 'deliverGoodsNum' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['deliverGoodsNum']):
                            deliver_goods_num = int(salesOrderCommodity['deliverGoodsNum'])
                            soc.deliver_goods_num = deliver_goods_num
                    if 'returnGoodsNum' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['returnGoodsNum']):
                            return_goods_num = int(salesOrderCommodity['returnGoodsNum'])
                            soc.return_goods_num = return_goods_num
                    if 'receivingGoodsMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['receivingGoodsMoney']):
                            receiving_goods_money = atof(salesOrderCommodity['receivingGoodsMoney'])
                            soc.receiving_goods_money = receiving_goods_money
                    if 'receivingGoodsNum' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['receivingGoodsNum']):
                            receiving_goods_num = int(salesOrderCommodity['receivingGoodsNum'])
                            soc.receiving_goods_num = receiving_goods_num
                    if 'damageNum' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['damageNum']):
                            damage_num = int(salesOrderCommodity['damageNum'])
                            soc.damage_num = damage_num
                    if 'damageMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['damageMoney']):
                            damage_money = atof(salesOrderCommodity['damageMoney'])
                            soc.damage_money = damage_money
                    if 'discount' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['discount']):
                            discount = atof(salesOrderCommodity['discount'])
                            soc.discount = discount
                    if 'unitPrice' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['unitPrice']):
                            unit_price = atof(salesOrderCommodity['unitPrice'])
                            soc.unit_price = unit_price
                    if 'taxesMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['taxesMoney']):
                            taxes_money = atof(salesOrderCommodity['taxesMoney'])
                            soc.taxes_money = taxes_money
                    if 'taxes' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['taxes']):
                            taxes = atof(salesOrderCommodity['taxes'])
                            soc.taxes = taxes
                    if 'batchNumber' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['batchNumber']):
                            batch_number = salesOrderCommodity['batchNumber']
                            soc.batch_number = batch_number
                    if 'remark' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['remark']):
                            remark = salesOrderCommodity['remark']
                            soc.remark = remark
                    if 'isSpecialOffer' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['isSpecialOffer']):
                            is_special_offer = int(salesOrderCommodity['isSpecialOffer'])
                            soc.is_special_offer = is_special_offer
                    if 'warehouseID' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['warehouseID']):
                            warehouse_id = int(salesOrderCommodity['warehouseID'])
                            soc.warehouse_id = warehouse_id
                    if 'appAmountMoney' in salesOrderCommodity:
                        if isValid(salesOrderCommodity['appAmountMoney']):
                            app_amountMoney = atof(salesOrderCommodity['appAmountMoney'])
                            soc.app_amountMoney = app_amountMoney
                    soc.save()
            salesOrderJSON = getSalesOrder(salesOrder)
            salesNormalUpdate = setStatus(200, salesOrderJSON)
        else:
            return notTokenExpired()
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        salesNormalUpdate = setStatus(500, traceback.format_exc())
    return HttpResponse(json.dumps(salesNormalUpdate), content_type='application/json')


def salesNormalSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    identifier = request.GET['identifier']
                    salesOrders = SalesOrder.objects.filter(identifier=identifier)
                    if len(salesOrders) > 0:
                        salesOrder = salesOrders[0]
                        salesNormalSelect = getSalesOrder(salesOrder)
                    else:
                        salesPlanSelect = setStatus(300,{} )
                        return HttpResponse(json.dumps(salesPlanSelect), content_type='application/json')
                else:
                    condition = {}
                    selectType = {}
                    supctoMessage = {}
                    if 'classificationID' in request.GET and isValid(request.GET['classificationID']):
                        supctoMessage['classification_id'] = request.GET['classificationID']
                    if 'provinceCode' in request.GET and isValid(request.GET['provinceCode']):
                        supctoMessage['province_code'] = request.GET['provinceCode']
                    if 'cityCode' in request.GET and isValid(request.GET['cityCode']):
                        supctoMessage['city_code'] = request.GET['cityCode']
                    if 'areaCode' in request.GET and isValid(request.GET['areaCode']):
                        supctoMessage['area_code'] = request.GET['areaCode']
                    if 'supctoName' in request.GET and isValid(request.GET['supctoName']):
                        supctoMessage['name'] = request.GET['supctoName']
                    if 'commodityID' in request.GET and isValid(request.GET['commodityID']):
                        commodityID = int(request.GET['commodityID'])
                    else:
                        commodityID = 0
                    if 'isSpecimen' in request.GET and isValid(request.GET['isSpecimen']):
                        condition['is_specimen'] = request.GET['isSpecimen']
                    if 'state' in request.GET and isValid(request.GET['state']):
                        condition['state'] = int(request.GET['state'])
                    if 'isAppOrder' in request.GET and isValid(request.GET['isAppOrder']):
                        condition['is_app_order'] = int(request.GET['isAppOrder'])
                    if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                        queryTime = request.GET['queryTime']
                        timeFrom = queryTime.split('~')[0].strip()
                        timeTo = queryTime.split('~')[1].strip()
                        selectType['timeFrom'] = timeFrom + ' 00:00:00'
                        selectType['timeTo'] = timeTo + ' 23:59:59'
                    salesNormalSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType,supctoMessage, commodityID)
            else:
                salesNormalSelect = paging(request, ONE_PAGE_OF_DATA, None, None,None, 0)
        else:
            return notTokenExpired()
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        salesNormalSelect = setStatus(500, traceback.format_exc())
    return HttpResponse(json.dumps(salesNormalSelect), content_type='application/json')


def paging(request, ONE_PAGE_OF_DATA, condition, selectType,supctoMessage, commodityID):
    logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    allPage = 1
    if condition == None:
        basicsCount = SalesOrder.objects.all().count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            salesOrderIDs = []
            socs = SalesOrderCommodity.objects.filter(commodity_specification_id=commodityID)
            for soc in socs:
                salesOrderIDs.append(soc.sales_order_id)
            supctos = Supcto.objects.filter(**supctoMessage)
            supctoIDs = []
            for supcto in supctos:
                supctoIDs.append(supcto.id)
            basicsCount = SalesOrder.objects.filter(Q(id__in=salesOrderIDs) & Q(supcto_id__in=supctoIDs) &
                Q(**condition) & Q(create_time__gte=timeFrom) & Q(create_time__lte=timeTo)).count()
        else:
            basicsCount = SalesOrder.objects.filter(**condition).count()
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
        basicObjs = SalesOrder.objects.all()[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            salesOrderIDs = []
            socs = SalesOrderCommodity.objects.filter(commodity_specification_id=commodityID)
            for soc in socs:
                salesOrderIDs.append(soc.sales_order_id)
            supctos = Supcto.objects.filter(**supctoMessage)
            supctoIDs = []
            for supcto in supctos:
                supctoIDs.append(supcto.id)
            basicObjs = SalesOrder.objects.filter(Q(id__in=salesOrderIDs) & Q(supcto_id__in=supctoIDs) &
                    Q(**condition) & Q(create_time__gte=timeFrom) & Q(create_time__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = SalesOrder.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getSalesOrder(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect
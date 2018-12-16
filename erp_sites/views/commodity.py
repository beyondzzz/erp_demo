#!usr/bin/python#coding=utf-8

import json,sys,time,base64
from string import upper, atof, atoi
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,getSpecification,getCommodity,isValid
import traceback
from erp_sites.models import Commodity,CommoditySpecification,Inventory,Unit,Person,Classification,Supcto,Permission
from django.db.models import Q

logRecord = basic_log.Logger('record')
reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def commodityInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            if 'classificationID' in json2Dict:
                if isValid(json2Dict['classificationID']):
                    classification_id = int(json2Dict['classificationID'])
                else:
                    classification_id = 0
            else:
                classification_id = 0
            if 'name' in json2Dict:
                if isValid(json2Dict['name']):
                    name = json2Dict['name']
                else:
                    name = None
            else:
                name = None
            if 'brand' in json2Dict:
                if isValid(json2Dict['brand']):
                    brand = json2Dict['brand']
                else:
                    brand = None
            else:
                brand = None
            if 'zeroStock' in json2Dict:
                if isValid(json2Dict['zeroStock']):
                    zero_stock = int(json2Dict['zeroStock'])
                else:
                    zero_stock = 0
            else:
                zero_stock = 0
            if 'shoutName' in json2Dict:
                if isValid(json2Dict['shoutName']):
                    shout_name = json2Dict['shoutName']
                else:
                    shout_name = 0
            else:
                shout_name = 0
            if 'mnemonicCode' in json2Dict:
                if isValid(json2Dict['mnemonicCode']):
                    mnemonic_code = json2Dict['mnemonicCode']
                else:
                    mnemonic_code = None
            else:
                mnemonic_code = None
            if 'basicsInformation' in json2Dict:
                if isValid(json2Dict['basicsInformation']):
                    basics_information = json2Dict['basicsInformation']
                else:
                    basics_information = None
            else:
                basics_information = None
            if 'attribute' in json2Dict:
                if isValid(json2Dict['attribute']):
                    attribute = json2Dict['attribute']
                else:
                    attribute = None
            else:
                attribute = None
            if 'supctoID' in json2Dict:
                if isValid(json2Dict['supctoID']):
                    supcto_id = int(json2Dict['supctoID'])
                else:
                    attribute = 0
            else:
                attribute = 0
            if 'taxes' in json2Dict:
                if isValid(json2Dict['taxes']):
                    taxes = atof(json2Dict['taxes'])
                else:
                    taxes = 0
            else:
                taxes = 0
            if 'isAssemble' in json2Dict:
                if isValid(json2Dict['isAssemble']):
                    is_assemble = int(json2Dict['isAssemble'])
                else:
                    is_assemble = 2
            else:
                is_assemble = 2
            if 'isPresell' in json2Dict:
                if isValid(json2Dict['isPresell']):
                    is_presell = int(json2Dict['isPresell'])
                else:
                    is_presell = 0
            else:
                is_presell = 0
            if 'tempTaxes' in json2Dict:
                if isValid(json2Dict['tempTaxes']):
                    temp_taxes = atof(json2Dict['tempTaxes'])
                else:
                    temp_taxes = 0
            else:
                temp_taxes = 0
            identifier = 'COM-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '-'
            commodity = Commodity(None,classification_id,name,brand,zero_stock,shout_name,mnemonic_code,basics_information,attribute,identifier,supcto_id,taxes,is_assemble,is_presell,temp_taxes)
            commodity.save()
            commodity.identifier = identifier + str(commodity.id)
            commodity.save()
            if 'commoditySpecifictions' in json2Dict:
                commoditySpecifictions = json2Dict['commoditySpecifictions']
                insertSpecification(commoditySpecifictions,commodity.id)
            commodityJSON = getCommodity(commodity)
            commodityInsert = setStatus(200,commodityJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        commodityInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(commodityInsert), content_type='application/json')


def commodityUpdate(request):
    try:
        if isTokenExpired(request):
            commodityUpdate = {}
            json2Dict = json.loads(request.body)
            identifier = json2Dict['commodityID']
            commoditys = Commodity.objects.filter(id=identifier)
            if len(commoditys) > 0:
                commodity = commoditys[0]
            else:
                commodityUpdate = setStatus(301, {})
                return HttpResponse(json.dumps(commodityUpdate), content_type='application/json')
            if 'classificationID' in json2Dict:
                if isValid(json2Dict['classificationID']):
                    classification_id = int(json2Dict['classificationID'])
                    commodity.classification_id = classification_id
            if 'name' in json2Dict:
                if isValid(json2Dict['name']):
                    name = json2Dict['name']
                    commodity.name = name
            if 'brand' in json2Dict:
                if isValid(json2Dict['brand']):
                    brand = json2Dict['brand']
                    commodity.brand = brand
            if 'zeroStock' in json2Dict:
                if isValid(json2Dict['zeroStock']):
                    zero_stock = int(json2Dict['zeroStock'])
                    commodity.zero_stock = zero_stock
            if 'shoutName' in json2Dict:
                if isValid(json2Dict['shoutName']):
                    shout_name = json2Dict['shoutName']
                    commodity.shout_name = shout_name
            if 'mnemonicCode' in json2Dict:
                if isValid(json2Dict['mnemonicCode']):
                    mnemonic_code = json2Dict['mnemonicCode']
                    commodity.mnemonic_code = mnemonic_code
            if 'basicsInformation' in json2Dict:
                if isValid(json2Dict['basicsInformation']):
                    basics_information = json2Dict['basicsInformation']
                    commodity.basics_information = basics_information
            if 'attribute' in json2Dict:
                if isValid(json2Dict['attribute']):
                    attribute = json2Dict['attribute']
                    commodity.attribute = attribute
            if 'supctoID' in json2Dict:
                if isValid(json2Dict['supctoID']):
                    supcto_id = int(json2Dict['supctoID'])
                    commodity.supcto_id = supcto_id
            if 'taxes' in json2Dict:
                if isValid(json2Dict['taxes']):
                    taxes = atof(json2Dict['taxes'])
                    commodity.taxes = taxes
            if 'isAssemble' in json2Dict:
                if isValid(json2Dict['isAssemble']):
                    is_assemble = int(json2Dict['isAssemble'])
                    commodity.is_assemble = is_assemble
            if 'isPresell' in json2Dict:
                if isValid(json2Dict['isPresell']):
                    is_presell = int(json2Dict['isPresell'])
                    commodity.is_presell = is_presell
            if 'tempTaxes' in json2Dict:
                if isValid(json2Dict['tempTaxes']):
                    temp_taxes = atof(json2Dict['tempTaxes'])
                    commodity.temp_taxes = temp_taxes
            commodity.save()
            if 'commoditySpecifictions' in json2Dict:
                commoditySpecifictions = json2Dict['commoditySpecifictions']
                if updateSpecification(commoditySpecifictions):
                    commodityJSON = getCommodity(commodity)
                    commodityUpdate = setStatus(200,commodityJSON)
                else:
                    commodityUpdate = setStatus(302, {})
            commoditys = Commodity.objects.filter(id=identifier)
            if len(commoditys) > 0:
                commodity = commoditys[0]
                commodityJSON = getCommodity(commodity)
                singleCommoditySelect = setStatus(200, commodityJSON)
            else:
                singleCommoditySelect = setStatus(300, {})
            return HttpResponse(json.dumps(singleCommoditySelect), content_type='application/json')
            '''
            specifications = CommoditySpecification.objects.filter(id=commoditySpecicicationID)
            if len(specifications) > 0:
                specification = specifications[0]
                specificationJSON = getSpecification(specification)
                singleCommoditySelect = setStatus(200,specificationJSON)
            else:
                singleCommoditySelect = setStatus(300,{})
                return HttpResponse(json.dumps(singleCommoditySelect), content_type='application/json')
            '''

        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        commodityUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(commodityUpdate), content_type='application/json')


def multiCommoditySelect(request):
    try:
        if isTokenExpired(request):
            #logRecord = basic_log.Logger('record')
            multiCommoditySelect = {}
            if len(request.GET) > 0:
                condition = {}
                selectType = {}
                specificationDic = {}
                if 'operatorIdentifier' in request.GET and isValid(request.GET['operatorIdentifier']):
                        specificationDic['operator_identifier'] = request.GET['operatorIdentifier']
                if 'state' in request.GET and isValid(request.GET['state']):
                        specificationDic['state'] = int(request.GET['state'])
                if 'classificationID' in request.GET and isValid(request.GET['classificationID']):
                        condition['classificationID'] = int(request.GET['classificationID'])
                if 'supctoID' in request.GET and isValid(request.GET['supctoID']):
                        condition['supcto_id'] = int(request.GET['supctoID'])
                if 'name' in request.GET and isValid(request.GET['name']):
                        condition['name'] = request.GET['name']
                if 'queryTime' in request.GET:
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                multiCommoditySelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType, specificationDic)
            else:
                multiCommoditySelect = paging(request, ONE_PAGE_OF_DATA, None, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        multiCommoditySelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(multiCommoditySelect), content_type='application/json')


def singleCommoditySelect(request):
    try:
        if isTokenExpired(request):
            singleCommoditySelect = {}
            commoditySpecicicationID = request.GET['commoditySpecicicationID']
            specifications = CommoditySpecification.objects.filter(id=commoditySpecicicationID)
            #logRecord.log("specification value: " + str(specifications))
            if len(specifications) > 0:
                specification = specifications[0]
                specificationJSON = getSpecification(specification)
                singleCommoditySelect = setStatus(200,specificationJSON)
            else:
                singleCommoditySelect = setStatus(300,{})
                return HttpResponse(json.dumps(singleCommoditySelect), content_type='application/json')
            '''
            commodityID = int(request.GET['commodityID'])
            commoditys = Commodity.objects.filter(id=commodityID)
            if len(commoditys) > 0:
                commodity = commoditys[0]
                commodityJSON = getCommodity(commodity)
                singleCommoditySelect = setStatus(200, commodityJSON)
            else:
                singleCommoditySelect = setStatus(300, {})
                return HttpResponse(json.dumps(singleCommoditySelect), content_type='application/json')
           ''' 
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        singleCommoditySelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(singleCommoditySelect), content_type='application/json')


def insertSpecification(commoditySpecifictions,commodity_id):
    for commoditySpecifiction in commoditySpecifictions:
        operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        specification_identifier = 'COM_SPE-' + operator_time[0:10] + '-'
        if 'specificationName' in commoditySpecifiction:
            if isValid(commoditySpecifiction['specificationName']):
                specification_name = commoditySpecifiction['specificationName']
            else:
                specification_name = None
        else:
            specification_name = None
        if 'qualityPeriod' in commoditySpecifiction:
            if isValid(commoditySpecifiction['qualityPeriod']):
                quality_period = int(commoditySpecifiction['qualityPeriod'])
            else:
                quality_period = 0
        else:
            quality_period = 0
        if 'qualityPeriodUnit' in commoditySpecifiction:
            if isValid(commoditySpecifiction['qualityPeriodUnit']):
                quality_period_unit = commoditySpecifiction['qualityPeriodUnit']
            else:
                quality_period_unit = None
        else:
            quality_period_unit = None
        if 'miniOrderQuantity' in commoditySpecifiction:
            if isValid(commoditySpecifiction['miniOrderQuantity']):
                mini_order_quantity = int(commoditySpecifiction['miniOrderQuantity'])
            else:
                mini_order_quantity = 0
        else:
            mini_order_quantity = 0
        if 'addOrderQuantity' in commoditySpecifiction:
            if isValid(commoditySpecifiction['addOrderQuantity']):
                add_order_quantity = int(commoditySpecifiction['addOrderQuantity'])
            else:
                add_order_quantity = 0
        else:
            add_order_quantity = 0
        if 'packagingSize' in commoditySpecifiction:
            if isValid(commoditySpecifiction['packagingSize']):
                packaging_size = commoditySpecifiction['packagingSize']
            else:
                packaging_size = None
        else:
            packaging_size = None
        is_delete = 0
        if 'warningNumber' in commoditySpecifiction:
            if isValid(commoditySpecifiction['warningNumber']):
                warning_number = int(commoditySpecifiction['warningNumber'])
            warning_number = 0
        else:
            warning_number = 0
        if 'weight' in commoditySpecifiction:
            if isValid(commoditySpecifiction['weight']):
                weight = atof(commoditySpecifiction['weight'])
            else:
                weight = 0
        else:
            weight = 0
        if 'operatorIdentifier' in commoditySpecifiction:
            if isValid(commoditySpecifiction['operatorIdentifier']):
                operator_identifier = commoditySpecifiction['operatorIdentifier']
            else:
                operator_identifier = None
        else:
            operator_identifier = None
        if 'state' in commoditySpecifiction:
            if isValid(commoditySpecifiction['state']):
                state = int(commoditySpecifiction['state'])
            else:
                state = 0
        else:
            state = 0
        if 'tempMiniOrderQuantity' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempMiniOrderQuantity']):
                temp_mini_order_quantity = int(commoditySpecifiction['tempMiniOrderQuantity'])
            else:
                temp_mini_order_quantity = 0
        else:
            temp_mini_order_quantity = 0
        if 'tempAddOrderQuantity' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempAddOrderQuantity']):
                temp_add_order_quantity = int(commoditySpecifiction['tempAddOrderQuantity'])
            else:
                temp_add_order_quantity = 0
        else:
            temp_add_order_quantity = 0
        if 'tempWarningNumber' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempWarningNumber']):
                temp_warning_number = int(commoditySpecifiction['tempWarningNumber'])
            else:
                temp_warning_number = 0
        else:
            temp_warning_number = 0
        if 'tempWarehouseID' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempWarehouseID']):
                temp_warehouse_id = int(commoditySpecifiction['tempWarehouseID'])
            else:
                temp_warehouse_id = 0
        else:
            temp_warehouse_id = 0
        if 'tempMaxInventory' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempMaxInventory']):
                temp_max_inventory = int(commoditySpecifiction['tempMaxInventory'])
            else:
                temp_max_inventory = 0
        else:
            temp_max_inventory = 0
        if 'tempMiniInventory' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempMiniInventory']):
                temp_mini_inventory = int(commoditySpecifiction['tempMiniInventory'])
            else:
                temp_mini_inventory = 0
        else:
            temp_mini_inventory = 0
        if 'tempInventory' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempInventory']):
                temp_inventory = int(commoditySpecifiction['tempInventory'])
            else:
                temp_inventory = 0
        else:
            temp_inventory = 0
        if 'tempState' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempState']):
                temp_state = int(commoditySpecifiction['tempState'])
            else:
                temp_state = 0
        else:
            temp_state = 0
        specification = CommoditySpecification(None, specification_identifier, specification_name, commodity_id,
                                              quality_period, quality_period_unit, mini_order_quantity,
                                              add_order_quantity, packaging_size, is_delete, warning_number, weight,
                                              operator_identifier, operator_time, state, temp_mini_order_quantity,
                                              temp_add_order_quantity, temp_warning_number, temp_warehouse_id,
                                              temp_max_inventory, temp_mini_inventory, temp_inventory, temp_state)
        specification.save()
        specification.specification_identifier = specification_identifier + str(specification.id)
        specification.save()
        if 'inventories' in commoditySpecifiction:
            inventories = commoditySpecifiction['inventories']
            insertInventory(inventories,specification.id)
        if 'units' in commoditySpecifiction:
            units = commoditySpecifiction['units']
            insertUnit(units,specification.id)
    return True


def insertUnit(units,specification_id):
    for unit in units:
        if 'name' in unit:
            if isValid(unit['name']):
                name = unit['name']
            else:
                name = None
        else:
            name = None
        if 'ratioDenominator' in unit:
            if isValid(unit['ratioDenominator']):
                ratio_denominator = int(unit['ratioDenominator'])
            else:
                ratio_denominator = 0
        else:
            ratio_denominator = 0
        if 'ratioMolecular' in unit:
            if isValid(unit['ratioMolecular']):
                ratio_molecular = int(unit['ratioMolecular'])
            else:
                ratio_molecular = 0
        else:
            ratio_molecular = 0
        if 'purchasePrice' in unit:
            if isValid(unit['purchasePrice']):
                purchase_price = atof(unit['purchasePrice'])
            else:
                purchase_price = 0
        else:
            purchase_price = 0
        if 'commonlyPrice' in unit:
            if isValid(unit['commonlyPrice']):
                commonly_price = atof(unit['commonlyPrice'])
            else:
                commonly_price = 0
        else:
            commonly_price = 0
        if 'miniPrice' in unit:
            if isValid(unit['miniPrice']):
                mini_price = atof(unit['miniPrice'])
            else:
                mini_price = 0
        else:
            mini_price = 0
        if 'barCode' in unit:
            if isValid(unit['barCode']):
                bar_code = unit['barCode']
            else:
                bar_code = None
        else:
            bar_code = None
        if 'salesUnit' in unit:
            if isValid(unit['salesUnit']):
                sales_unit = unit['salesUnit']
            else:
                sales_unit = None
        else:
            sales_unit = None
        if 'basicUnit' in unit:
            if isValid(unit['basicUnit']):
                basic_unit = int(unit['basicUnit'])
            else:
                basic_unit = 0
        else:
            basic_unit = 0
        if 'warehouseUnit' in unit:
            if isValid(unit['warehouseUnit']):
                warehouse_unit = unit['warehouseUnit']
            else:
                warehouse_unit = None
        else:
            warehouse_unit = None
        if 'purchasingUnit' in unit:
            if isValid(unit['purchasingUnit']):
                purchasing_unit = unit['purchasingUnit']
            else:
                purchasing_unit = None
        else:
            purchasing_unit = None
        if 'miniPurchasing' in unit:
            if isValid(unit['miniPurchasing']):
                mini_purchasing = int(unit['miniPurchasing'])
            else:
                mini_purchasing = 0
        else:
            mini_purchasing = 0
        if 'tempCommonlyPrice' in unit:
            if isValid(unit['tempCommonlyPrice']):
                temp_commonly_price = atof(unit['tempCommonlyPrice'])
            else:
                temp_commonly_price = 0
        else:
            temp_commonly_price = 0
        unit = Unit(None, name, specification_id, ratio_denominator, ratio_molecular, purchase_price,
                    commonly_price, mini_price, bar_code, sales_unit, basic_unit, warehouse_unit,
                    purchasing_unit, mini_purchasing, temp_commonly_price)
        unit.save()
    return True


def insertInventory(inventories,specification_id):
    for inventoryDict in inventories:
        if 'warehouseID' in inventoryDict:
            if isValid(inventoryDict['warehouseID']):
                warehouse_id = int(inventoryDict['warehouseID'])
            else:
                warehouse_id = 0
        else:
            warehouse_id = 0
        if 'inventory' in inventoryDict:
            if isValid(inventoryDict['inventory']):
                inventory = int(inventoryDict['inventory'])
            else:
                inventory = 0
        else:
            inventory = 0
        if 'presellInventory' in inventoryDict:
            if isValid(inventoryDict['presellInventory']):
                presell_inventory = int(inventoryDict['presellInventory'])
            else:
                presell_inventory = 0
        else:
            presell_inventory = 0
        if 'occupiedInventory' in inventoryDict:
            if isValid(inventoryDict['occupiedInventory']):
                occupied_inventory = int(inventoryDict['occupiedInventory'])
            else:
                occupied_inventory = 0
        else:
            occupied_inventory = 0
        if 'maxInventory' in inventoryDict:
            if isValid(inventoryDict['maxInventory']):
                max_inventory = int(inventoryDict['maxInventory'])
            else:
                max_inventory = 0
        else:
            max_inventory = 0
        if 'miniInventory' in inventoryDict:
            if isValid(inventoryDict['miniInventory']):
                mini_inventory = int(inventoryDict['miniInventory'])
            else:
                mini_inventory = 0
        else:
            mini_inventory = 0
        if 'costPrice' in inventoryDict:
            if isValid(inventoryDict['costPrice']):
                cost_price = int(inventoryDict['costPrice'])
            else:
                cost_price = 0
        else:
            cost_price = 0
        if 'commodityNum' in inventoryDict:
            if isValid(inventoryDict['commodityNum']):
                commodity_num = int(inventoryDict['commodityNum'])
            else:
                commodity_num = 0
        else:
            commodity_num = 0
        if 'isCreateProcurePlan' in inventoryDict:
            if isValid(inventoryDict['isCreateProcurePlan']):
                is_create_procure_plan = int(inventoryDict['isCreateProcurePlan'])
            else:
                is_create_procure_plan = 0
        else:
            is_create_procure_plan = 0
        inventoryObj = Inventory(None, specification_id, warehouse_id, inventory, presell_inventory,
                              occupied_inventory, max_inventory, mini_inventory, cost_price, commodity_num,
                              is_create_procure_plan)
        inventoryObj.save()
    return True


def updateSpecification(commoditySpecifictions):
    for commoditySpecifiction in commoditySpecifictions:
        operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if 'specificationIdentifier' in commoditySpecifiction:
            specificationIdentifier = commoditySpecifiction['specificationIdentifier']
            specifications = CommoditySpecification.objects.filter(specification_identifier=specificationIdentifier)
            if len(specifications) > 0:
                specification = specifications[0]
            else:
                return False
        else:
            continue
        if 'specificationName' in commoditySpecifiction:
            if isValid(commoditySpecifiction['specificationName']):
                specification_name = commoditySpecifiction['specificationName']
                specification.specification_name = specification_name
        if 'qualityPeriod' in commoditySpecifiction:
            if isValid(commoditySpecifiction['qualityPeriod']):
                quality_period = int(commoditySpecifiction['qualityPeriod'])
                specification.quality_period = quality_period
        if 'isDelete' in commoditySpecifiction:
            if isValid(commoditySpecifiction['isDelete']):
                is_delete = int(commoditySpecifiction['isDelete'])
                specification.is_delete = is_delete
        if 'qualityPeriodUnit' in commoditySpecifiction:
            if isValid(commoditySpecifiction['qualityPeriodUnit']):
                quality_period_unit = commoditySpecifiction['qualityPeriodUnit']
                specification.quality_period_unit = quality_period_unit
        if 'miniOrderQuantity' in commoditySpecifiction:
            if isValid(commoditySpecifiction['miniOrderQuantity']):
                mini_order_quantity = int(commoditySpecifiction['miniOrderQuantity'])
                specification.mini_order_quantity = mini_order_quantity
        if 'addOrderQuantity' in commoditySpecifiction:
            if isValid(commoditySpecifiction['addOrderQuantity']):
                add_order_quantity = int(commoditySpecifiction['addOrderQuantity'])
                specification.add_order_quantity = add_order_quantity
        if 'packagingSize' in commoditySpecifiction:
            if isValid(commoditySpecifiction['packagingSize']):
                packaging_size = commoditySpecifiction['packagingSize']
                specification.packaging_size = packaging_size
        if 'warning_number' in commoditySpecifiction:
            if isValid(commoditySpecifiction['warning_number']):
                warning_number = int(commoditySpecifiction['warning_number'])
                specification.warning_number = warning_number
        if 'weight' in commoditySpecifiction:
            if isValid(commoditySpecifiction['weight']):
                weight = atof(commoditySpecifiction['weight'])
                specification.weight = weight
        if 'operatorIdentifier' in commoditySpecifiction:
            if isValid(commoditySpecifiction['operatorIdentifier']):
                operator_identifier = commoditySpecifiction['operatorIdentifier']
                specification.operator_identifier = operator_identifier
        if 'state' in commoditySpecifiction:
            if isValid(commoditySpecifiction['state']):
                state = int(commoditySpecifiction['state'])
                specification.state = state
        if 'tempMiniOrderQuantity' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempMiniOrderQuantity']):
                temp_mini_order_quantity = int(commoditySpecifiction['tempMiniOrderQuantity'])
                specification.temp_mini_order_quantity = temp_mini_order_quantity
        if 'tempAddOrderQuantity' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempAddOrderQuantity']):
                temp_add_order_quantity = int(commoditySpecifiction['tempAddOrderQuantity'])
                specification.temp_add_order_quantity = temp_add_order_quantity
        if 'tempWarningNumber' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempWarningNumber']):
                temp_warning_number = int(commoditySpecifiction['tempWarningNumber'])
                specification.temp_warning_number = temp_warning_number
        if 'tempWarehouseID' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempWarehouseID']):
                temp_warehouse_id = int(commoditySpecifiction['tempWarehouseID'])
                specification.temp_warehouse_id = temp_warehouse_id
        if 'tempMaxInventory' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempMaxInventory']):
                temp_max_inventory = int(commoditySpecifiction['tempMaxInventory'])
                specification.temp_max_inventory = temp_max_inventory
        if 'tempMiniInventory' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempMiniInventory']):
                temp_mini_inventory = int(commoditySpecifiction['tempMiniInventory'])
                specification.temp_mini_inventory = temp_mini_inventory
        if 'tempInventory' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempInventory']):
                temp_inventory = int(commoditySpecifiction['tempInventory'])
                specification.temp_inventory = temp_inventory
        if 'tempState' in commoditySpecifiction:
            if isValid(commoditySpecifiction['tempState']):
                temp_state = int(commoditySpecifiction['tempState'])
                specification.temp_state = temp_state
        specification.save()
        if 'inventories' in commoditySpecifiction:
            inventories = commoditySpecifiction['inventories']
            if updateInventory(inventories):
                pass
            else:
                return False
        if 'units' in commoditySpecifiction:
            units = commoditySpecifiction['units']
            if updateUnit(units):
                pass
            else:
                return False
    return True


def updateInventory(inventories):
    for inventoryDict in inventories:
        if 'inventoryID' in inventoryDict:
            inventory_id = inventoryDict['inventoryID']
            inventories = Inventory.objects.filter(inventory_id=inventory_id)
            if len(inventories) > 0:
                inventoryObj = inventories[0]
            else:
                return False
            if 'specificationID' in inventoryDict:
                if isValid(inventoryDict['specificationID']):
                    specification_id = int(inventoryDict['specificationID'])
                    inventoryObj.specification_id = specification_id
            if 'warehouseID' in inventoryDict:
                if isValid(inventoryDict['warehouseID']):
                    warehouse_id = int(inventoryDict['warehouseID'])
                    inventoryObj.warehouse_id = warehouse_id
            if 'inventory' in inventoryDict:
                if isValid(inventoryDict['inventory']):
                    inventory = int(inventoryDict['inventory'])
                    inventoryObj.inventory = inventory
            if 'presellInventory' in inventoryDict:
                if isValid(inventoryDict['presellInventory']):
                    presell_inventory = int(inventoryDict['presellInventory'])
                    inventoryObj.presell_inventory = presell_inventory
            if 'occupiedInventory' in inventoryDict:
                if isValid(inventoryDict['occupiedInventory']):
                    occupied_inventory = int(inventoryDict['occupiedInventory'])
                    inventoryObj.occupied_inventory = occupied_inventory
            if 'maxInventory' in inventoryDict:
                if isValid(inventoryDict['maxInventory']):
                    max_inventory = int(inventoryDict['maxInventory'])
                    inventoryObj.max_inventory = max_inventory
            if 'miniInventory' in inventoryDict:
                if isValid(inventoryDict['miniInventory']):
                    mini_inventory = int(inventoryDict['miniInventory'])
                    inventoryObj.mini_inventory = mini_inventory
            if 'costPrice' in inventoryDict:
                if isValid(inventoryDict['costPrice']):
                    cost_price = int(inventoryDict['costPrice'])
                    inventoryObj.cost_price = cost_price
            if 'commodityNum' in inventoryDict:
                if isValid(inventoryDict['commodityNum']):
                    commodity_num = int(inventoryDict['commodityNum'])
                    inventoryObj.commodity_num = commodity_num
            if 'isCreateProcurePlan' in inventoryDict:
                if isValid(inventoryDict['isCreateProcurePlan']):
                    is_create_procure_plan = int(inventoryDict['isCreateProcurePlan'])
                    inventoryObj.is_create_procure_plan = is_create_procure_plan
            inventoryObj.save()
        else:
            continue
    return True


def updateUnit(units):
    for unit in units:
        if 'unitID' in unit:
            unit_id = unit['unitID']
            unitObjs = Unit.objects.filter(id=unit_id)
            if len(unitObjs) > 0:
                unitObj = unitObjs[0]
            else:
                return False
            if 'specificationID' in unit:
                if isValid(unit['specificationID']):
                    specification_id = int(unit['specificationID'])
                    unitObj.specification_id = specification_id
            if 'name' in unit:
                if isValid(unit['name']):
                    name = unit['name']
                    unitObj.name = name
            if 'ratioDenominator' in unit:
                if isValid(unit['ratioDenominator']):
                    ratio_denominator = int(unit['ratioDenominator'])
                    unitObj.ratio_denominator = ratio_denominator
            if 'ratioMolecular' in unit:
                if isValid(unit['ratioMolecular']):
                    ratio_molecular = int(unit['ratioMolecular'])
                    unitObj.ratio_molecular = ratio_molecular
            if 'purchasePrice' in unit:
                if isValid(unit['purchasePrice']):
                    purchase_price = atof(unit['purchasePrice'])
                    unitObj.purchase_price = purchase_price
            if 'commonlyPrice' in unit:
                if isValid(unit['commonlyPrice']):
                    commonly_price = atof(unit['commonlyPrice'])
                    unitObj.commonly_price = commonly_price
            if 'miniPrice' in unit:
                if isValid(unit['miniPrice']):
                    mini_price = atof(unit['miniPrice'])
                    unitObj.mini_price = mini_price
            if 'barCode' in unit:
                if isValid(unit['barCode']):
                    bar_code = unit['barCode']
                    unitObj.bar_code = bar_code
            if 'salesUnit' in unit:
                if isValid(unit['salesUnit']):
                    sales_unit = unit['salesUnit']
                    unitObj.sales_unit = sales_unit
            if 'basicUnit' in unit:
                if isValid(unit['basicUnit']):
                    basic_unit = int(unit['basicUnit'])
                    unitObj.basic_unit = basic_unit
            if 'warehouseUnit' in unit:
                if isValid(unit['warehouseUnit']):
                    warehouse_unit = unit['warehouseUnit']
                    unitObj.warehouse_unit = warehouse_unit
            if 'purchasingUnit' in unit:
                if isValid(unit['purchasingUnit']):
                    purchasing_unit = unit['purchasingUnit']
                    unitObj.purchasing_unit = purchasing_unit
            if 'miniPurchasing' in unit:
                if isValid(unit['miniPurchasing']):
                    mini_purchasing = int(unit['miniPurchasing'])
                    unitObj.mini_purchasing = mini_purchasing
            if 'tempCommonlyPrice' in unit:
                if isValid(unit['tempCommonlyPrice']):
                    temp_commonly_price = atof(unit['tempCommonlyPrice'])
                    unitObj.temp_commonly_price = temp_commonly_price
            unitObj.save()
        else:
            continue
    return True


def paging(request, ONE_PAGE_OF_DATA, condition, selectType, specificationDic):
    #logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    allPage = 1
    if condition == None:
        basicsCount = CommoditySpecification.objects.all().count()
    else:
        if len(condition) > 0:
            if 'name' in condition:
                name = condition['name']
                condition.pop('name')
                commoditys = Commodity.objects.filter(Q(**condition) & Q(name__icontains=name))
                condition['name'] = name
            else:
                commoditys = Commodity.objects.filter(**condition)
            commodity_id_list = []
            for commodity in commoditys:
                commodity_id_list.append(commodity.id)
            if specificationDic == None:
                specificationDic = {}
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                if len(commodity_id_list) > 0:
                    basicsCount = CommoditySpecification.objects.filter(Q(commodity_id__in=commodity_id_list) & Q(**specificationDic) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
                else:
                    basicsCount = 0
            else:
                if len(commodity_id_list) > 0:
                    basicsCount = CommoditySpecification.objects.filter(Q(commodity_id__in=commodity_id_list) & Q(**specificationDic)).count()
                else:
                    basicsCount = 0
        else:
            if specificationDic == None:
                specificationDic = {}
            if 'timeFrom' in selectType and 'timeTo' in selectType:
                timeFrom = selectType['timeFrom']
                timeTo = selectType['timeTo']
                basicsCount = CommoditySpecification.objects.filter(Q(**specificationDic) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
            else:
                basicsCount = CommoditySpecification.objects.filter(**specificationDic).count()
    if basicsCount != 0:
        if basicsCount % ONE_PAGE_OF_DATA == 0:
            allPage = basicsCount / ONE_PAGE_OF_DATA
        else:
            allPage = basicsCount / ONE_PAGE_OF_DATA + 1
    else:
        allPage = 1
    if curPage == 1:
        if condition == None:
            basicObjs = CommoditySpecification.objects.all()[0:ONE_PAGE_OF_DATA]
        else:
            if len(condition) > 0:
                if 'name' in condition:
                    name = condition['name']
                    condition.pop('name')
                    commoditys = Commodity.objects.filter(Q(**condition) & Q(name__icontains=name))
                    condition['name'] = name
                else:
                    commoditys = Commodity.objects.filter(**condition)
                commodity_id_list = []
                for commodity in commoditys:
                    commodity_id_list.append(commodity.id)
                if specificationDic == None:
                    specificationDic = {}
                if 'timeFrom' in selectType and 'timeTo' in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    if len(commodity_id_list) > 0:
                        basicObjs = CommoditySpecification.objects.filter(Q(commodity_id__in=commodity_id_list) & Q(**specificationDic) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[0:ONE_PAGE_OF_DATA]
                    else:
                        basicObjs = []
                else:
                    if len(commodity_id_list) > 0:
                        basicObjs = CommoditySpecification.objects.filter(Q(commodity_id__in=commodity_id_list) & Q(**specificationDic))[0:ONE_PAGE_OF_DATA]
                    else:
                        basicObjs = []
            else:
                if specificationDic == None:
                    specificationDic = {}
                if 'timeFrom' in selectType and 'timeTo' in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    basicObjs = CommoditySpecification.objects.filter(Q(**specificationDic) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[0:ONE_PAGE_OF_DATA]
                else:
                    basicObjs = CommoditySpecification.objects.filter(**specificationDic)[0:ONE_PAGE_OF_DATA]
        for basicObj in basicObjs:
            basicJSON = getSpecification(basicObj)
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
            basicObjs = CommoditySpecification.objects.all()[startPos:endPos]
        else:
            if len(condition) > 0:
                if 'name' in condition:
                    name = condition['name']
                    condition.pop('name')
                    commoditys = Commodity.objects.filter(Q(**condition) & Q(name__icontains=name))
                    condition['name'] = name
                else:
                    commoditys = Commodity.objects.filter(**condition)
                commodity_id_list = []
                for commodity in commoditys:
                    commodity_id_list.append(commodity.id)
                if specificationDic == None:
                    specificationDic = {}
                if 'timeFrom' in selectType and 'timeTo' in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    if len(commodity_id_list) > 0:
                        basicObjs = CommoditySpecification.objects.filter(Q(commodity_id__in=commodity_id_list) & Q(**specificationDic) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
                    else:
                        basicObjs = []
                else:
                    if len(commodity_id_list) > 0:
                        basicObjs = CommoditySpecification.objects.filter(Q(commodity_id__in=commodity_id_list) & Q(**specificationDic))[startPos:endPos]
                    else:
                        basicObjs = []
            else:
                if specificationDic == None:
                    specificationDic = {}
                if 'timeFrom' in selectType and 'timeTo' in selectType:
                    timeFrom = selectType['timeFrom']
                    timeTo = selectType['timeTo']
                    basicObjs = CommoditySpecification.objects.filter(Q(**specificationDic) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
                else:
                    basicObjs = CommoditySpecification.objects.filter(**specificationDic)[startPos:endPos]
        for basicObj in basicObjs:
            basicJSON = getSpecification(basicObj)
            datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect

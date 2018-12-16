#!usr/bin/python#coding=utf-8
import traceback,json,os,stat,base64,time
from random import randint,choice
from PIL import Image,ImageDraw,ImageFont
from cStringIO import StringIO
from string import printable
from erp_sites import basic_log
from django.http import HttpResponse
from erp_sites.models import Classification,ProcureTable,ProcureTable,ProcureCommodity,Supcto,SupctoCommodity,Commodity,CommoditySpecification,Person,Permission,Inventory,Unit,Classification,SalesPlanOrder,SalesPlanOrderCommodity,SalesOrder,SalesOrderCommodity,AllotOrder,AllotOrderCommodity,TakeStockOrder,TakeStockOrderCommodity,PackageOrTeardownOrder,PackageOrTeardownOrderCommodity,Bills,BillsSub,Writeoff,WriteoffSub,BreakageOrder,BreakageOrderCommodity,PersonToken,Department,Goods,Log
from erp.settings import BASE_DIR


def writeLog(operateType,operateObject,operatorIdentifier):
    try:
        operate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        operate_type = operateType
        operate_object = operateObject
        operator_identifier = operatorIdentifier
        log = Log(None,operate_type,operate_object,operator_identifier,operate_time)
        log.save()
        return True
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        return False
    

def makeCaptcha():
    #设置选用的字体
    font_path = BASE_DIR + '/static/Arial.ttf'
    font_color = (randint(150, 200), randint(0, 150), randint(0, 150))
    line_color = (randint(0, 150), randint(0, 150), randint(150, 200))
    point_color = (randint(0, 150), randint(50, 150), randint(150, 200))

    #设置验证码的宽与高
    width, height = 100, 34
    image = Image.new('RGB',(width, height),(200,200,200))
    font = ImageFont.truetype(font_path,height - 10)
    draw = ImageDraw.Draw(image)

    #生成验证码
    text = "".join([choice(printable[:62]) for i in xrange(4)])
    font_width, font_height = font.getsize(text)
    #把验证码写在画布上
    draw.text((10, 10), text, font=font, fill=font_color)
    #绘制干扰线
    for i in xrange(0, 5):
        draw.line(((randint(0, width), randint(0, height)),
                   (randint(0, width), randint(0, height))),
                  fill=line_color, width=2)

    # 绘制点
    for i in xrange(randint(100, 1000)):
        draw.point((randint(0, width), randint(0, height)), fill=point_color)
    #输出
    out = StringIO()
    image.save(out, format='jpeg')
    content = out.getvalue()
    out.close()
    return text, content


#token是否合法
def isTokenExpired(request):
    try:
        logRecord = basic_log.Logger('record')
        tokenValue = request.META.get('HTTP_TOKEN', 'unkown')
        personTokens = PersonToken.objects.filter(token=tokenValue)
        if len(personTokens) > 0:
            personToken = personTokens[0]
            tokenEndTime = personToken.end_time#.strftime('%Y-%m-%d %H:%M:%S')
            tokenEndTime = str(tokenEndTime)
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if nowTime < tokenEndTime:
                return True
            else:
                return False
        else:
            return False
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        return False


def notTokenExpired():
    logErr = basic_log.Logger('error')
    #logErr.log('token is not valid')
    tokenErrors = {}
    tokenErrors['code'] = 500
    tokenErrors['data'] = 'tokenValue is incorrect or please login again'
    return HttpResponse(json.dumps(tokenErrors), content_type='application/json')

def setStatus(code,data):
    setStatus = {}
    if code == 200:
        message = 'success'
    elif code == 300:
        message = 'invalid'
    else:
        message = 'failed'
    setStatus['code'] = code
    setStatus['message'] = message
    setStatus['data'] = data
    return setStatus


def touchFile(docFile,modelType,fileType,uploadDate_str,fileName):
    try:
        doc = BASE_DIR + '/static/' + modelType + '/' + fileType + '/' + uploadDate_str + '_' + fileName
        filePath = '/static/' + modelType + '/' + fileType + '/' + uploadDate_str + '_' + fileName
        with open(doc, 'wb+') as destination:
            for chunk in docFile.chunks():
                destination.write(chunk)
        os.chmod(doc, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        return filePath
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        return None
    
    
def removeFile(filePath):
    if filePath != None:
        filePath = BASE_DIR + filePath
        if os.path.isfile(filePath):
            os.remove(filePath)
            return True
        else:
            return False
        
        
def isValid(param):
    if param != '' and param != ' ' and param != 'null' and param != 'undefined':
        return True
    else:
        return False
        
        
def getCommoditySpecification(commodity_specification_id):
    specificationJSON = {}
    specifications = CommoditySpecification.objects.filter(id=commodity_specification_id)
    if len(specifications) > 0:
        specification = specifications[0]
        specificationJSON['specificationId'] = specification.id
        specificationJSON['specificationIdentifier'] = specification.specification_identifier
        specificationJSON['specificationName'] = specification.specification_name
        specificationJSON['commodityId'] = specification.commodity_id
        specificationJSON['qualityPeriod'] = specification.quality_period
        specificationJSON['qualityPeriod_unit'] = specification.quality_period_unit
        specificationJSON['miniOrderQuantity'] = specification.mini_order_quantity
        specificationJSON['addOrderQuantity'] = specification.add_order_quantity
        specificationJSON['packagingSize'] = specification.packaging_size
        specificationJSON['isDelete'] = specification.is_delete
        specificationJSON['warningNumber'] = specification.warning_number
        specificationJSON['weight'] = specification.weight
        specificationJSON['operatorIdentifier'] = specification.operator_identifier
        specificationJSON['operatorTime'] = str(specification.operator_time)
        specificationJSON['state'] = specification.state
        specificationJSON['tempMiniOrderQuantity'] = specification.temp_mini_order_quantity
        specificationJSON['tempAddOrderQuantity'] = specification.temp_add_order_quantity
        specificationJSON['tempWarningNumber'] = specification.temp_warning_number
        specificationJSON['tempWarehouseId'] = specification.temp_warehouse_id
        specificationJSON['tempMaxInventory'] = specification.temp_max_inventory
        specificationJSON['tempMiniInventory'] = specification.temp_mini_inventory
        specificationJSON['tempInventory'] = specification.temp_inventory
        specificationJSON['tempState'] = specification.temp_state
        specificationJSON['inventories'] = getInventories(specification.id)
        specificationJSON['units'] = getUnits(specification.id)
        specificationJSON['person'] = getPerson(specification.operator_identifier)
        specificationJSON['commodity'] = getCommoditySelect(specification.commodity_id)
    return specificationJSON


def getCommoditySelect(commodity_id):
    commodityJSON = {}
    commodities = Commodity.objects.filter(id=commodity_id)
    if len(commodities) > 0:
        commodity = commodities[0]
        commodityJSON['commodityId'] = commodity.id
        commodityJSON['classificationId'] = commodity.classification_id
        commodityJSON['name'] = commodity.name
        commodityJSON['brand'] = commodity.brand
        commodityJSON['zeroStock'] = commodity.zero_stock
        commodityJSON['shoutName'] = commodity.shout_name
        commodityJSON['mnemonicCode'] = commodity.mnemonic_code
        commodityJSON['basicsInformation'] = commodity.basics_information
        commodityJSON['attribute'] = commodity.attribute
        commodityJSON['identifier'] = commodity.identifier
        commodityJSON['supctoId'] = commodity.supcto_id
        commodityJSON['taxes'] = commodity.taxes
        commodityJSON['isAssemble'] = commodity.is_assemble
        commodityJSON['isPresell'] = commodity.is_presell
        commodityJSON['tempTaxes'] = commodity.temp_taxes
        commodityJSON['classification'] = getClassification(commodity.classification_id)
        commodityJSON['supcto'] = getSupcto(commodity.supcto_id)
    return commodityJSON


def getClassification(classification_id):
    classificationJSON = {}
    classifications = Classification.objects.filter(id=classification_id)
    if len(classifications) > 0:
        classification = classifications[0]
        classificationJSON['id'] = classification.id
        classificationJSON['identifier'] = classification.identifier
        classificationJSON['name'] = classification.name
        classificationJSON['parentId'] = classification.parent_id
        classificationJSON['keyWord'] = classification.key_word
        classificationJSON['operatorIdentifier'] = classification.operator_identifier
        classificationJSON['operatorTime'] = str(classification.operator_time)
        classificationJSON['type'] = classification.type
        classificationJSON['isDelete'] = classification.is_delete
        if classification.parent_id == 0:
            classificationJSON['children'] = []
    return classificationJSON


def getInventories(specification_id):
    inventoriesJSON = []
    inventories = Inventory.objects.filter(specification_id=specification_id)
    for inventory in inventories:
        inventoryJSON = {}
        inventoryJSON['inventoryId'] = inventory.id
        inventoryJSON['specificationId'] = inventory.specification_id
        inventoryJSON['warehouseId'] = inventory.warehouse_id
        inventoryJSON['inventory'] = inventory.inventory
        inventoryJSON['presellInventory'] = inventory.presell_inventory
        inventoryJSON['occupiedInventory'] = inventory.occupied_inventory
        inventoryJSON['maxInventory'] = inventory.max_inventory
        inventoryJSON['miniInventory'] = inventory.mini_inventory
        inventoryJSON['costPrice'] = inventory.cost_price
        inventoryJSON['commodityNum'] = inventory.commodity_num
        inventoryJSON['isCreateProcurePlan'] = inventory.is_create_procure_plan
        inventoriesJSON.append(inventoryJSON)
    return inventoriesJSON


def getUnits(specification_id):
    unitsJSON = []
    units = Unit.objects.filter(specification_id=specification_id)
    for unit in units:
        unitJSON = {}
        unitJSON['unitId'] = unit.id
        unitJSON['name'] = unit.name
        unitJSON['specificationId'] = unit.specification_id
        unitJSON['ratioDenominator'] = unit.ratio_denominator
        unitJSON['ratioMolecular'] = unit.ratio_molecular
        unitJSON['purchasePrice'] = unit.purchase_price
        unitJSON['commonlyPrice'] = unit.commonly_price
        unitJSON['miniPrice'] = unit.mini_price
        unitJSON['barCode'] = unit.bar_code
        unitJSON['salesUnit'] = unit.sales_unit
        unitJSON['basicUnit'] = unit.basic_unit
        unitJSON['warehouseUnit'] = unit.warehouse_unit
        unitJSON['purchasingUnit'] = unit.purchasing_unit
        unitJSON['miniPurchasing'] = unit.mini_purchasing
        unitJSON['tempCommonlyPrice'] = unit.temp_commonly_price
        unitsJSON.append(unitJSON)
    return unitsJSON


def getPerson(operator_identifier):
    personJSON = {}
    persons = Person.objects.filter(identifier=operator_identifier)
    if len(persons) > 0:
        person = persons[0]
        personJSON['personId'] = person.id
        personJSON['name'] = person.name
        personJSON['type'] = person.type
        personJSON['departmentId'] = person.department_id
        personJSON['entryTime'] = str(person.entry_time)
        personJSON['duties'] = person.duties
        personJSON['education'] = person.education
        personJSON['sex'] = person.sex
        personJSON['birthTime'] = str(person.birth_time)
        personJSON['nativePlace'] = person.native_place
        personJSON['phone'] = person.phone
        personJSON['homePhone'] = person.home_phone
        personJSON['commonPhone'] = person.common_phone
        personJSON['reservePhone'] = person.reserve_phone
        personJSON['postcode'] = person.postcode
        personJSON['homeAddress'] = person.home_address
        personJSON['mailbox'] = person.mailbox
        if person.quit_time != None:
            personJSON['quitTime'] = str(person.quit_time)
        else:
            personJSON['quitTime'] = None
        personJSON['business'] = person.business
        personJSON['quite'] = person.quite
        personJSON['operatorIdentifier'] = person.operator_identifier
        personJSON['operatorTime'] = str(person.operator_time)
        personJSON['remark'] = person.remark
        personJSON['idNumber'] = person.id_number
        personJSON['identifier'] = person.identifier
        personJSON['loginName'] = person.login_name
        personJSON['password'] = base64.b64decode(person.password)
        personJSON['warehouseId'] = person.warehouse_id
        personJSON['place'] = person.place
        personJSON['isDelete'] = person.is_delete
        resIds = []
        permissions = Permission.objects.filter(user_id=person.id)
        for permission in permissions:
            resIds.append(permission.menu_id)
        personJSON['resIds'] = resIds
    return personJSON


def getPersonObj(person):
    personJSON = {}
    personJSON['personId'] = person.id
    personJSON['name'] = person.name
    personJSON['type'] = person.type
    personJSON['departmentId'] = person.department_id
    personJSON['entryTime'] = str(person.entry_time)
    personJSON['duties'] = person.duties
    personJSON['education'] = person.education
    personJSON['sex'] = person.sex
    personJSON['birthTime'] = str(person.birth_time)
    personJSON['nativePlace'] = person.native_place
    personJSON['phone'] = person.phone
    personJSON['homePhone'] = person.home_phone
    personJSON['commonPhone'] = person.common_phone
    personJSON['reservePhone'] = person.reserve_phone
    personJSON['postcode'] = person.postcode
    personJSON['homeAddress'] = person.home_address
    personJSON['mailbox'] = person.mailbox
    if person.quit_time != None:
        personJSON['quitTime'] = str(person.quit_time)
    else:
        personJSON['quitTime'] = None
    personJSON['business'] = person.business
    personJSON['quite'] = person.quite
    personJSON['operatorIdentifier'] = person.operator_identifier
    personJSON['operatorTime'] = str(person.operator_time)
    personJSON['remark'] = person.remark
    personJSON['idNumber'] = person.id_number
    personJSON['identifier'] = person.identifier
    personJSON['loginName'] = person.login_name
    personJSON['password'] = base64.b64decode(person.password)
    personJSON['warehouseId'] = person.warehouse_id
    personJSON['place'] = person.place
    personJSON['isDelete'] = person.is_delete
    resIds = []
    permissions = Permission.objects.filter(user_id=person.id)
    for permission in permissions:
        resIds.append(permission.menu_id)
    personJSON['resIds'] = resIds
    return personJSON


def getSupcto(supcto_id):
    supCtoJSON = {}
    supCtos = Supcto.objects.filter(id=supcto_id)
    if len(supCtos) > 0:
        supCto = supCtos[0]
        supCtoJSON['id'] = supCto.id
        supCtoJSON['classificationId'] = supCto.classification_id
        supCtoJSON['name'] = supCto.name
        supCtoJSON['fullName'] = supCto.full_name
        supCtoJSON['frade'] = supCto.frade
        supCtoJSON['fromType'] = supCto.from_type
        supCtoJSON['settlementTypeId'] = supCto.settlement_type_id
        supCtoJSON['phone'] = supCto.phone
        supCtoJSON['contactPeople'] = supCto.contact_people
        supCtoJSON['postcode'] = supCto.postcode
        supCtoJSON['fax'] = supCto.fax
        supCtoJSON['bankAccount'] = supCto.bank_account
        supCtoJSON['bank'] = supCto.bank
        supCtoJSON['ratepaying'] = supCto.ratepaying
        supCtoJSON['mailbox'] = supCto.mailbox
        supCtoJSON['invoiceType'] = supCto.invoice_type
        supCtoJSON['deliveryAddress'] = supCto.delivery_address
        supCtoJSON['creditDays'] = supCto.credit_days
        supCtoJSON['creditMoney'] = supCto.credit_money
        supCtoJSON['identifier'] = supCto.identifier
        supCtoJSON['information'] = supCto.information
        supCtoJSON['otherInformation'] = supCto.other_information
        supCtoJSON['departmentId'] = supCto.department_id
        supCtoJSON['personId'] = supCto.person_id
        supCtoJSON['currency'] = supCto.currency
        supCtoJSON['communicationAddress'] = supCto.communication_address
        supCtoJSON['taxes'] = supCto.taxes
        supCtoJSON['member'] = supCto.member
        supCtoJSON['shippingModeId'] = supCto.shipping_mode_id
        supCtoJSON['remark'] = supCto.remark
        supCtoJSON['commonPhone'] = supCto.common_phone
        supCtoJSON['reservePhone'] = supCto.reserve_phone
        supCtoJSON['state'] = supCto.state
        supCtoJSON['province'] = supCto.province
        supCtoJSON['city'] = supCto.city
        supCtoJSON['area'] = supCto.area
        supCtoJSON['customerOrSupplier'] = supCto.customer_or_supplier
        supCtoJSON['operatorIdentifier'] = supCto.operator_identifier
        supCtoJSON['operatorTime'] = str(supCto.operator_time)
        supCtoJSON['provinceCode'] = supCto.province_code
        supCtoJSON['cityCode'] = supCto.city_code
        supCtoJSON['areaCode'] = supCto.area_code
        supCtoJSON['website'] = supCto.website
        supCtoJSON['memoryCode'] = supCto.memory_code
        supCtoJSON['useable'] = supCto.useable
        supCtoJSON['advanceMoney'] = supCto.advance_money
        supCtoJSON['isShow'] = supCto.is_show
        supCtoJSON['parentId'] = supCto.parent_id
        commodity_list = []
        supctoCommodities = SupctoCommodity.objects.filter(supcto_id=supCto.id)
        for supctoCommodity in supctoCommodities:
            supctoCommodityJSON = {}
            supctoCommodityJSON['commodityId'] = supctoCommodity.commodity_id
            supctoCommodityJSON['price'] = supctoCommodity.price
            commodity_list.append(supctoCommodityJSON)
        supCtoJSON['commodityList'] = commodity_list
    return supCtoJSON


def getProcure(procure):
    procureJSON = {}
    procureJSON['identifier'] = procure.identifier
    procureJSON['generateDate'] = str(procure.generate_date)
    procureJSON['supctoId'] = procure.supcto_id
    if procure.effective_period_end != None:
        procureJSON['effectivePeriodEnd'] = str(procure.effective_period_end)
    else:
        procureJSON['effectivePeriodEnd'] = None
    if procure.goods_arrival_time != None:
        procureJSON['goodsArrivalTime'] = str(procure.goods_arrival_time)
    else:
        procureJSON['goodsArrivalTime'] = None
    procureJSON['goodsArrivalPlace'] = procure.goods_arrival_place
    procureJSON['transportationMode'] = procure.transportation_mode
    procureJSON['deliveryman'] = procure.deliveryman
    procureJSON['fax'] = procure.fax
    procureJSON['phone'] = procure.phone
    procureJSON['orderer'] = procure.orderer
    procureJSON['prepaidAmount'] = procure.prepaid_amount
    procureJSON['departmentID'] = procure.department_id
    procureJSON['originator'] = procure.originator
    procureJSON['reviewer'] = procure.reviewer
    procureJSON['terminator'] = procure.terminator
    procureJSON['summary'] = procure.summary
    procureJSON['branch'] = procure.branch
    procureJSON['state'] = procure.state
    procureJSON['printNum'] = procure.print_num
    procureJSON['planType'] = procure.plan_type
    procureJSON['payType'] = procure.pay_type
    procureJSON['contractNumber'] = procure.contract_number
    procureJSON['planOrOrder'] = procure.plan_or_order
    procureJSON['beforeIsPlan'] = procure.before_is_plan
    procureJSON['paymentEvidence1'] = procure.payment_evidence1
    procureJSON['paymentEvidence2'] = procure.payment_evidence2
    procureJSON['paymentEvidence3'] = procure.payment_evidence3
    procureJSON['paymentEvidence4'] = procure.payment_evidence4
    procureJSON['paymentEvidence5'] = procure.payment_evidence5
    procureJSON['paymentEvidence6'] = procure.payment_evidence6
    procureJSON['isDelete'] = procure.is_delete
    procureJSON['parentID'] = procure.parent_id
    procureJSON['orderType'] = procure.order_type
    procureJSON['postfix'] = procure.postfix
    procureJSON['isVerification'] = procure.is_verification
    procureJSON['activityID'] = procure.activity_id
    procureJSON['isAppOrder'] = procure.is_app_order
    procureJSON['financialReviewer'] = procure.financial_reviewer
    procureJSON['isOtherReceipts'] = procure.is_other_receipts
    procureJSON['supcto'] = getSupcto(procure.supcto_id)
    procureJSON['procureCommodities'] = getprocureCommodities(procure.id)
    return procureJSON


def getprocureCommodities(procure_id):
    procureCommoditiesJSON = []
    procureCommodities = ProcureCommodity.objects.filter(procure_table_id=procure_id,is_delete=0)
    for procureCommodity in procureCommodities:
        procureCommodityJSON = {}
        procureCommodityJSON['commodityID'] = procureCommodity.commodity_id
        procureCommodityJSON['procureTableID'] = procureCommodity.procure_table_id
        procureCommodityJSON['taxRate'] = procureCommodity.tax_rate
        procureCommodityJSON['amountOfTax'] = procureCommodity.amount_of_tax
        procureCommodityJSON['totalTaxPrice'] = procureCommodity.total_tax_price
        procureCommodityJSON['orderNum'] = procureCommodity.order_num
        procureCommodityJSON['lotNumber'] = procureCommodity.lot_number
        procureCommodityJSON['arrivalQuantity'] = procureCommodity.arrival_quantity
        procureCommodityJSON['suspendQuantity'] = procureCommodity.suspend_quantity
        procureCommodityJSON['suspendPrice'] = procureCommodity.suspend_price
        procureCommodityJSON['discount'] = procureCommodity.discount
        procureCommodityJSON['isLargess'] = procureCommodity.is_largess
        procureCommodityJSON['originalUnitPrice'] = procureCommodity.original_unit_price
        procureCommodityJSON['businessUnitPrice'] = procureCommodity.business_unit_price
        procureCommodityJSON['remarks'] = procureCommodity.remarks
        procureCommodityJSON['containsTaxPrice'] = procureCommodity.contains_tax_price
        procureCommodityJSON['paymentForGoods'] = procureCommodity.payment_for_goods
        procureCommodityJSON['totalPrice'] = procureCommodity.total_price
        procureCommodityJSON['isDelete'] = procureCommodity.is_delete
        procureCommodityJSON['commoditySpecification'] = getCommoditySpecification(procureCommodity.commodity_id)
        procureCommoditiesJSON.append(procureCommodityJSON)
    return procureCommoditiesJSON


def getCommodity(commodity):
    commodityJSON = {}
    commodityJSON['commodityID'] = commodity.id
    commodityJSON['classificationID'] = commodity.classification_id
    commodityJSON['name'] = commodity.name
    commodityJSON['brand'] = commodity.brand
    commodityJSON['zeroStock'] = commodity.zero_stock
    commodityJSON['shoutName'] = commodity.shout_name
    commodityJSON['mnemonicCode'] = commodity.mnemonic_code
    commodityJSON['basicsInformation'] = commodity.basics_information
    commodityJSON['attribute'] = commodity.attribute
    commodityJSON['identifier'] = commodity.identifier
    commodityJSON['supctoID'] = commodity.supcto_id
    commodityJSON['taxes'] = commodity.taxes
    commodityJSON['isAssemble'] = commodity.is_assemble
    commodityJSON['isPresell'] = commodity.is_presell
    commodityJSON['tempTaxes'] = commodity.temp_taxes
    commodityJSON['commoditySpecifictions'] = getSpecifications(commodity.id)
    commodityJSON['classification'] = getClassification(commodity.classification_id)
    return commodityJSON


def getSpecifications(commodity_id):
    commoditySpecificationsJSON = []
    specifications = CommoditySpecification.objects.filter(commodity_id=commodity_id)
    for specification in specifications:
        specificationJSON = {}
        specificationJSON['specificationID'] = specification.id
        specificationJSON['specificationIdentifier'] = specification.specification_identifier
        specificationJSON['specificationName'] = specification.specification_name
        specificationJSON['commodityID'] = specification.commodity_id
        specificationJSON['qualityPeriod'] = specification.quality_period
        specificationJSON['qualityPeriodUnit'] = specification.quality_period_unit
        specificationJSON['miniOrderQuantity'] = specification.mini_order_quantity
        specificationJSON['addOrderQuantity'] = specification.add_order_quantity
        specificationJSON['packagingSize'] = specification.packaging_size
        specificationJSON['isDelete'] = specification.is_delete
        specificationJSON['warningNumber'] = specification.warning_number
        specificationJSON['weight'] = specification.weight
        specificationJSON['operatorIdentifier'] = specification.operator_identifier
        specificationJSON['operatorTime'] = str(specification.operator_time)
        specificationJSON['state'] = specification.state
        specificationJSON['tempMiniOrderQuantity'] = specification.temp_mini_order_quantity
        specificationJSON['tempAddOrdeQuantity'] = specification.temp_add_order_quantity
        specificationJSON['tempWarningNumber'] = specification.temp_warning_number
        specificationJSON['tempWarehouseID'] = specification.temp_warehouse_id
        specificationJSON['tempMaxInventory'] = specification.temp_max_inventory
        specificationJSON['tempMiniInventory'] = specification.temp_mini_inventory
        specificationJSON['tempInventory'] = specification.temp_inventory
        specificationJSON['tempState'] = specification.temp_state
        inventoriesJSON = getInventories(specification.id)
        specificationJSON['inventories'] = inventoriesJSON
        unitsJSON = getUnits(specification.id)
        specificationJSON['units'] = unitsJSON
        commoditySpecificationsJSON.append(specificationJSON)
        return commoditySpecificationsJSON
    
    
def getSpecification(specification):
    specificationJSON = {}
    specificationJSON['specificationID'] = specification.id
    specificationJSON['specificationIdentifier'] = specification.specification_identifier
    specificationJSON['specificationName'] = specification.specification_name
    specificationJSON['commodityID'] = specification.commodity_id
    specificationJSON['qualityPeriod'] = specification.quality_period
    specificationJSON['qualityPeriodUnit'] = specification.quality_period_unit
    specificationJSON['miniOrderQuantity'] = specification.mini_order_quantity
    specificationJSON['addOrderQuantity'] = specification.add_order_quantity
    specificationJSON['packagingSize'] = specification.packaging_size
    specificationJSON['isDelete'] = specification.is_delete
    specificationJSON['warningNumber'] = specification.warning_number
    specificationJSON['weight'] = specification.weight
    specificationJSON['operatorIdentifier'] = specification.operator_identifier
    specificationJSON['operatorTime'] = str(specification.operator_time)
    specificationJSON['state'] = specification.state
    specificationJSON['tempMiniOrderQuantity'] = specification.temp_mini_order_quantity
    specificationJSON['tempAddOrderQuantity'] = specification.temp_add_order_quantity
    specificationJSON['tempWarningNumber'] = specification.temp_warning_number
    specificationJSON['tempWarehouseID'] = specification.temp_warehouse_id
    specificationJSON['tempMaxInventory'] = specification.temp_max_inventory
    specificationJSON['tempMiniInventory'] = specification.temp_mini_inventory
    specificationJSON['tempInventory'] = specification.temp_inventory
    specificationJSON['tempState'] = specification.temp_state
    specificationJSON['inventories'] = getInventories(specification.id)
    specificationJSON['units'] = getUnits(specification.id)
    specificationJSON['person'] = getPerson(specification.operator_identifier)
    specificationJSON['commodity'] = getCommoditySelect(specification.commodity_id)
    return specificationJSON


def getSalesPlanOrder(salesPlanOrder):
    salesPlanOrderJSON = {}
    salesPlanOrderJSON['salesPlanOrderID'] = salesPlanOrder.id
    salesPlanOrderJSON['identifier'] = salesPlanOrder.identifier
    salesPlanOrderJSON['createTime'] = str(salesPlanOrder.create_time)
    if salesPlanOrder.end_time != None:
        salesPlanOrderJSON['endTime'] = str(salesPlanOrder.end_time)
    else:
        salesPlanOrderJSON['endTime'] = None
    salesPlanOrderJSON['currency'] = salesPlanOrder.currency
    salesPlanOrderJSON['branch'] = salesPlanOrder.branch
    salesPlanOrderJSON['originator'] = salesPlanOrder.originator
    salesPlanOrderJSON['summary'] = salesPlanOrder.summary
    salesPlanOrderJSON['supctoID'] = salesPlanOrder.supcto_id
    salesPlanOrderJSON['personID'] = salesPlanOrder.person_id
    salesPlanOrderJSON['state'] = salesPlanOrder.state
    salesPlanOrderJSON['isAppOrder'] = salesPlanOrder.is_app_order
    salesPlanOrderJSON['appConsigneeName'] = salesPlanOrder.app_consignee_name
    salesPlanOrderJSON['appConsigneePhone'] = salesPlanOrder.app_consignee_phone
    salesPlanOrderJSON['appConsigneeAddress'] = salesPlanOrder.app_consignee_address
    salesPlanOrderJSON['missOrderID'] = salesPlanOrder.miss_order_id
    salesPlanOrderJSON['activityID'] = salesPlanOrder.activity_id
    salesPlanOrderJSON['fax'] = salesPlanOrder.fax
    salesPlanOrderJSON['shippingModeID'] = salesPlanOrder.shipping_mode_id
    salesPlanOrderJSON['phone'] = salesPlanOrder.phone
    salesPlanOrderJSON['deliverGoodsPlace'] = salesPlanOrder.deliver_goods_place
    salesPlanOrderJSON['orderer'] = salesPlanOrder.orderer
    salesPlanOrderJSON['supcto'] = getSupcto(salesPlanOrder.supcto_id)
    salesPlanOrderJSON['salesPlanOrderCommodities'] = getSlesPlanOrderCommodities(salesPlanOrder.id)
    return salesPlanOrderJSON


def getSlesPlanOrderCommodities(salesPlanOrderID):
    slesPlanOrderCommoditiesJSON = []
    slesPlanOrderCommodities = SalesPlanOrderCommodity.objects.filter(sales_plan_order_id=salesPlanOrderID)
    for slesPlanOrderCommodity in slesPlanOrderCommodities:
        slesPlanOrderCommodityJSON = {}
        slesPlanOrderCommodityJSON['slesPlanOrderCommodityID'] = slesPlanOrderCommodity.id
        slesPlanOrderCommodityJSON['salesPlanOrderID'] = slesPlanOrderCommodity.sales_plan_order_id
        slesPlanOrderCommodityJSON['commoditySpecificationID'] = slesPlanOrderCommodity.commodity_specification_id
        slesPlanOrderCommodityJSON['number'] = slesPlanOrderCommodity.number
        slesPlanOrderCommodityJSON['unitPrice'] = slesPlanOrderCommodity.unit_price
        slesPlanOrderCommodityJSON['money'] = slesPlanOrderCommodity.money
        slesPlanOrderCommodityJSON['remark'] = slesPlanOrderCommodity.remark
        slesPlanOrderCommodityJSON['commoditySpecification'] = getCommoditySpecification(slesPlanOrderCommodity.commodity_specification_id)
        slesPlanOrderCommoditiesJSON.append(slesPlanOrderCommodityJSON)
    return slesPlanOrderCommoditiesJSON


def getSalesOrder(salesOrder):
    salesOrderJSON = {}
    salesOrderJSON['salesOrderID'] = salesOrder.id
    salesOrderJSON['parentID'] = salesOrder.parent_id
    salesOrderJSON['identifier'] = salesOrder.identifier
    salesOrderJSON['breakCode'] = salesOrder.break_code
    salesOrderJSON['payment'] = salesOrder.payment
    salesOrderJSON['orderType'] = salesOrder.order_type
    salesOrderJSON['createTime'] = str(salesOrder.create_time)
    if salesOrder.end_validity_time != None:
        salesOrderJSON['endCalidityTime'] = str(salesOrder.end_validity_time)
    else:
        salesOrderJSON['endCalidityTime'] = None
    salesOrderJSON['deliverGoodsPlace'] = salesOrder.deliver_goods_place
    salesOrderJSON['receiptGoodsPlace'] = salesOrder.receipt_goods_place
    salesOrderJSON['consignee'] = salesOrder.consignee
    salesOrderJSON['phone'] = salesOrder.phone
    salesOrderJSON['fax'] = salesOrder.fax
    salesOrderJSON['orderer'] = salesOrder.orderer
    salesOrderJSON['advanceScale'] = salesOrder.advance_scale
    salesOrderJSON['originator'] = salesOrder.originator
    salesOrderJSON['summary'] = salesOrder.summary
    salesOrderJSON['branch'] = salesOrder.branch
    salesOrderJSON['state'] = salesOrder.state
    salesOrderJSON['isSpecimen'] = salesOrder.is_specimen
    salesOrderJSON['supctoID'] = salesOrder.supcto_id
    salesOrderJSON['shippingModeID'] = salesOrder.shipping_mode_id
    salesOrderJSON['personID'] = salesOrder.person_id
    salesOrderJSON['salesPlanOrderID'] = salesOrder.sales_plan_order_id
    salesOrderJSON['printNum'] = salesOrder.print_num
    salesOrderJSON['isShow'] = salesOrder.is_show
    salesOrderJSON['isVerification'] = salesOrder.is_verification
    salesOrderJSON['missOrderID'] = salesOrder.miss_order_id
    salesOrderJSON['activityID'] = salesOrder.activity_id
    salesOrderJSON['isAppOrder'] = salesOrder.is_app_order
    salesOrderJSON['isReturnGoods'] = salesOrder.is_return_goods
    salesOrderJSON['appOrderIdentifier'] = salesOrder.app_order_identifier
    if salesOrder.app_send_time != None:
        salesOrderJSON['appSendTime'] = str(salesOrder.app_send_time)
    else:
        salesOrderJSON['appSendTime'] = None
    salesOrderJSON['isCreateStockOrder'] = salesOrder.is_create_stock_order
    salesOrderJSON['person'] = getPerson(salesOrder.person_id)
    salesOrderJSON['supcto'] = getSupcto(salesOrder.supcto_id)
    salesOrderJSON['salesOrderCommodities'] = getSalesOrderCommodities(salesOrder.id)
    return salesOrderJSON


def getSalesOrderCommodities(sales_order_id):
    salesPlanOrderCommodities = SalesOrderCommodity.objects.filter(sales_order_id=sales_order_id)
    salesPlanOrderCommoditiesJSON = []
    for salesPlanOrderCommodity in salesPlanOrderCommodities:
        salesPlanOrderCommodityJSON = {}
        salesPlanOrderCommodityJSON['salesOrderCommodityID'] = salesPlanOrderCommodity.id
        salesPlanOrderCommodityJSON['salesOrderID'] = salesPlanOrderCommodity.sales_order_id
        salesPlanOrderCommodityJSON['commoditySpecificationID'] = salesPlanOrderCommodity.commodity_specification_id
        salesPlanOrderCommodityJSON['deliverGoodsMoney'] = salesPlanOrderCommodity.deliver_goods_money
        salesPlanOrderCommodityJSON['deliverGoodsNum'] = salesPlanOrderCommodity.deliver_goods_num
        salesPlanOrderCommodityJSON['returnGoodsNum'] = salesPlanOrderCommodity.return_goods_num
        salesPlanOrderCommodityJSON['receivingGoodsMoney'] = salesPlanOrderCommodity.receiving_goods_money
        salesPlanOrderCommodityJSON['receivingGoodsnum'] = salesPlanOrderCommodity.receiving_goods_num
        salesPlanOrderCommodityJSON['damagenum'] = salesPlanOrderCommodity.damage_num
        salesPlanOrderCommodityJSON['damageMoney'] = salesPlanOrderCommodity.damage_money
        salesPlanOrderCommodityJSON['discount'] = salesPlanOrderCommodity.discount
        salesPlanOrderCommodityJSON['unitPrice'] = salesPlanOrderCommodity.unit_price
        salesPlanOrderCommodityJSON['taxesMoney'] = salesPlanOrderCommodity.taxes_money
        salesPlanOrderCommodityJSON['taxes'] = salesPlanOrderCommodity.taxes
        salesPlanOrderCommodityJSON['batchNumber'] = salesPlanOrderCommodity.batch_number
        salesPlanOrderCommodityJSON['remark'] = salesPlanOrderCommodity.remark
        salesPlanOrderCommodityJSON['isSpecialOffer'] = salesPlanOrderCommodity.is_special_offer
        salesPlanOrderCommodityJSON['warehouseID'] = salesPlanOrderCommodity.warehouse_id
        salesPlanOrderCommodityJSON['commoditySpecification'] = getCommoditySpecification(salesPlanOrderCommodity.commodity_specification_id)
        salesPlanOrderCommoditiesJSON.append(salesPlanOrderCommodityJSON)
    return salesPlanOrderCommoditiesJSON


def getAllot(allot):
    allotJSON = {}
    allotJSON['allotID'] = allot.id
    allotJSON['allotDate'] = str(allot.allot_date)
    allotJSON['identifier'] = allot.identifier
    allotJSON['exportWarehouseID'] = allot.export_warehouse_id
    allotJSON['importWarehouseID'] = allot.import_warehouse_id
    allotJSON['shippingModeID'] = allot.shipping_mode_id
    allotJSON['importBranch'] = allot.import_branch
    allotJSON['adjustSubject'] = allot.adjust_subject
    allotJSON['sendGoodsPlace'] = allot.send_goods_place
    allotJSON['personID'] = allot.person_id
    allotJSON['originator'] = allot.originator
    allotJSON['summary'] = allot.summary
    allotJSON['printNum'] = allot.print_num
    allotJSON['makePerson'] = allot.make_person
    allotJSON['description'] = allot.description
    allotJSON['exportName'] = allot.export_name
    allotJSON['importName'] = allot.import_name
    allotJSON['allotCommodities'] = getAllotCommodities(allot.id)
    return allotJSON

def getAllotCommodities(allot_order_id):
    allotCommoditiesJSON = []
    allotCommodities = AllotOrderCommodity.objects.filter(allot_order_id=allot_order_id)
    for allotCommodity in allotCommodities:
        allotCommodityJSON = {}
        allotCommodityJSON['allotCommodityID'] = allotCommodity.id
        allotCommodityJSON['allotOrderID'] = allotCommodity.allot_order_id
        allotCommodityJSON['commoditySpecificationID'] = allotCommodity.commodity_specification_id
        allotCommodityJSON['number'] = allotCommodity.number
        allotCommodityJSON['exportUnitPrice'] = allotCommodity.export_unit_price
        allotCommodityJSON['importUnitPrice'] = allotCommodity.import_unit_price
        allotCommodityJSON['importMoney'] = allotCommodity.import_money
        allotCommoditiesJSON.append(allotCommodityJSON)
    return allotCommoditiesJSON


def getStock(stock):
    stockJSON = {}
    stockJSON['stockID'] = stock.id
    stockJSON['takeStockDate'] = str(stock.take_stock_date)
    stockJSON['identifier'] = stock.identifier
    stockJSON['warehouseID'] = stock.warehouse_id
    stockJSON['personID'] = stock.person_id
    stockJSON['originator'] = stock.originator
    stockJSON['financeReviewer'] = stock.finance_reviewer
    stockJSON['managerReviewer'] = stock.manager_reviewer
    stockJSON['summary'] = stock.summary
    stockJSON['state'] = stock.state
    stockJSON['printNum'] = stock.print_num
    stockJSON['isDelete'] = stock.is_delete
    stockJSON['stockCommodities'] = getStockCommodities(stock.id)
    return stockJSON


def getStockCommodities(take_stock_order_id):
    stockCommoditiesJSON = []
    stockCommodities = TakeStockOrderCommodity.objects.filter(take_stock_order_id=take_stock_order_id)
    for stockCommodity in stockCommodities:
        stockCommodityJSON = {}
        stockCommodityJSON['stockCommodityID'] = stockCommodity.id
        stockCommodityJSON['stockID'] = stockCommodity.take_stock_order_id
        stockCommodityJSON['commoditySpecificationID'] = stockCommodity.commodity_specification_id
        stockCommodityJSON['inventoryNum'] = stockCommodity.inventory_num
        stockCommodityJSON['realNum'] = stockCommodity.real_num
        stockCommodityJSON['profitOrLossNum'] = stockCommodity.profit_or_loss_num
        stockCommodityJSON['unitPrice'] = stockCommodity.unit_price
        stockCommodityJSON['money'] = stockCommodity.money
        stockCommodityJSON['commoditySpecification'] = getCommoditySpecification(stockCommodity.commodity_specification_id)
        stockCommoditiesJSON.append(stockCommodityJSON)
    return stockCommoditiesJSON


def getPackage(package):
    packageJSON = {}
    packageJSON['packageID'] = package.id
    packageJSON['orderType'] = package.order_type
    packageJSON['packageOrTeardownDate'] = str(package.package_or_teardown_date)
    packageJSON['identifier'] = package.identifier
    packageJSON['warehouseID'] = package.warehouse_id
    packageJSON['commoditySpecificationID'] = package.commodity_specification_id
    packageJSON['packageOrTeardownNum'] = package.package_or_teardown_num
    packageJSON['unitPrice'] = package.unit_price
    packageJSON['totalMoney'] = package.total_money
    packageJSON['personID'] = package.person_id
    packageJSON['originator'] = package.originator
    packageJSON['reviewer'] = package.reviewer
    packageJSON['summary'] = package.summary
    packageJSON['state'] = package.state
    packageJSON['printNum'] = package.print_num
    packageJSON['isDelete'] = package.is_delete
    packageJSON['packageCommodities'] = getPackageCommodities(package.id)
    return packageJSON


def getPackageCommodities(package_or_teardown_order_id):
    packageCommoditiesJSON = []
    packageCommodities = PackageOrTeardownOrderCommodity.objects.filter(package_or_teardown_order_id=package_or_teardown_order_id)
    for packageCommodity in packageCommodities:
        packageCommodityJSON = {}
        packageCommodityJSON['packageCommodityID'] = packageCommodity.id
        packageCommodityJSON['packageOrTeardownOrderID'] = packageCommodity.package_or_teardown_order_id
        packageCommodityJSON['commoditySpecificationID'] = packageCommodity.commodity_specification_id
        packageCommodityJSON['number'] = packageCommodity.number
        packageCommodityJSON['unitPrice'] = packageCommodity.unit_price
        packageCommodityJSON['money'] = packageCommodity.money
        packageCommoditiesJSON.append(packageCommodityJSON)
    return packageCommoditiesJSON


def getBills(bill):
    billJSON = {}
    billJSON['billsID'] = bill.id
    billJSON['billsCode'] = bill.bills_code
    billJSON['customerSupplierID'] = bill.customer_supplier_id
    billJSON['billsType'] = bill.bills_type
    billJSON['billsDate'] = str(bill.bills_date)
    billJSON['bank'] = bill.bank
    billJSON['bankAccount'] = bill.bank_account
    billJSON['payment'] = bill.payment
    billJSON['originator'] = bill.originator
    billJSON['personID'] = bill.person_id
    billJSON['summary'] = bill.summary
    billJSON['remark'] = bill.remark
    billJSON['money'] = bill.money
    billJSON['ticketNo'] = bill.ticket_no
    billJSON['branch'] = bill.branch
    billJSON['balance'] = bill.balance
    billJSON['account'] = bill.account
    billJSON['orderType'] = bill.order_type
    billJSON['billsSubs'] = getBillsSubs(bill.id)
    return billJSON


def getBillsSubs(bills_id):
    billsSubsJSON = []
    billsSubs = BillsSub.objects.filter(bills_id=bills_id)
    for billsSub in billsSubs:
        billsSubJSON = {}
        billsSubJSON['billsSubID'] = billsSub.id
        billsSubJSON['billsID'] = billsSub.bills_id
        billsSubJSON['procureSalesID'] = billsSub.procure_sales_id
        billsSubJSON['clearingMoney'] = billsSub.clearing_money
        billsSubJSON['stayMoney'] = billsSub.stay_money
        billsSubJSON['theMoeny'] = billsSub.the_moeny
        billsSubJSON['actualMoney'] = billsSub.actual_money
        billsSubJSON['rebateMoney'] = billsSub.rebate_money
        billsSubJSON['isPayment'] = billsSub.is_payment
        billsSubJSON['rebate'] = billsSub.rebate
        billsSubJSON['remark'] = billsSub.remark
        billsSubJSON['payMoney'] = billsSub.pay_money
        billsSubsJSON.append(billsSubJSON)
    return billsSubsJSON


def getWriteoff(writeoff):
    writeoffJSON = {}
    writeoffJSON['writeoffID'] = writeoff.id
    writeoffJSON['writeoffCode'] = writeoff.writeoff_code
    writeoffJSON['writeoffType'] = writeoff.writeoff_type
    writeoffJSON['companyOne'] = writeoff.company_one
    writeoffJSON['companyTwo'] = writeoff.company_two
    writeoffJSON['money'] = writeoff.money
    writeoffJSON['createDate'] = str(writeoff.create_date)
    writeoffJSON['originator'] = writeoff.originator
    writeoffJSON['personID'] = writeoff.person_id
    writeoffJSON['summary'] = writeoff.summary
    writeoffJSON['remark'] = writeoff.remark
    writeoffJSON['voucherNo'] = writeoff.voucher_no
    writeoffJSON['branch'] = writeoff.branch
    writeoffJSON['writeOffSubs'] = getWriteOffSubs(writeoff.id)
    return writeoffJSON


def getWriteOffSubs(writeoff_id):
    writeOffSubsJSON = []
    writeOffSubs = WriteoffSub.objects.filter(writeoff_id=writeoff_id)
    for writeOffSub in writeOffSubs:
        writeOffSubJSON = {}
        writeOffSubJSON['writeOffSubID'] = writeOffSub.id
        writeOffSubJSON['writeoffID'] = writeOffSub.writeoff_id
        writeOffSubJSON['procureSalesID'] = writeOffSub.procure_sales_id
        writeOffSubJSON['clearMoney'] = writeOffSub.clear_money
        writeOffSubJSON['stayMoney'] = writeOffSub.stay_money
        writeOffSubJSON['theMoney'] = writeOffSub.the_money
        writeOffSubJSON['isWriteoff'] = writeOffSub.is_writeoff
        writeOffSubJSON['isProcureSales'] = writeOffSub.is_procure_sales
        writeOffSubJSON['remark'] = writeOffSub.remark
        writeOffSubsJSON.append(writeOffSubJSON)
    return writeOffSubsJSON


def getBreakage(breakage):
    breakageJSON = {}
    breakageJSON['breakageID'] = breakage.id
    breakageJSON['breakageDate'] = str(breakage.breakage_date)
    breakageJSON['identifier'] = breakage.identifier
    breakageJSON['warehouseID'] = breakage.warehouse_id
    breakageJSON['personID'] = breakage.person_id
    breakageJSON['originator'] = breakage.originator
    breakageJSON['reviewer'] = breakage.reviewer
    breakageJSON['summary'] = breakage.summary
    breakageJSON['state'] = breakage.state
    breakageJSON['printNum'] = breakage.print_num
    breakageJSON['isDelete'] = breakage.is_delete
    breakageJSON['breakageCommodities'] = getBreakageCommodities(breakage.id)
    return breakageJSON


def getBreakageCommodities(breakage_id):
    breakageCommoditiesJSON = []
    breakageCommodities = BreakageOrderCommodity.objects.filter(breakage_order_id=breakage_id)
    for breakageCommodity in breakageCommodities:
        breakageCommodityJSON = {}
        breakageCommodityJSON['breakageCommodityID'] = breakageCommodity.id
        breakageCommodityJSON['breakageOrderID'] = breakageCommodity.breakage_order_id
        breakageCommodityJSON['commoditySpecificationID'] = breakageCommodity.commodity_specification_id
        breakageCommodityJSON['number'] = breakageCommodity.number
        breakageCommodityJSON['unitPrice'] = breakageCommodity.unit_price
        breakageCommodityJSON['money'] = breakageCommodity.money
        breakageCommodityJSON['commoditySpecification'] = getCommoditySpecification(breakageCommodity.commodity_specification_id)
        breakageCommoditiesJSON.append(breakageCommodityJSON)
    return breakageCommoditiesJSON


def getDepartment(department):
    departmentJSON = {}
    departmentJSON['departmentID'] = department.id
    departmentJSON['name'] = department.name
    departmentJSON['operatorIdentifier'] = department.operator_identifier
    departmentJSON['operatorTime'] = str(department.operator_time)
    departmentJSON['identifier'] = department.identifier
    departmentJSON['isDelete'] = department.is_delete
    return departmentJSON


def getGoods(goods):
    goodsJSON = {}
    goodsJSON['goodsID'] = goods.id
    goodsJSON['stock'] = goods.stock
    goodsJSON['purchase'] = goods.purchase
    goodsJSON['brand'] = goods.brand
    goodsJSON['state'] = goods.state
    return goodsJSON


def getLog(log):
    logJSON = {}
    logJSON['logID'] = log.id
    logJSON['operateType'] = log.operate_type
    logJSON['operateObject'] = log.operate_object
    logJSON['operatorIdentifier'] = log.operator_identifier
    logJSON['operateTime'] = str(log.operate_time)
    return logJSON
#!usr/bin/python#coding=utf-8

import json,sys,time
from string import upper, atof, atoi
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,isValid
import traceback
from erp_sites.models import Supcto,SupctoCommodity
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10

def thirdPartyInsert(request):
    try:
        if isTokenExpired(request):
            thirdPartyInsert = {}
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
            if 'fullName' in json2Dict:
                if isValid(json2Dict['fullName']):
                    full_name = json2Dict['fullName']
                else:
                    full_name = None
            else:
                full_name = None
            if 'frade' in json2Dict:
                if isValid(json2Dict['frade']):
                    frade = int(json2Dict['frade'])
                else:
                    frade = 1
            else:
                frade = 1
            if 'fromType' in json2Dict:
                if isValid(json2Dict['fromType']):
                    from_type = int(json2Dict['fromType'])
                else:
                    from_type = 1
            else:
                from_type = 1
            if 'settlementTypeID' in json2Dict:
                if isValid(json2Dict['settlementTypeID']):
                    settlement_type_id = int(json2Dict['settlementTypeID'])
                else:
                    settlement_type_id = 0
            else:
                settlement_type_id = 0
            if 'phone' in json2Dict:
                if isValid(json2Dict['phone']):
                    phone = json2Dict['phone']
                else:
                    phone = None
            else:
                phone = None
            if 'contactPeople' in json2Dict:
                if isValid(json2Dict['contactPeople']):
                    contact_people = json2Dict['contactPeople']
                else:
                   contact_people = None 
            else:
                contact_people = None
            if 'postcode' in json2Dict:
                if isValid(json2Dict['postcode']):
                    postcode = json2Dict['postcode']
                else:
                    postcode = None
            else:
                postcode = None
            if 'fax' in json2Dict:
                if isValid(json2Dict['fax']):
                    fax = json2Dict['fax']
                else:
                    fax = None
            else:
                fax = None
            if 'bankAccount' in json2Dict:
                if isValid(json2Dict['bankAccount']):
                    bank_account = json2Dict['bankAccount']
                else:
                    bank_account = None
            else:
                bank_account = None
            if 'bank' in json2Dict:
                if isValid(json2Dict['bank']):
                    bank = json2Dict['bank']
                else:
                    bank = None
            else:
                bank = None
            if 'ratepaying' in json2Dict:
                if isValid(json2Dict['ratepaying']):
                    ratepaying = json2Dict['ratepaying']
                else:
                    ratepaying = None
            else:
                ratepaying = None
            if 'mailbox' in json2Dict:
                if isValid(json2Dict['mailbox']):
                    mailbox = json2Dict['mailbox']
                else:
                    mailbox = None
            else:
                mailbox = None
            if 'invoiceType' in json2Dict:
                if isValid(json2Dict['invoiceType']):
                    invoice_type = int(json2Dict['invoiceType'])
                else:
                    invoice_type = 1
            else:
                invoice_type = 1
            if 'deliveryAddress' in json2Dict:
                if isValid(json2Dict['deliveryAddress']):
                    delivery_address = json2Dict['deliveryAddress']
                else:
                    delivery_address = None
            else:
                delivery_address = None
            if 'creditDays' in json2Dict:
                if isValid(json2Dict['creditDays']):
                    credit_days = int(json2Dict['creditDays'])
                else:
                    credit_days = 0
            else:
                credit_days = 0
            if 'creditMoney' in json2Dict:
                if isValid(json2Dict['creditMoney']):
                    credit_money = atof(json2Dict['creditMoney'])
                else:
                    credit_money = 0
            else:
                credit_money = 0
            if 'information' in json2Dict:
                if isValid(json2Dict['information']):
                    information = json2Dict['information']
                else:
                    information = None
            else:
                information = None
            if 'otherInformation' in json2Dict:
                if isValid(json2Dict['otherInformation']):
                    other_information = json2Dict['otherInformation']
                else:
                    other_information = None
            else:
                other_information = None
            if 'departmentID' in json2Dict:
                if isValid(json2Dict['departmentID']):
                    department_id = int(json2Dict['departmentID'])
                else:
                    department_id = 0
            else:
                department_id = 0
            if 'personID' in json2Dict:
                if isValid(json2Dict['personID']):
                    person_id = int(json2Dict['personID'])
                else:
                    person_id = 0
            else:
                person_id = 0
            if 'currency' in json2Dict:
                if isValid(json2Dict['currency']):
                    currency = int(json2Dict['currency'])
                else:
                   currency = 0 
            else:
                currency = 0
            if 'communicationAddress' in json2Dict:
                if isValid(json2Dict['communicationAddress']):
                    communication_address = json2Dict['communicationAddress']
                else:
                    communication_address = None
            else:
                communication_address = None
            if 'taxes' in json2Dict:
                if isValid(json2Dict['taxes']):
                    taxes = atof(json2Dict['taxes'])
                else:
                    taxes = 0
            else:
                taxes = 0
            if 'member' in json2Dict:
                if isValid(json2Dict['member']):
                    member = json2Dict['member']
                else:
                    member = None
            else:
                member = None
            if 'shippingModeID' in json2Dict:
                if isValid(json2Dict['shippingModeID']):
                    shipping_mode_id = int(json2Dict['shippingModeID'])
                else:
                    shipping_mode_id = 0
            else:
                shipping_mode_id = 0
            if 'remark' in json2Dict:
                if isValid(json2Dict['remark']):
                    remark = json2Dict['remark']
                else:
                    remark = None
            else:
                remark = None
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
            if 'state' in json2Dict:
                if isValid(json2Dict['state']):
                    state = int(json2Dict['state'])
                else:
                    state = 1
            else:
                state = 1
            if 'province' in json2Dict:
                if isValid(json2Dict['province']):
                    province = json2Dict['province']
                else:
                    province = None
            else:
                province = None
            if 'city' in json2Dict:
                if isValid(json2Dict['city']):
                    city = json2Dict['city']
                else:
                    city = None
            else:
                city = None
            if 'area' in json2Dict:
                if isValid(json2Dict['area']):
                    area = json2Dict['area']
                else:
                    area = None
            else:
                area = None
            customer_or_supplier = int(json2Dict['customerOrSupplier'])
            operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if customer_or_supplier == 1:
                identifier = 'CTO-' + operator_time[0:10] + '-'
            elif customer_or_supplier == 2:
                identifier = 'SUP-' + operator_time[0:10] + '-'
            else:
                thirdPartyInsert = setStatus(300,{})
                return HttpResponse(json.dumps(thirdPartyInsert), content_type='application/json')
            if 'operatorIdentifier' in json2Dict:
                if isValid(json2Dict['operatorIdentifier']):
                    operator_identifier = json2Dict['operatorIdentifier']
                else:
                    operator_identifier = None
            else:
                operator_identifier = None
            if 'provinceCode' in json2Dict:
                if isValid(json2Dict['provinceCode']):
                    province_code = json2Dict['provinceCode']
                else:
                    province_code = None
            else:
                province_code = None
            if 'cityCode' in json2Dict:
                if isValid(json2Dict['cityCode']):
                    city_code = json2Dict['cityCode']
                else:
                    city_code = None
            else:
                city_code = None
            if 'areaCode' in json2Dict:
                if isValid(json2Dict['areaCode']):
                    area_code = json2Dict['areaCode']
                else:
                    area_code = None
            else:
                area_code = None
            if 'website' in json2Dict:
                if isValid(json2Dict['website']):
                    website = json2Dict['website']
                else:
                    website = None
            else:
                website = None
            if 'memoryCode' in json2Dict:
                if isValid(json2Dict['memoryCode']):
                    memory_code = json2Dict['memoryCode']
                else:
                    memory_code = None
            else:
                memory_code = None
            if 'useable' in json2Dict:
                if isValid(json2Dict['useable']):
                    useable = int(json2Dict['useable'])
                else:
                    useable = 1
            else:
                useable = 1
            if 'advanceMoney' in json2Dict:
                if isValid(json2Dict['advanceMoney']):
                    advance_money = atof(json2Dict['advanceMoney'])
                else:
                    advance_money = 0
            else:
                advance_money = 0
            if 'isShow' in json2Dict:
                if isValid(json2Dict['isShow']):
                    is_show = int(json2Dict['isShow'])
                else:
                    is_show = 1
            else:
                is_show = 1
            if 'parentID' in json2Dict:
                if isValid(json2Dict['parentID']):
                    parent_id = int(json2Dict['parentID'])
                else:
                    parent_id = 0 
            else:
                parent_id = 0
            supCto = Supcto(None,classification_id,name,full_name,frade,from_type,settlement_type_id,phone,contact_people,postcode,fax,bank_account,bank,ratepaying,mailbox,invoice_type,delivery_address,credit_days,credit_money,identifier,information,other_information,department_id,person_id,currency,communication_address,taxes,member,shipping_mode_id,remark,common_phone,reserve_phone,state,province,city,area,customer_or_supplier,operator_identifier,operator_time,province_code,city_code,area_code,website,memory_code,useable,advance_money,is_show,parent_id)
            supCto.save()
            supCto.identifier = identifier + str(supCto.id)
            supCto.save()
            if 'commodityList' in json2Dict:
                commodities = json2Dict['commodityList']
                for commodity in commodities:
                    commodity_id = commodity['commodityID']
                    price = commodity['price']
                    supcto_id = supCto.id
                    supctoCommodity = SupctoCommodity(None,commodity_id,supcto_id,price)
                    supctoCommodity.save()
            supCtoJSON = getSupCto(supCto)
            thirdPartyInsert = setStatus(200,supCtoJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        thirdPartyInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(thirdPartyInsert), content_type='application/json')


def thirdPartyDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                supCtos = Supcto.objects.filter(id=identifier)
                if len(supCtos) > 0:
                    supCto = supCtos[0]
                    supctoCommodities = SupctoCommodity.objects.filter(supcto_id=supCto.id)
                    for supctoCommodity in supctoCommodities:
                        supctoCommodity.delete()
                    supCto.delete()
                    thirdPartyDelete = setStatus(200,{})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    thirdPartyDelete = setStatus(300, errorIDs)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        thirdPartyDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(thirdPartyDelete), content_type='application/json')


def thirdPartyUpdate(request):
    try:
        if isTokenExpired(request):
            thirdPartyUpdate = {}
            json2Dict = json.loads(request.body)
            identifier = json2Dict['identifier']
            supCtos = Supcto.objects.filter(identifier=identifier)
            if len(supCtos) > 0:
                supCto = supCtos[0]
                if 'classificationID' in json2Dict:
                    if isValid(json2Dict['classificationID']):
                        classification_id = json2Dict['classificationID']
                        supCto.classification_id = classification_id
                if 'name' in json2Dict:
                    if isValid(json2Dict['name']):
                        name = json2Dict['name']
                        supCto.name = name
                if 'fullName' in json2Dict:
                    if isValid(json2Dict['fullName']):
                        full_name = json2Dict['fullName']
                        supCto.full_name = full_name
                if 'frade' in json2Dict:
                    if isValid(json2Dict['frade']):
                        frade = json2Dict['frade']
                        supCto.frade = frade
                if 'fromType' in json2Dict:
                    if isValid(json2Dict['fromType']):
                        from_type = json2Dict['fromType']
                        supCto.from_type = from_type
                if 'settlementTypeID' in json2Dict:
                    if isValid(json2Dict['settlementTypeID']):
                        settlement_type_id = json2Dict['settlementTypeID']
                        supCto.settlement_type_id = settlement_type_id
                if 'phone' in json2Dict:
                    if isValid(json2Dict['phone']):
                        phone = json2Dict['phone']
                        supCto.phone = phone
                if 'contactPeople' in json2Dict:
                    if isValid(json2Dict['contactPeople']):
                        contact_people = json2Dict['contactPeople']
                        supCto.contact_people = contact_people
                if 'postcode' in json2Dict:
                    if isValid(json2Dict['postcode']):
                        postcode = json2Dict['postcode']
                        supCto.postcode = postcode
                if 'fax' in json2Dict:
                    if isValid(json2Dict['fax']):
                        fax = json2Dict['fax']
                        supCto.fax = fax
                if 'bankAccount' in json2Dict:
                    if isValid(json2Dict['bankAccount']):
                        bank_account = json2Dict['bankAccount']
                        supCto.bank_account = bank_account
                if 'bank' in json2Dict:
                    if isValid(json2Dict['bank']):
                        bank = json2Dict['bank']
                        supCto.bank = bank
                if 'ratepaying' in json2Dict:
                    if isValid(json2Dict['ratepaying']):
                        ratepaying = json2Dict['ratepaying']
                        supCto.ratepaying = ratepaying
                if 'mailbox' in json2Dict:
                    if isValid(json2Dict['mailbox']):
                        mailbox = json2Dict['mailbox']
                        supCto.mailbox = mailbox
                if 'invoiceType' in json2Dict:
                    if isValid(json2Dict['invoiceType']):
                        invoice_type = json2Dict['invoiceType']
                        supCto.invoice_type = invoice_type
                if 'deliveryAddress' in json2Dict:
                    if isValid(json2Dict['deliveryAddress']):
                        delivery_address = json2Dict['deliveryAddress']
                        supCto.delivery_address = delivery_address
                if 'creditDays' in json2Dict:
                    if isValid(json2Dict['creditDays']):
                        credit_days = json2Dict['creditDays']
                        supCto.credit_days = credit_days
                if 'creditMoney' in json2Dict:
                    if isValid(json2Dict['creditMoney']):
                        credit_money = json2Dict['creditMoney']
                        supCto.credit_money = credit_money
                if 'information' in json2Dict:
                    if isValid(json2Dict['information']):
                        information = json2Dict['information']
                        supCto.information = information
                if 'otherInformation' in json2Dict:
                    if isValid(json2Dict['otherInformation']):
                        other_information = json2Dict['otherInformation']
                        supCto.other_information = other_information
                if 'departmentID' in json2Dict:
                    if isValid(json2Dict['departmentID']):
                        department_id = json2Dict['departmentID']
                        supCto.department_id = department_id
                if 'personID' in json2Dict:
                    if isValid(json2Dict['personID']):
                        person_id = json2Dict['personID']
                        supCto.person_id = person_id
                if 'currency' in json2Dict:
                    if isValid(json2Dict['currency']):
                        currency = json2Dict['currency']
                        supCto.currency = currency
                if 'communicationAddress' in json2Dict:
                    if isValid(json2Dict['communicationAddress']):
                        communication_address = json2Dict['communicationAddress']
                        supCto.communication_address = communication_address
                if 'taxes' in json2Dict:
                    if isValid(json2Dict['taxes']):
                        taxes = json2Dict['taxes']
                        supCto.taxes = taxes
                if 'member' in json2Dict:
                    if isValid(json2Dict['member']):
                        member = json2Dict['member']
                        supCto.member = member
                if 'shippingModeID' in json2Dict:
                    if isValid(json2Dict['shippingModeID']):
                        shipping_mode_id = json2Dict['shippingModeID']
                        supCto.shipping_mode_id = shipping_mode_id
                if 'remark' in json2Dict:
                    if isValid(json2Dict['remark']):
                        remark = json2Dict['remark']
                        supCto.remark = remark
                if 'commonPhone' in json2Dict:
                    if isValid(json2Dict['commonPhone']):
                        common_phone = json2Dict['commonPhone']
                        supCto.common_phone = common_phone
                if 'reservePhone' in json2Dict:
                    if isValid(json2Dict['reservePhone']):
                        reserve_phone = json2Dict['reservePhone']
                        supCto.reserve_phone = reserve_phone
                if 'state' in json2Dict:
                    if isValid(json2Dict['state']):
                        state = json2Dict['state']
                        supCto.state = state
                if 'province' in json2Dict:
                    if isValid(json2Dict['province']):
                        province = json2Dict['province']
                        supCto.province = province
                if 'city' in json2Dict:
                    if isValid(json2Dict['city']):
                        city = json2Dict['city']
                        supCto.city = city
                if 'area' in json2Dict:
                    if isValid(json2Dict['area']):
                        area = json2Dict['area']
                        supCto.area = area
                if 'customerOrSupplier' in json2Dict:
                    customer_or_supplier = int(json2Dict['customerOrSupplier'])
                    if supCto.customer_or_supplier != customer_or_supplier:
                        if customer_or_supplier  == 1:
                            identifier = 'CTO' + supCto.identifier[3:]
                            supCto.identifier = identifier
                            supCto.customer_or_supplier = customer_or_supplier
                        elif customer_or_supplier  == 2:
                            identifier = 'SUP' + supCto.identifier[3:]
                            supCto.identifier = identifier
                            supCto.customer_or_supplier = customer_or_supplier
                        else:
                            pass
                supCto.operator_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if 'operatorIdentifier' in json2Dict:
                    if isValid(json2Dict['operatorIdentifier']):
                        operator_identifier = json2Dict['operatorIdentifier']
                        supCto.operator_identifier = operator_identifier
                if 'provinceCode' in json2Dict:
                    if isValid(json2Dict['provinceCode']):
                        province_code = json2Dict['provinceCode']
                        supCto.province_code = province_code
                if 'cityCode' in json2Dict:
                    if isValid(json2Dict['cityCode']):
                        city_code = json2Dict['cityCode']
                        supCto.city_code = city_code
                if 'areaCode' in json2Dict:
                    if isValid(json2Dict['areaCode']):
                        area_code = json2Dict['areaCode']
                        supCto.area_code = area_code
                if 'website' in json2Dict:
                    if isValid(json2Dict['website']):
                        website = json2Dict['website']
                        supCto.website = website
                if 'memoryCode' in json2Dict:
                    if isValid(json2Dict['memoryCode']):
                        memory_code = json2Dict['memoryCode']
                        supCto.memory_code = memory_code
                if 'useable' in json2Dict:
                    if isValid(json2Dict['useable']):
                        useable = json2Dict['useable']
                        supCto.useable = useable
                if 'advanceMoney' in json2Dict:
                    if isValid(json2Dict['advanceMoney']):
                        advance_money = json2Dict['advanceMoney']
                        supCto.advance_money = advance_money
                if 'isShow' in json2Dict:
                    if isValid(json2Dict['isShow']):
                        is_show = json2Dict['isShow']
                        supCto.is_show = is_show
                if 'parentID' in json2Dict:
                    if isValid(json2Dict['parentID']):
                        parent_id = json2Dict['parentID']
                        supCto.parent_id = parent_id
                supCto.save()
                if 'commodityList' in json2Dict:
                    commodity_list = json2Dict['commodityList']
                    for commodity in commodity_list:
                        if 'supctoCommodityID' in commodity:
                            supcto_commodity_id = commodity['supctoCommodityID']
                            supctoCommodity = SupctoCommodity.objects.get(id=supcto_commodity_id)
                            if 'commodityID' in commodity:
                                if isValid(commodity['commodityID']):
                                    commodity_id = commodity['commodityID']
                                    supctoCommodity.commodity_id = commodity_id
                            if 'price' in commodity:
                                if isValid(commodity['price']):
                                    price = commodity['price']
                                    supctoCommodity.price = price
                            if 'supctoID' in commodity:
                                if isValid(commodity['supctoID']):
                                    supcto_id = commodity['supctoID']
                                    supctoCommodity.supcto_id = supcto_id
                            supctoCommodity.save()
                        else:
                            continue
                supCtoJSON = getSupCto(supCto)
                thirdPartyUpdate = setStatus(200,supCtoJSON)
            else:
                thirdPartyUpdate = setStatus(300,{})
                return HttpResponse(json.dumps(thirdPartyUpdate), content_type='application/json')
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        thirdPartyUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(thirdPartyUpdate), content_type='application/json')


def thirdPartySelect(request):
    try:
        if isTokenExpired(request):
            thirdPartySelect = {}
            condition = {}
            selectType = {}
            if len(request.GET) > 0:
                if 'name' in request.GET and isValid(request.GET['name']):
                    name = request.GET['name']
                    condition['name'] = name
                if 'fromType' in request.GET and isValid(request.GET['fromType']):
                    from_type = request.GET['fromType']
                    condition['from_type'] = from_type
                if 'queryTime' in request.GET:
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                if 'state' in request.GET and isValid(request.GET['state']):
                    state = request.GET['state']
                    condition['state'] = state
                if 'province' in request.GET and isValid(request.GET['province']):
                    province = request.GET['province']
                    condition['province'] = province
                if 'city' in request.GET and isValid(request.GET['city']):
                    city = request.GET['city']
                    condition['city'] = city
                if 'area' in request.GET and isValid(request.GET['area']):
                    area = request.GET['area']
                    condition['area'] = area
                if 'classificationID' in request.GET and isValid(request.GET['classificationID']):
                    classificationID = int(request.GET['classificationID'])
                    condition['classification_id'] = classificationID
                thirdPartySelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                thirdPartySelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        thirdPartySelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(thirdPartySelect), content_type='application/json')


def thirdPartySingleSelect(request):
    try:
        if isTokenExpired(request):
            thirdPartySingleSelect = {}
            identifier = request.GET['identifier']
            supCtos = Supcto.objects.filter(identifier=identifier)
            if len(supCtos) > 0:
                supCto = supCtos[0]
                supCtoJSON = getSupCto(supCto)
                thirdPartySingleSelect = setStatus(200,supCtoJSON)
            else:
                thirdPartySingleSelect = setStatus(300,{})
                return HttpResponse(json.dumps(thirdPartySingleSelect), content_type='application/json')
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        thirdPartySingleSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(thirdPartySingleSelect), content_type='application/json')


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
        basicsCount = Supcto.objects.all().count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = Supcto.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo)).count()
        else:
            basicsCount = Supcto.objects.filter(**condition).count()
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
        basicObjs = Supcto.objects.all()[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = Supcto.objects.filter(Q(**condition) & Q(operator_time__gte=timeFrom) & Q(operator_time__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = Supcto.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicObjJSON = getSupCto(basicObj)
        datasJSON.append(basicObjJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect


def getSupCto(supCto):
    supCtoJSON = {}
    supCtoJSON['supCtoID'] = supCto.id
    supCtoJSON['classificationID'] = supCto.classification_id
    supCtoJSON['name'] = supCto.name
    supCtoJSON['fullName'] = supCto.full_name
    supCtoJSON['frade'] = supCto.frade
    supCtoJSON['fromType'] = supCto.from_type
    supCtoJSON['settlementTypeID'] = supCto.settlement_type_id
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
    supCtoJSON['departmentID'] = supCto.department_id
    supCtoJSON['personID'] = supCto.person_id
    supCtoJSON['currency'] = supCto.currency
    supCtoJSON['communication_address'] = supCto.communication_address
    supCtoJSON['taxes'] = supCto.taxes
    supCtoJSON['member'] = supCto.member
    supCtoJSON['shippingModeID'] = supCto.shipping_mode_id
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
    supCtoJSON['parentID'] = supCto.parent_id
    commodityList = []
    supctoCommodities = SupctoCommodity.objects.filter(supcto_id=supCto.id)
    for supctoCommodity in supctoCommodities:
        supctoCommodityJSON = {}
        supctoCommodityJSON['commodityID'] = supctoCommodity.commodity_id
        supctoCommodityJSON['price'] = supctoCommodity.price
        commodityList.append(supctoCommodityJSON)
    supCtoJSON['commodityList'] = commodityList
    return supCtoJSON
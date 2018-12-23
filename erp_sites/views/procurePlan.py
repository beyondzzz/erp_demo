#!usr/bin/python#coding=utf-8

import json,sys,time,datetime,base64
from string import upper, atof
from django.db import transaction,connection
from django.http import HttpResponse
from erp_sites import basic_log
from erp_sites.public import setStatus,isTokenExpired,notTokenExpired,touchFile,getProcure,isValid,toStream
import traceback
from erp_sites.models import ProcureTable,ProcureCommodity
from django.db.models import Q
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph,Image,Table,TableStyle

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
reload(sys)
sys.setdefaultencoding('utf-8')
ONE_PAGE_OF_DATA = 10
logRecord = basic_log.Logger('record')

def procurePlanInsert(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            generate_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            identifier = 'PO-' + generate_date[0:10] + '-'
            if 'supctoID' in json2Dict:
                if isValid(json2Dict['supctoID']):
                    supcto_id = int(json2Dict['supctoID'])
                else:
                    supcto_id = 0
            else:
                supcto_id = 0
            if 'effectivePeriodEnd' in json2Dict:
                if isValid(json2Dict['effectivePeriodEnd']):
                    effective_period_end_str = json2Dict['effectivePeriodEnd']
                    effective_period_end = time.strptime(effective_period_end_str, '%Y-%m-%d')
                    effective_period_end = datetime.datetime(*effective_period_end[:3]).date()
                else:
                    effective_period_end = None
            else:
                effective_period_end = None
            if 'goodsArrivalTime' in json2Dict:
                if isValid(json2Dict['goodsArrivalTime']):
                    goods_arrival_time_str = json2Dict['goodsArrivalTime']
                    goods_arrival_time = time.strptime(goods_arrival_time_str, '%Y-%m-%d')
                    goods_arrival_time = datetime.datetime(*goods_arrival_time[:3]).date()
                else:
                    goods_arrival_time = None
            else:
                goods_arrival_time = None
            if 'goodsArrivalPlace' in json2Dict:
                if isValid(json2Dict['goodsArrivalPlace']):
                    goods_arrival_place = json2Dict['goodsArrivalPlace']
                else:
                    goods_arrival_place = None
            else:
                goods_arrival_place = None
            if 'transportationMode' in json2Dict:
                if isValid(json2Dict['transportationMode']):
                    transportation_mode = int(json2Dict['transportationMode'])
                else:
                    transportation_mode = 0
            else:
                transportation_mode = 0
            if 'deliveryman' in json2Dict:
                if isValid(json2Dict['deliveryman']):
                    deliveryman = json2Dict['deliveryman']
                else:
                    deliveryman = None
            else:
                deliveryman = None
            if 'fax' in json2Dict:
                if isValid(json2Dict['fax']):
                    fax = json2Dict['fax']
                else:
                    fax = None
            else:
                fax = None
            if 'phone' in json2Dict:
                if isValid(json2Dict['phone']):
                    phone = json2Dict['phone']
                else:
                    phone = None
            else:
                phone = None
            if 'orderer' in json2Dict:
                if isValid(json2Dict['orderer']):
                    orderer = json2Dict['orderer']
                else:
                    orderer = None
            else:
                orderer = None
            if 'prepaidAmount' in json2Dict:
                if isValid(json2Dict['prepaidAmount']):
                    prepaid_amount = atof(json2Dict['prepaidAmount'])
                else:
                    prepaid_amount = 0
            else:
                prepaid_amount = 0
            if 'departmentID' in json2Dict:
                if isValid(json2Dict['departmentID']):
                    department_id = int(json2Dict['departmentID'])
                else:
                    department_id = 0
            else:
                department_id = 0
            if 'originator' in json2Dict:
                if isValid(json2Dict['originator']):
                    originator = json2Dict['originator']
                else:
                    originator = None
            else:
                originator = None
            if 'reviewer' in json2Dict:
                if isValid(json2Dict['reviewer']):
                    reviewer = json2Dict['reviewer']
                else:
                    reviewer = None
            else:
                reviewer = None
            if 'terminator' in json2Dict:
                if isValid(json2Dict['terminator']):
                    terminator = json2Dict['terminator']
                else:
                    terminator = None
            else:
                terminator = None
            if 'summary' in json2Dict:
                if isValid(json2Dict['summary']):
                    summary = json2Dict['summary']
                else:
                    summary = None
            else:
                summary = None
            if 'branch' in json2Dict:
                if isValid(json2Dict['branch']):
                    branch = json2Dict['branch']
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
            if 'printNum' in json2Dict:
                if isValid(json2Dict['printNum']):
                    print_num = int(json2Dict['printNum'])
                else:
                    print_num = 0
            else:
                print_num = 0
            if 'planType' in json2Dict:
                if isValid(json2Dict['planType']):
                    plan_type = int(json2Dict['planType'])
                else:
                    plan_type = 0
            else:
                plan_type = 0
            if 'payType' in json2Dict:
                if isValid(json2Dict['payType']):
                    pay_type = int(json2Dict['payType'])
                else:
                    pay_type = 0
            else:
                pay_type = 0
            if 'contractNumber' in json2Dict:
                if isValid(json2Dict['contractNumber']):
                    contract_number = json2Dict['contractNumber']
                else:
                    contract_number = None
            else:
                contract_number = None
            if 'planOrOrder' in json2Dict:
                if isValid(json2Dict['planOrOrder']):
                    plan_or_order = int(json2Dict['planOrOrder'])
                else:
                    plan_or_order = 0
            else:
                plan_or_order = 0
            if 'beforeIsPlan' in json2Dict:
                if isValid(json2Dict['beforeIsPlan']):
                    before_is_plan = int(json2Dict['beforeIsPlan'])
                else:
                    before_is_plan = 0
            else:
                before_is_plan = 0
            if 'paymentEvidence1' in json2Dict:
                if isValid(json2Dict['paymentEvidence1']):
                    payment_evidence1 = json2Dict['paymentEvidence1']
                else:
                    payment_evidence1 = None
            else:
                payment_evidence1 = None
            if 'paymentEvidence2' in json2Dict:
                if isValid(json2Dict['paymentEvidence2']):
                    payment_evidence2 = json2Dict['paymentEvidence2']
                else:
                    payment_evidence2 = None
            else:
                payment_evidence2 = None
            if 'paymentEvidence3' in json2Dict:
                if isValid(json2Dict['paymentEvidence3']):
                    payment_evidence3 = json2Dict['paymentEvidence3']
                else:
                    payment_evidence3 = None
            else:
                payment_evidence3 = None
            if 'paymentEvidence4' in json2Dict:
                if isValid(json2Dict['paymentEvidence4']):
                    payment_evidence4 = json2Dict['paymentEvidence4']
                else:
                    payment_evidence4 = None
            else:
                payment_evidence4 = None
            if 'paymentEvidence5' in json2Dict:
                if isValid(json2Dict['paymentEvidence5']):
                    payment_evidence5 = json2Dict['paymentEvidence5']
                else:
                    payment_evidence5 = None
            else:
                payment_evidence5 = None
            if 'paymentEvidence6' in json2Dict:
                if isValid(json2Dict['paymentEvidence6']):
                    payment_evidence6 = json2Dict['paymentEvidence6']
                else:
                    payment_evidence6 = None
            else:
                payment_evidence6 = None
            is_delete = 0
            if 'parentID' in json2Dict:
                if isValid(json2Dict['parentID']):
                    parent_id = int(json2Dict['parentID'])
                else:
                    parent_id = 0
            else:
                parent_id = 0
            if 'orderType' in json2Dict:
                if isValid(json2Dict['orderType']):
                    order_type = int(json2Dict['orderType'])
                else:
                    order_type = 0
            else:
                order_type = 0
            if 'postfix' in json2Dict:
                if isValid(json2Dict['postfix']):
                    postfix = int(json2Dict['postfix'])
                else:
                    postfix = 0
            else:
                postfix = 0
            if 'isVerification' in json2Dict:
                if isValid(json2Dict['isVerification']):
                    is_verification = json2Dict['isVerification']
                else:
                    is_verification = None
            else:
                is_verification = None
            if 'activityID' in json2Dict:
                if isValid(json2Dict['activityID']):
                    activity_id = int(json2Dict['activityID'])
                else:
                    activity_id = 0
            else:
                activity_id = 0
            if 'isAppOrder' in json2Dict:
                if isValid(json2Dict['isAppOrder']):
                    is_app_order = int(json2Dict['isAppOrder'])
                else:
                    is_app_order = 0
            else:
                is_app_order = 0
            if 'financialReviewer' in json2Dict:
                if isValid(json2Dict['financialReviewer']):
                    financial_reviewer = json2Dict['financialReviewer']
                else:
                    financial_reviewer = None
            else:
                financial_reviewer = None
            if 'isOtherReceipts' in json2Dict:
                if isValid(json2Dict['isOtherReceipts']):
                    is_other_receipts = int(json2Dict['isOtherReceipts'])
                else:
                    is_other_receipts = 0
            else:
                is_other_receipts = 0
            procure = ProcureTable(None,identifier,generate_date,supcto_id,effective_period_end,goods_arrival_time,goods_arrival_place,transportation_mode,deliveryman,fax,phone,orderer,prepaid_amount,department_id,originator,reviewer,terminator,summary,branch,state,print_num,plan_type,pay_type,contract_number,plan_or_order,before_is_plan,payment_evidence1,payment_evidence2,payment_evidence3,payment_evidence4,payment_evidence5,payment_evidence6,is_delete,parent_id,order_type,postfix,is_verification,activity_id ,is_app_order,financial_reviewer,is_other_receipts)
            procure.save()
            procure.identifier = identifier + str(procure.id)
            procure.save()
            if 'procureCommodities' in json2Dict:

                procure_commodities = json2Dict['procureCommodities']
                logRecord.log("debug:" + str(procure_commodities))
                for procure_commodity in procure_commodities:
                    if 'specificationID' in procure_commodity:
                        if isValid(procure_commodity['specificationID']):
                            commodity_id = int(procure_commodity['specificationID'])
                        else:
                            commodity_id = 0
                    else:
                        commodity_id = 0
                    procure_table_id = procure.id
                    if 'taxRate' in procure_commodity:
                        if isValid(procure_commodity['taxRate']):
                            tax_rate = atof(procure_commodity['taxRate'])
                        else:
                            tax_rate = 0.0
                    else:
                        tax_rate = 0.0
                    if 'amountOfTax' in procure_commodity:
                        if isValid(procure_commodity['amountOfTax']):
                            amount_of_tax = atof(procure_commodity['amountOfTax'])
                        else:
                            amount_of_tax = 0.0
                    else:
                        amount_of_tax = 0.0
                    if 'totalTaxPrice' in procure_commodity:
                        if isValid(procure_commodity['totalTaxPrice']):
                            total_tax_price = atof(procure_commodity['totalTaxPrice'])
                        else:
                            total_tax_price = 0.0
                    else:
                        total_tax_price = 0.0
                    if 'orderNum' in procure_commodity:
                        if isValid(procure_commodity['orderNum']):
                            order_num = int(procure_commodity['orderNum'])
                        else:
                            order_num = 0
                    else:
                        order_num = 0
                    if 'lotNumber' in procure_commodity:
                        if isValid(procure_commodity['lotNumber']):
                            lot_number = procure_commodity['lotNumber']
                        else:
                            lot_number = None
                    else:
                        lot_number = None
                    if 'arrivalQuantity' in procure_commodity:
                        if isValid(procure_commodity['arrivalQuantity']):
                            arrival_quantity = int(procure_commodity['arrivalQuantity'])
                        else:
                            arrival_quantity = 0
                    else:
                        arrival_quantity = 0
                    if 'suspendQuantity' in procure_commodity:
                        if isValid(procure_commodity['suspendQuantity']):
                            suspend_quantity = int(procure_commodity['suspendQuantity'])
                        else:
                            suspend_quantity = 0
                    else:
                        suspend_quantity = 0
                    if 'suspendPrice' in procure_commodity:
                        if isValid(procure_commodity['suspendPrice']):
                            suspend_price = atof(procure_commodity['suspendPrice'])
                        else:
                            suspend_price = 0.0
                    else:
                        suspend_price = 0.0
                    if 'discount' in procure_commodity:
                        if isValid(procure_commodity['discount']):
                            discount = int(procure_commodity['discount'])
                        else:
                            discount = 0
                    else:
                        discount = 0
                    if 'isLargess' in procure_commodity:
                        if isValid(procure_commodity['isLargess']):
                            is_largess = int(procure_commodity['isLargess'])
                        else:
                            is_largess = 0
                    else:
                        is_largess = 0
                    if 'originalUnitPrice' in procure_commodity:
                        if isValid(procure_commodity['originalUnitPrice']):
                            original_unit_price = atof(procure_commodity['originalUnitPrice'])
                        else:
                            original_unit_price = 0.0
                    else:
                        original_unit_price = 0.0
                    if 'businessUnitPrice' in procure_commodity:
                        if isValid(procure_commodity['businessUnitPrice']):
                            business_unit_price = atof(procure_commodity['businessUnitPrice'])
                        else:
                            business_unit_price = 0.0
                    else:
                        business_unit_price = 0.0
                    if 'remarks' in procure_commodity:
                        if isValid(procure_commodity['remarks']):
                            remarks = procure_commodity['remarks']
                        else:
                            remarks = None
                    else:
                        remarks = None
                    if 'containsTaxPrice' in procure_commodity:
                        if isValid(procure_commodity['containsTaxPrice']):
                            contains_tax_price = atof(procure_commodity['containsTaxPrice'])
                        else:
                            contains_tax_price = 0.0
                    else:
                        contains_tax_price = 0.0
                    if 'paymentForGoods' in procure_commodity:
                        if isValid(procure_commodity['paymentForGoods']):
                            payment_for_goods = atof(procure_commodity['paymentForGoods'])
                        else:
                            payment_for_goods = 0.0
                    else:
                        payment_for_goods = 0.0
                    if 'totalPrice' in procure_commodity:
                        if isValid(procure_commodity['totalPrice']):
                            total_price = atof(procure_commodity['totalPrice'])
                        else:
                            total_price = 0.0
                    else:
                        total_price = 0.0
                    is_delete = 0
                    procureCommodity = ProcureCommodity(None,commodity_id,procure_table_id,tax_rate,amount_of_tax,total_tax_price,order_num,lot_number,arrival_quantity,suspend_quantity,suspend_price,discount,is_largess,original_unit_price,business_unit_price,remarks,contains_tax_price,payment_for_goods,total_price,is_delete)
                    procureCommodity.save()
            procureJSON = getProcure(procure)
            procurePlanInsert = setStatus(200,procureJSON)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        procurePlanInsert = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(procurePlanInsert), content_type='application/json')


def procurePlanDelete(request):
    try:
        if isTokenExpired(request):
            json2Dict = json.loads(request.body)
            identifiers = int(json2Dict['identifiers'])
            errorIDs = []
            for identifier in identifiers:
                identifier = int(identifier)
                procureTables = ProcureTable.objects.filter(id=identifier)
                if len(procureTables) > 0:
                    procureTable = procureTables[0]
                    procureTable.is_delete = 1
                    procureTable.save()
                    procurePlanDelete = setStatus(200,{})
                else:
                    errorIDs.append(identifier)
                if len(errorIDs) > 0:
                    procurePlanDelete = setStatus(300, errorIDs)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        procurePlanDelete = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(procurePlanDelete), content_type='application/json')


def procurePlanUpdate(request):
    try:
        if isTokenExpired(request):
            jsonList = json.loads(request.body)
            for json2Dict in jsonList:
                identifier = json2Dict['identifier']
                procures = ProcureTable.objects.filter(identifier=identifier)
                if len(procures) > 0:
                    procure = procures[0]
                else:
                    procurePlanUpdate = setStatus(300, {})
                    return HttpResponse(json.dumps(procurePlanUpdate), content_type='application/json')
                if 'supctoID' in json2Dict:
                    if isValid(json2Dict['supctoID']):
                        supcto_id = int(json2Dict['supctoID'])
                        procure.supcto_id = supcto_id
                if 'effectivePeriodEnd' in json2Dict:
                    if isValid(json2Dict['effectivePeriodEnd']):
                        effective_period_end_str = json2Dict['effectivePeriodEnd']
                        effective_period_end = time.strptime(effective_period_end_str, '%Y-%m-%d')
                        effective_period_end = datetime.datetime(*effective_period_end[:3]).date()
                        procure.effective_period_end = effective_period_end
                if 'goodsArrivalTime' in json2Dict:
                     if isValid(json2Dict['goodsArrivalTime']):
                         goods_arrival_time_str = json2Dict['goodsArrivalTime']
                         goods_arrival_time = time.strptime(goods_arrival_time_str, '%Y-%m-%d')
                         goods_arrival_time = datetime.datetime(*goods_arrival_time[:3]).date()
                         procure.goods_arrival_time = goods_arrival_time
                if 'goodsArrivalPlace' in json2Dict:
                    if isValid(json2Dict['goodsArrivalPlace']):
                        goods_arrival_place = json2Dict['goodsArrivalPlace']
                        procure.goods_arrival_place = goods_arrival_place
                if 'transportationMode' in json2Dict:
                    if isValid(json2Dict['transportationMode']):
                        transportation_mode = int(json2Dict['transportationMode'])
                        procure.transportation_mode = transportation_mode
                if 'deliveryman' in json2Dict:
                    if isValid(json2Dict['deliveryman']):
                        deliveryman = json2Dict['deliveryman']
                        procure.deliveryman = deliveryman
                if 'fax' in json2Dict:
                    if isValid(json2Dict['fax']):
                        fax = json2Dict['fax']
                        procure.fax = fax
                if 'phone' in json2Dict:
                    if isValid(json2Dict['phone']):
                        phone = json2Dict['phone']
                        procure.phone = phone
                if 'orderer' in json2Dict:
                    if isValid(json2Dict['orderer']):
                        orderer = json2Dict['orderer']
                        procure.orderer = orderer
                if 'prepaidAmount' in json2Dict:
                    if isValid(json2Dict['prepaidAmount']):
                        prepaid_amount = atof(json2Dict['prepaidAmount'])
                        procure.prepaid_amount = prepaid_amount
                if 'departmentID' in json2Dict:
                    if isValid(json2Dict['departmentID']):
                        department_id = int(json2Dict['departmentID'])
                        procure.department_id = department_id
                if 'originator' in json2Dict:
                    if isValid(json2Dict['originator']):
                        originator = json2Dict['originator']
                        procure.originator = originator
                if 'reviewer' in json2Dict:
                    if isValid(json2Dict['reviewer']):
                        reviewer = json2Dict['reviewer']
                        procure.reviewer = reviewer
                if 'terminator' in json2Dict:
                    if isValid(json2Dict['terminator']):
                        terminator = json2Dict['terminator']
                        procure.terminator = terminator
                if 'summary' in json2Dict:
                    if isValid(json2Dict['summary']):
                        summary = json2Dict['summary']
                        procure.summary = summary
                if 'branch' in json2Dict:
                    if isValid(json2Dict['branch']):
                        branch = json2Dict['branch']
                        procure.branch = branch
                if 'state' in json2Dict:
                    if isValid(json2Dict['state']):
                        state = int(json2Dict['state'])
                        procure.state = state
                if 'printNum' in json2Dict:
                    if isValid(json2Dict['printNum']):
                        print_num = int(json2Dict['printNum'])
                        procure.print_num = print_num
                if 'planType' in json2Dict:
                    if isValid(json2Dict['planType']):
                        plan_type = int(json2Dict['planType'])
                        procure.plan_type = plan_type
                if 'payType' in json2Dict:
                    if isValid(json2Dict['payType']):
                        pay_type = int(json2Dict['payType'])
                        procure.pay_type = pay_type
                if 'contractNumber' in json2Dict:
                    if isValid(json2Dict['contractNumber']):
                        contract_number = json2Dict['contractNumber']
                        procure.contract_number = contract_number
                if 'planOrOrder' in json2Dict:
                    if isValid(json2Dict['planOrOrder']):
                        plan_or_order = int(json2Dict['planOrOrder'])
                        procure.plan_or_order = plan_or_order
                if 'beforeIsPlan' in json2Dict:
                    if isValid(json2Dict['beforeIsPlan']):
                        before_is_plan = int(json2Dict['beforeIsPlan'])
                        procure.before_is_plan = before_is_plan
                if 'paymentEvidence1' in json2Dict:
                    if isValid(json2Dict['paymentEvidence1']):
                        payment_evidence1 = json2Dict['paymentEvidence1']
                        procure.payment_evidence1 = payment_evidence1
                if 'paymentEvidence2' in json2Dict:
                    if isValid(json2Dict['paymentEvidence2']):
                        payment_evidence2 = json2Dict['paymentEvidence2']
                        procure.payment_evidence2 = payment_evidence2
                if 'paymentEvidence3' in json2Dict:
                    if isValid(json2Dict['paymentEvidence3']):
                        payment_evidence3 = json2Dict['paymentEvidence3']
                        procure.payment_evidence3 = payment_evidence3
                if 'paymentEvidence4' in json2Dict:
                    if isValid(json2Dict['paymentEvidence4']):
                        payment_evidence4 = json2Dict['paymentEvidence4']
                        procure.payment_evidence4 = payment_evidence4
                if 'paymentEvidence5' in json2Dict:
                    if isValid(json2Dict['paymentEvidence5']):
                        payment_evidence5 = json2Dict['paymentEvidence5']
                        procure.payment_evidence5 = payment_evidence5
                if 'paymentEvidence6' in json2Dict:
                    if isValid(json2Dict['paymentEvidence6']):
                        payment_evidence6 = json2Dict['paymentEvidence6']
                        procure.payment_evidence6 = payment_evidence6
                if 'parentID' in json2Dict:
                    if isValid(json2Dict['parentID']):
                        parent_id = int(json2Dict['parentID'])
                        procure.parent_id = parent_id
                if 'order_type' in json2Dict:
                    if isValid(json2Dict['order_type']):
                        orderType = int(json2Dict['orderType'])
                        procure.order_type = orderType
                if 'postfix' in json2Dict:
                    if isValid(json2Dict['postfix']):
                        postfix = int(json2Dict['postfix'])
                        procure.postfix = postfix
                if 'isVerification' in json2Dict:
                    if isValid(json2Dict['isVerification']):
                        is_verification = json2Dict['isVerification']
                        procure.is_verification = is_verification
                if 'activityID' in json2Dict:
                    if isValid(json2Dict['activityID']):
                        activity_id = int(json2Dict['activityID'])
                        procure.activity_id = activity_id
                if 'isAppOrder' in json2Dict:
                    if isValid(json2Dict['isAppOrder']):
                        is_app_order = int(json2Dict['isAppOrder'])
                        procure.is_app_order = is_app_order
                if 'financialReviewer' in json2Dict:
                    if isValid(json2Dict['financialReviewer']):
                        financial_reviewer = json2Dict['financialReviewer']
                        procure.financial_reviewer = financial_reviewer
                if 'isOtherReceipts' in json2Dict:
                    if isValid(json2Dict['isOtherReceipts']):
                        is_other_receipts = int(json2Dict['isOtherReceipts'])
                        procure.is_other_receipts = is_other_receipts
                procure.save()
                if 'procureCommodities' in json2Dict:
                    procure_commodities = json2Dict['procureCommodities']
                    for procure_commodity in procure_commodities:
                        if 'procureCommodityID' in procure_commodity:
                            procure_commodity_id = procure_commodity['procureCommodityID']
                            procureCommodities = ProcureCommodity.objects.filter(id=procure_commodity_id)
                            if len(procureCommodities) > 0:
                                procureCommodity = procureCommodities[0]
                            else:
                                procurePlanUpdate = setStatus(300, {})
                                return HttpResponse(json.dumps(procurePlanUpdate), content_type='application/json')
                        else:
                            continue
                        if 'commodityID' in procure_commodity:
                            if isValid(procure_commodity['commodityID']):
                                commodity_id = int(procure_commodity['commodityID'])
                                procureCommodity.commodity_id = commodity_id
                        if 'taxRate' in procure_commodity:
                            if isValid(procure_commodity['taxRate']):
                                tax_rate = atof(procure_commodity['taxRate'])
                                procureCommodity.tax_rate = tax_rate
                        if 'amountOfTax' in procure_commodity:
                            if isValid(procure_commodity['amountOfTax']):
                                amount_of_tax = atof(procure_commodity['amountOfTax'])
                                procureCommodity.amount_of_tax = amount_of_tax
                        if 'totalTaxPrice' in procure_commodity:
                            if isValid(procure_commodity['totalTaxPrice']):
                                total_tax_price = atof(procure_commodity['totalTaxPrice'])
                                procureCommodity.total_tax_price = total_tax_price
                        if 'orderNum' in procure_commodity:
                            if isValid(procure_commodity['orderNum']):
                                order_num = int(procure_commodity['orderNum'])
                                procureCommodity.order_num = order_num
                        if 'lotNumber' in procure_commodity:
                            if isValid(procure_commodity['lotNumber']):
                                lot_number = procure_commodity['lotNumber']
                                procureCommodity.lot_number = lot_number
                        if 'arrivalQuantity' in procure_commodity:
                            if isValid(procure_commodity['arrivalQuantity']):
                                arrival_quantity = int(procure_commodity['arrivalQuantity'])
                                procureCommodity.arrival_quantity = arrival_quantity
                        if 'suspendQuantity' in procure_commodity:
                            if isValid(procure_commodity['suspendQuantity']):
                                suspend_quantity = int(procure_commodity['suspendQuantity'])
                                procureCommodity.suspend_quantity = suspend_quantity
                        if 'suspendPrice' in procure_commodity:
                            if isValid(procure_commodity['suspendPrice']):
                                suspend_price = atof(procure_commodity['suspendPrice'])
                                procureCommodity.suspend_price = suspend_price
                        if 'discount' in procure_commodity:
                            if isValid(procure_commodity['discount']):
                                discount = int(procure_commodity['discount'])
                                procureCommodity.discount = discount
                        if 'isLargess' in procure_commodity:
                            if isValid(procure_commodity['isLargess']):
                                is_largess = int(procure_commodity['isLargess'])
                                procureCommodity.is_largess = is_largess
                        if 'originalUnitPrice' in procure_commodity:
                            if isValid(procure_commodity['originalUnitPrice']):
                                original_unit_price = atof(procure_commodity['originalUnitPrice'])
                                procureCommodity.original_unit_price = original_unit_price
                        if 'businessUnitPrice' in procure_commodity:
                            if isValid(procure_commodity['businessUnitPrice']):
                                business_unit_price = atof(procure_commodity['businessUnitPrice'])
                                procureCommodity.business_unit_price = business_unit_price
                        if 'remarks' in procure_commodity:
                            if isValid(procure_commodity['remarks']):
                                remarks = procure_commodity['remarks']
                                procureCommodity.remarks = remarks
                        if 'containsTaxPrice' in procure_commodity:
                            if isValid(procure_commodity['containsTaxPrice']):
                                contains_tax_price = atof(procure_commodity['containsTaxPrice'])
                                procureCommodity.contains_tax_price = contains_tax_price
                        if 'paymentForGoods' in procure_commodity:
                            if isValid(procure_commodity['paymentForGoods']):
                                payment_for_goods = atof(procure_commodity['paymentForGoods'])
                                procureCommodity.payment_for_goods = payment_for_goods
                        if 'totalPrice' in procure_commodity:
                            if isValid(procure_commodity['totalPrice']):
                                total_price = atof(procure_commodity['totalPrice'])
                                procureCommodity.total_price = total_price
                        procureCommodity.save()
                #procureJSON = getProcure(procure)
            procurePlanUpdate = setStatus(200,{})
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        procurePlanUpdate = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(procurePlanUpdate), content_type='application/json')


def procurePlanSelect(request):
    try:
        if isTokenExpired(request):
            if len(request.GET) > 0:
                condition = {}
                selectType = {}
                if 'identifier' in request.GET and isValid(request.GET['identifier']):
                    condition['identifier'] = request.GET['identifier']
                if 'supctoID' in request.GET and isValid(request.GET['supctoID']):
                    condition['supcto_id'] = int(request.GET['supctoID'])
                if 'commodityID' in request.GET and isValid(request.GET['commodityID']):
                    condition['commodity_id'] = int(request.GET['commodityID'])
                if 'planOrOrder' in request.GET and isValid(request.GET['planOrOrder']):
                    condition['plan_or_order'] = int(request.GET['planOrOrder'])
                if 'state' in request.GET and isValid(request.GET['state']):
                    condition['state__in'] = request.GET['state'].split(",")
                condition['is_delete'] = 0
                if 'queryTime' in request.GET and isValid(request.GET['queryTime']):
                    queryTime = request.GET['queryTime']
                    timeFrom = queryTime.split('~')[0].strip()
                    timeTo = queryTime.split('~')[1].strip()
                    selectType['timeFrom'] = timeFrom + ' 00:00:00'
                    selectType['timeTo'] = timeTo + ' 23:59:59'
                if 'noPaging' in request.GET and request.GET['noPaging'] == "true":
                    procurePlanSelect = conditionSelect(condition, selectType)
                else:
                    procurePlanSelect = paging(request, ONE_PAGE_OF_DATA, condition, selectType)
            else:
                procurePlanSelect = paging(request, ONE_PAGE_OF_DATA, None, None)
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        procurePlanSelect = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(procurePlanSelect), content_type='application/json')


def procureUpload(request):
    try:
        if isTokenExpired(request):
            if request.method == 'POST':
                procureFiles = {}
                identifier = request.POST['identifier']
                procures = ProcureTable.objects.filter(identifier=identifier)
                uploadDate = time.strftime("%Y-%m-%d",time.localtime(time.time()))
                modelType = 'procure'
                fileType = 'paymentEvidence'
                if len(procures) > 0:
                    procure = procures[0]
                else:
                    procureUpload = setStatus(300,{})
                    return HttpResponse(json.dumps(procureUpload), content_type='application/json')
                if 'paymentEvidence1' in request.FILES:
                    file = request.FILES['paymentEvidence1']
                    fileName = file.name.split('.')[0] + '_1.' + file.name.split('.')[1]
                    filePath = touchFile(file,modelType,fileType,str(uploadDate),fileName)
                    if filePath != None:
                        procureFiles['paymentEvidence1'] = filePath
                if 'paymentEvidence2' in request.FILES:
                    file = request.FILES['paymentEvidence2']
                    fileName = file.name.split('.')[0] + '_2.' + file.name.split('.')[1]
                    filePath = touchFile(file,modelType,fileType,str(uploadDate),fileName)
                    if filePath != None:
                        procureFiles['paymentEvidence2'] = filePath
                if 'paymentEvidence3' in request.FILES:
                    file = request.FILES['paymentEvidence3']
                    fileName = file.name.split('.')[0] + '_3.' + file.name.split('.')[1]
                    filePath = touchFile(file,modelType,fileType,str(uploadDate),fileName)
                    if filePath != None:
                        procureFiles['paymentEvidence3'] = filePath
                if 'paymentEvidence4' in request.FILES:
                    file = request.FILES['paymentEvidence4']
                    fileName = file.name.split('.')[0] + '_4.' + file.name.split('.')[1]
                    filePath = touchFile(file,modelType,fileType,str(uploadDate),fileName)
                    if filePath != None:
                        procureFiles['paymentEvidence4'] = filePath
                if 'paymentEvidence5' in request.FILES:
                    file = request.FILES['paymentEvidence5']
                    fileName = file.name.split('.')[0] + '_5.' + file.name.split('.')[1]
                    filePath = touchFile(file,modelType,fileType,str(uploadDate),fileName)
                    if filePath != None:
                        procureFiles['paymentEvidence5'] = filePath
                if 'paymentEvidence6' in request.FILES:
                    file = request.FILES['paymentEvidence6']
                    fileName = file.name.split('.')[0] + '_6.' + file.name.split('.')[1]
                    filePath = touchFile(file,modelType,fileType,str(uploadDate),fileName)
                    if filePath != None:
                        procureFiles['paymentEvidence6'] = filePath
                if 'paymentEvidence1' in procureFiles:
                    payment_evidence1 = procureFiles['paymentEvidence1']
                    procure.payment_evidence1 = payment_evidence1
                if 'paymentEvidence2' in procureFiles:
                    payment_evidence2 = procureFiles['paymentEvidence2']
                    procure.payment_evidence2 = payment_evidence2
                if 'paymentEvidence3' in procureFiles:
                    payment_evidence3 = procureFiles['paymentEvidence3']
                    procure.payment_evidence3 = payment_evidence3
                if 'paymentEvidence4' in procureFiles:
                    payment_evidence4 = procureFiles['paymentEvidence4']
                    procure.payment_evidence4 = payment_evidence4
                if 'paymentEvidence5' in procureFiles:
                    payment_evidence5 = procureFiles['paymentEvidence5']
                    procure.payment_evidence5 = payment_evidence5
                if 'paymentEvidence6' in procureFiles:
                    payment_evidence6 = procureFiles['paymentEvidence6']
                    procure.payment_evidence6 = payment_evidence6
                procure.save()
                procureUpload = setStatus(200,{})
        else:
            return notTokenExpired()
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        procureUpload = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(procureUpload), content_type='application/json')


def getProcurePDFByID(request):
    try:
        if isTokenExpired(request):
            getProcurePDF = {}
            pdf  = order2PDF(orderBasic)
            if pdf['status'] == 0:
                pdfPath = pdf['data']
                downloadName = 'export_procure.pdf'
                response = toStream(pdfPath,downloadName)
                return response
            else:
                getProcurePDF = setStatus(2, 'change order status is successful.But, ' + pdf['data'])
    except Exception,e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        transaction.rollback()
        getProcurePDF = setStatus(500,traceback.format_exc())
    return HttpResponse(json.dumps(getProcurePDF), content_type='application/json')


def procure2PDF(procurePlan):
    try:
        logRecord = basic_log.Logger('record')
        pdf = {}
        orders = []
        stylesheet = getSampleStyleSheet()
        normalStyle = stylesheet['Normal']
        orderTitle = '<para autoLeading="off" fontSize=20 align=center><b><font face="STSong-Light">Purchase Order</font></b><br/><br/>_______________________________________<br/><br/><br/><br/></para>'
        orders.append(Paragraph(orderTitle,normalStyle))
        supplier = Supplier.objects.get(id=orderBasic.providerID)
        branch = Branch.objects.get(id=orderBasic.branchID)
        leftText = '<para autoLeading="off">Purchase ID: <br/><br/>Date:  ' + str(orderBasic.orderGenerateTime) + '<br/><br/><br/><br/>Supplier:  ' + supplier.tradingName + '<br/><br/>Tel:  '+ supplier.contactNo +'<br/><br/>Mail:  ' + supplier.email + '<br/></para>'
        leftContents = Paragraph(leftText,normalStyle)
        rightText = '<para autoLeading="off">Order: '+ str(orderBasic.id) + '<br/><br/>Branch: '+ branch.branchName +'<br/><br/>Company:  ' + '' + '<br/><br/>Address:  ' + branch.branchAddress + '<br/><br/>Tel:  '+ branch.contactNo +'<br/><br/>Mail: ' + branch.contactEmail + '<br/></para>'
        rightContents = Paragraph(rightText,normalStyle)
        emptyContents = Paragraph('<para autoLeading="off"></para>',normalStyle)
        topData = [[leftContents,emptyContents,rightContents]]
        topTable = Table(topData, colWidths=[210,10,210],hAlign='CENTER')
        topTable.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'STSong-Light'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(-1,0),(-2,0),'LEFT'),
        ('VALIGN',(-1,0),(-2,0),'LEFT'),
        ('TEXTCOLOR',(0,1),(-2,-1),colors.royalblue),
        ('GRID',(0,0),(0,-1),0,colors.darkgreen),
        ('GRID',(2,0),(2,-1),0,colors.darkgreen),
        ]))
        orders.append(topTable)
        text = '<para align="right" autoLeading="off"><br/><br/><br/></para>'
        orders.append(Paragraph(text,normalStyle))
        orderContents = OrderContent.objects.filter(orderID=orderBasic.id)
        middleHeadData = [['Image','Code','Name','Price','Qty','Amount']]
        middleHeadTable = Table(middleHeadData, colWidths=[50,80,150,40,40,40])
        middleHeadTable.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'STSong-Light'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('ALIGN',(-1,0),(-2,0),'LEFT'),
        ('VALIGN',(-1,0),(-2,0),'LEFT'),
        ('GRID',(0,0),(-1,-1),0,colors.black),
        ]))
        orders.append(middleHeadTable)
        for orderContent in orderContents:
            productBasics = ProductBasicInfo.objects.filter(id=orderContent.productID)
            if len(productBasics) > 0:
                productBasic = productBasics[0]
                productPictures = ProductPicture.objects.filter(productID=productBasic.id)
                if len(productPictures) > 0:
                    productPicture = productPictures[0]
                    if productPicture.picPath != None:
                        picPath = BASE_DIR + productPicture.picPath
                    else:
                        picPath = None
                else:
                    picPath = None
                productName = productBasic.productName[0:30]
                if picPath != None and os.path.exists(picPath):
                    img = Image(picPath)
                    img.drawHeight = 40
                    img.drawWidth = 40
                    middleEndDate = [[img,productBasic.productCode,productName,orderContent.finalPurchasePrice,orderContent.finalPurchaseQuantity,orderContent.amount]]
                else:
                    picPath = None
                    middleEndDate = [[picPath,productBasic.productCode,productName,orderContent.finalPurchasePrice,orderContent.finalPurchaseQuantity,orderContent.amount]]
                middleEndTable = Table(middleEndDate, colWidths=[50,80,150,40,40,40])
                middleEndTable.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'STSong-Light'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ALIGN', (-1, 0), (-2, 0), 'LEFT'),
                    ('VALIGN', (-1, 0), (-2, 0), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 0, colors.black),
                ]))
                orders.append(middleEndTable)
            else:
                pdf['status'] = 2
                pdf['data'] = 'the productID: ' + str(orderContent.productID) + 'is invalid'
                return pdf
        text = '<para align="right" autoLeading="off"><br/><br/><br/></para>'
        orders.append(Paragraph(text, normalStyle))
        if orderBasic.note != None:
            noteText = '<para autoLeading="off">Note: <br/>' + orderBasic.note + '<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/></para>'
        else:
            noteText = '<para autoLeading="off">Note: <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/></para>'
        noteContents = Paragraph(noteText, normalStyle)
        SEtextL = '''<para align="left" autoLeading="off" fontSize=14>
            <font face="STSong-Light">Sub Total: </font><br/><br/>
            <font face="STSong-Light">Freight: </font><br/><br/>
            <font face="STSong-Light">Tax: </font><br/><br/>
            <font face="STSong-Light">Total: </font><br/><br/>
            </para>'''
        SEContentsL = Paragraph(SEtextL, normalStyle)
        
        SEtextR = '''<para align="right" autoLeading="off" fontSize=14>
            <font face="STSong-Light">''' + str(orderBasic.subTotal) + '''</font><br/><br/>
            <font face="STSong-Light">''' + str(orderBasic.Freight) + '''</font><br/><br/>
            <font face="STSong-Light">''' + str(orderBasic.Tax) + '''</font><br/><br/>
            <font face="STSong-Light">''' + str(orderBasic.amountTotal) + '''</font><br/><br/>
            </para>'''
        SEContentsR = Paragraph(SEtextR, normalStyle)
        
        endData = [[noteContents, emptyContents, SEContentsL,SEContentsR]]
        endTable = Table(endData, colWidths=[210, 110, 90,50], hAlign='CENTER')
        endTable.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'STSong-Light'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (-1, 0), (-2, 0), 'LEFT'),
            ('VALIGN', (-1, 0), (-2, 0), 'LEFT'),
            ('TEXTCOLOR', (0, 1), (-2, -1), colors.royalblue),
            ('GRID', (0, 0), (0, -1), 0, colors.darkgreen),
        ]))
        orders.append(endTable)
        touchTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        fileName = 'PurchaseOrder_' + str(orderBasic.id) + '.pdf'
        filePath = BASE_DIR + '/static/pdf/'+ fileName
        doc = SimpleDocTemplate(filePath)
        doc.build(orders)
        pdf['status'] = 0
        pdf['data'] = filePath
        logRecord.log('order to PDF is successful')
    except Exception, e:
        logErr = basic_log.Logger('error')
        logErr.log(traceback.format_exc())
        pdf['status'] = 1
        pdf['data'] = traceback.format_exc()
    return pdf


def paging(request, ONE_PAGE_OF_DATA, condition, selectType):
    logRecord = basic_log.Logger('record')
    pagingSelect = {}
    datasJSON = []
    if 'curPage' in request.GET:
        curPage = int(request.GET['curPage'])
    else:
        curPage = 1
    if 'sizePage' in request.GET:
        ONE_PAGE_OF_DATA = int(request.GET['sizePage'])
    allPage = 1
    if condition == None:
        basicsCount = ProcureTable.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = ProcureTable.objects.filter(
                Q(**condition) & Q(generate_date__gte=timeFrom) & Q(generate_date__lte=timeTo)).count()
        else:
            basicsCount = ProcureTable.objects.filter(**condition).count()
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
        basicObjs = ProcureTable.objects.filter(is_delete=0)[startPos:endPos]
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = ProcureTable.objects.filter(
                    Q(**condition) & Q(generate_date__gte=timeFrom) & Q(generate_date__lte=timeTo))[startPos:endPos]
        else:
            basicObjs = ProcureTable.objects.filter(**condition)[startPos:endPos]
    for basicObj in basicObjs:
        basicJSON = getProcure(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect


def conditionSelect(condition, selectType):
    pagingSelect = {}
    datasJSON = []
    curPage = 1
    allPage = 1
    if condition == None:
        basicsCount = ProcureTable.objects.filter(is_delete=0).count()
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicsCount = ProcureTable.objects.filter(
                Q(**condition) & Q(generate_date__gte=timeFrom) & Q(generate_date__lte=timeTo)).count()
        else:
            basicsCount = ProcureTable.objects.filter(**condition).count()
    if curPage > allPage or curPage < 1:
        pagingSelect['code'] = 300
        pagingSelect['curPage'] = curPage
        pagingSelect['allPage'] = allPage
        pagingSelect['data'] = 'curPage is invalid !'
        return pagingSelect
    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    if condition == None:
        basicObjs = ProcureTable.objects.filter(is_delete=0)
    else:
        if 'timeFrom' in selectType and 'timeTo' in selectType:
            timeFrom = selectType['timeFrom']
            timeTo = selectType['timeTo']
            basicObjs = ProcureTable.objects.filter(Q(**condition) & Q(generate_date__gte=timeFrom) & Q(generate_date__lte=timeTo))
        else:
            basicObjs = ProcureTable.objects.filter(**condition)
    for basicObj in basicObjs:
        basicJSON = getProcure(basicObj)
        datasJSON.append(basicJSON)
    pagingSelect['code'] = 200
    dataJSON = {}
    dataJSON['curPage'] = curPage
    dataJSON['allPage'] = allPage
    dataJSON['total'] = basicsCount
    dataJSON['datas'] = datasJSON
    pagingSelect['data'] = dataJSON
    return pagingSelect

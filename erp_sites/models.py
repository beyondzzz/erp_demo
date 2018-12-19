#!usr/bin/python#coding=utf-8
from django.db import models
from django.template.defaultfilters import default
from cgi import maxlen
from unittest.util import _MAX_LENGTH
# Create your models here.

class Activity(models.Model):

    activity_id = models.IntegerField('activity_id')
    generated_time = models.DateTimeField('generated_time', null=True)
    activity_type = models.CharField('activity_type', max_length=1)
    is_generated = models.CharField("is_generated",max_length = 1)

    def create(self,activity_id,generated_time,activity_type,is_generated):
        obj = self.create(activity_id=activity_id,generated_time=generated_time,activity_type=activity_type,is_generated=is_generated)
        return obj

    def __unicode__(self):
        aaa = ['activity_id','generated_time','activity_type','is_generated']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "activity"
        verbose_name = "activity表"
        verbose_name_plural = "activity表"
        
class AllotOrder(models.Model):
    
    allot_date = models.DateTimeField('allot_date', null=True)
    identifier = models.CharField('identifier', max_length=255)
    export_warehouse_id = models.IntegerField('export_warehouse_id')
    import_warehouse_id = models.IntegerField('import_warehouse_id')
    shipping_mode_id = models.IntegerField('shipping_mode_id')
    import_branch = models.CharField('import_branch', max_length=255)
    adjust_subject = models.CharField('adjust_subject', max_length=255)
    send_goods_place = models.CharField('send_goods_place', max_length=255)
    person_id = models.IntegerField('person_id')
    originator = models.CharField('originator', max_length=255)
    summary = models.CharField('summary', max_length=255)
    print_num = models.IntegerField('print_num',default=0)
    make_person = models.CharField('make_person', max_length=255)
    description = models.CharField('description', max_length=255)
    export_name = models.CharField('export_name', max_length=255)
    import_name = models.CharField('import_name', max_length=255)
    
    def create(self,allot_date,identifier,export_warehouse_id,import_warehouse_id,shipping_mode_id,import_branch,adjust_subject,send_goods_place,person_id,originator,summary,print_num,make_person,description,export_name,import_name):
        obj = self.create(allot_date=allot_date,identifier=identifier,export_warehouse_id=export_warehouse_id,import_warehouse_id=import_warehouse_id,shipping_mode_id=shipping_mode_id,import_branch=import_branch,adjust_subject=adjust_subject,send_goods_place=send_goods_place,person_id=person_id,originator=originator,summary=summary,print_num=print_num,make_person=make_person,description=description,export_name=export_name,import_name=import_name)
        return obj

    def __unicode__(self):
        aaa = ['allot_date','identifier','export_warehouse_id','import_warehouse_id','shipping_mode_id','import_branch','adjust_subject','send_goods_place','person_id','originator','summary','print_num','make_person','description','export_name','import_name']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "allot_order"
        verbose_name = "allot_order表"
        verbose_name_plural = "allot_order表"

    
class AllotOrderCommodity(models.Model):

    allot_order_id = models.IntegerField('allot_order_id')
    commodity_specification_id = models.IntegerField('commodity_specification_id')
    number = models.IntegerField('number')
    export_unit_price = models.FloatField('export_unit_price',null=True)
    import_unit_price = models.FloatField('import_unit_price',null=True)
    import_money = models.FloatField('import_money',null=True)

    def create(self,allot_order_id,commodity_specification_id,number,export_unit_price,import_unit_price,import_money):
        obj = self.create(allot_order_id=allot_order_id,commodity_specification_id=commodity_specification_id,number=number,export_unit_price=export_unit_price,import_unit_price=import_unit_price,import_money=import_money)
        return obj

    def __unicode__(self):
        aaa = ['allot_order_id','commodity_specification_id','number','export_unit_price','import_unit_price','import_money']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "allot_order_commodity"
        verbose_name = "allot_order_commodity表"
        verbose_name_plural = "allot_order_commodity表"
        

class Bills(models.Model):
    
    bills_code = models.CharField('bills_code', max_length=255)
    customer_supplier_id = models.IntegerField('customer_supplier_id')
    bills_type = models.CharField('bills_type', max_length=1)
    bills_date = models.DateTimeField('bills_date', null=True)
    bank = models.CharField('bank', max_length=50)
    bank_account = models.CharField('bank_account', max_length=50)
    payment = models.IntegerField('payment')
    originator = models.CharField('originator', max_length=255)
    person_id = models.IntegerField('person_id')
    summary = models.CharField('summary', max_length=255)
    remark = models.CharField('remark', max_length=255)
    money = models.FloatField('money',null=True)
    ticket_no = models.CharField('ticket_no', max_length=255)
    branch = models.CharField('branch', max_length=50)
    balance = models.FloatField('balance',null=True)
    account = models.CharField('account', max_length=255)
    order_type = models.CharField('order_type', max_length=1)
    

    def create(self,bills_code,customer_supplier_id,bills_type,bills_date,bank,bank_account,payment,originator,person_id,summary,remark,money,ticket_no,branch,balance,account,order_type):
        obj = self.create(bills_code=bills_code,customer_supplier_id=customer_supplier_id,bills_type=bills_type,bills_date=bills_date,bank=bank,bank_account=bank_account,payment=payment,originator=originator,person_id=person_id,summary=summary,remark=remark,money=money,ticket_no=ticket_no,branch=branch,balance=balance,account=account,order_type=order_type)
        return obj

    def __unicode__(self):
        aaa = ['bills_code','customer_supplier_id','bills_type','bills_date','bank','bank_account','payment','originator','person_id','summary','remark','money','ticket_no','branch','balance','account','order_type']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "bills"
        verbose_name = "bills表"
        verbose_name_plural = "bills表"
        

class BillsSub(models.Model):
    
    bills_id = models.IntegerField('bills_id')
    procure_sales_id = models.IntegerField('procure_sales_id')
    clearing_money = models.FloatField('clearing_money',null=True)
    stay_money = models.FloatField('stay_money',null=True)
    the_moeny = models.FloatField('the_moeny',null=True)
    actual_money = models.FloatField('actual_money',null=True)
    rebate_money = models.FloatField('rebate_money',null=True)
    is_payment = models.CharField('is_payment', max_length=1)
    rebate = models.IntegerField('rebate')
    remark = models.CharField('remark', max_length=255)
    pay_money = models.FloatField('pay_money',null=True)

    def create(self,bills_id,procure_sales_id,clearing_money,stay_money,the_moeny,actual_money,rebate_money,is_payment,rebate,remark,pay_money):
        obj = self.create(bills_id=bills_id,procure_sales_id=procure_sales_id,clearing_money=clearing_money,stay_money=stay_money,the_moeny=the_moeny,actual_money=actual_money,rebate_money=rebate_money,is_payment=is_payment,rebate=rebate,remark=remark,pay_money=pay_money)
        return obj

    def __unicode__(self):
        aaa = ['bills_id','procure_sales_id','clearing_money','stay_money','the_moeny','actual_money','rebate_money','is_payment','rebate','remark','pay_money']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "bills_sub"
        verbose_name = "bills_sub表"
        verbose_name_plural = "bills_sub表"
        

class BreakageOrder(models.Model):

    breakage_date = models.DateTimeField('breakage_date', null=True)
    identifier = models.CharField('identifier', max_length=255)
    warehouse_id = models.IntegerField('warehouse_id')
    person_id = models.IntegerField('person_id')
    originator = models.CharField('originator', max_length=255)
    reviewer = models.CharField('reviewer', max_length=255)
    summary = models.CharField('summary', max_length=255)
    state = models.IntegerField('state')
    print_num = models.IntegerField('print_num',default=0)
    is_delete = models.IntegerField('is_delete',default=0)

    def create(self,breakage_date,identifier,warehouse_id,person_id,originator,reviewer,summary,state,print_num,is_delete):
        obj = self.create(breakage_date=breakage_date,identifier=identifier,warehouse_id=warehouse_id,person_id=person_id,originator=originator,reviewer=reviewer,summary=summary,state=state,print_num=print_num,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['breakage_date','identifier','warehouse_id','person_id','originator','reviewer','summary','state','print_num','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "breakage_order"
        verbose_name = "breakage_order表"
        verbose_name_plural = "breakage_order表"
        
        
class BreakageOrderCommodity(models.Model):
    
    breakage_order_id = models.IntegerField('breakage_order_id')
    commodity_specification_id = models.IntegerField('commodity_specification_id')
    number = models.IntegerField('number')
    unit_price = models.FloatField('unit_price',null=True)
    money = models.FloatField('money',null=True)

    def create(self,breakage_order_id,commodity_specification_id,number,unit_price,money):
        obj = self.create(breakage_order_id=breakage_order_id,commodity_specification_id=commodity_specification_id,number=number,unit_price=unit_price,money=money)
        return obj

    def __unicode__(self):
        aaa = ['breakage_order_id','commodity_specification_id','number','unit_price','money']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "breakage_order_commodity"
        verbose_name = "breakage_order_commodity表"
        verbose_name_plural = "breakage_order_commodity表"
    
    
class Classification(models.Model):

    identifier = models.CharField('identifier', max_length=255)
    name = models.CharField('name', max_length=255)
    parent_id = models.IntegerField('parent_id')
    key_word = models.CharField('key_word', max_length=40)
    operator_identifier = models.CharField('operator_identifier', max_length=255)
    operator_time = models.DateTimeField('operator_time', null=True)
    type = models.IntegerField('type')
    is_delete = models.IntegerField('is_delete',default=0)

    def create(self,identifier,name,parent_id,key_word,operator_identifier,operator_time,type,is_delete):
        obj = self.create(identifier=identifier,name=name,parent_id=parent_id,key_word=key_word,operator_identifier=operator_identifier,operator_time=operator_time,type=type,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['identifier','name','parent_id','key_word','operator_identifier','operator_time','type','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "classification"
        verbose_name = "classification表"
        verbose_name_plural = "classification表"
        
        
class Commodity(models.Model):

    classification_id = models.IntegerField('classification_id')
    name = models.CharField('name', max_length=255)
    brand = models.CharField('brand', max_length=255)
    zero_stock = models.IntegerField('zero_stock')
    shout_name = models.CharField('shout_name', max_length=255)
    mnemonic_code = models.CharField('mnemonic_code', max_length=255)
    basics_information = models.CharField('basics_information', max_length=255)
    attribute = models.CharField('attribute', max_length=255)
    identifier = models.CharField('identifier', max_length=255)
    supcto_id = models.IntegerField('supcto_id')
    taxes = models.FloatField('taxes',null=True)
    is_assemble = models.IntegerField('supcto_id',default=2)
    is_presell = models.IntegerField('supcto_id')
    temp_taxes = models.FloatField('temp_taxes',null=True)

    def create(self,classification_id,name,brand,zero_stock,shout_name,mnemonic_code,basics_information,attribute,identifier,supcto_id,taxes,is_assemble,is_presell,temp_taxes):
        obj = self.create(classification_id=classification_id,name=name,brand=brand,zero_stock=zero_stock,shout_name=shout_name,mnemonic_code=mnemonic_code,basics_information=basics_information,attribute=attribute,identifier=identifier,supcto_id=supcto_id,taxes=taxes,is_assemble=is_assemble,is_presell=is_presell,temp_taxes=temp_taxes)
        return obj

    def __unicode__(self):
        aaa = ['classification_id','name','brand','zero_stock','shout_name','mnemonic_code','basics_information','attribute','identifier','supcto_id','taxes','is_assemble','is_presell','temp_taxes']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "commodity"
        verbose_name = "commodity表"
        verbose_name_plural = "commodity表"
    
    
class CommoditySpecification(models.Model):

    specification_identifier = models.CharField('specification_identifier', max_length=255)
    specification_name = models.CharField('specification_name', max_length=255)
    commodity_id = models.IntegerField('commodity_id')
    quality_period = models.IntegerField('quality_period')
    quality_period_unit = models.CharField('quality_period_unit', max_length=255)
    mini_order_quantity = models.IntegerField('mini_order_quantity')
    add_order_quantity = models.IntegerField('add_order_quantity')
    packaging_size = models.CharField('packaging_size', max_length=255)
    is_delete = models.IntegerField('is_delete')
    warning_number = models.IntegerField('warning_number',default=0)
    weight = models.FloatField('weight',null=True)
    operator_identifier = models.CharField('operator_identifier', max_length=255)
    operator_time = models.DateTimeField('operator_time', null=True)
    state = models.IntegerField('state')
    temp_mini_order_quantity = models.IntegerField('temp_mini_order_quantity')
    temp_add_order_quantity = models.IntegerField('temp_add_order_quantity')
    temp_warning_number = models.IntegerField('temp_warning_number')
    temp_warehouse_id = models.IntegerField('temp_warehouse_id')
    temp_max_inventory = models.IntegerField('temp_max_inventory')
    temp_mini_inventory = models.IntegerField('temp_mini_inventory')
    temp_inventory = models.IntegerField('temp_inventory')
    temp_state = models.IntegerField('temp_state')

    def create(self,specification_identifier,specification_name,commodity_id,quality_period,quality_period_unit,mini_order_quantity,add_order_quantity,packaging_size,is_delete,warning_number,weight,operator_identifier,operator_time,state,temp_mini_order_quantity,temp_add_order_quantity,temp_warning_number,temp_warehouse_id,temp_max_inventory,temp_mini_inventory,temp_inventory,temp_state):
        obj = self.create(specification_identifier=specification_identifier,specification_name=specification_name,commodity_id=commodity_id,quality_period=quality_period,quality_period_unit=quality_period_unit,mini_order_quantity=mini_order_quantity,add_order_quantity=add_order_quantity,packaging_size=packaging_size,is_delete=is_delete,warning_number=warning_number,weight=weight,operator_identifier=operator_identifier,operator_time=operator_time,state=state,temp_mini_order_quantity=temp_mini_order_quantity,temp_add_order_quantity=temp_add_order_quantity,temp_warning_number=temp_warning_number,temp_warehouse_id=temp_warehouse_id,temp_max_inventory=temp_max_inventory,temp_mini_inventory=temp_mini_inventory,temp_inventory=temp_inventory,temp_state=temp_state)
        return obj

    def __unicode__(self):
        aaa = ['specification_identifier','specification_name','commodity_id','quality_period','quality_period_unit','mini_order_quantity','add_order_quantity','packaging_size','is_delete','warning_number','weight','operator_identifier','operator_time','state','temp_mini_order_quantity','temp_add_order_quantity','temp_warning_number','temp_warehouse_id','temp_max_inventory','temp_mini_inventory','temp_inventory','temp_state']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "commodity_specification"
        verbose_name = "commodity_specification表"
        verbose_name_plural = "commodity_specification表"
        
        
class Department(models.Model):

    name = models.CharField('name', max_length=255)
    operator_identifier = models.CharField('operator_identifier', max_length=255)
    operator_time = models.DateTimeField('operator_time', null=True)
    identifier = models.CharField('identifier', max_length=255)
    is_delete = models.IntegerField('is_delete',default=0)

    def create(self,name,operator_identifier,operator_time,identifier,is_delete):
        obj = self.create(name=name,operator_identifier=operator_identifier,operator_time=operator_time,identifier=identifier,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['name','operator_identifier','operator_time','identifier','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "department"
        verbose_name = "department表"
        verbose_name_plural = "department表"
        
        
class Goods(models.Model):
    
    stock = models.IntegerField('stock')
    purchase = models.FloatField('purchase',null=True)
    brand = models.CharField('brand', max_length=255)
    state = models.IntegerField('state')

    def create(self,stock,purchase,brand,state):
        obj = self.create(stock=stock,purchase=purchase,brand=brand,state=state)
        return obj

    def __unicode__(self):
        aaa = ['stock','purchase','brand','state']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "goods"
        verbose_name = "goods表"
        verbose_name_plural = "goods表"
        
    
class Inventory(models.Model):

    specification_id = models.IntegerField('specification_id')
    warehouse_id = models.IntegerField('warehouse_id')
    inventory = models.IntegerField('inventory',default=0)
    presell_inventory = models.IntegerField('presell_inventory',default=0)
    occupied_inventory = models.IntegerField('occupied_inventory',default=0)
    max_inventory = models.IntegerField('max_inventory',default=0)
    mini_inventory = models.IntegerField('mini_inventory',default=0)
    cost_price = models.FloatField('cost_price',null=True)
    commodity_num = models.IntegerField('commodity_num',default=0)
    is_create_procure_plan = models.IntegerField('is_create_procure_plan',default=0)

    def create(self,specification_id,warehouse_id,inventory,presell_inventory,occupied_inventory,max_inventory,mini_inventory,cost_price,commodity_num,is_create_procure_plan):
        obj = self.create(specification_id=specification_id,warehouse_id=warehouse_id,inventory=inventory,presell_inventory=presell_inventory,occupied_inventory=occupied_inventory,max_inventory=max_inventory,mini_inventory=mini_inventory,cost_price=cost_price,commodity_num=commodity_num,is_create_procure_plan=is_create_procure_plan)
        return obj

    def __unicode__(self):
        aaa = ['specification_id','warehouse_id','inventory','presell_inventory','occupied_inventory','max_inventory','mini_inventory','cost_price','commodity_num','is_create_procure_plan']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "inventory"
        verbose_name = "inventory表"
        verbose_name_plural = "inventory表"
        
        
class Log(models.Model):

    operate_type = models.IntegerField('operate_type')
    operate_object = models.TextField('operate_object')
    operator_identifier = models.CharField('operator_identifier', max_length=255)
    operate_time = models.DateTimeField('operate_time', null=True)

    def create(self,operate_type,operate_object,operator_identifier,operate_time):
        obj = self.create(operate_type=operate_type,operate_object=operate_object,operator_identifier=operator_identifier,operate_time=operate_time)
        return obj

    def __unicode__(self):
        aaa = ['operate_type','operate_object','operator_identifier','operate_time']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "log"
        verbose_name = "log表"
        verbose_name_plural = "log表"
        
        
class Menu(models.Model):

    parent_id = models.IntegerField('parent_id')
    name = models.CharField('name',max_length=20)
    url = models.CharField('url',max_length=100)
    icon = models.CharField('icon',max_length=100)
    sort = models.IntegerField('parent_id')
    is_effective = models.IntegerField('parent_id')
    is_message = models.IntegerField('parent_id')
    service_type = models.IntegerField('parent_id')
    is_add = models.IntegerField('parent_id')

    def create(self,parent_id,name,url,icon,sort,is_effective,is_message,service_type,is_add):
        obj = self.create(parent_id=parent_id,name=name,url=url,icon=icon,sort=sort,is_effective=is_effective,is_message=is_message,service_type=service_type,is_add=is_add)
        return obj

    def __unicode__(self):
        aaa = ['parent_id','name','url','icon','sort','is_effective','is_message','service_type','is_add']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "menu"
        verbose_name = "menu表"
        verbose_name_plural = "menu表"
        
    
class Message(models.Model):

    menu_id = models.IntegerField('menu_id')
    service_type = models.IntegerField('service_type')
    service_id = models.IntegerField('service_id')
    message_time = models.DateTimeField('message_time', null=True)

    def create(self,menu_id,service_type,service_id,message_time):
        obj = self.create(menu_id=menu_id,service_type=service_type,service_id=service_id,message_time=message_time)
        return obj

    def __unicode__(self):
        aaa = ['menu_id','service_type','service_id','message_time']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "message"
        verbose_name = "message表"
        verbose_name_plural = "message表"
        
        
class PackageOrTeardownOrder(models.Model):

    order_type = models.IntegerField('order_type')
    package_or_teardown_date = models.DateTimeField('package_or_teardown_date', null=True)
    identifier = models.CharField('identifier',max_length=255)
    warehouse_id = models.IntegerField('warehouse_id')
    commodity_specification_id = models.IntegerField('commodity_specification_id')
    package_or_teardown_num = models.IntegerField('package_or_teardown_num')
    unit_price = models.FloatField('unit_price',null=True)
    total_money = models.FloatField('total_money',null=True)
    person_id = models.IntegerField('person_id')
    originator = models.CharField('originator',max_length=255)
    reviewer = models.CharField('reviewer',max_length=255)
    summary = models.CharField('summary',max_length=255)
    state = models.IntegerField('state')
    print_num = models.IntegerField('print_num',default=0)
    is_delete = models.IntegerField('is_delete',default=0)

    def create(self,order_type,package_or_teardown_date,identifier,warehouse_id,commodity_specification_id,package_or_teardown_num,unit_price,total_money,person_id,originator,reviewer,summary,state,print_num,is_delete):
        obj = self.create(order_type=order_type,package_or_teardown_date=package_or_teardown_date,identifier=identifier,warehouse_id=warehouse_id,commodity_specification_id=commodity_specification_id,package_or_teardown_num=package_or_teardown_num,unit_price=unit_price,total_money=total_money,person_id=person_id,originator=originator,reviewer=reviewer,summary=summary,state=state,print_num=print_num,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['order_type','package_or_teardown_date','identifier','warehouse_id','commodity_specification_id','package_or_teardown_num','unit_price','total_money','person_id','originator','reviewer','summary','state','print_num','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "package_or_teardown_order"
        verbose_name = "package_or_teardown_ordere表"
        verbose_name_plural = "package_or_teardown_order表"
        
    
class PackageOrTeardownOrderCommodity(models.Model):

    package_or_teardown_order_id = models.IntegerField('package_or_teardown_order_id')
    commodity_specification_id = models.IntegerField('commodity_specification_id')
    number = models.IntegerField('number')
    unit_price = models.FloatField('unit_price',null=True)
    money = models.FloatField('money',null=True)

    def create(self,package_or_teardown_order_id,commodity_specification_id,number,unit_price,money):
        obj = self.create(package_or_teardown_order_id=package_or_teardown_order_id,commodity_specification_id=commodity_specification_id,number=number,unit_price=unit_price,money=money)
        return obj

    def __unicode__(self):
        aaa = ['package_or_teardown_order_id','commodity_specification_id','number','unit_price','money']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "package_or_teardown_order_commodity"
        verbose_name = "package_or_teardown_order_commodity表"
        verbose_name_plural = "package_or_teardown_order_commodity表"
        
        
class Permission(models.Model):

    user_id = models.IntegerField('user_id')
    menu_id = models.IntegerField('menu_id')
    operator_identifier = models.CharField('operator_identifier',max_length=255)
    create_time = models.DateTimeField('create_time', null=True)

    def create(self,user_id,menu_id,operator_identifier,create_time):
        obj = self.create(user_id=user_id,menu_id=menu_id,operator_identifier=operator_identifier,create_time=create_time)
        return obj

    def __unicode__(self):
        aaa = ['user_id','menu_id','operator_identifier','create_time']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "permission"
        verbose_name = "permission表"
        verbose_name_plural = "permission表"
        
        
class Person(models.Model):

    name = models.CharField('name',max_length=255)
    type = models.CharField('type',max_length=255)
    department_id = models.IntegerField('department_id')
    entry_time = models.DateField('entry_time', null=True)
    duties = models.CharField('duties',max_length=255)
    education = models.CharField('education',max_length=255)
    sex = models.CharField('sex',max_length=10)
    birth_time = models.DateField('birth_time', null=True)
    native_place = models.CharField('native_place',max_length=255)
    phone = models.CharField('phone',max_length=255)
    home_phone = models.CharField('home_phone',max_length=255)
    common_phone = models.CharField('common_phone',max_length=255)
    reserve_phone = models.CharField('reserve_phone',max_length=255)
    postcode = models.CharField('postcode',max_length=255)
    home_address = models.CharField('home_address',max_length=255)
    mailbox = models.CharField('mailbox',max_length=255)
    quit_time = models.DateField('quit_time', null=True)
    business = models.IntegerField('business')
    quite = models.IntegerField('quite')
    operator_identifier = models.CharField('operator_identifier',max_length=255)
    operator_time = models.DateTimeField('operator_time', null=True)
    remark = models.CharField('remark',max_length=255)
    id_number = models.CharField('id_number',max_length=20)
    identifier = models.CharField('identifier',max_length=255)
    login_name = models.CharField('login_name',max_length=50)
    password = models.CharField('password',max_length=50)
    warehouse_id = models.IntegerField('warehouse_id')
    place = models.CharField('place',max_length=50)
    is_delete = models.IntegerField('is_delete',default=0)

    def create(self,name,type,department_id,entry_time,duties,education,sex,birth_time,native_place,phone,home_phone,common_phone,reserve_phone,postcode,home_address,mailbox,quit_time,business,quite,operator_identifier,operator_time,remark,id_number,identifier,login_name,password,warehouse_id,place,is_delete):
        obj = self.create(name=name,type=type,department_id=department_id,entry_time=entry_time,duties=duties,education=education,sex=sex,birth_time=birth_time,native_place=native_place,phone=phone,home_phone=home_phone,common_phone=common_phone,reserve_phone=reserve_phone,postcode=postcode,home_address=home_address,mailbox=mailbox,quit_time=quit_time,business=business,quite=quite,operator_identifier=operator_identifier,operator_time=operator_time,remark=remark,id_number=id_number,identifier=identifier,login_name=login_name,password=password,warehouse_id=warehouse_id,place=place,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['name','type','department_id','entry_time','duties','education','sex','birth_time','native_place','phone','home_phone','common_phone','reserve_phone','postcode','home_address','mailbox','quit_time','business','quite','operator_identifier','operator_time','remark','id_number','identifier','login_name','password','warehouse_id','place','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "person"
        verbose_name = "person表"
        verbose_name_plural = "person表"
        
        
class PersonToken(models.Model):
    
    person_id = models.IntegerField('person_id')
    login_name = models.CharField('login_name',max_length=255)
    start_time = models.DateTimeField('start_time', null=True)
    end_time = models.DateTimeField('end_time', null=True)
    token = models.CharField('token',max_length=255)
    
    def create(self,person_id,login_name,start_time,end_time,token):
        obj = self.create(person_id=person_id,login_name=login_name,start_time=start_time,end_time=end_time,token=token)
        return obj

    def __unicode__(self):
        aaa = ['person_id','login_name','start_time','end_time','token']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz
    
    class Meta:
        db_table = "person_token"
        verbose_name = "person_token表"
        verbose_name_plural = "person_token表"
        
 
class ProcureCommodity(models.Model):

    commodity_id = models.IntegerField('commodity_id')
    procure_table_id = models.IntegerField('procure_table_id')
    tax_rate = models.FloatField('tax_rate',default=0,null=True)
    amount_of_tax = models.FloatField('amount_of_tax',default=0,null=True)
    total_tax_price = models.FloatField('total_tax_price',default=0,null=True)
    order_num = models.IntegerField('order_num',default=0)
    lot_number = models.CharField('lot_number',max_length=255)
    arrival_quantity = models.IntegerField('arrival_quantity',default=0)
    suspend_quantity = models.IntegerField('suspend_quantity',default=0)
    suspend_price = models.FloatField('suspend_price',default=0,null=True)
    discount = models.IntegerField('discount')
    is_largess = models.IntegerField('is_largess')
    original_unit_price = models.FloatField('original_unit_price',default=0,null=True)
    business_unit_price = models.FloatField('business_unit_price',default=0,null=True)
    remarks = models.CharField('remarks',max_length=255)
    contains_tax_price = models.FloatField('contains_tax_price',default=0,null=True)
    payment_for_goods = models.FloatField('payment_for_goods',default=0,null=True)
    total_price = models.FloatField('total_price',default=0,null=True)
    is_delete = models.CharField('is_delete',max_length=1)

    def create(self,commodity_id,procure_table_id,tax_rate,amount_of_tax,total_tax_price,order_num,lot_number,arrival_quantity,suspend_quantity,suspend_price,discount,is_largess,original_unit_price,business_unit_price,remarks,contains_tax_price,payment_for_goods,total_price,is_delete):
        obj = self.create(commodity_id=commodity_id,procure_table_id=procure_table_id,tax_rate=tax_rate,amount_of_tax=amount_of_tax,total_tax_price=total_tax_price,order_num=order_num,lot_number=lot_number,arrival_quantity=arrival_quantity,suspend_quantity=suspend_quantity,suspend_price=suspend_price,discount=discount,is_largess=is_largess,original_unit_price=original_unit_price,business_unit_price=business_unit_price,remarks=remarks,contains_tax_price=contains_tax_price,payment_for_goods=payment_for_goods,total_price=total_price,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['commodity_id','procure_table_id','tax_rate','amount_of_tax','total_tax_price','order_num','lot_number','arrival_quantity','suspend_quantity','suspend_price','discount','is_largess','original_unit_price','business_unit_price','remarks','contains_tax_price','payment_for_goods','total_price','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "procure_commodity"
        verbose_name = "procure_commodity表"
        verbose_name_plural = "procure_commodity表"
        
        
class ProcureTable(models.Model):

    identifier = models.CharField('identifier',max_length=255)
    generate_date = models.DateTimeField('generate_date', null=True)
    supcto_id = models.IntegerField('supcto_id',max_length=255)
    effective_period_end = models.DateField('effective_period_end', null=True)
    goods_arrival_time = models.DateField('goods_arrival_time', null=True)
    goods_arrival_place = models.CharField('goods_arrival_place',max_length=255)
    transportation_mode = models.IntegerField('transportation_mode')
    deliveryman = models.CharField('deliveryman',max_length=255)
    fax = models.CharField('fax',max_length=255)
    phone = models.CharField('phone',max_length=255)
    orderer = models.CharField('orderer',max_length=255)
    prepaid_amount = models.FloatField('prepaid_amount',null=True)
    department_id = models.IntegerField('department_id')
    originator = models.CharField('originator',max_length=255)
    reviewer = models.CharField('reviewer',max_length=255)
    terminator = models.CharField('terminator',max_length=255)
    summary = models.CharField('summary',max_length=255)
    branch = models.CharField('branch',max_length=255)
    state = models.IntegerField('state')
    print_num = models.IntegerField('print_num',default=0)
    plan_type = models.IntegerField('plan_type')
    pay_type = models.IntegerField('pay_type')
    contract_number = models.CharField('contract_number',max_length=255)
    plan_or_order = models.IntegerField('plan_or_order')
    before_is_plan = models.IntegerField('before_is_plan')
    payment_evidence1 = models.CharField('payment_evidence1',max_length=255)
    payment_evidence2 = models.CharField('payment_evidence2',max_length=255)
    payment_evidence3 = models.CharField('payment_evidence3',max_length=255)
    payment_evidence4 = models.CharField('payment_evidence4',max_length=255)
    payment_evidence5 = models.CharField('payment_evidence5',max_length=255)
    payment_evidence6 = models.CharField('payment_evidence6',max_length=255)
    is_delete = models.IntegerField('is_delete',default=0)
    parent_id = models.IntegerField('parent_id')
    order_type = models.IntegerField('order_type')
    postfix = models.IntegerField('postfix')
    is_verification = models.CharField('is_verification',max_length=1)
    activity_id = models.IntegerField('activity_id')
    is_app_order = models.IntegerField('is_app_order')
    financial_reviewer = models.CharField('financial_reviewer',max_length=255)
    is_other_receipts = models.IntegerField('is_other_receipts',default=0)

    def create(self,identifier,generate_date,supcto_id,effective_period_end,goods_arrival_time,goods_arrival_place,transportation_mode,deliveryman,fax,phone,orderer,prepaid_amount,department_id,originator,reviewer,terminator,summary,branch,state,print_num,plan_type,pay_type,contract_number,plan_or_order,before_is_plan,payment_evidence1,payment_evidence2,payment_evidence3,payment_evidence4,payment_evidence5,payment_evidence6,is_delete,parent_id,order_type,postfix,is_verification,activity_id ,is_app_order,financial_reviewer,is_other_receipts):
        obj = self.create(identifier=identifier,generate_date=generate_date,supcto_id=supcto_id,effective_period_end=effective_period_end,goods_arrival_time=goods_arrival_time,goods_arrival_place=goods_arrival_place,transportation_mode=transportation_mode,deliveryman=deliveryman,fax=fax,phone=phone,orderer=orderer,prepaid_amount=prepaid_amount,department_id=department_id,originator=originator,reviewer=reviewer,terminator=terminator,summary=summary,branch=branch,state=state,print_num=print_num,plan_type=plan_type,pay_type=pay_type,contract_number=contract_number,plan_or_order=plan_or_order,before_is_plan=before_is_plan,payment_evidence1=payment_evidence1,payment_evidence2=payment_evidence2,payment_evidence3=payment_evidence3,payment_evidence4=payment_evidence4,payment_evidence5=payment_evidence5,payment_evidence6=payment_evidence6,is_delete=is_delete,parent_id=parent_id,order_type=order_type,postfix=postfix,is_verification=is_verification,activity_id=activity_id,is_app_order=is_app_order,financial_reviewer=financial_reviewer,is_other_receipts=is_other_receipts)
        return obj

    def __unicode__(self):
        aaa = ['identifier','generate_date','supcto_id','effective_period_end','goods_arrival_time','goods_arrival_place','transportation_mode','deliveryman','fax','phone','orderer','prepaid_amount','department_id','originator','reviewer','terminator','summary','branch','state','print_num','plan_type','pay_type','contract_number','plan_or_order','before_is_plan','payment_evidence1','payment_evidence2','payment_evidence3','payment_evidence4','payment_evidence5','payment_evidence6','is_delete','parent_id','order_type','postfix','is_verification','activity_id' ,'is_app_order','financial_reviewer','is_other_receipts']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "procure_table"
        verbose_name = "procure_table表"
        verbose_name_plural = "procure_table表"
        
        
class SalesOrder(models.Model):

    parent_id = models.IntegerField('parent_id')
    identifier = models.CharField('identifier',max_length=255)
    break_code = models.CharField('break_code',max_length=255)
    payment = models.IntegerField('payment')
    order_type = models.IntegerField('order_type')
    create_time = models.DateTimeField('create_time',null=True)
    end_validity_time = models.DateField('end_validity_time',null=True)
    deliver_goods_place = models.CharField('deliver_goods_place',max_length=255)
    receipt_goods_place = models.CharField('receipt_goods_place',max_length=255)
    consignee = models.CharField('consignee',max_length=255)
    phone = models.CharField('phone',max_length=255)
    fax = models.CharField('fax',max_length=255)
    orderer = models.CharField('orderer',max_length=255)
    advance_scale = models.FloatField('advance_scale',null=True)
    originator = models.CharField('originator',max_length=255)
    summary = models.CharField('summary',max_length=255)
    branch = models.CharField('branch',max_length=255)
    state = models.IntegerField('state')
    is_specimen = models.IntegerField('is_specimen')
    supcto_id = models.IntegerField('supcto_id')
    shipping_mode_id = models.IntegerField('shipping_mode_id')
    person_id = models.IntegerField('person_id')
    sales_plan_order_id = models.IntegerField('sales_plan_order_id')
    print_num = models.IntegerField('print_num',default=0)
    is_show = models.IntegerField('is_show',default=2)
    is_verification = models.CharField('is_verification',max_length=1)
    miss_order_id = models.IntegerField('miss_order_id')
    activity_id = models.IntegerField('activity_id')
    is_app_order = models.IntegerField('is_app_order')
    is_return_goods = models.IntegerField('print_num',default=0)
    app_order_identifier = models.CharField('branch',max_length=255)
    app_send_time = models.DateTimeField('create_time',null=True)
    is_create_stock_order = models.IntegerField('print_num',default=0)

    def create(self,parent_id,identifier,break_code,payment,order_type,create_time,end_validity_time,deliver_goods_place,receipt_goods_place,consignee,phone,fax,orderer,advance_scale,originator,summary,branch,state,is_specimen,supcto_id,shipping_mode_id,person_id,sales_plan_order_id,print_num,is_show,is_verification,miss_order_id,activity_id,is_app_order,is_return_goods,app_order_identifier,app_send_time,is_create_stock_order):
        obj = self.create(parent_id=parent_id,identifier=identifier,break_code=break_code,payment=payment,order_type=order_type,create_time=create_time,end_validity_time=end_validity_time,deliver_goods_place=deliver_goods_place,receipt_goods_place=receipt_goods_place,consignee=consignee,phone=phone,fax=fax,orderer=orderer,advance_scale=advance_scale,originator=originator,summary=summary,branch=branch,state=state,is_specimen=is_specimen,supcto_id=supcto_id,shipping_mode_id=shipping_mode_id,person_id=person_id,sales_plan_order_id=sales_plan_order_id,print_num=print_num,is_show=is_show,is_verification=is_verification,miss_order_id=miss_order_id,activity_id=activity_id,is_app_order=is_app_order,is_return_goods=is_return_goods,app_order_identifier=app_order_identifier,app_send_time=app_send_time,is_create_stock_order=is_create_stock_order)
        return obj

    def __unicode__(self):
        aaa = ['parent_id','identifier','break_code','payment','order_type','create_time','end_validity_time','deliver_goods_place','receipt_goods_place','consignee','phone','fax','orderer','advance_scale','originator','summary','branch','state','is_specimen','supcto_id','shipping_mode_id','person_id','sales_plan_order_id','print_num','is_show','is_verification','miss_order_id','activity_id','is_app_order','is_return_goods','app_order_identifier','app_send_time','is_create_stock_order']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "sales_order"
        verbose_name = "sales_order表"
        verbose_name_plural = "sales_order表"
        
        
class SalesOrderCommodity(models.Model):

    sales_order_id = models.IntegerField('sales_order_id')
    commodity_specification_id = models.IntegerField('commodity_specification_id')
    deliver_goods_money = models.FloatField('deliver_goods_money',null=True)
    deliver_goods_num = models.IntegerField('deliver_goods_num')
    return_goods_num = models.IntegerField('return_goods_num')
    receiving_goods_money = models.FloatField('receiving_goods_money',null=True)
    receiving_goods_num = models.IntegerField('receiving_goods_num')
    damage_num = models.IntegerField('damage_num')
    damage_money = models.FloatField('damage_money',null=True)
    discount = models.FloatField('discount',null=True)
    unit_price = models.FloatField('unit_price',null=True)
    taxes_money = models.FloatField('taxes_money',null=True)
    taxes = models.FloatField('taxes',null=True)
    batch_number = models.CharField('batch_number',max_length=255)
    remark = models.CharField('remark',max_length=255)
    is_special_offer = models.IntegerField('is_special_offer')
    warehouse_id = models.IntegerField('warehouse_id')
    app_amountMoney = models.FloatField('app_amountMoney',null=True)

    def create(self,sales_order_id,commodity_specification_id,deliver_goods_money,deliver_goods_num,return_goods_num,receiving_goods_money,receiving_goods_num,damage_num,damage_money,discount,unit_price,taxes_money,taxes,batch_number,remark,is_special_offer,warehouse_id,app_amountMoney):
        obj = self.create(sales_order_id=sales_order_id,commodity_specification_id=commodity_specification_id,deliver_goods_money=deliver_goods_money,deliver_goods_num=deliver_goods_num,return_goods_num=return_goods_num,receiving_goods_money=receiving_goods_money,receiving_goods_num=receiving_goods_num,damage_num=damage_num,damage_money=damage_money,discount=discount,unit_price=unit_price,taxes_money=taxes_money,taxes=taxes,batch_number=batch_number,remark=remark,is_special_offer=is_special_offer,warehouse_id=warehouse_id,app_amountMoney=app_amountMoney)
        return obj

    def __unicode__(self):
        aaa = ['sales_order_id','commodity_specification_id','deliver_goods_money','deliver_goods_num','return_goods_num','receiving_goods_money','receiving_goods_num','damage_num','damage_money','discount','unit_price','taxes_money','taxes','batch_number','remark','is_special_offer','warehouse_id','app_amountMoney']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "sales_order_commodity"
        verbose_name = "sales_order_commodity表"
        verbose_name_plural = "sales_order_commodity表"
        
        
class SalesOrderReviewer(models.Model):

    sales_order_id = models.IntegerField('sales_order_id')
    reviewer_id = models.IntegerField('reviewer_id')
    reviewer_type = models.IntegerField('reviewer_type')

    def create(self,sales_order_id,reviewer_id,reviewer_type):
        obj = self.create(sales_order_id=sales_order_id,reviewer_id=reviewer_id,reviewer_type=reviewer_type)
        return obj

    def __unicode__(self):
        aaa = ['sales_order_id','reviewer_id','reviewer_type']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "sales_order_reviewer"
        verbose_name = "sales_order_reviewer表"
        verbose_name_plural = "sales_order_reviewer表"
        
    
class SalesPlanOrder(models.Model):

    identifier = models.CharField('identifier',max_length=255)
    create_time = models.DateTimeField('create_time',null=True)
    end_time = models.DateField('end_time',null=True)
    currency = models.IntegerField('currency')
    branch = models.CharField('branch',max_length=255)
    originator = models.CharField('originator',max_length=255)
    summary = models.CharField('summary',max_length=255)
    supcto_id = models.IntegerField('supcto_id')
    person_id = models.IntegerField('person_id')
    state = models.IntegerField('state')
    is_app_order = models.IntegerField('is_app_order')
    app_consignee_name = models.CharField('app_consignee_name',max_length=255)
    app_consignee_phone = models.CharField('app_consignee_phone',max_length=255)
    app_consignee_address = models.CharField('app_consignee_address',max_length=255)
    miss_order_id = models.IntegerField('miss_order_id')
    activity_id = models.IntegerField('activity_id')
    fax = models.CharField('fax',max_length=255)
    shipping_mode_id = models.IntegerField('shipping_mode_id')
    phone = models.CharField('phone',max_length=255)
    deliver_goods_place = models.CharField('deliver_goods_place',max_length=255)
    orderer = models.CharField('orderer',max_length=255)

    def create(self,identifier,create_time,end_time,currency,branch,originator,summary,supcto_id,person_id,state,is_app_order,app_consignee_name,app_consignee_phone,app_consignee_address,miss_order_id,activity_id,fax,shipping_mode_id,phone,deliver_goods_place,orderer):
        obj = self.create(identifier=identifier,create_time=create_time,end_time=end_time,currency=currency,branch=branch,originator=originator,summary=summary,supcto_id=supcto_id,person_id=person_id,state=state,is_app_order=is_app_order,app_consignee_name=app_consignee_name,app_consignee_phone=app_consignee_phone,app_consignee_address=app_consignee_address,miss_order_id=miss_order_id,activity_id=activity_id,fax=fax,shipping_mode_id=shipping_mode_id,phone=phone,deliver_goods_place=deliver_goods_place,orderer=orderer)
        return obj

    def __unicode__(self):
        aaa = ['identifier','create_time','end_time','currency','branch','originator','summary','supcto_id','person_id','state','is_app_order','app_consignee_name','app_consignee_phone','app_consignee_address','miss_order_id','activity_id','fax','shipping_mode_id','phone','deliver_goods_place','orderer']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "sales_plan_order"
        verbose_name = "sales_plan_order表"
        verbose_name_plural = "sales_plan_order表"


class SalesPlanOrderCommodity(models.Model):

    sales_plan_order_id = models.IntegerField('sales_plan_order_id')
    commodity_specification_id = models.IntegerField('commodity_specification_id')
    number = models.IntegerField('number')
    unit_price = models.FloatField('unit_price',null=True)
    money = models.FloatField('money',null=True)
    remark = models.CharField('remark',max_length=255)

    def create(self,sales_plan_order_id,commodity_specification_id,number,unit_price,money,remark):
        obj = self.create(sales_plan_order_id=sales_plan_order_id,commodity_specification_id=commodity_specification_id,number=number,unit_price=unit_price,money=money,remark=remark)
        return obj

    def __unicode__(self):
        aaa = ['sales_plan_order_id','commodity_specification_id','number','unit_price','money','remark']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "sales_plan_order_commodity"
        verbose_name = "sales_plan_order_commodity表"
        verbose_name_plural = "sales_plan_order_commodity表"


class SettlementType(models.Model):

    name = models.CharField('orderer',max_length=255)
    identifier = models.CharField('identifier',max_length=255)
    operator_identifier = models.CharField('operator_identifier',max_length=255)
    operator_time = models.DateTimeField('operator_time', null=True)
    is_delete = models.IntegerField('number',default=0)

    def create(self,name,identifier,operator_identifier,operator_time,is_delete):
        obj = self.create(name=name,identifier=identifier,operator_identifier=operator_identifier,operator_time=operator_time,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['name','identifier','operator_identifier','operator_time','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "settlement_type"
        verbose_name = "settlement_type表"
        verbose_name_plural = "settlement_type表"


class ShippingMode(models.Model):

    name = models.CharField('orderer',max_length=255)
    operator_identifier = models.CharField('operator_identifier',max_length=255)
    operator_time = models.DateTimeField('operator_time', null=True)
    is_delete = models.IntegerField('number',default=0)
    identifier = models.CharField('identifier', max_length=255)

    def create(self,name,operator_identifier,operator_time,is_delete,identifier):
        obj = self.create(name=name,operator_identifier=operator_identifier,operator_time=operator_time,is_delete=is_delete,identifier=identifier)
        return obj

    def __unicode__(self):
        aaa = ['name','operator_identifier','operator_time','is_delete','identifier']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "shipping_mode"
        verbose_name = "shipping_mode表"
        verbose_name_plural = "shipping_mode表"


class Supcto(models.Model):
    classification_id = models.IntegerField('classification_id')
    name = models.CharField('name',max_length=255)
    full_name = models.CharField('full_name',max_length=255)
    frade = models.IntegerField('frade')
    from_type = models.IntegerField('from_type')
    settlement_type_id = models.IntegerField('settlement_type_id')
    phone = models.CharField('phone',max_length=255)
    contact_people = models.CharField('contact_people',max_length=255)
    postcode = models.CharField('postcode',max_length=255)
    fax = models.CharField('fax',max_length=255)
    bank_account = models.CharField('bank_account',max_length=255)
    bank = models.CharField('bank',max_length=255)
    ratepaying = models.CharField('ratepaying',max_length=255)
    mailbox = models.CharField('mailbox',max_length=255)
    invoice_type = models.IntegerField('invoice_type')
    delivery_address = models.CharField('delivery_address',max_length=255)
    credit_days = models.IntegerField('credit_days')
    credit_money = models.IntegerField('credit_money')
    identifier = models.CharField('identifier',max_length=255)
    information = models.CharField('information',max_length=255)
    other_information = models.CharField('other_information',max_length=255)
    department_id = models.IntegerField('department_id')
    person_id = models.IntegerField('person_id')
    currency = models.IntegerField('currency')
    communication_address = models.CharField('communication_address',max_length=255)
    taxes = models.FloatField('taxes',null=True)
    member = models.CharField('member',max_length=255)
    shipping_mode_id = models.IntegerField('shipping_mode_id')
    remark = models.CharField('remark',max_length=255)
    common_phone = models.CharField('common_phone',max_length=255)
    reserve_phone = models.CharField('reserve_phone',max_length=255)
    state = models.IntegerField('state')
    province = models.CharField('province',max_length=255)
    city = models.CharField('city',max_length=255)
    area = models.CharField('area',max_length=255)
    customer_or_supplier = models.IntegerField('customer_or_supplier')
    operator_identifier = models.CharField('operator_identifier',max_length=255)
    operator_time = models.DateTimeField('operator_time', null=True)
    province_code = models.CharField('province_code',max_length=255)
    city_code = models.CharField('city_code',max_length=255)
    area_code = models.CharField('area_code',max_length=255)
    website = models.CharField('website',max_length=255)
    memory_code = models.CharField('memory_code',max_length=255)
    useable = models.IntegerField('currency')
    advance_money = models.FloatField('advance_money',null=True)
    is_show = models.IntegerField('is_show',default=1)
    parent_id = models.IntegerField('parent_id')

    def create(self,classification_id,name,full,frade,from_type,settlement_type_id,phone,contact_people,postcode,fax,bank_account,bank,ratepaying,mailbox,invoice_type,delivery_address,credit_days,credit_money,identifier,information,other_information,department_id,person_id,currency,communication_address,taxes,member,shipping_mode_id,remark,common_phone,reserve_phone,state,province,city,area,customer_or_supplier,operator_identifier,operator_time,province_code,city_code,area_code,website,memory_code,useable,advance_money,is_show,parent_id):
        obj = self.create(classification_id=classification_id,name=name,full=full,frade=frade,from_type=from_type,settlement_type_id=settlement_type_id,phone=phone,contact_people=contact_people,postcode=postcode,fax=fax,bank_account=bank_account,bank=bank,ratepaying=ratepaying,mailbox=mailbox,invoice_type=invoice_type,delivery_address=delivery_address,credit_days=credit_days,credit_money=credit_money,identifier=identifier,information=information,other_information=other_information,department_id=department_id,person_id=person_id,currency=currency,communication_address=communication_address,taxes=taxes,member=member,shipping_mode_id=shipping_mode_id,remark=remark,common_phone=common_phone,reserve_phone=reserve_phone,state=state,province=province,city=city,area=area,customer_or_supplier=customer_or_supplier,operator_identifier=operator_identifier,operator_time=operator_time,province_code=province_code,city_code=city_code,area_code=area_code,website=website,memory_code=memory_code,useable=useable,advance_money=advance_money,is_show=is_show,parent_id=parent_id)
        return obj

    def __unicode__(self):
        aaa = ['classification_id','name','full','frade','from_type','settlement_type_id','phone','contact_people','postcode','fax','bank_account','bank','ratepaying','mailbox','invoice_type','delivery_address','credit_days','credit_money','identifier','information','other_information','department_id','person_id','currency','communication_address','taxes','member','shipping_mode_id','remark','common_phone','reserve_phone','state','province','city','area','customer_or_supplier','operator_identifier','operator_time','province_code','city_code','area_code','website','memory_code','useable','advance_money','is_show','parent_id']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "supcto"
        verbose_name = "supcto表"
        verbose_name_plural = "supcto表"


class SupctoCommodity(models.Model):

    commodity_id = models.IntegerField('commodity_id')
    supcto_id = models.IntegerField('supcto_id')
    price = models.FloatField('price',null=True)

    def create(self,commodity_id,supcto_id,price):
        obj = self.create(commodity_id=commodity_id,supcto_id=supcto_id,price=price)
        return obj

    def __unicode__(self):
        aaa = ['commodity_id','supcto_id','price']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "supcto_commodity"
        verbose_name = "supcto_commodity表"
        verbose_name_plural = "supcto_commodity表"


class TakeStockOrder(models.Model):

    take_stock_date = models.DateTimeField('take_stock_date', null=True)
    identifier = models.CharField('identifier',max_length=255)
    warehouse_id = models.IntegerField('warehouse_id')
    person_id = models.IntegerField('person_id')
    originator = models.CharField('originator',max_length=255)
    finance_reviewer = models.CharField('finance_reviewer',max_length=255)
    manager_reviewer = models.CharField('manager_reviewer',max_length=255)
    summary = models.CharField('summary',max_length=255)
    state = models.IntegerField('state')
    print_num = models.IntegerField('print_num',default=0)
    is_delete = models.IntegerField('is_delete',default=0)

    def create(self,take_stock_date,identifier,warehouse_id,person_id,originator,finance_reviewer,manager_reviewer,summary,state,print_num,is_delete):
        obj = self.create(take_stock_date=take_stock_date,identifier=identifier,warehouse_id=warehouse_id,person_id=person_id,originator=originator,finance_reviewer=finance_reviewer,manager_reviewer=manager_reviewer,summary=summary,state=state,print_num=print_num,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['take_stock_date','identifier','warehouse_id','person_id','originator','finance_reviewer','manager_reviewer','summary','state','print_num','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "take_stock_order"
        verbose_name = "take_stock_order表"
        verbose_name_plural = "take_stock_order表"


class TakeStockOrderCommodity(models.Model):

    take_stock_order_id = models.IntegerField('take_stock_order_id')
    commodity_specification_id = models.IntegerField('commodity_specification_id')
    inventory_num = models.IntegerField('inventory_num')
    real_num = models.IntegerField('real_num')
    profit_or_loss_num = models.IntegerField('profit_or_loss_num')
    unit_price = models.FloatField('unit_price',null=True)
    money = models.FloatField('money',null=True)

    def create(self,take_stock_order_id,commodity_specification_id,inventory_num,real_num,profit_or_loss_num,unit_price,money):
        obj = self.create(take_stock_order_id=take_stock_order_id,commodity_specification_id=commodity_specification_id,inventory_num=inventory_num,real_num=real_num,profit_or_loss_num=profit_or_loss_num,unit_price=unit_price,money=money)
        return obj

    def __unicode__(self):
        aaa = ['take_stock_order_id','commodity_specification_id','inventory_num','real_num','profit_or_loss_num','unit_price,money']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "take_stock_order_commodity"
        verbose_name = "take_stock_order_commodity表"
        verbose_name_plural = "take_stock_order_commodity表"


class Unit(models.Model):

    name = models.CharField('name',max_length=255)
    specification_id = models.IntegerField('specification_id')
    ratio_denominator = models.IntegerField('ratio_denominator')
    ratio_molecular = models.IntegerField('ratio_molecular')
    purchase_price = models.FloatField('purchase_price',null=True)
    commonly_price = models.FloatField('commonly_price',null=True)
    mini_price = models.FloatField('mini_price',null=True)
    bar_code = models.CharField('bar_code',max_length=255)
    sales_unit = models.CharField('sales_unit',max_length=255)
    basic_unit = models.IntegerField('basic_unit')
    warehouse_unit = models.CharField('warehouse_unit',max_length=255)
    purchasing_unit = models.CharField('purchasing_unit',max_length=255)
    mini_purchasing = models.IntegerField('mini_purchasing')
    temp_commonly_price = models.FloatField('temp_commonly_price',null=True)

    def create(self,name,specification_id,ratio_denominator,ratio_molecular,purchase_price,commonly_price,mini_price,bar_code,sales_unit,basic_unit,warehouse_unit,purchasing_unit,mini_purchasing,temp_commonly_price):
        obj = self.create(name=name,specification_id=specification_id,ratio_denominator=ratio_denominator,ratio_molecular=ratio_molecular,purchase_price=purchase_price,commonly_price=commonly_price,mini_price=mini_price,bar_code=bar_code,sales_unit=sales_unit,basic_unit=basic_unit,warehouse_unit=warehouse_unit,purchasing_unit=purchasing_unit,mini_purchasing=mini_purchasing,temp_commonly_price=temp_commonly_price)
        return obj

    def __unicode__(self):
        aaa = ['name','specification_id','ratio_denominator','ratio_molecular','purchase_price','commonly_price','mini_price','bar_code','sales_unit','basic_unit','warehouse_unit','purchasing_unit','mini_purchasing','temp_commonly_price']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "unit"
        verbose_name = "unit表"
        verbose_name_plural = "unit表"


class Warehouse(models.Model):

    name = models.CharField('name',max_length=255)
    position = models.CharField('position',max_length=255)
    operator_identifier = models.CharField('operator_identifier',max_length=255)
    operator_time = models.DateTimeField('operator_time', null=True)
    identifier = models.CharField('identifier',max_length=255)
    is_delete = models.IntegerField('is_delete')

    def create(self,name,position,operator_identifier,operator_time,identifier,is_delete):
        obj = self.create(name=name,position=position,operator_identifier=operator_identifier,operator_time=operator_time,identifier=identifier,is_delete=is_delete)
        return obj

    def __unicode__(self):
        aaa = ['name','position','operator_identifier','operator_time','identifier','is_delete']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "warehouse"
        verbose_name = "warehouse表"
        verbose_name_plural = "warehouse表"


class Writeoff(models.Model):

    writeoff_code = models.CharField('writeoff_code',max_length=255)
    writeoff_type = models.CharField('writeoff_type',max_length=1)
    company_one = models.IntegerField('company_one')
    company_two = models.IntegerField('company_two')
    money = models.FloatField('money',null=True)
    create_date = models.DateTimeField('create_date', null=True)
    originator = models.CharField('originator',max_length=255)
    person_id = models.IntegerField('person_id')
    summary = models.CharField('summary',max_length=255)
    remark = models.CharField('remark',max_length=255)
    voucher_no = models.CharField('voucher_no',max_length=255)
    branch = models.CharField('branch',max_length=255)

    def create(self,writeoff_code,writeoff_type,company_one,company_two,money,create_date,originator,person_id,summary,remark,voucher_no,branch):
        obj = self.create(writeoff_code=writeoff_code,writeoff_type=writeoff_type,company_one=company_one,company_two=company_two,money=money,create_date=create_date,originator=originator,person_id=person_id,summary=summary,remark=remark,voucher_no=voucher_no,branch=branch)
        return obj

    def __unicode__(self):
        aaa = ['writeoff_code','writeoff_type','company_one','company_two','money','create_date','originator','person_id','summary','remark','voucher_no','branch']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "writeoff"
        verbose_name = "writeoff表"
        verbose_name_plural = "writeoff表"


class WriteoffSub(models.Model):

    writeoff_id = models.IntegerField('writeoff_id')
    procure_sales_id = models.IntegerField('procure_sales_id')
    clear_money = models.FloatField('clear_money',null=True)
    stay_money = models.FloatField('stay_money',null=True)
    the_money = models.IntegerField('the_money')
    is_writeoff = models.CharField('is_writeoff',max_length=255)
    is_procure_sales = models.IntegerField('is_procure_sales')
    remark = models.CharField('remark',max_length=255)

    def create(self,writeoff_id,procure_sales_id,clear_money,stay_money,the_money,is_writeoff,is_procure_sales,remark):
        obj = self.create(writeoff_id=writeoff_id,procure_sales_id=procure_sales_id,clear_money=clear_money,stay_money=stay_money,the_money=the_money,is_writeoff=is_writeoff,is_procure_sales=is_procure_sales,remark=remark)
        return obj

    def __unicode__(self):
        aaa = ['writeoff_id','procure_sales_id','clear_money','stay_money','the_money','is_writeoff','is_procure_sales','remark']
        xz = ''
        for a in aaa:
            value = getattr(self, a)
            xz = a + ':' + str(value) + '\n' +xz
        return xz

    class Meta:
        db_table = "writeoff_sub"
        verbose_name = "writeoff_sub表"
        verbose_name_plural = "writeoff_sub表"
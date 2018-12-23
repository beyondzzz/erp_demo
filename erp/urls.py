"""erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from erp_sites.views import auth,classification,supplierCustomer,commodity,basicOperat,person,procurePlan,salesPlan,salesNormal,allotOrder,takeStock,package,bills,writeoff,breakage,department,goods,log

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^api/basic/login$', auth.loginPost),
    url(r'^api/basic/getCaptcha$', auth.getCaptcha),
    url(r'^api/basic/firstClassification/insert$', classification.firstClassificationInsert),
    url(r'^api/basic/firstClassification/delete$', classification.firstClassificationDelete),
    url(r'^api/basic/firstClassification/update$', classification.firstClassificationUpdate),
    url(r'^api/basic/firstClassification/select$', classification.firstClassificationSelect),
    url(r'^api/basic/secondClassification/insert$', classification.secondClassificationInsert),
    url(r'^api/basic/secondClassification/delete$', classification.secondClassificationDelete),
    url(r'^api/basic/secondClassification/update$', classification.secondClassificationUpdate),
    url(r'^api/basic/secondClassification/select$', classification.secondClassificationSelect),
    url(r'^api/basic/thirdParty/insert$', supplierCustomer.thirdPartyInsert),
    url(r'^api/basic/thirdParty/delete$', supplierCustomer.thirdPartyDelete),
    url(r'^api/basic/thirdParty/update$', supplierCustomer.thirdPartyUpdate),
    url(r'^api/basic/thirdParty/select$', supplierCustomer.thirdPartySelect),
    url(r'^api/basic/thirdParty/singleSelect$', supplierCustomer.thirdPartySingleSelect),
    url(r'^api/basic/commodity/insert$', commodity.commodityInsert),
    url(r'^api/basic/commodity/update$', commodity.commodityUpdate),
    url(r'^api/basic/commodity/multiSelect$', commodity.multiCommoditySelect),
    url(r'^api/basic/commodity/singleSelect$', commodity.singleCommoditySelect),
    url(r'^api/basic/basic/insert$', basicOperat.basicInsert),
    url(r'^api/basic/basic/delete$', basicOperat.basicDelete),
    url(r'^api/basic/basic/update$', basicOperat.basicUpdate),
    url(r'^api/basic/basic/select$', basicOperat.basicSelect),
    url(r'^api/basic/person/insert$', person.personInsert),
    url(r'^api/basic/person/delete$', person.personDelete),
    url(r'^api/basic/person/update$', person.personUpdate),
    url(r'^api/basic/person/select$', person.personSelect),
    url(r'^api/basic/person/updatePwdById$', person.updatePwdByID),
    url(r'^api/basic/procurePlan/insert$', procurePlan.procurePlanInsert),
    url(r'^api/basic/procurePlan/delete$', procurePlan.procurePlanDelete),
    url(r'^api/basic/procurePlan/update$', procurePlan.procurePlanUpdate),
    url(r'^api/basic/procurePlan/select$', procurePlan.procurePlanSelect),
    url(r'^api/basic/procurePlan/upload$', procurePlan.procureUpload),
    url(r'^api/basic/salesPlan/insert$', salesPlan.salesPlanInsert),
    url(r'^api/basic/salesPlan/delete$', salesPlan.salesPlanDelete),
    url(r'^api/basic/salesPlan/update$', salesPlan.salesPlanUpdate),
    url(r'^api/basic/salesPlan/select$', salesPlan.salesPlanSelect),
    url(r'^api/basic/salesPlan/planToNormal$', salesPlan.orderPlanToNormal),
    url(r'^api/basic/salesNormal/insert$', salesNormal.salesNormalInsert),
    url(r'^api/basic/salesNormal/delete$', salesNormal.salesNormalDelete),
    url(r'^api/basic/salesNormal/update$', salesNormal.salesNormalUpdate),
    url(r'^api/basic/salesNormal/select$', salesNormal.salesNormalSelect),
    url(r'^api/basic/allot/insert$', allotOrder.allotInsert),
    url(r'^api/basic/allot/delete$', allotOrder.allotDelete),
    url(r'^api/basic/allot/update$', allotOrder.allotUpdate),
    url(r'^api/basic/allot/select$', allotOrder.allotSelect),
    url(r'^api/basic/stockCheck/insert$', takeStock.stockCheckInsert),
    url(r'^api/basic/stockCheck/delete$', takeStock.stockCheckDelete),
    url(r'^api/basic/stockCheck/update$', takeStock.stockCheckUpdate),
    url(r'^api/basic/stockCheck/select$', takeStock.stockCheckSelect),
    url(r'^api/basic/package/insert$', package.packageOrTeardownInsert),
    url(r'^api/basic/package/delete$', package.packageOrTeardownDelete),
    url(r'^api/basic/package/update$', package.packageOrTeardownUpdate),
    url(r'^api/basic/package/select$', package.packageOrTeardownSelect),
    url(r'^api/basic/bill/insert$', bills.billInsert),
    url(r'^api/basic/bill/singleSelect$', bills.singleBillSelect),
    url(r'^api/basic/bill/multiSelect$', bills.multiBillSelect),
    url(r'^api/basic/writeoff/insert$', writeoff.writeoffInsert),
    url(r'^api/basic/writeoff/singleSelect$', writeoff.singleWriteoffSelect),
    url(r'^api/basic/writeoff/multiSelect$', writeoff.multiWriteoffSelect),
    url(r'^api/basic/breakage/insert$', breakage.breakageInsert),
    url(r'^api/basic/breakage/delete$', breakage.breakageDelete),
    url(r'^api/basic/breakage/update$', breakage.breakageUpdate),
    url(r'^api/basic/breakage/select$', breakage.breakageSelect),
    url(r'^api/basic/goods/insert$', goods.goodsInsert),
    url(r'^api/basic/goods/delete$', goods.goodsDelete),
    url(r'^api/basic/goods/update$', goods.goodsUpdate),
    url(r'^api/basic/goods/select$', goods.goodsSelect),
    url(r'^api/basic/log/select$', log.getLogMsg),
]

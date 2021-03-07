import shutil

import xlrd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Max, F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.core.paginator import Paginator
import time

import requests, re
from .models import *
from django.conf import settings
import os, json
from django.core.paginator import *
from bs4 import BeautifulSoup
from bs4 import element
import os
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from bs4 import BeautifulSoup
from bs4 import element
from concurrent.futures import ThreadPoolExecutor


# 视图接受Web请求并且返回Web响应
# 视图就是一个python函数，被定义在views.py中


# Create your views here.
@login_required
def newService(request):
    return render(request, 'NewFireWall/newService.html')


@login_required
def newAddress(request):
    return render(request, 'NewFireWall/newAddress.html')


@login_required
def newPolicy(request):
    return render(request, 'NewFireWall/newPolicy.html')


@login_required
@csrf_exempt
def searchnewService(request):
    newServiceName = request.GET.get('newServiceName', None)
    newServiceProtocol = request.GET.get('newServiceProtocol', None)
    newServiceComment = request.GET.get('newServiceComment', None)

    # 方法一：
    newServiceobj = NewServiceName.objects.all()

    if newServiceName:
        newServiceobj = newServiceobj.filter(newServiceName__icontains=newServiceName)
    if newServiceProtocol:
        newServiceobj = newServiceobj.filter(newServiceProtocol__icontains=newServiceProtocol)
    if newServiceComment:
        newServiceobj = newServiceobj.filter(newServiceComment__icontains=newServiceComment)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = newServiceobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for newService in newServiceobj:
        dict = {}
        # print("++++++++++++++++")
        # print((newService.newServiceName))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        dict['newServiceName'] = newService.newServiceName
        dict['newServiceProtocol'] = newService.newServiceProtocol
        dict['newServiceComment'] = newService.newServiceComment

        list1.append(dict)

    # try:
    #     list1.sort(key=lambda k: (k.get('newServiceName')), reverse=False)
    #     # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    # except TypeError as e:
    #     pass

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def searchnewAddress(request):
    newAddressName = request.GET.get('newAddressName', None)
    newAddressIP = request.GET.get('newAddressIP', None)
    newAddressComment = request.GET.get('newAddressComment', None)

    # 方法一：
    newAddressobj = NewAddressName.objects.all()

    if newAddressName:
        newAddressobj = newAddressobj.filter(newAddressName__icontains=newAddressName)
    if newAddressIP:
        newAddressobj = newAddressobj.filter(newAddressIP__icontains=newAddressIP)
    if newAddressComment:
        newAddressobj = newAddressobj.filter(newAddressComment__icontains=newAddressComment)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = newAddressobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for newAddress in newAddressobj:
        dict = {}
        # print("++++++++++++++++")
        # print((newService.newServiceName))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        dict['newAddressName'] = newAddress.newAddressName
        dict['newAddressIP'] = newAddress.newAddressIP
        dict['newAddressComment'] = newAddress.newAddressComment

        list1.append(dict)

    # try:
    #     list1.sort(key=lambda k: (k.get('newServiceName')), reverse=False)
    #     # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    # except TypeError as e:
    #     pass

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def searchnewPolicy(request):
    newRuleSa = request.GET.get('sourceIP', None)
    newRuleDa = request.GET.get('directionIP', None)
    newRuleService = request.GET.get('newPolicyService', None)
    newRuleComment = request.GET.get('newPolicyComment', None)

    # 方法一：
    newPolicyobj = NewPolicyManage.objects.all()

    if newRuleSa:
        newPolicyobj = newPolicyobj.filter(newRuleSa__icontains=newRuleSa)
    if newRuleDa:
        newPolicyobj = newPolicyobj.filter(newRuleDa__icontains=newRuleDa)
    if newRuleService:
        newPolicyobj = newPolicyobj.filter(newRuleService__icontains=newRuleService)
    if newRuleComment:
        newPolicyobj = newPolicyobj.filter(newRuleComment__icontains=newRuleComment)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = newPolicyobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for newPolicy in newPolicyobj:
        dict = {}
        dict['newRuleId'] = newPolicy.newRuleId
        dict['newRuleName'] = newPolicy.newRuleName
        dict['newRuleSa'] = newPolicy.newRuleSa
        dict['newRuleDa'] = newPolicy.newRuleDa
        # dict['newRuleIzone'] = newPolicy.newRuleIzone
        # dict['newRuleOzone'] = newPolicy.newRuleOzone
        dict['newRuleService'] = newPolicy.newRuleService
        dict['newRuleOpentime'] = newPolicy.newRuleOpentime
        # dict['newRuleStatus'] = newPolicy.newRuleStatus
        dict['newRuleActive'] = newPolicy.newRuleActive
        dict['newRuleComment'] = newPolicy.newRuleComment
        # dict['newRuleAccount'] = newPolicy.newRuleAccount

        list1.append(dict)

    # try:
    #     list1.sort(key=lambda k: (k.get('newServiceName')), reverse=False)
    #     # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    # except TypeError as e:
    #     pass

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def deletenewServiceall(request):
    try:
        NewServiceName.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deletenewAddressall(request):
    try:
        NewServiceName.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deletenewPolicyall(request):
    try:
        NewPolicyManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initnewService(request):
    NewServiceName.objects.all().delete()

    try:
        filepath = 'static/upload/NewFirewallManage/pf.log'
        with open(filepath, "r", encoding='GBK') as filetmp:
            iptable_Files = filetmp.readlines()

        if "service " not in str(iptable_Files):
            result = "log 文件内容不正确, 请使用启明防火墙导出的策略文件</br>内容形如: service 00001 ..."
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        iptable_Files = str(iptable_Files).split("!")


        serviceList = iptable_Files[37].split("'service ")
        # print(serviceList)
        for num in range(len(serviceList)):
            if serviceList[num] == "\\n', ":
                    continue
            perService = "service " + serviceList[num]
            # print(perService)

            serviceName = re.findall("^service (.*?)', '", perService)
            # print("serviceName: ", serviceName[0].strip("\\n"))
            serviceName = serviceName[0].strip("\\n")

            serviceDescription = re.findall("description (.*?)', '", perService)
            if serviceDescription != []:
                # print("serviceDescription: ", serviceDescription[0].strip("\\n"))
                comment = serviceDescription[0].strip("\\n")
            else:
                # print("serviceDescription 为空")
                comment = "无"


            service_port = re.findall("tcp dest (.*?) source 1 65535", perService)
            servicePort = ""
            for port in service_port:
                servicePort = servicePort + port + "; "
            # print("servicePort: ", servicePort)

            newService = NewServiceName()
            newService.newServiceName = serviceName
            newService.newServiceProtocol = servicePort
            newService.newServiceComment = comment
            newService.save()


        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    # print("------------------")

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initnewAddress(request):
    NewServiceName.objects.all().delete()

    try:
        filepath = 'static/upload/NewFirewallManage/pf.log'


        with open(filepath, "r", encoding='GBK') as filetmp:
            iptable_Files = filetmp.readlines()

        if "address aly" not in str(iptable_Files):
            result = "log 文件内容不正确, 请使用启明防火墙导出的策略文件</br>内容形如: address aly_ ..."
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)


        # print(iptable_Files)
        iptable_Files = str(iptable_Files).split("!")



        # address
        addressList = iptable_Files[35].split("'address ")
        # print(addressList)
        for num in range(len(addressList)):
            # print("***")
            if addressList[num] == "\\n', ":
                continue

            perAddr = "address " + addressList[num]
            # print(perAddr)

            address = re.findall("^address (.*?)', '", perAddr)
            # print("addressName: ", address[0].strip("\\n"))
            addressName = address[0].strip("\\n")



            description = re.findall("description (.*?)', '", perAddr)
            if description != []:
                # print("description: ", description[0].strip("\\n"))
                comment = description[0].strip("\\n")
            else:
                comment = "无"


            hostAddress = re.findall("-address (.*?)', ", perAddr)
            hostAdd = ""
            for per_host_add in hostAddress:
                hostAdd = hostAdd + per_host_add + "; "
            # print("hostAddress: ", hostAdd.replace("\\n", ""))
            ipaddre = hostAdd.replace("\\n", "")

            # print("----------------------")

            # print(addressName, "-", ipaddre, "-", comment)

            newAddress = NewAddressName()
            newAddress.newAddressName = addressName
            newAddress.newAddressIP = ipaddre
            newAddress.newAddressComment = comment
            newAddress.save()


        result = "success"
    except Exception as e:
        print(str(e))

        result = "failed"
    print("------------------")

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initnewPolicy(request):
    NewPolicyManage.objects.all().delete()

    # try:
    filepath = 'static/upload/NewFirewallManage/pf.log'
    f = open(filepath, 'r', encoding='GBK')
    fileContent = f.readlines()


    if "firewall policy " not in str(fileContent):
        result = "log 文件内容不正确, 请使用启明防火墙导出的策略文件</br>内容形如: firewall policy 1 ..."
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)



    # print(iptable_Files)
    iptable_Files = str(fileContent).split("!")
    # print(iptable_Files[60])
    # for num in range(len(iptable_Files)):
    #     print(num)
    #     print(iptable_Files[num])


    # policy
    # print(iptable_Files[70].split("'firewall policy "))
    policyList = iptable_Files[70].split("'firewall policy ")
    # print(policyList)
    for num in range(len(policyList)):
        if policyList[num] == "\\n', ":
                continue
        perPolicy = "firewall policy " + policyList[num]
        # print(perPolicy)

        policyNum = re.findall("^firewall policy (.*?)', '", perPolicy)
        # print("policyNum: ", policyNum[0].strip("\\n"))
        ruleId = policyNum[0].strip("\\n")


        policyAct = re.findall(" action(.*?)', '", perPolicy)
        # print("policyAct: ", policyAct[0].strip("\\n"))
        ruleActive = policyAct[0].strip("\\n")




        policyName = re.findall("' name (.*?)', '", perPolicy)
        # print("policyName: ", policyName[0].strip("\\n"))
        ruleName = policyName[0].strip("\\n")

        policyDescription = re.findall("' description (.*?)', '", perPolicy)
        if policyDescription != []:
            # print("policyDescription: ", policyDescription[0].strip("\\n"))
            comment = policyDescription[0].strip("\\n")
        else:
            # print("policyDescription 为空")
            comment ="无"

        policySrcAddr = re.findall("' src-addr (.*?)', '", perPolicy)
        # print("srcAddr: ", policySrcAddr[0].strip("\\n"))
        ruleSa = policySrcAddr[0].strip("\\n")

        policyDstAddr = re.findall("' dst-addr (.*?)', '", perPolicy)
        # print("dstAddr: ", policyDstAddr[0].strip("\\n"))
        ruleDa = policyDstAddr[0].strip("\\n")


        policyService = re.findall("' service (.*?)', '", perPolicy)
        # print("policyService: ", policyService[0].strip("\\n"))
        rulenewService = policyService[0].strip("\\n")

        policyTimerange = re.findall("' timerange (.*?)', '", perPolicy)
        # print("policyTimerange: ", policyTimerange[0].strip("\\n"))
        ruleOpentime =policyTimerange[0].strip("\\n")



        print(ruleId, "-", ruleActive, "-", ruleName, "-", ruleSa, "-", ruleDa, "-", rulenewService, "-", ruleOpentime, "-", comment)

        newPolicy = NewPolicyManage()
        newPolicy.newRuleId = ruleId
        newPolicy.newRuleName = ruleName
        # print("ruleName:")
        # print("------------------++++++++++++++++++++++")
        # print(ruleName)
        newPolicy.newRuleSa = ruleSa
        newPolicy.newRuleDa = ruleDa
        # newPolicy.newRuleIzone = ruleIzone
        # newPolicy.newRuleOzone = ruleOzone
        newPolicy.newRuleService = rulenewService
        newPolicy.newRuleOpentime = ruleOpentime
        # newPolicy.newRuleStatus = ruleStatus
        newPolicy.newRuleActive = ruleActive
        newPolicy.newRuleComment = comment
        # newPolicy.newRuleAccount = ruleAccount
        newPolicy.save()


















    # 命中次数
    # # 设置路径
    # path = 'static/upload/NewFirewallManage/NewFirewall.xls'
    #
    # # 打开execl
    # workbook = xlrd.open_workbook(path)
    #
    # # 输出Excel文件中所有sheet的名字
    # # print(workbook.sheet_names())
    #
    # # 根据sheet索引或者名称获取sheet内容
    # NewFirewallSheet = workbook.sheets()[0]  # 通过索引获取
    # # NewFirewallSheet = workbook.sheet_by_index(0)  # 通过索引获取
    # # NewFirewallSheet = workbook.sheet_by_name('ECS')  # 通过名称获取
    #
    # # print(ecsSheet.name)  # 获取sheet名称
    # rowNum = NewFirewallSheet.nrows  # sheet行数
    # colNum = NewFirewallSheet.ncols  # sheet列数
    #
    # firstLineValue = ['序号 ', '规则名 ', '源地址 ', '目的地址 ', '流入安全域 ', '流出安全域 ', '服务 ', '动作 ', '生效 ', '命中数 ', '所属策略组 ', '操作 ']
    # # print(firstLineValue)
    # # print(NewFirewallSheet.row_values(0))
    #
    # if NewFirewallSheet.row_values(0) != firstLineValue:
    #     result = "xls 文件列名不正确,请参考模板文件</br>列名例如: '规则名 '"
    #     print("[ log ] -> ", result)
    #     return JsonResponse(result, safe=False)
    #
    # # # 获取所有单元格的内容
    # # list = []
    # # for i in range(rowNum):
    # #     rowlist = []
    # #     for j in range(colNum):
    # #         rowlist.append(Data_sheet.cell_value(i, j))
    # #
    # #         print(type(date_value), date_value)
    # #     list.append(rowlist)
    #
    # # 输出所有单元格的内容
    # for row in range(rowNum):
    #     if row == 0:
    #         continue
    #
    #     ruleId = NewFirewallSheet.cell_value(row, 0)
    #     ruleName = NewFirewallSheet.cell_value(row, 1)
    #     ruleSa = NewFirewallSheet.cell_value(row, 2)
    #     ruleDa = NewFirewallSheet.cell_value(row, 3)
    #     ruleIzone = NewFirewallSheet.cell_value(row, 4)
    #     ruleOzone = NewFirewallSheet.cell_value(row, 5)
    #     rulenewService = NewFirewallSheet.cell_value(row, 6)
    #     ruleActive = NewFirewallSheet.cell_value(row, 7)
    #     ruleStatus = NewFirewallSheet.cell_value(row, 8)
    #     ruleAccount = NewFirewallSheet.cell_value(row, 9)
    #     ruleComment = NewFirewallSheet.cell_value(row, 10)
    #
    #     if "..." in str(ruleAccount):
    #         ruleAccount = str(ruleAccount).strip("...")
    #         ruleAccount = ruleAccount + "00000000"
    #     ruleAccount = int(ruleAccount)
    #
    #     NewPolicyManage.objects.filter(ruleName=ruleName).update(ruleAccount=ruleAccount)

    result = "success"
    #
    # except Exception as e:
    #     print(str(e))
    #
    #     result = "failed"
    # # print("------------------")

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def uploadnewService(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filename = textFile.name
        filepath = "static/upload/NewFirewallManage/newService.log"
        # filepath = os.path.join(settings.UPLOAD_DIR, filename)
        # print(filepath)

        dirpath = os.path.join(settings.UPLOAD_DIR, "NewFirewallManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "NewFirewallManage/bak/newService" + time.strftime('%Y_%b_%d-%H_%M_%S'))
            # print(filepath)
            # print(new_filepath)
            shutil.move(filepath, new_filepath)
            # os.rename(filepath, new_filepath)
            # print("ok")

        with open(filepath, 'wb') as f:
            for text in textFile.chunks():  # 分包写入
                f.write(text)

    newServiceobj = NewServiceName.objects.all()

    total = newServiceobj.count()
    resultdict = {}
    list1 = []
    for newService in newServiceobj:
        dict = {}
        dict['newServiceName'] = newService.newServiceName
        dict['newServiceProtocol'] = newService.newServiceProtocol
        dict['newServiceComment'] = newService.newServiceComment

        list1.append(dict)

    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

    # 分页，?page=3&limit=20
    # page = request.GET.get('page')
    # limit = request.GET.get('limit')
    # pageInator = Paginator(list1, limit)
    # list1 = pageInator.page(page)
    # print(page, list1)
    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def uploadnewAddress(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        filepath = os.path.join(settings.UPLOAD_DIR, "NewFirewallManage/newAddress.log")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "NewFirewallManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "NewFirewallManage/bak/" + "newAddress" + time.strftime('%Y_%b_%d-%H_%M_%S') + ".log")
            # print(filepath)
            # print(new_filepath)
            shutil.move(filepath, new_filepath)
            # os.rename(filepath, new_filepath)
            # print("ok")

        with open(filepath, 'wb') as f:
            for text in textFile.chunks():  # 分包写入
                f.write(text)

    resultdict = {"code": 0}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def uploadnewPolicy(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        filepath = os.path.join(settings.UPLOAD_DIR, "NewFirewallManage/pf.log")

        dirpath = os.path.join(settings.UPLOAD_DIR, "NewFirewallManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        # print(filepath)
        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "NewFirewallManage/bak/" + "pf" + time.strftime('%Y_%b_%d-%H_%M_%S') + ".log")
            # print(filepath)
            # print(new_filepath)
            shutil.move(filepath, new_filepath)
            # os.rename(filepath, new_filepath)
            # print("ok")

        with open(filepath, 'wb') as f:
            for text in textFile.chunks():  # 分包写入
                f.write(text)

    resultdict = {"code": 0}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def uploadhitnumber(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        filepath = os.path.join(settings.UPLOAD_DIR, "NewFirewallManage/NewFirewall.xls")

        dirpath = os.path.join(settings.UPLOAD_DIR, "NewFirewallManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        # print(filepath)
        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "NewFirewallManage/bak/NewFirewall" + time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")
            # print(filepath)
            # print(new_filepath)
            shutil.move(filepath, new_filepath)
            # os.rename(filepath, new_filepath)
            # print("ok")

        with open(filepath, 'wb') as f:
            for text in textFile.chunks():  # 分包写入
                f.write(text)

    resultdict = {"code": 0}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def getnewServicelist(request):
    newServiceobj = NewServiceName.objects.all()

    total = newServiceobj.count()
    resultdict = {}
    list1 = []
    for newService in newServiceobj:
        dict = {}
        dict['newServiceName'] = newService.newServiceName
        dict['newServiceProtocol'] = newService.newServiceProtocol
        dict['newServiceComment'] = newService.newServiceComment

        list1.append(dict)

    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

    # try:
    #     list1.sort(key=lambda k: (k.get('newServiceName')), reverse=False)
    #     # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    # except TypeError as e:
    #     pass

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def getnewAddresslist(request):
    newAddressobj = NewAddressName.objects.all()

    total = newAddressobj.count()
    resultdict = {}
    list1 = []
    for newAddress in newAddressobj:
        dict = {}
        dict['newAddressName'] = newAddress.newAddressName
        dict['newAddressIP'] = newAddress.newAddressIP
        dict['newAddressComment'] = newAddress.newAddressComment

        list1.append(dict)

    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

    # try:
    #     list1.sort(key=lambda k: (k.get('newServiceName')), reverse=False)
    #     # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    # except TypeError as e:
    #     pass

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def getnewPolicylist(request):
    newPolicyobj = NewPolicyManage.objects.all()

    total = newPolicyobj.count()
    resultdict = {}
    list1 = []
    for newPolicy in newPolicyobj:
        dict = {}
        dict['newRuleId'] = newPolicy.newRuleId
        dict['newRuleName'] = newPolicy.newRuleName
        dict['newRuleSa'] = newPolicy.newRuleSa
        dict['newRuleDa'] = newPolicy.newRuleDa
        # dict['newRuleIzone'] = newPolicy.newRuleIzone
        # dict['newRuleOzone'] = newPolicy.newRuleOzone
        dict['newRuleService'] = newPolicy.newRuleService
        dict['newRuleOpentime'] = newPolicy.newRuleOpentime
        # dict['newRuleStatus'] = newPolicy.newRuleStatus
        dict['newRuleActive'] = newPolicy.newRuleActive
        dict['newRuleComment'] = newPolicy.newRuleComment
        # dict['newRuleAccount'] = newPolicy.newRuleAccount

        list1.append(dict)

    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

    # try:
    #     list1.sort(key=lambda k: (k.get('ruleId')), reverse=False)
    #     # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    # except TypeError as e:
    #     pass

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def getsourceip(request):
    ruleSa = request.POST.get('ruleSa', None).strip(" ")
    if "any" in ruleSa:
        ipaddr = "该数据不是单一IP组，无法查询！"
        return JsonResponse(ipaddr, safe=False)
    elif ";" not in ruleSa:

        newAddressobj = NewServiceName.objects.filter(newAddressName__icontains=ruleSa.replace(" ", ""))
        ipaddr = ''
        for newAddress in newAddressobj:
            ipaddr = ruleSa + ": " + newAddress.newAddressIP + ipaddr + " "

    elif ";" in ruleSa:
        sourceip = ruleSa.split(";")
        ipaddr = ''
        for source in sourceip:
            newAddressobj = NewServiceName.objects.filter(newAddressName__icontains=source.replace(" ", ""))
            ipnewAddress = ''
            for newAddress in newAddressobj:
                ipnewAddress = source + ": " + newAddress.newAddressIP + ipnewAddress + " \r\n" + "</br>"
            ipaddr = ipnewAddress + ipaddr

    ipaddr = ipaddr.replace(":", ":</br>")
    ipaddr = ipaddr.replace(";", ",</br>")
    # ipaddr = ipaddr.split(";")
    # ipaddr = ruleSa + "\n" + ipaddr
    return JsonResponse(ipaddr, safe=False)


@login_required
@csrf_exempt
def getdirectionip(request):
    ruleDa = request.POST.get('ruleDa', None).strip(" ")
    if "" == ruleDa:
        ipaddr = "该数据不是单一IP组，无法查询！"

        # ipaddr = ipaddr.split(";")

    elif ";" in ruleDa:
        directionip = ruleDa.split(";")
        ipaddr = ''
        for direction in directionip:
            newAddressobj = NewServiceName.objects.filter(newAddressName__icontains=direction.replace(" ", ""))
            ipnewAddress = ''
            for newAddress in newAddressobj:
                ipnewAddress = direction + ": " + newAddress.newAddressIP + ipnewAddress + " \r\n" + "</br>"
            ipaddr = ipnewAddress + ipaddr

    else:

        # elif ruleDa.startswith(" aly") | ruleDa.startswith(" ad"):

        newAddressobj = NewServiceName.objects.filter(newAddressName__icontains=ruleDa.replace(" ", ""))
        ipaddr = ''
        for newAddress in newAddressobj:
            ipaddr = ruleDa + ": " + newAddress.newAddressIP + ipaddr + " \r\n" + "</br>"

    ipaddr = ipaddr.replace(":", ":</br>")
    ipaddr = ipaddr.replace(";", ",</br>")
    # else:
    #     ipaddr = "该数据不是单一IP组，无法查询！"
    return JsonResponse(ipaddr, safe=False)


@login_required
@csrf_exempt
def getrulenewService(request):
    rulenewService = request.POST.get('rulenewService', None).strip(" ")
    # print(";" in rulenewService)
    # print(rulenewService)
    # print(rulenewService)

    if "any" == rulenewService:
        newService = "该数据存在多个服务组，查询失败！"
        return JsonResponse(newService, safe=False)

    elif ";" in rulenewService:
        rulenewService = rulenewService.split(";")
        newService = ''
        for rule in rulenewService:
            # print("rule:", rule)
            # newServiceobj = NewServiceName.objects.filter(newServiceName__icontains="rule")
            newServiceobj = NewServiceName.objects.filter(newServiceName__icontains=rule.replace(" ", ""))
            serv = ''
            for ser in newServiceobj:
                serv = rule + ": </br>" + ser.newServiceProtocol + serv + " \r\n" + "</br>"
                # print("---++++++++++++", serv)
            newService = serv + newService
        # print("-------", newService)

        # newService = newService.split(";")

    else:
        newServiceobj = NewServiceName.objects.filter(newServiceName__icontains=rulenewService.replace(" ", ""))
        newService = ''
        for srv in newServiceobj:
            newService = srv.newServiceProtocol + newService + " \r\n" + "</br>"

    # newService = newService.replace(":", ":</br>")
    # newService = newService.replace(";", ",</br>")
    if newService == "":
        newService = "未查询到数据"

    return JsonResponse(newService, safe=False)


@login_required
@csrf_exempt
def downloadNewFirewallTemplateFile(request):
    print("ooooooooooooooooooooooooooooooooo")
    file = open('static/upload/NewFirewallManage/newFirewallTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="newFirewallTemplate%s.xls"' % int(time.time())
    return response

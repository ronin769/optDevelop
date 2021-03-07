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
def service(request):
    return render(request, 'FireWall/service.html')


@login_required
def address(request):
    return render(request, 'FireWall/address.html')


@login_required
def policy(request):
    return render(request, 'FireWall/policy.html')


@login_required
@csrf_exempt
def searchservice(request):
    serviceName = request.GET.get('serviceName', None)
    serviceProtocol = request.GET.get('serviceProtocol', None)
    serviceComment = request.GET.get('serviceComment', None)

    # 方法一：
    serviceobj = ServiceName.objects.all()

    if serviceName:
        serviceobj = serviceobj.filter(serviceName__iexact=serviceName)
    if serviceProtocol:
        serviceobj = serviceobj.filter(serviceProtocol__iexact=serviceProtocol)
    if serviceComment:
        serviceobj = serviceobj.filter(serviceComment__iexact=serviceComment)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = serviceobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for service in serviceobj:
        dict = {}
        # print("++++++++++++++++")
        # print((service.serviceName))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        dict['serviceName'] = service.serviceName
        dict['serviceProtocol'] = service.serviceProtocol
        dict['serviceComment'] = service.serviceComment

        list1.append(dict)

    # try:
    #     list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
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
def searchaddress(request):
    addressName = request.GET.get('addressName', None)
    addressIP = request.GET.get('addressIP', None)
    addressComment = request.GET.get('addressComment', None)

    # 方法一：
    addressobj = AddressName.objects.all()

    if addressName:
        addressobj = addressobj.filter(addressName__iexact=addressName)
    if addressIP:
        addressobj = addressobj.filter(addressIP__iexact=addressIP)
    if addressComment:
        addressobj = addressobj.filter(addressComment__iexact=addressComment)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = addressobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for address in addressobj:
        dict = {}
        # print("++++++++++++++++")
        # print((service.serviceName))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        dict['addressName'] = address.addressName
        dict['addressIP'] = address.addressIP
        dict['addressComment'] = address.addressComment

        list1.append(dict)

    # try:
    #     list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
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
def searchpolicy(request):
    ruleSa = request.GET.get('sourceIP', None)
    ruleDa = request.GET.get('directionIP', None)
    ruleService = request.GET.get('policyService', None)
    ruleComment = request.GET.get('policyComment', None)

    # 方法一：
    policyobj = PolicyManage.objects.all()

    if ruleSa:
        policyobj = policyobj.filter(ruleSa__iexact=ruleSa)
    if ruleDa:
        policyobj = policyobj.filter(ruleDa__iexact=ruleDa)
    if ruleService:
        policyobj = policyobj.filter(ruleService__iexact=ruleService)
    if ruleComment:
        policyobj = policyobj.filter(ruleComment__iexact=ruleComment)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = policyobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for policy in policyobj:
        dict = {}
        dict['ruleId'] = policy.ruleId
        dict['ruleName'] = policy.ruleName
        dict['ruleSa'] = policy.ruleSa
        dict['ruleDa'] = policy.ruleDa
        dict['ruleIzone'] = policy.ruleIzone
        dict['ruleOzone'] = policy.ruleOzone
        dict['ruleService'] = policy.ruleService
        dict['ruleOpentime'] = policy.ruleOpentime
        dict['ruleStatus'] = policy.ruleStatus
        dict['ruleActive'] = policy.ruleActive
        dict['ruleComment'] = policy.ruleComment
        dict['ruleAccount'] = policy.ruleAccount

        list1.append(dict)

    # try:
    #     list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
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
def deleteserviceall(request):
    try:
        ServiceName.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deleteaddressall(request):
    try:
        AddressName.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deletepolicyall(request):
    try:
        PolicyManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initservice(request):
    ServiceName.objects.all().delete()

    try:
        filepath = 'static/upload/FirewallManage/service.log'
        f = open(filepath, 'r', encoding='utf-8')
        fileContent = f.readlines()

        if "service add" not in str(fileContent):
            result = "log 文件内容不正确, 请使用启明防火墙导出的策略文件</br>内容形如: service refresh ftp service add name ..."
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        for line in fileContent:

            line = line.strip()
            # print(line)

            if line.startswith("#") | line.startswith("service refresh"):
                continue
            elif line.startswith("service add"):
                # print(line)
                name = line.split(" ")[3].replace('"', '')
                # print(name)

                protocol = ''
                for pro in re.findall("protocol (.*?) comment", line):
                    protocol = protocol + " " + pro

                comment = line.split(" ")[-1].replace('"', "")
                # for num in line.split(" ")[-1]:
                # for pro in re.findall('comment "(.*)"', line):
                #     comment = comment + " " + num
                # print(name, "-", protocol, "-", comment)

                service = ServiceName()
                service.serviceName = name
                service.serviceProtocol = protocol
                service.serviceComment = comment
                service.save()
        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    # print("------------------")

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initaddress(request):
    AddressName.objects.all().delete()

    try:
        filepath = 'static/upload/FirewallManage/address.log'
        f = open(filepath, 'r', encoding='utf-8')
        fileContent = f.readlines()

        if "addrgrp add" not in str(fileContent):
            result = "log 文件内容不正确, 请使用启明防火墙导出的策略文件</br>内容形如: addrgrp add name '网上国网电商调用支付宝' member ..."
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        for line in fileContent:

            line = line.strip()
            # print(line)
            if line.startswith("#"):
                continue
            elif line.startswith("addrgrp add"):
                addrgrp = ''
                for pro in re.findall('name "(.*?)" member', line):
                    addrgrp = addrgrp + " " + pro

                ipaddre = ""
                for add in re.findall('member "(.*?)" comment', line):
                    ipaddre = ipaddre + " " + add

                comment = line.split(" ")[-1].replace('"', "")

                # print(name, "-", ipaddr, "-", comment)

                address = AddressName()
                address.addressName = addrgrp
                address.addressIP = ipaddre
                address.addressComment = comment
                address.save()

                # continue
            elif line.startswith("address add"):
                name = ''
                for pro in re.findall('name "(.*?)" ip', line):
                    name = name + " " + pro

                ipaddr = ""
                for addr in re.findall('ip "(.*?)" comment', line):
                    ipaddr = ipaddr + " " + addr

                comment = line.split(" ")[-1].replace('"', "")

                # print(name, "-", ipaddr, "-", comment)

                address = AddressName()
                address.addressName = name
                address.addressIP = ipaddr
                address.addressComment = comment
                address.save()
        result = "success"
    except Exception as e:
        print(str(e))

        result = "failed"
    # print("------------------")

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initpolicy(request):
    PolicyManage.objects.all().delete()

    # try:
    filepath = 'static/upload/FirewallManage/pf.log'
    f = open(filepath, 'r', encoding='utf-8')
    fileContent = f.readlines()

    if "rule add" not in str(fileContent):
        result = "log 文件内容不正确, 请使用启明防火墙导出的策略文件</br>内容形如: rule add type deny id 1 name ..."
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    for line in fileContent:

        line = line.strip()
        # print(line)
        if line.startswith("rule add"):
            ruleId = ''
            for id in re.findall('id (.*?) name', line):
                ruleId = ruleId + " " + id

            ruleName = ""
            for name in re.findall('name "(.*?)" sa', line):
                ruleName = ruleName + name

            ruleSa = ""
            for sa in re.findall('sa (.*?) da', line):
                ruleSa = ruleSa + " " + sa

            ruleDa = ""
            for da in re.findall('da "(.*?)" izone', line):
                ruleDa = ruleDa + " " + da

            ruleIzone = ""
            for izone in re.findall('izone (.*?) ozone', line):
                ruleIzone = ruleIzone + " " + izone

            ruleOzone = ""
            for ozone in re.findall('ozone (.*?) service', line):
                ruleOzone = ruleOzone + " " + ozone

            ruleService = ""
            for service in re.findall('service (.*?) time', line):
                ruleService = ruleService + " " + service

            ruleOpentime = ""
            for opentime in re.findall('time (.*?) log', line):
                ruleOpentime = ruleOpentime + " " + opentime

            ruleStatus = ""
            for service in re.findall('service (.*?) time', line):
                ruleStatus = ruleStatus + " " + service

            ruleActive = ""
            for active in re.findall('type (.*?) id', line):
                ruleActive = ruleActive + " " + active

            comment = line.split(" ")[-1].replace('"', "")

            # print(ruleId, "-", ruleName, "-", ruleSa, "-", ruleDa, "-", ruleIzone, "-", ruleOzone, "-", ruleService, "-", ruleOpentime, "-", ruleStatus, "-", ruleActive, "-", comment)

            policy = PolicyManage()
            policy.ruleId = ruleId
            policy.ruleName = ruleName.strip(" ")
            # print("ruleName:")
            # print("------------------++++++++++++++++++++++")
            # print(ruleName)
            policy.ruleSa = ruleSa.replace('"', '')
            policy.ruleDa = ruleDa
            policy.ruleIzone = ruleIzone
            policy.ruleOzone = ruleOzone
            policy.ruleService = ruleService.replace('"', '')
            policy.ruleOpentime = ruleOpentime
            policy.ruleStatus = ruleStatus
            policy.ruleActive = ruleActive
            policy.ruleComment = comment
            # policy.ruleAccount = ruleAccount
            policy.save()

    # 设置路径
    path = 'static/upload/FirewallManage/firewall.xls'

    # 打开execl
    workbook = xlrd.open_workbook(path)

    # 输出Excel文件中所有sheet的名字
    # print(workbook.sheet_names())

    # 根据sheet索引或者名称获取sheet内容
    firewallSheet = workbook.sheets()[0]  # 通过索引获取
    # firewallSheet = workbook.sheet_by_index(0)  # 通过索引获取
    # firewallSheet = workbook.sheet_by_name('ECS')  # 通过名称获取

    # print(ecsSheet.name)  # 获取sheet名称
    rowNum = firewallSheet.nrows  # sheet行数
    colNum = firewallSheet.ncols  # sheet列数

    firstLineValue = ['序号 ', '规则名 ', '源地址 ', '目的地址 ', '流入安全域 ', '流出安全域 ', '服务 ', '动作 ', '生效 ', '命中数 ', '所属策略组 ', '操作 ']
    # print(firstLineValue)
    # print(firewallSheet.row_values(0))

    if firewallSheet.row_values(0) != firstLineValue:
        result = "xls 文件列名不正确,请参考模板文件</br>列名例如: '规则名 '"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    # # 获取所有单元格的内容
    # list = []
    # for i in range(rowNum):
    #     rowlist = []
    #     for j in range(colNum):
    #         rowlist.append(Data_sheet.cell_value(i, j))
    #
    #         print(type(date_value), date_value)
    #     list.append(rowlist)

    # 输出所有单元格的内容
    for row in range(rowNum):
        if row == 0:
            continue

        ruleId = firewallSheet.cell_value(row, 0)
        ruleName = firewallSheet.cell_value(row, 1)
        ruleSa = firewallSheet.cell_value(row, 2)
        ruleDa = firewallSheet.cell_value(row, 3)
        ruleIzone = firewallSheet.cell_value(row, 4)
        ruleOzone = firewallSheet.cell_value(row, 5)
        ruleService = firewallSheet.cell_value(row, 6)
        ruleActive = firewallSheet.cell_value(row, 7)
        ruleStatus = firewallSheet.cell_value(row, 8)
        ruleAccount = firewallSheet.cell_value(row, 9)
        ruleComment = firewallSheet.cell_value(row, 10)

        if "..." in str(ruleAccount):
            ruleAccount = str(ruleAccount).strip("...")
            ruleAccount = ruleAccount + "00000000"
        ruleAccount = int(ruleAccount)

        PolicyManage.objects.filter(ruleName=ruleName).update(ruleAccount=ruleAccount)

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
def uploadService(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filename = textFile.name
        filepath = "static/upload/firewallManage/service.log"
        # filepath = os.path.join(settings.UPLOAD_DIR, filename)
        # print(filepath)

        dirpath = os.path.join(settings.UPLOAD_DIR, "firewallManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "firewallManage/bak/service" + time.strftime('%Y_%b_%d-%H_%M_%S'))
            # print(filepath)
            # print(new_filepath)
            shutil.move(filepath, new_filepath)
            # os.rename(filepath, new_filepath)
            # print("ok")

        with open(filepath, 'wb') as f:
            for text in textFile.chunks():  # 分包写入
                f.write(text)

    serviceobj = ServiceName.objects.all()

    total = serviceobj.count()
    resultdict = {}
    list1 = []
    for service in serviceobj:
        dict = {}
        dict['serviceName'] = service.serviceName
        dict['serviceProtocol'] = service.serviceProtocol
        dict['serviceComment'] = service.serviceComment

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
def uploadaddress(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        filepath = os.path.join(settings.UPLOAD_DIR, "firewallManage/address.log")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "firewallManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "firewallManage/bak/" + "address" + time.strftime('%Y_%b_%d-%H_%M_%S') + ".log")
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
def uploadpolicy(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        filepath = os.path.join(settings.UPLOAD_DIR, "firewallManage/pf.log")

        dirpath = os.path.join(settings.UPLOAD_DIR, "firewallManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        # print(filepath)
        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "firewallManage/bak/" + "pf" + time.strftime('%Y_%b_%d-%H_%M_%S') + ".log")
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
        filepath = os.path.join(settings.UPLOAD_DIR, "firewallManage/firewall.xls")

        dirpath = os.path.join(settings.UPLOAD_DIR, "firewallManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        # print(filepath)
        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "firewallManage/bak/firewall" + time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")
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
def getservicelist(request):
    serviceobj = ServiceName.objects.all()

    total = serviceobj.count()
    resultdict = {}
    list1 = []
    for service in serviceobj:
        dict = {}
        dict['serviceName'] = service.serviceName
        dict['serviceProtocol'] = service.serviceProtocol
        dict['serviceComment'] = service.serviceComment

        list1.append(dict)

    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

    # try:
    #     list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
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
def getaddresslist(request):
    addressobj = AddressName.objects.all()

    total = addressobj.count()
    resultdict = {}
    list1 = []
    for address in addressobj:
        dict = {}
        dict['addressName'] = address.addressName
        dict['addressIP'] = address.addressIP
        dict['addressComment'] = address.addressComment

        list1.append(dict)

    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

    # try:
    #     list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
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
def getpolicylist(request):
    policyobj = PolicyManage.objects.all()

    total = policyobj.count()
    resultdict = {}
    list1 = []
    for policy in policyobj:
        dict = {}
        dict['ruleId'] = policy.ruleId
        dict['ruleName'] = policy.ruleName
        dict['ruleSa'] = policy.ruleSa
        dict['ruleDa'] = policy.ruleDa
        dict['ruleIzone'] = policy.ruleIzone
        dict['ruleOzone'] = policy.ruleOzone
        dict['ruleService'] = policy.ruleService
        dict['ruleOpentime'] = policy.ruleOpentime
        dict['ruleStatus'] = policy.ruleStatus
        dict['ruleActive'] = policy.ruleActive
        dict['ruleComment'] = policy.ruleComment
        dict['ruleAccount'] = policy.ruleAccount

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

        addressobj = AddressName.objects.filter(addressName__iexact=ruleSa.replace(" ", ""))
        ipaddr = ''
        for address in addressobj:
            ipaddr = ruleSa + ": " + address.addressIP + ipaddr + " "

    elif ";" in ruleSa:
        sourceip = ruleSa.split(";")
        ipaddr = ''
        for source in sourceip:
            addressobj = AddressName.objects.filter(addressName__iexact=source.replace(" ", ""))
            ipaddress = ''
            for address in addressobj:
                ipaddress = source + ": " + address.addressIP + ipaddress + " \r\n" + "</br>"
            ipaddr = ipaddress + ipaddr

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
            addressobj = AddressName.objects.filter(addressName__iexact=direction.replace(" ", ""))
            ipaddress = ''
            for address in addressobj:
                ipaddress = direction + ": " + address.addressIP + ipaddress + " \r\n" + "</br>"
            ipaddr = ipaddress + ipaddr

    else:

        # elif ruleDa.startswith(" aly") | ruleDa.startswith(" ad"):

        addressobj = AddressName.objects.filter(addressName__iexact=ruleDa.replace(" ", ""))
        ipaddr = ''
        for address in addressobj:
            ipaddr = ruleDa + ": " + address.addressIP + ipaddr + " \r\n" + "</br>"

    ipaddr = ipaddr.replace(":", ":</br>")
    ipaddr = ipaddr.replace(";", ",</br>")
    # else:
    #     ipaddr = "该数据不是单一IP组，无法查询！"
    return JsonResponse(ipaddr, safe=False)


@login_required
@csrf_exempt
def getruleservice(request):
    ruleService = request.POST.get('ruleService', None).strip(" ")
    # print(";" in ruleService)
    # print(ruleService)
    # print(ruleService)

    if "any" == ruleService:
        service = "该数据存在多个服务组，查询失败！"
        return JsonResponse(service, safe=False)

    elif ";" in ruleService:
        ruleservice = ruleService.split(";")
        service = ''
        for rule in ruleservice:
            # print("rule:", rule)
            # serviceobj = ServiceName.objects.filter(serviceName__iexact="rule")
            serviceobj = ServiceName.objects.filter(serviceName__iexact=rule.replace(" ", ""))
            serv = ''
            for ser in serviceobj:
                serv = rule + ": </br>" + ser.serviceProtocol + serv + " \r\n" + "</br>"
                # print("---++++++++++++", serv)
            service = serv + service
        # print("-------", service)

        # service = service.split(";")

    else:
        serviceobj = ServiceName.objects.filter(serviceName__iexact=ruleService.replace(" ", ""))
        service = ''
        for srv in serviceobj:
            service = srv.serviceProtocol + service + " \r\n" + "</br>"

    # service = service.replace(":", ":</br>")
    # service = service.replace(";", ",</br>")
    if service == "":
        service = "未查询到数据"

    return JsonResponse(service, safe=False)


@login_required
@csrf_exempt
def downloadFirewallTemplateFile(request):
    file = open('static/upload/FirewallManage/firewallTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="FirewallTemplate_%s.xls"' % int(time.time())
    return response

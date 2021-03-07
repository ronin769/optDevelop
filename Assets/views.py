# codding = utf8

import datetime
import shutil
import xml
import time

import xlwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Max, F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.core.paginator import Paginator

import xlrd
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

@login_required
def index(request):
    return render(request, 'Assets/vuln.html')


@login_required
def ecsManage(request):
    return render(request, 'Assets/ecs.html')


@login_required
def vulnManage(request):
    return render(request, 'Assets/vuln.html')


@login_required
def domainManage(request):
    return render(request, 'Assets/domain.html')

@login_required
def addDomainpage(request):
    return render(request, 'Assets/adddomain.html')


@login_required
def produceFirewallManage(request):
    return render(request, 'Assets/produceFirewall.html')


@login_required
def workFirewallManage(request):
    return render(request, 'Assets/workFirewall.html')





@csrf_exempt
@login_required
def getEcsList(request):
    ecsobj = V2ECSManage.objects.all()

    total = ecsobj.count()
    list1 = []
    for ecs in ecsobj:
        dict = {}
        dict['createTime'] = ecs.createTime
        dict['description'] = ecs.description
        dict['eipAddress'] = ecs.eipAddress
        dict['instanceId'] = ecs.instanceId
        dict['instanceName'] = ecs.instanceName
        dict['loadBalancerId'] = ecs.loadBalancerId
        dict['loadBalancerName'] = ecs.loadBalancerName
        dict['natIpAddress'] = ecs.natIpAddress
        dict['networkType'] = ecs.networkType
        dict['physicalHostName'] = ecs.physicalHostName
        dict['privateIpAddress'] = ecs.privateIpAddress
        dict['projectId'] = ecs.projectId
        dict['projectName'] = ecs.projectName
        dict['regionId'] = ecs.regionId
        dict['securityGroupIdList'] = ecs.securityGroupIdList

        dict['domain'] = ecs.domain
        dict['systemName'] = ecs.systemName
        dict['businessPeople'] = ecs.businessPeople
        dict['DevelopPeople'] = ecs.DevelopPeople
        dict['accessURL'] = ecs.accessURL

        dict['slbIp'] = ecs.slbIp
        dict['slbStatus'] = ecs.slbStatus
        dict['slbport'] = ecs.slbport
        dict['startTime'] = ecs.startTime
        dict['vpcId'] = ecs.vpcId

        list1.append(dict)



    try:
        list1.sort(key=lambda k: (k.get('privateIpAddress')), reverse=False)
        # list1.sort(key=lambda k: (k.get('createTime')), reverse=True)
        # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    except TypeError as e:
        print(str(e))

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
def getVulnlist(request):
    vulnobj = ShaoBingYunManage.objects.all()

    total = vulnobj.count()
    list1 = []
    for vuln in vulnobj:
        dict = {}
        dict['vulName'] = vuln.vulName
        dict['vulLevel'] = vuln.vulLevel
        dict['vulURL'] = vuln.vulURL
        dict['vulStatus'] = vuln.vulStatus
        dict['vulAddress'] = vuln.vulAddress
        dict['vulIP'] = vuln.vulIP
        dict['vulDomain'] = vuln.vulDomain
        dict['vulService'] = vuln.vulService
        dict['vulCoutry'] = vuln.vulCoutry
        dict['vulIsRepair'] = vuln.vulIsRepair
        dict['vulIsHandle'] = vuln.vulIsHandle
        dict['vulGroup'] = vuln.vulGroup
        dict['vulMark'] = vuln.vulMark
        dict['vulScore'] = vuln.vulScore
        dict['vulID'] = vuln.vulID
        dict['vulDescribe'] = vuln.vulDescribe
        dict['vulType'] = vuln.vulType
        dict['vulDamage'] = vuln.vulDamage
        dict['vulDetails'] = vuln.vulDetails
        dict['vulSuggest'] = vuln.vulSuggest
        dict['vulRequest'] = vuln.vulRequest
        dict['vulResponse'] = vuln.vulResponse
        dict['vulFirstFindTime'] = vuln.vulFirstFindTime
        dict['vulUpdateTime'] = vuln.vulUpdateTime

        list1.append(dict)

    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

    try:
        list1.sort(key=lambda k: (k.get('vulIP')), reverse=False)
        # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    except TypeError as e:
        pass

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
def getProduceFirewallPolicyList(request):
    policyobj = ProduceFirewallManage.objects.all()

    total = policyobj.count()
    list1 = []
    for policy in policyobj:
        dict = {}
        dict['id'] = policy.id
        dict['protocol'] = policy.protocol
        dict['name'] = policy.name
        dict['pl_grp_profile'] = policy.pl_grp_profile
        dict['mode'] = policy.mode
        dict['enable'] = policy.enable
        dict['bingo'] = policy.bingo
        dict['cur_conn_num'] = policy.cur_conn_num
        dict['syslog'] = policy.syslog
        dict['log_sess_start'] = policy.log_sess_start
        dict['log_sess_end'] = policy.log_sess_end
        dict['refer_id'] = policy.refer_id
        dict['mv_opt'] = policy.mv_opt
        dict['szone_list'] = policy.szone_list
        dict['dzone_list'] = policy.dzone_list
        dict['saddr_list'] = policy.saddr_list
        dict['saddr_content'] = policy.saddr_content
        dict['saddr_desc'] = policy.saddr_desc
        dict['daddr_list'] = policy.daddr_list
        dict['daddr_content'] = policy.daddr_content
        dict['daddr_desc'] = policy.daddr_desc
        dict['sev_list'] = policy.sev_list
        dict['sev_content'] = policy.sev_content
        dict['sev_desc'] = policy.sev_desc
        dict['tr_list'] = policy.tr_list
        dict['user_list'] = policy.user_list
        dict['app_list'] = policy.app_list
        dict['flowstat'] = policy.flowstat
        dict['is_end'] = policy.is_end
        dict['page'] = policy.page
        dict['recordsTotal'] = policy.recordsTotal
        dict['recordsFiltered'] = policy.recordsFiltered
        dict['eurl'] = policy.eurl
        dict['durl'] = policy.durl
        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('id')), reverse=False)
    except TypeError as e:
        print(str(e))

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
def getWorkFirewallPolicyList(request):
    policyobj = WorkFirewallManage.objects.all()

    total = policyobj.count()
    list1 = []
    for policy in policyobj:
        dict = {}
        dict['src_ip'] = policy.src_ip
        dict['src_ip_content'] = policy.src_ip_content
        dict['dst_ip'] = policy.dst_ip
        dict['dst_ip_content'] = policy.dst_ip_content
        dict['description'] = policy.description
        dict['status'] = policy.status
        dict['group'] = policy.group
        dict['name'] = policy.name
        dict['log'] = policy.log
        dict['priority'] = policy.priority
        dict['conflict_num'] = policy.conflict_num
        dict['num'] = policy.num
        dict['active_time'] = policy.active_time
        dict['dst_zone'] = policy.dst_zone
        dict['invalid_id'] = policy.invalid_id
        dict['src_zone'] = policy.src_zone
        dict['last_hittime'] = policy.last_hittime
        dict['not_hit_day'] = policy.not_hit_day
        dict['create_time'] = policy.create_time
        dict['highlight'] = policy.highlight
        dict['invalid_name'] = policy.invalid_name
        dict['action'] = policy.action
        dict['src_port'] = policy.src_port
        dict['service_app'] = policy.service_app
        dict['is_sc_create'] = policy.is_sc_create
        dict['down_interface'] = policy.down_interface
        dict['hit'] = policy.hit
        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('name')), reverse=False)
    except TypeError as e:
        print(str(e))

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
def getDomainlist(request):
    domainobj = DomainManage.objects.all()

    # total = DomainManage.objects.filter(systemStatus__contains="使用中").count()
    total = 0
    resultdict = {}
    list1 = []
    for domain in domainobj:
        # print(domain.systemStatus)
        # if domain.systemStatus == "已下线":
        #     continue
        # if (".baidu.com" not in domain.domainName) and (".evs.sgcc.com.cn" not in domain.domainName) and (":" not in domain.domainName):
        #     # print(domain.domainName)
        #     continue

        # print("--")
        if ".baidu.com" in domain.domainName and "使用中" in domain.systemStatus:
            total = total + 1
        dict = {}
        dict['departmentName'] = domain.departmentName
        dict['systemName'] = domain.systemName
        dict['domainName'] = domain.domainName
        dict['SLBIP'] = domain.SLBIP
        dict['ECSIP'] = domain.ECSIP
        dict['SLBPort'] = domain.SLBPort
        dict['systemType'] = domain.systemType
        dict['systemStatus'] = domain.systemStatus
        dict['accessURL'] = domain.accessURL
        dict['developmentCompany'] = domain.developmentCompany
        dict['extranetAccess'] = domain.extranetAccess
        dict['businessPeople'] = domain.businessPeople
        dict['businessPhone'] = domain.businessPhone
        dict['projectPeopleName'] = domain.projectPeopleName
        dict['projectPeoplePhone'] = domain.projectPeoplePhone
        dict['DevelopPeople'] = domain.DevelopPeople
        dict['DevelopPhone'] = domain.DevelopPhone
        dict['systemMiddleware'] = domain.systemMiddleware
        dict['systemDescribe'] = domain.systemDescribe
        dict['systemCommon'] = domain.systemCommon
        dict['CreateTime'] = domain.CreateTime
        dict['updateTime'] = domain.updateTime
        dict['CreatePeople'] = domain.CreatePeople
        dict['updatePeople'] = domain.updatePeople
        dict['systemUsername'] = domain.systemUsername
        dict['systemPassword'] = domain.systemPassword


        # if not domain.SLBIP:
        #     continue

        # 从ECS库里,通过SLB查询ECS和EIP
        # print(domain.SLBIP)
        if domain.SLBIP:
            ecsobj = V2ECSManage.objects.filter(slbIp__iexact=domain.SLBIP)
            if ecsobj:
                privateIpAddressStr = ""
                eipAddressStr = ""

                for ecs in ecsobj:
                    if ecs.privateIpAddress:
                        privateIpAddressStr = privateIpAddressStr + ecs.privateIpAddress + "; "
                for ecs in ecsobj:
                    if ecs.eipAddress:
                        eipAddressStr = eipAddressStr + ecs.eipAddress + "; "

                dict['ECSIP'] = str(privateIpAddressStr)
                dict['EIP'] = str(eipAddressStr)
            else:
                dict['ECSIP'] = ""
                dict['EIP'] = ""


        list1.append(dict)
    # print(list1)
    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

    try:
        list1.sort(key=lambda k: (k.get('CreateTime')), reverse=True)
        # list1.sort(key=lambda k: (k.get('domainName')), reverse=False)
    except TypeError as e:
        pass

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
def domainPocicyInit(request):
    print("11111111111111111")
    domainobj = DomainManage.objects.all()
    for domain in domainobj:
        if ".baidu.com" not in domain.domainName:
            continue

        try:
            line = "https://" + domain.domainName
            print(line)
            res = requests.get(url=line, verify=False, timeout=10, allow_redirects=True)
            print(res.status_code)
            DomainManage.objects.filter(domainName__iexact=domain.domainName).update(systemStatus="使用中", extranetAccess="开放访问")

        except requests.exceptions.ConnectionError as e:
            print(str(e))
            print(domain.domainName, "域名不存在")
            DomainManage.objects.filter(domainName__iexact=domain.domainName).update(systemStatus="已下线", extranetAccess="本地访问")

        except requests.exceptions.ReadTimeout as e:
            print(str(e))
            print(domain.domainName, "超时")
            DomainManage.objects.filter(domainName__iexact=domain.domainName).update(systemStatus="使用中", extranetAccess="本地访问")


    resultdict = {"code": 0, "msg": "成功", "count": "total", "data": "res"}
    return JsonResponse(resultdict, safe=False)

@login_required
@csrf_exempt
def uploadecsfile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/ecsAssets.xls")
        # print(filepath)

        dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "AssetsManage/bak/ecsAssets_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")
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
def uploadVulnfile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/shaoBingYunThreat.xls")
        # print(filepath)

        dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/shaoBingYunThreat%s" % time.strftime(
                '%Y_%b_%d-%H_%M_%S') + ".xls")
            # print(filepath)
            # print(new_filepath)
            shutil.move(filepath, new_filepath)
            # os.rename(filepath, new_filepath)
            # print("ok")

        with open(filepath, 'wb') as f:
            for text in textFile.chunks():  # 分包写入
                f.write(text)

    resultdict = {"code": 0}
    # resultdict = ''

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def uploadDomainfile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/domainAsset.xls")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "AssetsManage/bak/domainAsset%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")

            # print(filepath)
            # print(new_filepath)
            shutil.move(filepath, new_filepath)
            # os.rename(filepath, new_filepath)
            # print("ok")

        with open(filepath, 'wb') as f:
            for text in textFile.chunks():  # 分包写入
                f.write(text)

    resultdict = {"code": 0}
    # resultdict = ''
    print(resultdict)
    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def uploadproducefirewallpolicyfile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/produceFirewallPolicyAll.xls")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "AssetsManage/bak/produceFirewallPolicyAll%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")

            # print(filepath)
            # print(new_filepath)
            shutil.move(filepath, new_filepath)
            # os.rename(filepath, new_filepath)
            # print("ok")

        with open(filepath, 'wb') as f:
            for text in textFile.chunks():  # 分包写入
                f.write(text)

    resultdict = {"code": 0}
    # resultdict = ''

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def uploadworkfirewallpolicyfile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/workFirewallPolicyAll.xls")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "AssetsManage/bak/workFirewallPolicyAll%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")

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
def initECSfile(request):
    try:

        ECSManage.objects.all().delete()

        # 设置路径
        path = 'static/upload/AssetsManage/ecsAssets.xls'

        # 打开execl
        workbook = xlrd.open_workbook(path)

        # 输出Excel文件中所有sheet的名字
        # print(workbook.sheet_names())

        # 根据sheet索引或者名称获取sheet内容
        # ecsSheet = workbook.sheets()[0]  # 通过索引获取
        # ecsSheet = workbook.sheet_by_index(0)  # 通过索引获取
        ecsSheet = workbook.sheet_by_name('ECS')  # 通过名称获取

        # print(ecsSheet.name)  # 获取sheet名称
        rowNum = ecsSheet.nrows  # sheet行数
        colNum = ecsSheet.ncols  # sheet列数

        firstLineValue = ['实例ID', '实例名称', '部门', '项目', '区域', '状态', '网络类型', 'IP地址', '弹性外网IP', 'CPU(核)', '内存(GB)',
                          '系统盘（GB）', '数据盘（GB）', '操作系统', '描述', '备注']
        # print(ecsSheet.row_values(0))
        # print(firstLineValue)
        if ecsSheet.row_values(0) != firstLineValue:
            result = "文件列名不正确,请参考模板文件"
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
            # for j in range(colNum):
            #     # # 获取单元格内容为日期的数据
            #     # date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(i, j), workbook.datemode)
            #     # print(date_value)
            #     print(ecsSheet.cell_value(row, j))
            #     # print(list[i][j], '\t\t', end="")

            ecsID = ecsSheet.cell_value(row, 0)
            ecsName = ecsSheet.cell_value(row, 1)
            ecsPartment = ecsSheet.cell_value(row, 2)
            ecsProject = ecsSheet.cell_value(row, 3)
            ecsZone = ecsSheet.cell_value(row, 4)
            ecsStatus = ecsSheet.cell_value(row, 5)
            ecsNetwork = ecsSheet.cell_value(row, 6)

            ecsIPEX = ecsSheet.cell_value(row, 7)
            ecsIPS = re.compile(r'((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)')
            ecsIP = ecsIPS.search(ecsIPEX).group()
            ecsSLBIP = ecsSheet.cell_value(row, 8)
            ecsCPU = str(ecsSheet.cell_value(row, 9))
            ecsMemory = str(ecsSheet.cell_value(row, 10))
            ecsSystemStore = str(ecsSheet.cell_value(row, 11))
            ecsDataStore = str(ecsSheet.cell_value(row, 12))
            ecsSystemOS = ecsSheet.cell_value(row, 13)
            ecsDescribe = ecsSheet.cell_value(row, 14)
            ecsComment = ecsSheet.cell_value(row, 15)

            ecsobj = ECSManage()
            ecsobj.ecsID = ecsID
            ecsobj.ecsName = ecsName
            ecsobj.ecsPartment = ecsPartment
            ecsobj.ecsProject = ecsProject
            ecsobj.ecsZone = ecsZone
            ecsobj.ecsStatus = ecsStatus
            ecsobj.ecsNetwork = ecsNetwork
            ecsobj.ecsIP = ecsIP
            ecsobj.ecsSLBIP = ecsSLBIP
            ecsobj.ecsCPU = ecsCPU
            ecsobj.ecsMemory = ecsMemory
            ecsobj.ecsSystemStore = ecsSystemStore
            ecsobj.ecsDataStore = ecsDataStore
            ecsobj.ecsSystemOS = ecsSystemOS
            ecsobj.ecsDescribe = ecsDescribe
            ecsobj.ecsComment = str(ecsComment)
            ecsobj.save()

        print("---------ok---------")
        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initVulnfile(request):
    try:

        ShaoBingYunManage.objects.all().delete()

        # 设置路径
        path = 'static/upload/AssetsManage/shaoBingYunThreat.xls'

        # 打开execl
        workbook = xlrd.open_workbook(path)

        # 输出Excel文件中所有sheet的名字
        # print(workbook.sheet_names())

        # 根据sheet索引或者名称获取sheet内容
        vulnSheet = workbook.sheets()[0]  # 通过索引获取
        # vulnSheet = workbook.sheet_by_index(0)  # 通过索引获取
        # vulnSheet = workbook.sheet_by_name('ECS')  # 通过名称获取

        # print(vulnSheet.name)  # 获取sheet名称
        rowNum = vulnSheet.nrows  # sheet行数
        colNum = vulnSheet.ncols  # sheet列数

        # firstLineValue = ['风险名称', '风险等级', '风险地址', '检测状态', '资产地址', 'ip地址', '关联域名', '服务信息', '地理位置', '风险状态', '处理状态',
        #                   '资产分组', '标签', '漏洞评分', '评分编号', '风险描述', '风险类型', '风险危害', '风险细节', '修复建议', '请求', '响应', '首次发现时间',
        #                   '最后更新时间']
        firstLineValue = ['风险名称', '风险等级', '风险地址', '检测状态', '资产地址', 'ip地址', '关联域名', '服务信息', '地理位置', '风险状态', '处理状态', '资产分组',
                          '标签', '漏洞评分', '评分编号', '风险描述', '风险类型', '风险危害', '风险细节', '修复建议', '请求', '响应', '首次发现时间', '最后更新时间', '负责人', '手机', '邮箱', '用户名称']


        # print(vulnSheet.row_values(0))
        # print(firstLineValue)
        if vulnSheet.row_values(0) != firstLineValue:
            result = "文件列名不正确,请参考模板文件"
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

            vulName = vulnSheet.cell_value(row, 0)
            vulLevel = vulnSheet.cell_value(row, 1)
            vulURL = vulnSheet.cell_value(row, 2)
            vulStatus = vulnSheet.cell_value(row, 3)
            vulAddress = vulnSheet.cell_value(row, 4)
            vulIP = vulnSheet.cell_value(row, 5)
            vulDomain = vulnSheet.cell_value(row, 6)
            vulService = vulnSheet.cell_value(row, 7)
            vulCoutry = vulnSheet.cell_value(row, 8)
            vulIsRepair = vulnSheet.cell_value(row, 9)
            vulIsHandle = vulnSheet.cell_value(row, 10)
            vulGroup = vulnSheet.cell_value(row, 11)
            vulMark = vulnSheet.cell_value(row, 12)
            vulScore = vulnSheet.cell_value(row, 13)
            vulID = vulnSheet.cell_value(row, 14)
            vulDescribe = vulnSheet.cell_value(row, 15)
            vulType = vulnSheet.cell_value(row, 16)
            vulDamage = vulnSheet.cell_value(row, 17)
            vulDetails = vulnSheet.cell_value(row, 18)
            vulSuggest = vulnSheet.cell_value(row, 19)
            vulRequest = vulnSheet.cell_value(row, 20)
            vulResponse = vulnSheet.cell_value(row, 21)
            vulFirstFindTime = vulnSheet.cell_value(row, 22)
            vulUpdateTime = vulnSheet.cell_value(row, 23)
            # for j in range(colNum):
            #     # # 获取单元格内容为日期的数据
            #     # date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(i, j), workbook.datemode)
            #     # print(date_value)
            #     print(ecsSheet.cell_value(row, j))
            #     # print(list[i][j], '\t\t', end="")
            #

            # ecsIPS = re.compile(r'((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)')

            vulnobj = ShaoBingYunManage()
            vulnobj.vulName = vulName
            vulnobj.vulLevel = vulLevel
            vulnobj.vulURL = vulURL
            vulnobj.vulStatus = vulStatus
            vulnobj.vulAddress = vulAddress
            vulnobj.vulIP = vulIP
            vulnobj.vulDomain = vulDomain
            vulnobj.vulService = vulService
            vulnobj.vulCoutry = vulCoutry
            vulnobj.vulIsRepair = vulIsRepair
            vulnobj.vulIsHandle = vulIsHandle
            vulnobj.vulGroup = vulGroup
            vulnobj.vulMark = vulMark
            vulnobj.vulScore = vulScore
            vulnobj.vulID = vulID
            vulnobj.vulDescribe = vulDescribe
            vulnobj.vulType = vulType
            vulnobj.vulDamage = vulDamage
            vulnobj.vulDetails = vulDetails
            vulnobj.vulSuggest = vulSuggest
            vulnobj.vulRequest = vulRequest
            vulnobj.vulResponse = vulResponse
            vulnobj.vulFirstFindTime = vulFirstFindTime
            vulnobj.vulUpdateTime = vulUpdateTime
            vulnobj.save()

        print("---------ok---------")
        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initDomainfile(request):
    try:

        DomainManage.objects.all().delete()

        path = 'static/upload/AssetsManage/domainAsset.xls'
        workbook = xlrd.open_workbook(path)  # 打开execl

        # 输出Excel文件中所有sheet的名字
        # print(workbook.sheet_names())
        # 根据sheet索引或者名称获取sheet内容
        domainSheet = workbook.sheets()[0]  # 通过索引获取
        # vulnSheet = workbook.sheet_by_index(0)  # 通过索引获取
        # vulnSheet = workbook.sheet_by_name('ECS')  # 通过名称获取
        # print(vulnSheet.name)  # 获取sheet名称
        rowNum = domainSheet.nrows  # sheet行数
        # colNum = domainSheet.ncols  # sheet列数

        firstLineValue = ['系统名称', '部门名称', '域名', 'SLB地址', '访问URL', 'SLB端口', 'ECS地址', '系统类型', '外网访问', '业务联系人', '业务联系方式', '项目经理', '经理联系方式', '研发人员', '研发人员', '系统状态', '开发单位', '中间件', '系统描述', '备注', '创建时间', '修改时间', '创建人', '修改人', '账号', '密码']

        print(firstLineValue)
        print(domainSheet.row_values(0))

        if domainSheet.row_values(0) != firstLineValue:
            result = "文件列名不正确,请参考模板文件"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        # # 获取所有单元格的内容
        # list = []
        # for i in range(rowNum):
        #     rowlist = []
        #     for j in range(colNum):
        #         rowlist.append(Data_sheet.cell_value(i, j))
        #         print(type(date_value), date_value)
        #     list.append(rowlist)

        # 输出所有单元格的内容
        for row in range(rowNum):
            if row == 0:
                continue
            systemName = domainSheet.cell_value(row, 0).replace('"', '^')
            departmentName = domainSheet.cell_value(row, 1)
            domainName = domainSheet.cell_value(row, 2)
            SLBIP = domainSheet.cell_value(row, 3)
            accessURL = domainSheet.cell_value(row, 4).replace('"', '^')
            SLBPort = str(domainSheet.cell_value(row, 5)).replace(".0", "")
            ECSIP = domainSheet.cell_value(row, 6)
            systemType = domainSheet.cell_value(row, 7)
            extranetAccess = domainSheet.cell_value(row, 8)
            businessPeople = str((domainSheet.cell_value(row, 9))).replace(".0", "")
            businessPhone = str((domainSheet.cell_value(row, 10))).replace(".0", "")
            projectPeopleName = str((domainSheet.cell_value(row, 11))).replace(".0", "")
            projectPeoplePhone = str((domainSheet.cell_value(row, 12))).replace(".0", "")
            DevelopPeople = str((domainSheet.cell_value(row, 13))).replace(".0", "")
            DevelopPhone = str((domainSheet.cell_value(row, 14))).replace(".0", "")
            systemStatus = domainSheet.cell_value(row, 15)
            developmentCompany = domainSheet.cell_value(row, 16)
            systemMiddleware = domainSheet.cell_value(row, 17)
            systemDescribe = domainSheet.cell_value(row, 18).replace('"', '^')
            systemCommon = domainSheet.cell_value(row, 19).replace('"', '^')
            CreateTime = domainSheet.cell_value(row, 20)
            updateTime = domainSheet.cell_value(row, 21)
            CreatePeople = domainSheet.cell_value(row, 22)
            updatePeople = domainSheet.cell_value(row, 23)
            systemUsername = domainSheet.cell_value(row, 24)
            systemPassword = domainSheet.cell_value(row, 25)

            # for j in range(colNum):
            #     # # 获取单元格内容为日期的数据
            #     # date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(i, j), workbook.datemode)
            #     # print(date_value)
            #     print(ecsSheet.cell_value(row, j))
            #     # print(list[i][j], '\t\t', end="")
            #
            # ecsIPS = re.compile(r'((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)')

            domainobj = DomainManage()
            domainobj.systemName = systemName
            domainobj.departmentName = departmentName
            domainobj.domainName = domainName
            domainobj.SLBIP = SLBIP
            domainobj.accessURL = accessURL
            domainobj.SLBPort = SLBPort
            domainobj.ECSIP = ECSIP
            domainobj.systemType = systemType
            domainobj.extranetAccess = extranetAccess
            domainobj.businessPeople = businessPeople
            domainobj.businessPhone = businessPhone
            domainobj.projectPeopleName = projectPeopleName
            domainobj.projectPeoplePhone = projectPeoplePhone
            domainobj.DevelopPeople = DevelopPeople
            domainobj.DevelopPhone = DevelopPhone
            domainobj.systemStatus = systemStatus
            domainobj.developmentCompany = developmentCompany
            domainobj.systemMiddleware = systemMiddleware
            domainobj.systemDescribe = systemDescribe
            domainobj.systemCommon = systemCommon
            domainobj.CreateTime = CreateTime
            domainobj.updateTime = updateTime
            domainobj.CreatePeople = CreatePeople
            domainobj.updatePeople = updatePeople
            domainobj.systemUsername = systemUsername
            domainobj.systemPassword = systemPassword
            domainobj.save()

        print("[ log ] -> 初始化成功")
        result = "success"
    except xlrd.biffh.XLRDError as e:
        print("[ Exception ] -> ", str(e))
        result = "文件损坏,请重新创建文件"
        return JsonResponse(result, safe=False)

    except Exception as e:
        print("[ Exception ] -> ", str(e))
        result = "创建失败"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initproducefirewallpolicyfile(request):
    try:

        ProduceFirewallManage.objects.all().delete()

        path = 'static/upload/AssetsManage/produceFirewallPolicyAll.xls'
        workbook = xlrd.open_workbook(path)  # 打开execl

        # 输出Excel文件中所有sheet的名字
        # print(workbook.sheet_names())
        # 根据sheet索引或者名称获取sheet内容
        domainSheet = workbook.sheets()[0]  # 通过索引获取
        # vulnSheet = workbook.sheet_by_index(0)  # 通过索引获取
        # vulnSheet = workbook.sheet_by_name('ECS')  # 通过名称获取
        # print(vulnSheet.name)  # 获取sheet名称
        rowNum = domainSheet.nrows  # sheet行数
        # colNum = domainSheet.ncols  # sheet列数

        firstLineValue = ['id', 'protocol', 'name', 'pl_grp_profile', 'mode', 'enable', 'bingo', 'cur_conn_num', 'syslog', 'log_sess_start', 'log_sess_end', 'refer_id', 'mv_opt', 'szone_list', 'dzone_list', 'saddr_list', 'saddr_content', 'saddr_desc', 'daddr_list', 'daddr_content', 'daddr_desc', 'sev_list', 'sev_content', 'sev_desc', 'tr_list', 'user_list', 'app_list', 'flowstat', 'is_end', 'page', 'recordsTotal', 'recordsFiltered', 'eurl', 'durl']


        # print(firstLineValue)
        # print(domainSheet.row_values(0))


        if domainSheet.row_values(0) != firstLineValue:
            result = "文件列名不正确,请参考模板文件"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        # # 获取所有单元格的内容
        # list = []
        # for i in range(rowNum):
        #     rowlist = []
        #     for j in range(colNum):
        #         rowlist.append(Data_sheet.cell_value(i, j))
        #         print(type(date_value), date_value)
        #     list.append(rowlist)

        # 输出所有单元格的内容
        for row in range(rowNum):
            if row == 0:
                continue
            id = domainSheet.cell_value(row, 0)
            protocol = domainSheet.cell_value(row, 1)
            name = domainSheet.cell_value(row, 2)
            pl_grp_profile = domainSheet.cell_value(row, 3)
            mode = domainSheet.cell_value(row, 4)
            enable = domainSheet.cell_value(row, 5)
            bingo = domainSheet.cell_value(row, 6)
            cur_conn_num = domainSheet.cell_value(row, 7)
            syslog = domainSheet.cell_value(row, 8)
            log_sess_start = domainSheet.cell_value(row, 9)
            log_sess_end = domainSheet.cell_value(row, 10)
            refer_id = domainSheet.cell_value(row, 11)
            mv_opt = domainSheet.cell_value(row, 12)
            szone_list = domainSheet.cell_value(row, 13)
            dzone_list = domainSheet.cell_value(row, 14)
            saddr_list = domainSheet.cell_value(row, 15)
            saddr_content = domainSheet.cell_value(row, 16)
            saddr_desc = domainSheet.cell_value(row, 17)
            daddr_list = domainSheet.cell_value(row, 18)
            daddr_content = domainSheet.cell_value(row, 19)
            daddr_desc = domainSheet.cell_value(row, 20)
            sev_list = domainSheet.cell_value(row, 21)
            sev_content = domainSheet.cell_value(row, 22)
            sev_desc = domainSheet.cell_value(row, 23)
            tr_list = domainSheet.cell_value(row, 24)
            user_list = domainSheet.cell_value(row, 25)
            app_list = domainSheet.cell_value(row, 26)
            flowstat = domainSheet.cell_value(row, 27)
            is_end = domainSheet.cell_value(row, 28)
            page = domainSheet.cell_value(row, 29)
            recordsTotal = domainSheet.cell_value(row, 30)
            recordsFiltered = domainSheet.cell_value(row, 31)
            eurl = domainSheet.cell_value(row, 32)
            durl = domainSheet.cell_value(row, 33)
            # for j in range(colNum):
            #     # # 获取单元格内容为日期的数据
            #     # date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(i, j), workbook.datemode)
            #     # print(date_value)
            #     print(ecsSheet.cell_value(row, j))
            #     # print(list[i][j], '\t\t', end="")
            #
            # ecsIPS = re.compile(r'((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)')

            producefirewallobj = ProduceFirewallManage()
            producefirewallobj.id = id
            producefirewallobj.protocol = protocol
            producefirewallobj.name = name
            producefirewallobj.pl_grp_profile = pl_grp_profile
            producefirewallobj.mode = mode
            producefirewallobj.enable = enable
            producefirewallobj.bingo = bingo
            producefirewallobj.cur_conn_num = cur_conn_num
            producefirewallobj.syslog = syslog
            producefirewallobj.log_sess_start = log_sess_start
            producefirewallobj.log_sess_end = log_sess_end
            producefirewallobj.refer_id = refer_id
            producefirewallobj.mv_opt = mv_opt
            producefirewallobj.szone_list = szone_list
            producefirewallobj.dzone_list = dzone_list
            producefirewallobj.saddr_list = saddr_list
            producefirewallobj.saddr_content = saddr_content
            producefirewallobj.saddr_desc = saddr_desc
            producefirewallobj.daddr_list = daddr_list
            producefirewallobj.daddr_content = daddr_content
            producefirewallobj.daddr_desc = daddr_desc
            producefirewallobj.sev_list = sev_list
            producefirewallobj.sev_content = sev_content
            producefirewallobj.sev_desc = sev_desc
            producefirewallobj.tr_list = tr_list
            producefirewallobj.user_list = user_list
            producefirewallobj.app_list = app_list
            producefirewallobj.flowstat = flowstat
            producefirewallobj.is_end = is_end
            producefirewallobj.page = page
            producefirewallobj.recordsTotal = recordsTotal
            producefirewallobj.recordsFiltered = recordsFiltered
            producefirewallobj.eurl = eurl
            producefirewallobj.durl = durl
            producefirewallobj.save()

        print("[ log ] -> 初始化成功")
        result = "success"
    except xlrd.biffh.XLRDError as e:
        print("[ Exception ] -> ", str(e))
        result = "文件损坏,请重新创建文件"
        return JsonResponse(result, safe=False)

    except Exception as e:
        print("[ Exception ] -> ", str(e))
        result = "创建失败"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def initworkfirewallpolicyfile(request):
    try:

        WorkFirewallManage.objects.all().delete()

        path = 'static/upload/AssetsManage/workFirewallPolicyAll.xls'
        workbook = xlrd.open_workbook(path)  # 打开execl

        # 输出Excel文件中所有sheet的名字
        # print(workbook.sheet_names())
        # 根据sheet索引或者名称获取sheet内容
        policySheet = workbook.sheets()[0]  # 通过索引获取
        # vulnSheet = workbook.sheet_by_index(0)  # 通过索引获取
        # vulnSheet = workbook.sheet_by_name('ECS')  # 通过名称获取
        # print(vulnSheet.name)  # 获取sheet名称
        rowNum = policySheet.nrows  # sheet行数
        # colNum = domainSheet.ncols  # sheet列数

        firstLineValue = ['id', 'protocol', 'name', 'pl_grp_profile', 'mode', 'enable', 'bingo', 'cur_conn_num', 'syslog', 'log_sess_start', 'log_sess_end', 'refer_id', 'mv_opt', 'szone_list', 'dzone_list', 'saddr_list', 'saddr_content', 'saddr_desc', 'daddr_list', 'daddr_content', 'daddr_desc', 'sev_list', 'sev_content', 'sev_desc', 'tr_list', 'user_list', 'app_list', 'flowstat', 'is_end', 'page', 'recordsTotal', 'recordsFiltered', 'eurl', 'durl']


        # print(firstLineValue)
        # print(domainSheet.row_values(0))


        if policySheet.row_values(0) != firstLineValue:
            result = "文件列名不正确,请参考模板文件"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        # # 获取所有单元格的内容
        # list = []
        # for i in range(rowNum):
        #     rowlist = []
        #     for j in range(colNum):
        #         rowlist.append(Data_sheet.cell_value(i, j))
        #         print(type(date_value), date_value)
        #     list.append(rowlist)

        # 输出所有单元格的内容
        for row in range(rowNum):
            if row == 0:
                continue

            src_ip = policySheet.cell_value(row, 0)
            src_ip_content = policySheet.cell_value(row, 1)
            dst_ip = policySheet.cell_value(row, 2)
            dst_ip_content = policySheet.cell_value(row, 3)
            description = policySheet.cell_value(row, 4)
            status = policySheet.cell_value(row, 5)
            group = policySheet.cell_value(row, 6)
            name = policySheet.cell_value(row, 7)
            log = policySheet.cell_value(row, 8)
            priority = policySheet.cell_value(row, 9)
            conflict_num = policySheet.cell_value(row, 10)
            num = policySheet.cell_value(row, 11)
            active_time = policySheet.cell_value(row, 12)
            dst_zone = policySheet.cell_value(row, 13)
            invalid_id = policySheet.cell_value(row, 14)
            src_zone = policySheet.cell_value(row, 15)
            last_hittime = policySheet.cell_value(row, 16)
            not_hit_day = policySheet.cell_value(row, 17)
            create_time = policySheet.cell_value(row, 18)
            highlight = policySheet.cell_value(row, 19)
            invalid_name = policySheet.cell_value(row, 20)
            action = policySheet.cell_value(row, 21)
            src_port = policySheet.cell_value(row, 22)
            service_app = policySheet.cell_value(row, 23)
            is_sc_create = policySheet.cell_value(row, 24)
            down_interface = policySheet.cell_value(row, 25)
            hit = policySheet.cell_value(row, 26)



            workfirewallobj = WorkFirewallManage()
            workfirewallobj.src_ip = src_ip
            workfirewallobj.src_ip_content = src_ip_content
            workfirewallobj.dst_ip = dst_ip
            workfirewallobj.dst_ip_content = dst_ip_content
            workfirewallobj.description = description
            workfirewallobj.status = status
            workfirewallobj.group = group
            workfirewallobj.name = name
            workfirewallobj.log = log
            workfirewallobj.priority = priority
            workfirewallobj.conflict_num = conflict_num
            workfirewallobj.num = num
            workfirewallobj.active_time = active_time
            workfirewallobj.dst_zone = dst_zone
            workfirewallobj.invalid_id = invalid_id
            workfirewallobj.src_zone = src_zone
            workfirewallobj.last_hittime = last_hittime
            workfirewallobj.not_hit_day = not_hit_day
            workfirewallobj.create_time = create_time
            workfirewallobj.highlight = highlight
            workfirewallobj.invalid_name = invalid_name
            workfirewallobj.action = action
            workfirewallobj.src_port = src_port
            workfirewallobj.service_app = service_app
            workfirewallobj.is_sc_create = is_sc_create
            workfirewallobj.down_interface = down_interface
            workfirewallobj.hit = hit
            workfirewallobj.save()

        print("[ log ] -> 初始化成功")
        result = "success"
    except xlrd.biffh.XLRDError as e:
        print("[ Exception ] -> ", str(e))
        result = "文件损坏,请重新创建文件"
        return JsonResponse(result, safe=False)

    except Exception as e:
        print("[ Exception ] -> ", str(e))
        result = "创建失败"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def addWorkFirewallPolicySubmit(request):
    try:
        # print(request.POST)
        # print(json.loads(request.POST.get('addWorkFirewallPolicy')).keys())
        addWorkFirewallPolicy = request.POST.get('addWorkFirewallPolicy')


        if addWorkFirewallPolicy == "":
            result = "禁止为空"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        try:
            if json.loads(addWorkFirewallPolicy):
                pass
        except json.decoder.JSONDecodeError as e:
            result = "请输入json格式的数据"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        # print(type(json.loads(addWorkFirewallPolicy).keys()))

        # if json.loads(addWorkFirewallPolicy).keys() != ['success', 'cf', 'count', 'data', 'idx']:
        #     result = "不是特定防火墙策略"
        #     print("[ log ] -> ", result)
        #     return JsonResponse(result, safe=False)


        WorkFirewallManage.objects.all().delete()

        policyList = json.loads(addWorkFirewallPolicy)['data']
        for policy in policyList:
            print(policy)
            # print(policy.keys())
            workfirewallobj = WorkFirewallManage()


            # exit()
            try:
                print(policy['src_ip'][0]['name'])
                print(policy['src_ip'][0]['content'])


                if type(policy['src_ip']) != "list":
                    workfirewallobj.src_ip = policy['src_ip'][0]['name']
                    workfirewallobj.src_ip_content = policy['src_ip'][0]['content']
                    workfirewallobj.dst_ip = policy['dst_ip'][0]['name']
                    workfirewallobj.dst_ip_content = policy['dst_ip'][0]['content']
            except Exception as e:
                print(str(e))
                workfirewallobj.src_ip = policy['src_ip']
                workfirewallobj.src_ip_content = "None"
                workfirewallobj.dst_ip = policy['dst_ip']
                workfirewallobj.dst_ip_content = "None"



            workfirewallobj.description = policy['description']
            workfirewallobj.status = policy['status']
            workfirewallobj.group = policy['group']
            workfirewallobj.name = policy['name']
            workfirewallobj.log = policy['log']
            workfirewallobj.priority = policy['priority']
            workfirewallobj.conflict_num = policy['conflict_num']
            workfirewallobj.num = policy['num']
            workfirewallobj.active_time = policy['active_time']
            workfirewallobj.dst_zone = policy['dst_zone']
            workfirewallobj.invalid_id = policy['invalid_id']
            workfirewallobj.src_zone = policy['src_zone']

            if policy['last_hittime'] != "-":
                workfirewallobj.last_hittime = policy['last_hittime']
            else:
                workfirewallobj.last_hittime = None
            workfirewallobj.not_hit_day = policy['not_hit_day']

            if policy['create_time'] != "-":
                workfirewallobj.create_time = "2020-" + policy['create_time']
            else:
                workfirewallobj.create_time = None

            workfirewallobj.highlight = policy['highlight']
            workfirewallobj.invalid_name = policy['invalid_name']
            workfirewallobj.action = policy['action']
            workfirewallobj.src_port = policy['src_port']
            workfirewallobj.service_app = policy['service_app'].replace("自定义服务/", "").replace("预定义服务/", "")
            workfirewallobj.is_sc_create = policy['is_sc_create']
            workfirewallobj.down_interface = policy['down_interface']
            workfirewallobj.hit = policy['hit']
            workfirewallobj.save()

            # exit()

        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    print("[ log ] -> ", result)
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def addDomainSubmit(request):
    try:
        print(request.POST)
        print(dict(request.POST).keys())

        if request.POST.get('domainName') == "":
            result = "域名禁止为空"
            print("[ log ] -> ", result)

            return JsonResponse(result, safe=False)

        if DomainManage.objects.filter(domainName__iexact=request.POST.get('domainName').replace(" ", "")):
            result = "该域名已存在"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        domainobj = DomainManage()
        domainobj.departmentName = request.POST.get('departmentName')
        domainobj.systemName = request.POST.get('systemName')
        domainobj.domainName = request.POST.get('domainName')
        domainobj.SLBIP = request.POST.get('SLBIP')
        domainobj.ECSIP = request.POST.get('ECSIP')
        domainobj.SLBPort = request.POST.get('SLBPort')
        domainobj.systemType = request.POST.get('systemType')
        if request.POST.get('systemStatus') == "true":
            domainobj.systemStatus = "使用中"
        elif request.POST.get('systemStatus') == "false":
            domainobj.systemStatus = "已下线"

        domainobj.accessURL = request.POST.get('accessURL')
        domainobj.developmentCompany = request.POST.get('developmentCompany')

        if request.POST.get('extranetAccess') == "true":
            domainobj.extranetAccess = "开放访问"
        elif request.POST.get('extranetAccess') == "false":
            domainobj.extranetAccess = "本地访问"

        domainobj.businessPeople = request.POST.get('businessPeople')
        domainobj.businessPhone = request.POST.get('businessPhone')
        domainobj.DevelopPeople = request.POST.get('DevelopPeople')
        domainobj.DevelopPhone = request.POST.get('DevelopPhone')
        domainobj.systemDescribe = request.POST.get('systemDescribe')
        domainobj.projectPeopleName = request.POST.get('projectPeopleName')
        domainobj.projectPeoplePhone = request.POST.get('projectPeoplePhone')
        domainobj.systemMiddleware = request.POST.get('systemMiddleware')
        domainobj.systemCommon = request.POST.get('systemCommon')
        domainobj.CreateTime = datetime.datetime.now()
        domainobj.updateTime = datetime.datetime.now()
        domainobj.CreatePeople = request.user
        domainobj.updatePeople = request.user
        domainobj.systemUsername = request.POST.get('systemUsername')
        domainobj.systemPassword = request.POST.get('systemPassword')

        domainobj.save()

        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def addV2EcsSubmit(request):
    # try:
    # print(request.POST)
    # print("-----------------++++++++++")
    # exit()
    # print(json.loads(request.POST.get('addWorkFirewallPolicy')).keys())
    addEcs = request.POST.get('addV2Ecs')


    if addEcs == "":
        result = "禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)


    V2ECSManage.objects.all().delete()

    # print(eval(addEcs))

    for ecs in eval(addEcs):
        # print(ecs.keys())
        # exit()
        v2ecsobj = V2ECSManage()
        v2ecsobj.regionId = ecs['regionId']
        v2ecsobj.instanceId = ecs['instanceId']
        v2ecsobj.instanceName = ecs['instanceName']
        if len(ecs['privateIpAddress']) == 1:
            v2ecsobj.privateIpAddress = ecs['privateIpAddress'][0]
        else:
            v2ecsobj.privateIpAddress = ecs['privateIpAddress']
        v2ecsobj.physicalHostName = ecs['physicalHostName']
        v2ecsobj.projectId = ecs['projectId']
        v2ecsobj.projectName = ecs['projectName']
        v2ecsobj.securityGroupIdList = ecs['securityGroupIdList']
        v2ecsobj.eipAddress = ecs['eipAddress']
        v2ecsobj.natIpAddress = ecs['natIpAddress']
        v2ecsobj.vpcId = ecs['vpcId']
        v2ecsobj.description = ecs['description']
        v2ecsobj.createTime = ecs['createTime']

        v2ecsobj.save()


    result = "success"
    # except Exception as e:
    #     print(str(e))
    #     result = "failed"

    print("[ log ] -> ", result)
    return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def addV2SlbSubmit(request):
    # try:
    # print(request.POST)
    # print("-----------------++++++++++")
    # exit()
    # print(json.loads(request.POST.get('addWorkFirewallPolicy')).keys())
    addSlb = request.POST.get('addV2Slb')


    if addSlb == "":
        result = "禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)



    # print(eval(addSlb))



    for slb in eval(addSlb):
        # print(slb.keys())
        # exit()
        # print("ecsip: ", slb['ecsip'])


        for ip in slb['ecsip']:
            # print("**************")
            # print("ip: ", ip)

            V2ECSManage.objects.filter(privateIpAddress__exact=ip).update(
                loadBalancerId=slb['loadBalancerId']
                ,slbIp=slb['slbIp']
                ,networkType=slb['networkType']
                ,loadBalancerName=slb['loadBalancerName']
                ,projectId=slb['projectId']
                ,projectName=slb['projectName']
                ,slbStatus=slb['slbStatus']
                ,startTime=slb['startTime']
                ,regionId=slb['regionId']
                ,slbport=str(slb['slbport']).strip("[]")
            )

            domainobj = DomainManage.objects.filter(SLBIP__iexact=slb['slbIp'])
            if domainobj.exists():
                for domain in domainobj:
                    domainStr = ''

                    v2obj = V2ECSManage.objects.filter(privateIpAddress__exact=ip)
                    for v2 in v2obj:
                        # print(v2.domain)
                        if v2.domain:
                            tmp = v2.domain + ", " + domain.domainName
                        else:
                            tmp = domain.domainName
                        domainStr = tmp
                        # print(domainStr)

                    V2ECSManage.objects.filter(privateIpAddress__exact=ip).update(
                        domain=domainStr
                        ,systemName=domain.systemName
                        ,businessPeople=domain.businessPeople
                        ,DevelopPeople=domain.DevelopPeople
                        ,accessURL=domain.accessURL
                    )


    result = "success"
    # except Exception as e:
    #     print(str(e))
    #     result = "failed"

    print("[ log ] -> ", result)
    return JsonResponse(result, safe=False)






@login_required
@csrf_exempt
def addV3EcsSubmit(request):
    # try:
    # print(request.POST)
    # print("-----------------++++++++++")
    # exit()
    # print(json.loads(request.POST.get('addWorkFirewallPolicy')).keys())
    addEcs = request.POST.get('addV3Ecs')


    if addEcs == "":
        result = "禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)


    # V2ECSManage.objects.all().delete()

    # print(eval(addEcs))

    for ecs in eval(addEcs):
        # print(ecs.keys())
        # exit()
        if not V2ECSManage.objects.filter(privateIpAddress__exact=ecs).exists():
            v3ecsobj = V2ECSManage()
            v3ecsobj.regionId = ecs['regionId']
            v3ecsobj.instanceId = ecs['instanceId']
            v3ecsobj.instanceName = ecs['instanceName']
            if len(ecs['privateIpAddress']) == 1:
                v3ecsobj.privateIpAddress = ecs['privateIpAddress'][0]
            else:
                v3ecsobj.privateIpAddress = ecs['privateIpAddress']
            v3ecsobj.physicalHostName = ecs['physicalHostName']
            v3ecsobj.projectId = ecs['projectId']
            v3ecsobj.projectName = ecs['projectName']
            v3ecsobj.securityGroupIdList = ecs['securityGroupIdList']
            v3ecsobj.eipAddress = ecs['eipAddress']
            v3ecsobj.natIpAddress = ecs['natIpAddress']
            v3ecsobj.vpcId = ecs['vpcId']
            v3ecsobj.description = ecs['description']
            v3ecsobj.createTime = ecs['createTime']

            v3ecsobj.save()
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    result = "success"
    # except Exception as e:
    #     print(str(e))
    #     result = "failed"

    print("[ log ] -> ", result)
    return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def addV3SlbSubmit(request):
    # try:
    # print(request.POST)
    # print("-----------------++++++++++")
    # exit()
    # print(json.loads(request.POST.get('addWorkFirewallPolicy')).keys())
    addSlb = request.POST.get('addV3Slb')


    if addSlb == "":
        result = "禁止为空"
        # print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)



    # print(eval(addSlb))



    for slb in eval(addSlb):
        # print(slb.keys())
        # exit()
        # print("ecsip: ", slb['ecsip'])
        # print(slb['startTime'].strip("000"))
        # print(int(slb['startTime'].strip("000")))


        for ip in slb['ecsip']:
            # print("**************")
            # print("ip: ", ip)
            # print("slbport: ", slb['slbport'])

            V2ECSManage.objects.filter(privateIpAddress__exact=ip).update(
                loadBalancerId=slb['loadBalancerId']
                ,slbIp=slb['slbIp']
                ,networkType=slb['networkType']
                ,loadBalancerName=slb['loadBalancerName']
                ,projectId=slb['projectId']
                ,projectName=slb['projectName']
                ,slbStatus=slb['slbStatus']
                ,startTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(slb['startTime'].strip("000"))))
                ,regionId=slb['regionId']
                ,slbport=str(slb['slbport']).strip("[]")
            )

            domainobj = DomainManage.objects.filter(SLBIP__iexact=slb['slbIp'])
            if domainobj.exists():
                for domain in domainobj:
                    domainStr = ''

                    v2obj = V2ECSManage.objects.filter(privateIpAddress__exact=ip)
                    for v2 in v2obj:
                        # print(v2.domain)
                        if v2.domain:
                            tmp = v2.domain + ", " + domain.domainName
                        else:
                            tmp = domain.domainName
                        domainStr = tmp
                        # print(domainStr)

                    V2ECSManage.objects.filter(privateIpAddress__exact=ip).update(
                        domain=domainStr
                        ,systemName=domain.systemName
                        ,businessPeople=domain.businessPeople
                        ,DevelopPeople=domain.DevelopPeople
                        ,accessURL=domain.accessURL
                    )


    result = "success"
    # except Exception as e:
    #     print(str(e))
    #     result = "failed"

    print("\n[ log ] -> ", result)
    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def addProduceFirewallPolicySubmit(request):
    # try:
    print(request.POST)
    addProduceFirewallPolicy = request.POST.get('addProduceFirewallPolicy')

    ProduceFirewallManage.objects.all().delete()

    if addProduceFirewallPolicy == "":
        result = "禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    try:
        if json.loads(addProduceFirewallPolicy):
            pass
    except json.decoder.JSONDecodeError as e:
        result = "请输入json格式的数据"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)
    # ['policyList']

    policyList = json.loads(addProduceFirewallPolicy)['data'][0]['policyList']
    # print(type(policyList))
    for policy in policyList:
        # print(policy.keys())
        # print(policy)
        producefirewallobj = ProduceFirewallManage()
        producefirewallobj.id = policy['id']
        producefirewallobj.protocol = policy['protocol']
        if "name" in policy.keys():
            producefirewallobj.name = policy['name']
        else:
            producefirewallobj.name = "None"
        producefirewallobj.pl_grp_profile = policy['pl_grp_profile']
        producefirewallobj.mode = policy['mode']
        producefirewallobj.enable = policy['enable']
        producefirewallobj.bingo = policy['bingo']
        producefirewallobj.cur_conn_num = policy['cur_conn_num']
        producefirewallobj.syslog = policy['syslog']
        producefirewallobj.log_sess_start = policy['log_sess_start']
        producefirewallobj.log_sess_end = policy['log_sess_end']
        producefirewallobj.refer_id = policy['refer_id']
        producefirewallobj.mv_opt = policy['mv_opt']
        producefirewallobj.szone_list = policy['szone_list']["0"]["name"]
        producefirewallobj.dzone_list = policy['dzone_list']["0"]["name"]
        producefirewallobj.saddr_list = policy['saddr_list']["0"]["name"]
        producefirewallobj.daddr_list = policy['daddr_list']["0"]["name"]
        producefirewallobj.sev_list = policy['sev_list']["0"]["name"]
        if "tr_list" in policy.keys():
            producefirewallobj.tr_list = policy['tr_list']["0"]["name"]
        else:
            producefirewallobj.tr_list = "None"

        if "user_list" in policy.keys():
            producefirewallobj.user_list = policy['user_list']["0"]["name"]
        else:
            producefirewallobj.user_list = "None"
        if "app_list" in policy.keys():
            producefirewallobj.app_list = policy['app_list']["0"]["name"]
        else:
            producefirewallobj.app_list = "None"
        producefirewallobj.flowstat = policy['flowstat']
        producefirewallobj.is_end = policy['is_end']
        producefirewallobj.page = policy['page']
        producefirewallobj.recordsTotal = policy['recordsTotal']
        producefirewallobj.recordsFiltered = policy['recordsFiltered']
        producefirewallobj.eurl = policy['eurl']
        producefirewallobj.durl = policy['durl']
        producefirewallobj.save()
        # print("------------------------\n\n\n")


    result = "success"
    print(result)

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def addWorkFirewallIPGroupSubmit(request):
    # try:
    print(request.POST)
    addProduceFirewallIPGroup = request.POST.get('addProduceFirewallIPGroup')

    if addProduceFirewallIPGroup == "":
        result = "禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    try:
        if json.loads(addProduceFirewallIPGroup):
            pass
    except json.decoder.JSONDecodeError as e:
        result = "请输入json格式的数据"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)



    #
    result = "success"
    # except Exception as e:
    #     print(str(e))
    # result = "failed"

    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def addProduceFirewallIPGroupSubmit(request):
    try:
        # print(request.POST)
        addProduceFirewallIPGroup = request.POST.get('addProduceFirewallIPGroup')

        if addProduceFirewallIPGroup == "":
            result = "禁止为空"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        try:
            if json.loads(addProduceFirewallIPGroup):
                pass
        except json.decoder.JSONDecodeError as e:
            result = "请输入json格式的数据"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        ipGroup = json.loads(addProduceFirewallIPGroup)['data']
        # print(ipGroup)
        # print("---------------\n\n")
        #
        # print(type(ipGroup))
        # print("---------------\n\n")

        # ProduceFirewallManage.objects.filter().delete().all()

        # print(len(ipGroup))
        for group in ipGroup:
            # print(type(group))
            # print(group)

            name = group['name']
            if "desc" in group.keys():
                desc = group['desc'].replace("&lt;br&gt;", "; ")
            else:
                desc = None
            content = group['content'].replace("&lt;br&gt;", "; ")
            print(content)
            print("----------------------**********************")


            ProduceFirewallManage.objects.filter(saddr_list=name).update(
                saddr_content=content, saddr_desc=desc)

            ProduceFirewallManage.objects.filter(daddr_list=name).update(
                daddr_content=content, daddr_desc=desc)


        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    print("[ log ] -> ", result)
    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def addProduceFirewallServiceGroupSubmit(request):
    try:
        # print(request.POST)
        # exit()
        addProduceFirewallServiceGroup = request.POST.get('addProduceFirewallServiceGroup')

        if addProduceFirewallServiceGroup == "":
            result = "禁止为空"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        try:
            if json.loads(addProduceFirewallServiceGroup):
                pass
        except json.decoder.JSONDecodeError as e:
            result = "请输入json格式的数据"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        serviceGroup = json.loads(addProduceFirewallServiceGroup)['data']
        # print(serviceGroup)
        # print("---------------\n\n")
        # #
        # print(type(serviceGroup))
        # print("---------------\n\n")

        # ProduceFirewallManage.objects.filter().delete().all()

        # print(len(ipGroup))
        for service in serviceGroup:
            # print(type(service))
            # print(service)

            name = service['name']
            if "desc" in service.keys():
                desc = service['desc']
            else:
                desc = None
            content = service['content'].replace("&lt;br&gt;", "; ").replace("TCP/1-65535:", "")
            # print(content)
            # print("----------------------**********************")

            ProduceFirewallManage.objects.filter(sev_list=name).update(
                sev_content=content, sev_desc=desc)

        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    print("[ log ] -> ", result)
    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def addWorkFirewallServiceGroupSubmit(request):
    # try:
    print(request.POST)
    addProduceFirewallServiceGroup = request.POST.get('addProduceFirewallServiceGroup')

    if addProduceFirewallServiceGroup == "":
        result = "禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    try:
        if json.loads(addProduceFirewallServiceGroup):
            pass
    except json.decoder.JSONDecodeError as e:
        result = "请输入json格式的数据"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)



    #
    #     result = "success"
    # except Exception as e:
    #     print(str(e))
    result = "failed"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def addWorkFirewallNatSubmit(request):
    # try:
    print(request.POST)
    addProduceFirewallNat = request.POST.get('addProduceFirewallNat')

    if addProduceFirewallNat == "":
        result = "禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    try:
        if json.loads(addProduceFirewallNat):
            pass
    except json.decoder.JSONDecodeError as e:
        result = "请输入json格式的数据"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)



    #
    #     result = "success"
    # except Exception as e:
    #     print(str(e))
    result = "failed"

    return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def editDomainForLine(request):
    # try:
    print(request.POST)
    domainName = request.POST.get('domainName')

    obj1 = DomainManage.objects.filter(domainName__iexact=domainName)
    if obj1:
        # obj1.delete()  # 删除旧的,增加新的


        if request.POST.get('systemStatus') == "true":
            status = "使用中"
        elif request.POST.get('systemStatus') == "false":
            status = "已下线"

        if request.POST.get('extranetAccess') == "true":
            extranetAccess = "开放访问"
        elif request.POST.get('extranetAccess') == "false":
            extranetAccess = "本地访问"


        DomainManage.objects.filter(domainName__iexact=domainName).update(
            departmentName=request.POST.get('departmentName'),
            systemName=request.POST.get('systemName'),
            SLBIP=request.POST.get('SLBIP'),
            ECSIP=request.POST.get('ECSIP'),
            SLBPort=request.POST.get('SLBPort'),
            systemType=request.POST.get('systemType'),
            systemStatus=status,
            accessURL=request.POST.get('accessURL'),
            developmentCompany=request.POST.get('developmentCompany'),
            extranetAccess=extranetAccess,
            businessPeople=request.POST.get('businessPeople'),
            businessPhone=request.POST.get('businessPhone'),
            DevelopPeople=request.POST.get('DevelopPeople'),
            DevelopPhone=request.POST.get('DevelopPhone'),
            projectPeopleName=request.POST.get('projectPeopleName'),
            projectPeoplePhone=request.POST.get('projectPeoplePhone'),
            systemMiddleware=request.POST.get('systemMiddleware'),
            systemCommon=request.POST.get('systemCommon'),
            systemDescribe =request.POST.get('systemDescribe'),
            # CreateTime=datetime.datetime.now(),
            updateTime=datetime.datetime.now(),
            updatePeople=str(request.user),
            systemUsername=request.POST.get('systemUsername'),
            systemPassword=request.POST.get('systemPassword')




        )



        result = "success"

    else:
        result = "该域名资产不存在,无法修改</br>提示 :禁止对域名进行编辑"
    # except Exception as e:
    #     print(str(e))
    #     result = "failed"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deleteECSall(request):
    try:
        V2ECSManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)

@login_required
@csrf_exempt
def deleteProduceFirewallPolicyAll(request):
    try:
        ProduceFirewallManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deleteDomainAll(request):
    try:
        DomainManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deleteVulnall(request):
    try:
        ShaoBingYunManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)

@login_required
@csrf_exempt
def deleteProducefirewallpolicyfileAll(request):
    try:
        ProduceFirewallManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)

@login_required
@csrf_exempt
def deleteWorkfirewallpolicyfileAll(request):
    try:
        WorkFirewallManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def searchECS(request):
    privateIpAddress = request.GET.get('privateIpAddress', None).strip(" ")
    slbIp = request.GET.get('slbIp', None).strip(" ")
    projectName = request.GET.get('projectName', None).strip(" ")
    description = request.GET.get('description', None).strip(" ")
    eipAddress = request.GET.get('eipAddress', None).strip(" ")

    # 方法一：
    ecsobj = V2ECSManage.objects.all()

    if privateIpAddress:
        ecsobj = ecsobj.filter(privateIpAddress__icontains=privateIpAddress)
    if slbIp:
        ecsobj = ecsobj.filter(slbIp__iexact=slbIp)
    if projectName:
        ecsobj = ecsobj.filter(projectName__icontains=projectName)
    if description:
        ecsobj = ecsobj.filter(description__icontains=description)
    if eipAddress:
        ecsobj = ecsobj.filter(eipAddress__iexact=eipAddress)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = ecsobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for ecs in ecsobj:
        dict = {}
        # print("++++++++++++++++")
        # print((service.serviceName))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        dict['createTime'] = ecs.createTime
        dict['description'] = ecs.description
        dict['eipAddress'] = ecs.eipAddress
        dict['instanceId'] = ecs.instanceId
        dict['instanceName'] = ecs.instanceName
        dict['loadBalancerId'] = ecs.loadBalancerId
        dict['loadBalancerName'] = ecs.loadBalancerName
        dict['natIpAddress'] = ecs.natIpAddress
        dict['networkType'] = ecs.networkType
        dict['physicalHostName'] = ecs.physicalHostName
        dict['privateIpAddress'] = ecs.privateIpAddress
        dict['projectId'] = ecs.projectId
        dict['projectName'] = ecs.projectName
        dict['regionId'] = ecs.regionId
        dict['securityGroupIdList'] = ecs.securityGroupIdList

        dict['domain'] = ecs.domain
        dict['systemName'] = ecs.systemName
        dict['businessPeople'] = ecs.businessPeople
        dict['DevelopPeople'] = ecs.DevelopPeople
        dict['accessURL'] = ecs.accessURL

        dict['slbIp'] = ecs.slbIp
        dict['slbStatus'] = ecs.slbStatus
        dict['slbport'] = ecs.slbport
        dict['startTime'] = ecs.startTime
        dict['vpcId'] = ecs.vpcId


        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('privateIpAddress')), reverse=False)
        # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    except TypeError as e:
        pass

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
def searchProduceFirewallPolicy(request):
    name = request.GET.get('name', None).strip(" ")
    saddr_list = request.GET.get('saddr_list', None).strip(" ")
    daddr_list = request.GET.get('daddr_list', None).strip(" ")
    sev_list = request.GET.get('sev_list', None).strip(" ")
    bingo = request.GET.get('bingo', None).strip(" ")

    # 方法一：
    policyobj = ProduceFirewallManage.objects.all()

    if name:
        policyobj = policyobj.filter(name__icontains=name)
    if saddr_list:
        policyobj = policyobj.filter(saddr_list__icontains=saddr_list)
    if daddr_list:
        policyobj = policyobj.filter(daddr_list__icontains=daddr_list)
    if sev_list:
        policyobj = policyobj.filter(sev_list__icontains=sev_list)
    if bingo:
        policyobj = policyobj.filter(bingo__iexact=bingo)

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

    list1 = []
    for policy in policyobj:
        dict = {}

        dict['id'] = policy.id
        dict['protocol'] = policy.protocol
        dict['name'] = policy.name
        dict['pl_grp_profile'] = policy.pl_grp_profile
        dict['mode'] = policy.mode
        dict['enable'] = policy.enable
        dict['bingo'] = policy.bingo
        dict['cur_conn_num'] = policy.cur_conn_num
        dict['syslog'] = policy.syslog
        dict['log_sess_start'] = policy.log_sess_start
        dict['log_sess_end'] = policy.log_sess_end
        dict['refer_id'] = policy.refer_id
        dict['mv_opt'] = policy.mv_opt
        dict['szone_list'] = policy.szone_list
        dict['dzone_list'] = policy.dzone_list
        dict['saddr_list'] = policy.saddr_list
        dict['saddr_content'] = policy.saddr_content
        dict['saddr_desc'] = policy.saddr_desc
        dict['daddr_list'] = policy.daddr_list
        dict['daddr_content'] = policy.daddr_content
        dict['daddr_desc'] = policy.daddr_desc
        dict['sev_list'] = policy.sev_list
        dict['sev_content'] = policy.sev_content
        dict['sev_desc'] = policy.sev_desc
        dict['tr_list'] = policy.tr_list
        dict['user_list'] = policy.user_list
        dict['app_list'] = policy.app_list
        dict['flowstat'] = policy.flowstat
        dict['is_end'] = policy.is_end
        dict['page'] = policy.page
        dict['recordsTotal'] = policy.recordsTotal
        dict['recordsFiltered'] = policy.recordsFiltered
        dict['eurl'] = policy.eurl
        dict['durl'] = policy.durl


        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('bingo')), reverse=True)
        # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    except TypeError as e:
        pass

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
def searchvuln(request):
    vulIP = request.GET.get('ipId', None).strip(" ")
    vulType = request.GET.get('typeID', None).strip(" ")
    vulService = request.GET.get('serviceId', None).strip(" ")
    vulAddress = request.GET.get('addressId', None).strip(" ")
    vulDescribe = request.GET.get('describeId', None).strip(" ")

    # 方法一：
    vulnobj = ShaoBingYunManage.objects.all()

    if vulIP:
        vulnobj = vulnobj.filter(vulIP__iexact=vulIP)
    if vulType:
        vulnobj = vulnobj.filter(vulType__iexact=vulType)
    if vulService:
        vulnobj = vulnobj.filter(vulService__iexact=vulService)
    if vulAddress:
        vulnobj = vulnobj.filter(vulAddress__iexact=vulAddress)
    if vulDescribe:
        vulnobj = vulnobj.filter(vulDescribe__iexact=vulDescribe)

    # if vulIP:
    #     vulnobj = vulnobj.filter(vulIP__iexact=vulIP)
    # if vulType:
    #     vulnobj = vulnobj.filter(vulType__iexact=vulType)
    # if vulService:
    #     vulnobj = vulnobj.filter(vulService__iexact=vulService)
    # if vulAddress:
    #     vulnobj = vulnobj.filter(vulAddress__iexact=vulAddress)
    # if vulDescribe:
    #     vulnobj = vulnobj.filter(vulDescribe__iexact=vulDescribe)
    #

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = vulnobj.count()
    # print("total:", total)
    resultdict = {}
    list1 = []
    for vuln in vulnobj:
        dict = {}
        # print("++++++++++++++++")
        # print((service.serviceName))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        dict['vulName'] = vuln.vulName
        dict['vulLevel'] = vuln.vulLevel
        dict['vulURL'] = vuln.vulURL
        dict['vulStatus'] = vuln.vulStatus
        dict['vulAddress'] = vuln.vulAddress
        dict['vulIP'] = vuln.vulIP
        dict['vulDomain'] = vuln.vulDomain
        dict['vulService'] = vuln.vulService
        dict['vulCoutry'] = vuln.vulCoutry
        dict['vulIsRepair'] = vuln.vulIsRepair
        dict['vulIsHandle'] = vuln.vulIsHandle
        dict['vulGroup'] = vuln.vulGroup
        dict['vulMark'] = vuln.vulMark
        dict['vulScore'] = vuln.vulScore
        dict['vulID'] = vuln.vulID
        dict['vulDescribe'] = vuln.vulDescribe
        dict['vulType'] = vuln.vulType
        dict['vulDamage'] = vuln.vulDamage
        dict['vulDetails'] = vuln.vulDetails
        dict['vulSuggest'] = vuln.vulSuggest
        dict['vulRequest'] = vuln.vulRequest
        dict['vulResponse'] = vuln.vulResponse
        dict['vulFirstFindTime'] = vuln.vulFirstFindTime
        dict['vulUpdateTime'] = vuln.vulUpdateTime

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
def searchDomain(request):
    # print(request.GET)
    # print(request.post)

    departmentName = request.GET.get('departmentName', None).strip(" ")
    systemName = request.GET.get('systemName', None).strip(" ")
    domainName = request.GET.get('domainName', None).strip(" ")
    SLBIP = request.GET.get('SLBIP', None).strip(" ")
    systemType = request.GET.get('systemType', None).strip(" ")
    systemStatus = request.GET.get('systemStatus', None).strip(" ")
    developmentCompany = request.GET.get('developmentCompany', None).strip(" ")

    # 方法一：
    domainobj = DomainManage.objects.all()

    if departmentName:
        domainobj = domainobj.filter(departmentName__iexact=departmentName)
    if systemName:
        domainobj = domainobj.filter(systemName__icontains=systemName)
    if domainName:
        domainobj = domainobj.filter(domainName__icontains=domainName)
    if SLBIP:
        domainobj = domainobj.filter(SLBIP__iexact=SLBIP)
    if systemType:
        domainobj = domainobj.filter(systemType__iexact=systemType)
    if systemStatus:
        domainobj = domainobj.filter(systemStatus__iexact=systemStatus)
    if developmentCompany:
        domainobj = domainobj.filter(developmentCompany__icontains=developmentCompany)

    # if vulIP:
    #     vulnobj = vulnobj.filter(vulIP__iexact=vulIP)
    # if vulType:
    #     vulnobj = vulnobj.filter(vulType__iexact=vulType)
    # if vulService:
    #     vulnobj = vulnobj.filter(vulService__iexact=vulService)
    # if vulAddress:
    #     vulnobj = vulnobj.filter(vulAddress__iexact=vulAddress)
    # if vulDescribe:
    #     vulnobj = vulnobj.filter(vulDescribe__iexact=vulDescribe)
    #

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = domainobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for domain in domainobj:
        dict = {}
        # print("++++++++++++++++")
        # print((service.serviceName))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        dict['departmentName'] = domain.departmentName
        dict['systemName'] = domain.systemName
        dict['domainName'] = domain.domainName
        dict['SLBIP'] = domain.SLBIP
        dict['SLBPort'] = domain.SLBPort
        dict['systemType'] = domain.systemType
        dict['systemStatus'] = domain.systemStatus
        dict['accessURL'] = domain.accessURL
        dict['developmentCompany'] = domain.developmentCompany
        dict['extranetAccess'] = domain.extranetAccess
        dict['businessPeople'] = domain.businessPeople
        dict['businessPhone'] = domain.businessPhone
        dict['DevelopPeople'] = domain.DevelopPeople
        dict['DevelopPhone'] = domain.DevelopPhone
        dict['systemDescribe'] = domain.systemDescribe
        dict['CreateTime'] = domain.CreateTime
        dict['updateTime'] = domain.updateTime
        dict['CreatePeople'] = domain.CreatePeople
        dict['updatePeople'] = domain.updatePeople
        dict['systemUsername'] = domain.systemUsername
        dict['systemPassword'] = domain.systemPassword
        dict['ECSIP'] = domain.ECSIP
        dict['projectPeopleName'] = domain.projectPeopleName
        dict['projectPeoplePhone'] = domain.projectPeoplePhone
        dict['systemMiddleware'] = domain.systemMiddleware
        dict['systemCommon'] = domain.systemCommon

        print(domain.SLBIP)

        # if not domain.SLBIP:
        #     continue

        # 从ECS库里,通过SLB查询ECS和EIP
        # print(domain.SLBIP)
        if domain.SLBIP:

            ecsobj = V2ECSManage.objects.filter(slbIp__iexact=domain.SLBIP)
            if ecsobj:
                privateIpAddressStr = ""
                eipAddressStr = ""

                for ecs in ecsobj:
                    if ecs.privateIpAddress:
                        privateIpAddressStr = privateIpAddressStr + ecs.privateIpAddress + "; "
                for ecs in ecsobj:
                    if ecs.eipAddress:
                        eipAddressStr = eipAddressStr + ecs.eipAddress + "; "

                dict['ECSIP'] = str(privateIpAddressStr)
                dict['EIP'] = str(eipAddressStr)
            else:
                dict['ECSIP'] = ""
                dict['EIP'] = ""



        list1.append(dict)

    # try:
    #     list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
    list1.sort(key=lambda k: (k.get('updateTime')), reverse=True)
    # except TypeError as e:
    #     pass
    # print(list1)

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)

    # print(list1)
    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


@login_required
@csrf_exempt
def deleteDomainForLine(request):
    try:
        # print(request.POST.get('delete'))
        # print(request.POST.get('cnvdNumber'))
        if request.POST:
            delete = request.POST.get('delete')
            domainName = request.POST.get('domainName')
            systemName = request.POST.get('systemName')
            SLBIP = request.POST.get('SLBIP')

            # print(type(deleteStr))
            # print(cnvdNumberStr)

            if delete == "yes":
                DomainManage.objects.filter(domainName=domainName, systemName=systemName, SLBIP=SLBIP).delete()

                result = "success"
                print(result)

            else:
                result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse(str(e), safe=False)


@login_required
@csrf_exempt
def downloadEcsTemplateFile(request):
    file = open('static/upload/AssetsManage/ecsAssetsTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="EcsAssetsTemplate_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response


@login_required
@csrf_exempt
def downloadVulnTemplateFile(request):
    file = open('static/upload/AssetsManage/shaoBingYunTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="ShaoBingYunTemplate_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response


@login_required
@csrf_exempt
def downloadDomainTemplateFile(request):
    file = open('static/upload/AssetsManage/domainAssetTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="DomainAssetTemplate_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response


@login_required
@csrf_exempt
def downloadProduceFirewallPolicyTemplateFile(request):
    file = open('static/upload/AssetsManage/produceFirewallPolicyTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="produceFirewallPolicyTemplate_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response


@login_required
@csrf_exempt
def downloadWorkFirewallPolicyTemplateFile(request):
    file = open('static/upload/AssetsManage/workFirewallPolicyTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="workFirewallPolicyTemplate_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response




@login_required
@csrf_exempt
def downloadDomainAllToFile(request):

    filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/domainAssetAll.xls")
    # print(filepath)

    dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if os.path.exists(filepath):
        new_filepath = dirpath + "domainAssetAll_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls"
        # print(filepath)
        # print(new_filepath)
        shutil.move(filepath, new_filepath)
        # os.rename(filepath, new_filepath)
        # print("ok")



    domainobj = DomainManage.objects.all()


    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    domainSheet = workbook.add_sheet('domainAll')

    #生成第一行
    row0 = ['系统名称', '部门名称', '域名', 'SLB地址', '访问URL', 'SLB端口', 'ECS地址', '系统类型', '外网访问', '业务联系人', '业务联系方式', '项目经理', '经理联系方式', '研发人员', '研发人员', '系统状态', '开发单位', '中间件', '系统描述', '备注', '创建时间', '修改时间', '创建人', '修改人', '账号', '密码']
    for i in range(0, len(row0)):
        domainSheet.write(0, i, row0[i])


    rownum = 0

    for domain in domainobj:
        # if domain.systemStatus == "已下线":
        #     continue
        rownum = rownum + 1
        domainSheet.write(rownum, 0, domain.systemName)
        domainSheet.write(rownum, 1, domain.departmentName)
        domainSheet.write(rownum, 2, domain.domainName)
        domainSheet.write(rownum, 3, domain.SLBIP)
        domainSheet.write(rownum, 4, domain.accessURL)
        domainSheet.write(rownum, 5, domain.SLBPort)
        domainSheet.write(rownum, 6, domain.ECSIP)
        domainSheet.write(rownum, 7, domain.systemType)
        domainSheet.write(rownum, 8, domain.extranetAccess)
        domainSheet.write(rownum, 9, domain.businessPeople)
        domainSheet.write(rownum, 10, domain.businessPhone)
        domainSheet.write(rownum, 11, domain.projectPeopleName)
        domainSheet.write(rownum, 12, domain.projectPeoplePhone)
        domainSheet.write(rownum, 13, domain.DevelopPeople)
        domainSheet.write(rownum, 14, domain.DevelopPhone)
        domainSheet.write(rownum, 15, domain.systemStatus)
        domainSheet.write(rownum, 16, domain.developmentCompany)
        domainSheet.write(rownum, 17, domain.systemMiddleware)
        domainSheet.write(rownum, 18, domain.systemDescribe)
        domainSheet.write(rownum, 19, domain.systemCommon)
        domainSheet.write(rownum, 20, str(domain.CreateTime))
        domainSheet.write(rownum, 21, str(domain.updateTime))
        domainSheet.write(rownum, 22, domain.CreatePeople)
        domainSheet.write(rownum, 23, domain.updatePeople)
        domainSheet.write(rownum, 24, domain.systemUsername)
        domainSheet.write(rownum, 25, domain.systemPassword)
        print(rownum)


    workbook.save(filepath)


    file = open(filepath, 'rb')


    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="domainAll_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response



@login_required
@csrf_exempt
def downloadProduceFirewallPolicyAllToFile(request):

    filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/produceFirewallPolicyAll.xls")
    # print(filepath)

    dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if os.path.exists(filepath):
        new_filepath = dirpath + "produceFirewallPolicyAll_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls"
        # print(filepath)
        # print(new_filepath)
        shutil.move(filepath, new_filepath)
        # os.rename(filepath, new_filepath)
        # print("ok")

    producefirewallpolicyobj = ProduceFirewallManage.objects.all()


    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    firewallpolicySheet = workbook.add_sheet('domainAll')

    #生成第一行
    row0 = ['id', 'protocol', 'name', 'pl_grp_profile', 'mode', 'enable', 'bingo', 'cur_conn_num', 'syslog', 'log_sess_start', 'log_sess_end', 'refer_id', 'mv_opt', 'szone_list', 'dzone_list', 'saddr_list', 'saddr_content', 'saddr_desc', 'daddr_list', 'daddr_content', 'daddr_desc', 'sev_list', 'sev_content', 'sev_desc', 'tr_list', 'user_list', 'app_list', 'flowstat', 'is_end', 'page', 'recordsTotal', 'recordsFiltered', 'eurl', 'durl']

    for i in range(0, len(row0)):
        firewallpolicySheet.write(0, i, row0[i])


    rownum = 0

    for policy in producefirewallpolicyobj:
        # if domain.systemStatus == "已下线":
        #     continue
        rownum = rownum + 1
        firewallpolicySheet.write(rownum, 0, policy.id)
        firewallpolicySheet.write(rownum, 1, policy.protocol)
        firewallpolicySheet.write(rownum, 2, policy.name)
        firewallpolicySheet.write(rownum, 3, policy.pl_grp_profile)
        firewallpolicySheet.write(rownum, 4, policy.mode)
        firewallpolicySheet.write(rownum, 5, policy.enable)
        firewallpolicySheet.write(rownum, 6, policy.bingo)
        firewallpolicySheet.write(rownum, 7, policy.cur_conn_num)
        firewallpolicySheet.write(rownum, 8, policy.syslog)
        firewallpolicySheet.write(rownum, 9, policy.log_sess_start)
        firewallpolicySheet.write(rownum, 10, policy.log_sess_end)
        firewallpolicySheet.write(rownum, 11, policy.refer_id)
        firewallpolicySheet.write(rownum, 12, policy.mv_opt)
        firewallpolicySheet.write(rownum, 13, policy.szone_list)
        firewallpolicySheet.write(rownum, 14, policy.dzone_list)
        firewallpolicySheet.write(rownum, 15, policy.saddr_list)
        firewallpolicySheet.write(rownum, 16, policy.saddr_content)
        firewallpolicySheet.write(rownum, 17, policy.saddr_desc)
        firewallpolicySheet.write(rownum, 18, policy.daddr_list)
        firewallpolicySheet.write(rownum, 19, policy.daddr_content)
        firewallpolicySheet.write(rownum, 20, policy.daddr_desc)
        firewallpolicySheet.write(rownum, 21, policy.sev_list)
        firewallpolicySheet.write(rownum, 22, policy.sev_content)
        firewallpolicySheet.write(rownum, 23, policy.sev_desc)
        firewallpolicySheet.write(rownum, 24, policy.tr_list)
        firewallpolicySheet.write(rownum, 25, policy.user_list)
        firewallpolicySheet.write(rownum, 26, policy.app_list)
        firewallpolicySheet.write(rownum, 27, policy.flowstat)
        firewallpolicySheet.write(rownum, 28, policy.is_end)
        firewallpolicySheet.write(rownum, 29, policy.page)
        firewallpolicySheet.write(rownum, 30, policy.recordsTotal)
        firewallpolicySheet.write(rownum, 31, policy.recordsFiltered)
        firewallpolicySheet.write(rownum, 32, policy.eurl)
        firewallpolicySheet.write(rownum, 33, policy.durl)
        # print(rownum)

    workbook.save(filepath)


    file = open(filepath, 'rb')


    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="produceFirewallPolicyAll_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response




@login_required
@csrf_exempt
def downloadWorkFirewallPolicyAllToFile(request):

    filepath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/workFirewallPolicyAll.xls")
    # print(filepath)

    dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if os.path.exists(filepath):
        new_filepath = dirpath + "workFirewallPolicyAll_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls"
        # print(filepath)
        # print(new_filepath)
        shutil.move(filepath, new_filepath)
        # os.rename(filepath, new_filepath)
        # print("ok")



    workfirewallpolicyobj = WorkFirewallManage.objects.all()


    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    firewallpolicySheet = workbook.add_sheet('domainAll')

    #生成第一行
    row0 = ['id', 'protocol', 'name', 'pl_grp_profile', 'mode', 'enable', 'bingo', 'cur_conn_num', 'syslog', 'log_sess_start', 'log_sess_end', 'refer_id', 'mv_opt', 'szone_list', 'dzone_list', 'saddr_list', 'saddr_content', 'saddr_desc', 'daddr_list', 'daddr_content', 'daddr_desc', 'sev_list', 'sev_content', 'sev_desc', 'tr_list', 'user_list', 'app_list', 'flowstat', 'is_end', 'page', 'recordsTotal', 'recordsFiltered', 'eurl', 'durl']

    for i in range(0, len(row0)):
        firewallpolicySheet.write(0, i, row0[i])


    rownum = 0

    for work in workfirewallpolicyobj:
        # if domain.systemStatus == "已下线":
        #     continue
        rownum = rownum + 1
        firewallpolicySheet.write(rownum, 0, work.src_ip)
        firewallpolicySheet.write(rownum, 1, work.src_ip_content)
        firewallpolicySheet.write(rownum, 2, work.dst_ip)
        firewallpolicySheet.write(rownum, 3, work.dst_ip_content)
        firewallpolicySheet.write(rownum, 4, work.description)
        firewallpolicySheet.write(rownum, 5, work.status)
        firewallpolicySheet.write(rownum, 6, work.group)
        firewallpolicySheet.write(rownum, 7, work.name)
        firewallpolicySheet.write(rownum, 8, work.log)
        firewallpolicySheet.write(rownum, 9, work.priority)
        firewallpolicySheet.write(rownum, 10, work.conflict_num)
        firewallpolicySheet.write(rownum, 11, work.num)
        firewallpolicySheet.write(rownum, 12, work.active_time)
        firewallpolicySheet.write(rownum, 13, work.dst_zone)
        firewallpolicySheet.write(rownum, 14, work.invalid_id)
        firewallpolicySheet.write(rownum, 15, work.src_zone)
        firewallpolicySheet.write(rownum, 16, str(work.last_hittime))
        firewallpolicySheet.write(rownum, 17, work.not_hit_day)
        firewallpolicySheet.write(rownum, 18, str(work.create_time))
        firewallpolicySheet.write(rownum, 19, work.highlight)
        firewallpolicySheet.write(rownum, 20, work.invalid_name)
        firewallpolicySheet.write(rownum, 21, work.action)
        firewallpolicySheet.write(rownum, 22, work.src_port)
        firewallpolicySheet.write(rownum, 23, work.service_app)
        firewallpolicySheet.write(rownum, 24, work.is_sc_create)
        firewallpolicySheet.write(rownum, 25, work.down_interface)
        firewallpolicySheet.write(rownum, 26, work.hit)



        # print(rownum)

    workbook.save(filepath)


    file = open(filepath, 'rb')


    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="workFirewallPolicyAll_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response







@login_required
@csrf_exempt
def getEcsSLBIP(request):
    ecsSLBIP = request.POST.get('ecsslbip', None).replace(" ", "").replace("\n", "")
    # print(ecsSLBIP)


    if "" == ecsSLBIP or "无" in ecsSLBIP:
        result = {"code": 500, "msg": "该 SLB IP 为空，查询失败！"}
        return JsonResponse(result, safe=False)

    elif "10.111" in ecsSLBIP:

        domainobj = DomainManage.objects.filter(SLBIP__iexact=ecsSLBIP)

        if domainobj.count() == 0:
            result = {"code": 500, "msg": "查询该 SLB: %s 无域名" % ecsSLBIP}
            return JsonResponse(result, safe=False)

        for domain in domainobj:
            result = {"code": 200, "msg": "查询该 SLB: %s 域名为 " % (ecsSLBIP, domain.domainName)}
            return JsonResponse(result, safe=False)

    else:
        result = {"code": 500, "msg": "未查询到数据"}
        return JsonResponse(result, safe=False)

@login_required
@csrf_exempt
def getVulSLBipAndDomain(request):
    vulIP = request.POST.get('vulIP', None).replace(" ", "").replace("\n", "")
    # print(vulIP)

    if "" == vulIP or "无" in vulIP:
        result = {"code": 500, "msg": "查询该 ECS: %s </br>无 SLB  </br>无域名" % vulIP}
        print(result)
        return JsonResponse(result, safe=False)

    ecsSLBIPs = []

    ecsobj = V2ECSManage.objects.filter(ecsIP__iexact=vulIP)
    for ecs in ecsobj:
        if ecs.ecsSLBIP == "" or ecs.ecsSLBIP == "无":
            continue
        ecsSLBIPs.append(ecs.ecsSLBIP)


    if len(ecsSLBIPs) == 0:
        result = {"code": 500, "msg": "查询该 ECS: %s </br>无 SLB  </br>无域名" % vulIP}

    elif len(ecsSLBIPs) == 1:
        domainobj = DomainManage.objects.filter(SLBIP__iexact=ecsSLBIPs[0])

        if domainobj.count() == 0:
            result = {"code": 200, "msg": "查询该 ECS: %s  </br>SLB 为: %s </br>无域名" \
                                          % (vulIP, ecsSLBIPs[0])}

        else:
            result = {"code": 200, "msg": ""}
            for domain in domainobj:
                result = {"code": 200, "msg": "查询该 ECS: %s </br>SLB 为:%s </br>域名为:%s " \
                                              % (vulIP, ecsSLBIPs[0], domain.domainName)}

    else:
        domains = {}
        for slb in ecsSLBIPs:
            domainobj = DomainManage.objects.filter(SLBIP__iexact=slb)
            if domainobj.count() == 0:
                domains[str(slb)] = "无域名"
            else:
                for domain in domainobj:
                    domains[str(slb)] = domain.domainName


        msg = "查询该 ECS: %s: </br>" % vulIP
        for key, value in domains.items():
            msg += key + ": " + value + "</br>"

        result = {"code": 200, "msg": msg}
        print(result)


    return JsonResponse(result, safe=False)




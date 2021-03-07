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
from Assets.models import *
from ProjectName.models import *
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
    return render(request, 'HostVuln/hostVuln.html')


@login_required
def hostVuln(request):
    return render(request, 'HostVuln/hostVuln.html')



@login_required
@csrf_exempt
def getHostVulnlist(request):
    hostvulnobj = HostVulnManage.objects.all()

    # total = shipManage.objects.filter(systemStatus__contains="使用中").count()
    total = 0
    resultdict = {}
    list1 = []
    for hostvuln in hostvulnobj:
        # print("--")
        total = total + 1
        dict = {}
        dict['vulnName'] = hostvuln.vulnName
        dict['urgent'] = hostvuln.urgent
        dict['assetId'] = hostvuln.assetId
        dict['assetPublicIP'] = hostvuln.assetPublicIP  #EIP & ECSIP
        dict['assetPrivateIP'] = hostvuln.assetPrivateIP    #ECSIP
        dict['assetRemarks'] = hostvuln.assetRemarks
        dict['firstFindTime'] = hostvuln.firstFindTime
        dict['lastFindTime'] = hostvuln.lastFindTime
        dict['vulnExplain'] = hostvuln.vulnExplain
        dict['vulnStatus'] = hostvuln.vulnStatus
        dict['repairCommand'] = hostvuln.repairCommand
        dict['CVEID'] = hostvuln.CVEID
        dict['label'] = hostvuln.label


        # v2ecsobj = V2ECSManage.objects.filter(privateIpAddress__exact=hostvuln.assetPublicIP)
        #
        # if not v2ecsobj:
        #     v2ecsobj = V2ECSManage.objects.filter(privateIpAddress__exact=hostvuln.assetPrivateIP)
        #
        # for v2ecs in v2ecsobj:
        #     # print(v2ecs.domain)
        #     # print(v2ecs.systemName)
        #     # print(v2ecs.projectName)
        #     # print(v2ecs.description)
        #     # print(v2ecs.slbIp)
        #     # print(v2ecs.businessPeople)
        #     # print(v2ecs.DevelopPeople)
        #     dict['domain'] = v2ecs.domain
        #     dict['systemName'] = v2ecs.systemName
        #     dict['projectName'] = v2ecs.projectName
        #     dict['description'] = v2ecs.description
        #     dict['slbIp'] = v2ecs.slbIp
        #     dict['businessPeople'] = v2ecs.businessPeople
        #     dict['DevelopPeople'] = v2ecs.DevelopPeople



        list1.append(dict)


    try:
        # list1.sort(key=lambda k: (k.get('CreateTime')), reverse=False)
        list1.sort(key=lambda k: (k.get('vulnName')), reverse=False)
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
def uploadHostVulnfile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "HostVulnManage/HostVulnAsset.xlsx")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "HostVulnManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "HostVulnManage/bak/HostVulnAsset%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xlsx")

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
def initHostVuln(request):
    try:

        path = 'static/upload/HostVulnManage/HostVulnAsset.xlsx'
        workbook = xlrd.open_workbook(path)  # 打开execl

        # 输出Excel文件中所有sheet的名字
        # print(workbook.sheet_names())
        # 根据sheet索引或者名称获取sheet内容
        dataSheet = workbook.sheets()[0]  # 通过索引获取
        # vulnSheet = workbook.sheet_by_index(0)  # 通过索引获取
        # vulnSheet = workbook.sheet_by_name('ECS')  # 通过名称获取
        # print(vulnSheet.name)  # 获取sheet名称
        # print(dataSheet)
        rowNum = dataSheet.nrows  # sheet行数
        # colNum = shipSheet.ncols  # sheet列数

        firstLineValue = ["漏洞名称", "修复紧急度", "影响资产ID ", "影响资产IP（公网）", "影响资产IP（私网）", "影响资产备注名称", "首次发现时间", "最近一次发现时间", "漏洞说明", "漏洞状态", "修复命令", "CVE编号", " 标签"]


        print(firstLineValue)
        print(dataSheet.row_values(0))


        if dataSheet.row_values(0) != firstLineValue:
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

            vulnName = str((dataSheet.cell_value(row, 0)))
            # print(vulnName)
            urgent = str((dataSheet.cell_value(row, 1)))
            assetId = str((dataSheet.cell_value(row, 2)))
            assetPublicIP = str((dataSheet.cell_value(row, 3)))
            assetPrivateIP = str((dataSheet.cell_value(row, 4)))
            assetRemarks = str((dataSheet.cell_value(row, 5)))
            firstFindTime = str((dataSheet.cell_value(row, 6)))
            lastFindTime = str((dataSheet.cell_value(row, 7)))
            vulnExplain = str((dataSheet.cell_value(row, 8)))[:2000]
            # print(vulnExplain)
            vulnStatus = str((dataSheet.cell_value(row, 9)))
            repairCommand = str((dataSheet.cell_value(row, 10)))
            CVEID = str((dataSheet.cell_value(row, 11)))
            # print(CVEID)
            label = str((dataSheet.cell_value(row, 12)))


            # print(vulnName, assetPublicIP, assetId)

            hostvulnobj = HostVulnManage.objects.filter(vulnName__iexact=vulnName
                                                        ,assetPublicIP__iexact=assetPublicIP
                                                        ,assetId__iexact=assetId)
            if not hostvulnobj:
                print("新增漏洞: ", vulnName, assetPublicIP, assetId)
                hostvulnobj = HostVulnManage()
                hostvulnobj.vulnName = vulnName
                hostvulnobj.urgent = urgent
                hostvulnobj.assetId = assetId
                hostvulnobj.assetPublicIP = assetPublicIP
                hostvulnobj.assetPrivateIP = assetPrivateIP
                hostvulnobj.assetRemarks = assetRemarks
                if firstFindTime:
                    hostvulnobj.firstFindTime = firstFindTime
                else:
                    hostvulnobj.firstFindTime = None
                if lastFindTime:
                    hostvulnobj.lastFindTime = lastFindTime
                else:
                    hostvulnobj.lastFindTime = lastFindTime
                hostvulnobj.vulnExplain = vulnExplain
                hostvulnobj.vulnStatus = vulnStatus
                hostvulnobj.repairCommand = repairCommand
                hostvulnobj.CVEID = CVEID
                hostvulnobj.label = label
                hostvulnobj.save()
            else:
                print("更新漏洞: ", vulnName, assetPublicIP, assetId)
                hostvulnobj.update(urgent=urgent
                                   ,assetPrivateIP=assetPrivateIP
                                   ,assetRemarks=assetRemarks
                                   ,firstFindTime=firstFindTime
                                   ,lastFindTime=lastFindTime
                                   ,vulnExplain=vulnExplain
                                   ,vulnStatus=vulnStatus
                                   ,repairCommand=repairCommand
                                   ,CVEID=CVEID
                                   ,label=label)


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
def addHostVulnsubmit(request):
    try:
        # print(request.POST)
        # print(dict(request.POST).keys())

        if request.POST.get('HostVuln') == "":
            result = "项目名禁止为空"
            print("[ log ] -> ", result)

            return JsonResponse(result, safe=False)

        if HostVulnManage.objects.filter(HostVuln__iexact=request.POST.get('HostVuln').replace(" ", "")):
            result = "该项目名已存在"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        hostvulnobj = HostVulnManage()
        hostvulnobj.HostVuln = request.POST.get('HostVuln')
        hostvulnobj.hostvulnDesc = request.POST.get('hostvulnDesc')
        hostvulnobj.businessPeople = request.POST.get('businessPeople')
        hostvulnobj.businessPhone = request.POST.get('businessPhone')
        hostvulnobj.developPeople = request.POST.get('developPeople')
        hostvulnobj.developPhone = request.POST.get('developPhone')
        hostvulnobj.developmentCompany = request.POST.get('developmentCompany')
        hostvulnobj.common = request.POST.get('common')
        hostvulnobj.createTime = datetime.datetime.now()
        hostvulnobj.updateTime = datetime.datetime.now()
        hostvulnobj.createPeople = request.user

        hostvulnobj.save()

        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def editHostVulnsubmit(request):
    try:
        # print(request.POST.dict())
        HostVuln = request.POST.get('HostVuln')
        hostvulnDesc = request.POST.get('hostvulnDesc')

        obj1 = HostVulnManage.objects.filter(HostVuln=HostVuln, hostvulnDesc=hostvulnDesc)
        if obj1:
            obj1.update(
                HostVuln=request.POST.get('HostVuln'),
                hostvulnDesc=request.POST.get('hostvulnDesc'),
                businessPeople=request.POST.get('businessPeople'),
                businessPhone=request.POST.get('businessPhone'),
                developPeople=request.POST.get('developPeople'),
                developPhone=request.POST.get('developPhone'),
                developmentCompany=request.POST.get('developmentCompany'),
                common=request.POST.get('common'),
                updateTime=datetime.datetime.now()
            )
            result = "success"

        else:
            result = "该资产不存在,无法修改</br>提示 :禁止对系统名进行编辑"
    except Exception as e:
        print(str(e))
        result = "failed"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deleteHostVulnall(request):
    try:
        HostVulnManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def searchHostVuln(request):
    # print(request.GET)

    vulnName = request.GET.get('vulnName', None).strip(" ")
    urgent = request.GET.get('urgent', None).strip(" ")
    assetId = request.GET.get('assetId', None).strip(" ")
    assetPublicIP = request.GET.get('assetPublicIP', None).strip(" ")
    CVEID = request.GET.get('CVEID', None).strip(" ")

    # 方法一：
    hostvulnobj = HostVulnManage.objects.all()

    if vulnName:
        hostvulnobj = hostvulnobj.filter(vulnName__icontains=vulnName)
    if urgent:
        hostvulnobj = hostvulnobj.filter(urgent__icontains=urgent)
    if assetId:
        hostvulnobj = hostvulnobj.filter(assetId__icontains=assetId)
    if assetPublicIP:
        hostvulnobj = hostvulnobj.filter(assetPublicIP__iexact=assetPublicIP)
    if CVEID:
        hostvulnobj = hostvulnobj.filter(CVEID__icontains=CVEID)


    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)



    total = hostvulnobj.count()
    print("total:", total)
    list1 = []
    for hostvuln in hostvulnobj:
        dict = {}
        dict['vulnName'] = hostvuln.vulnName
        dict['urgent'] = hostvuln.urgent
        dict['assetId'] = hostvuln.assetId
        dict['assetPublicIP'] = hostvuln.assetPublicIP
        dict['assetPrivateIP'] = hostvuln.assetPrivateIP
        dict['assetRemarks'] = hostvuln.assetRemarks
        dict['firstFindTime'] = hostvuln.firstFindTime
        dict['lastFindTime'] = hostvuln.lastFindTime
        dict['vulnExplain'] = hostvuln.vulnExplain
        dict['vulnStatus'] = hostvuln.vulnStatus
        dict['repairCommand'] = hostvuln.repairCommand
        dict['CVEID'] = hostvuln.CVEID
        dict['label'] = hostvuln.label

        

        list1.append(dict)

    try:
        # list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
        list1.sort(key=lambda k: (k.get('firstFindTime')), reverse=False)
    except TypeError as e:
        pass
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
def deleteHostVulnforline(request):
    try:
        if request.POST:
            delete = request.POST.get('delete')
            vulnName = request.POST.get('vulnName')
            assetId = request.POST.get('assetId')
            assetPublicIP = request.POST.get('assetPublicIP')
            assetRemarks = request.POST.get('assetRemarks')

            if delete == "yes":
                print(assetPublicIP, assetId, assetRemarks, vulnName)
                HostVulnManage.objects.filter(vulnName__iexact=vulnName
                                              ,assetId__iexact=assetId
                                              ,assetPublicIP__iexact=assetPublicIP
                                              ,assetRemarks__iexact=assetRemarks
                                              ).delete()
                result = "success"
                print(result)
            else:
                result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        print(str(e))
        return JsonResponse(str(e), safe=False)


@login_required
@csrf_exempt
def downloadHostVulnTemplateFile(request):
    file = open('static/upload/HostVulnManage/HostVulnTemplate.xlsx', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = '.xlsx,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="HostVulnTemplate_%s.xlsx"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response


@login_required
@csrf_exempt
def downloadHostVulnAllToFile(request):

    filepath = os.path.join(settings.UPLOAD_DIR, "HostVulnManage/HostVulnAssetAll.xlsx")
    # print(filepath)

    dirpath = os.path.join(settings.UPLOAD_DIR, "HostVulnManage/bak/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if os.path.exists(filepath):
        new_filepath = dirpath + "HostVulnAssetAll_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xlsx"
        # print(filepath)
        # print(new_filepath)
        shutil.move(filepath, new_filepath)
        # os.rename(filepath, new_filepath)
        # print("ok")

    hostvulnobj = HostVulnManage.objects.all()


    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    dataSheet = workbook.add_sheet('hostVulnAll', cell_overwrite_ok=True)

    #生成第一行
    row0 = ["漏洞名称", "修复紧急度", "影响资产ID ", "影响资产IP（公网）", "影响资产IP（私网）", "影响资产备注名称", "首次发现时间", "最近一次发现时间", "漏洞说明", "漏洞状态", "修复命令", "CVE编号", "标签", "domain", "systemName", "projectName", "description", "slbIp", "businessPeople", "DevelopPeople", "businessPeople", "developPeople", "common"]

    for i in range(0, len(row0)):
        dataSheet.write(0, i, row0[i])

    rownum = 0

    for hostvuln in hostvulnobj:
        rownum = rownum + 1
        print("rownum: ", rownum)
        dataSheet.write(rownum, 0, hostvuln.vulnName)
        dataSheet.write(rownum, 1, hostvuln.urgent)
        dataSheet.write(rownum, 2, hostvuln.assetId)
        dataSheet.write(rownum, 3, hostvuln.assetPublicIP)
        dataSheet.write(rownum, 4, hostvuln.assetPrivateIP)
        dataSheet.write(rownum, 5, hostvuln.assetRemarks)
        dataSheet.write(rownum, 6, str(hostvuln.firstFindTime))
        dataSheet.write(rownum, 7, str(hostvuln.lastFindTime))
        dataSheet.write(rownum, 8, hostvuln.vulnExplain)
        dataSheet.write(rownum, 9, hostvuln.vulnStatus)
        dataSheet.write(rownum, 10, hostvuln.repairCommand)
        dataSheet.write(rownum, 11, hostvuln.CVEID)
        dataSheet.write(rownum, 12, hostvuln.label)


        # 关联ECS管理
        v2ecsobj = V2ECSManage.objects.filter(privateIpAddress__iexact=hostvuln.assetPublicIP)
        if not v2ecsobj:
            v2ecsobj = V2ECSManage.objects.filter(privateIpAddress__iexact=hostvuln.assetPrivateIP)
        for v2ecs in v2ecsobj:
            # print(v2ecs.domain)
            dataSheet.write(rownum, 13, v2ecs.domain)
            dataSheet.write(rownum, 14, v2ecs.systemName)
            dataSheet.write(rownum, 15, v2ecs.projectName)
            dataSheet.write(rownum, 16, v2ecs.description)
            dataSheet.write(rownum, 17, v2ecs.slbIp)
            dataSheet.write(rownum, 18, v2ecs.businessPeople)
            dataSheet.write(rownum, 19, v2ecs.DevelopPeople)


            # 关联项目名管理
            if v2ecs.description and v2ecs.projectName:
                projectobj = ProjectNameManage.objects.filter(projectName__iexact=v2ecs.projectName
                ,projectDesc__iexact=v2ecs.description)
                if projectobj:
                    for project in projectobj:
                        print(project.businessPeople)
                        print(project.developPeople)
                        print(project.common)
                        dataSheet.write(rownum, 20, v2ecs.businessPeople)
                        dataSheet.write(rownum, 21, v2ecs.developPeople)
                        dataSheet.write(rownum, 22, v2ecs.common)

    # print(rownum)
    workbook.save(filepath)

    file = open(filepath, 'rb')

    response = FileResponse(file)
    response['Content-Type'] = '.xlsx,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="HostVulnAssetAll_%s.xlsx"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response





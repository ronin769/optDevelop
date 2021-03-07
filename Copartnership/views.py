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
    return render(request, 'Copartnership/copartnership.html')


@login_required
def copartnershipManage(request):
    return render(request, 'Copartnership/copartnership.html')


@login_required
def addCopartnershippage(request):
    return render(request, 'Copartnership/addcopartnership.html')




@login_required
@csrf_exempt
def getCopartnershiplist(request):
    copartnershipobj = CopartnershipManage.objects.all()

    # total = shipManage.objects.filter(systemStatus__contains="使用中").count()
    total = 0
    resultdict = {}
    list1 = []
    for ship in copartnershipobj:
        # print("--")
        total = total + 1
        dict = {}

        dict['companyName'] = ship.companyName
        dict['systemName'] = ship.systemName
        dict['IP'] = ship.IP
        dict['domain'] = ship.domain
        dict['portService'] = ship.portService
        dict['information'] = ship.information
        dict['isdesensitization'] = ship.isdesensitization
        dict['securityPeopleNum'] = ship.securityPeopleNum
        dict['testCycle'] = ship.testCycle
        dict['userSize'] = ship.userSize
        dict['systemSize'] = ship.systemSize
        dict['deployPoint'] = ship.deployPoint
        dict['securityTest'] = ship.securityTest
        dict['testResult'] = ship.testResult
        dict['systemType'] = ship.systemType
        dict['defensivePower'] = ship.defensivePower
        dict['systemStatus'] = ship.systemStatus
        dict['accessURL'] = ship.accessURL
        dict['developmentCompany'] = ship.developmentCompany
        dict['extranetAccess'] = ship.extranetAccess
        dict['businessPeople'] = ship.businessPeople
        dict['businessPhone'] = ship.businessPhone
        dict['DevelopPeople'] = ship.DevelopPeople
        dict['DevelopPhone'] = ship.DevelopPhone
        dict['systemCommon'] = ship.systemCommon
        dict['systemDescribe'] = ship.systemDescribe
        dict['deployTime'] = ship.deployTime
        dict['createTime'] = ship.createTime
        dict['updateTime'] = ship.updateTime
        dict['createPeople'] = ship.createPeople
        dict['systemUsername'] = ship.systemUsername
        dict['systemPassword'] = ship.systemPassword


        list1.append(dict)


    try:
        # list1.sort(key=lambda k: (k.get('CreateTime')), reverse=False)
        list1.sort(key=lambda k: (k.get('companyName')), reverse=False)
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
def uploadCopartnershipfile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "CopartnershipManage/copartnershipAsset.xls")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "CopartnershipManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "CopartnershipManage/bak/copartnershipAsset%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")

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
def initshipfile(request):
    try:

        CopartnershipManage.objects.all().delete()

        path = 'static/upload/CopartnershipManage/shipAsset.xls'
        workbook = xlrd.open_workbook(path)  # 打开execl

        # 输出Excel文件中所有sheet的名字
        # print(workbook.sheet_names())
        # 根据sheet索引或者名称获取sheet内容
        shipSheet = workbook.sheets()[0]  # 通过索引获取
        # vulnSheet = workbook.sheet_by_index(0)  # 通过索引获取
        # vulnSheet = workbook.sheet_by_name('ECS')  # 通过名称获取
        # print(vulnSheet.name)  # 获取sheet名称
        rowNum = shipSheet.nrows  # sheet行数
        # colNum = shipSheet.ncols  # sheet列数

        firstLineValue = ['公司名称', '系统名称', 'IP地址', '域名', '端口及服务', '敏感信息', '是否脱敏', '安全人数', '检查周期', '用户规模', '系统规模', '部署位置', '安全测评', '测评结果', '系统类型', '安全防御能力', '系统状态', '访问URL', '开发单位', '外网访问', '业务联系人', '业务联系方式', '开发联系人', '开发联系方式', '备注', '系统简介', '部署时间', '创建时间', '修改时间', '创建人', '账号', '密码']


        print(firstLineValue)
        print(shipSheet.row_values(0))


        if shipSheet.row_values(0) != firstLineValue:
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
            companyName = str((shipSheet.cell_value(row, 9)))
            systemName = str((shipSheet.cell_value(row, 9)))
            IP = str((shipSheet.cell_value(row, 9)))
            domain = str((shipSheet.cell_value(row, 9)))
            portService = str((shipSheet.cell_value(row, 9)))
            information = str((shipSheet.cell_value(row, 9)))
            isdesensitization = str((shipSheet.cell_value(row, 9)))
            securityPeopleNum = str((shipSheet.cell_value(row, 9)))
            testCycle = str((shipSheet.cell_value(row, 9)))
            userSize = str((shipSheet.cell_value(row, 9)))
            systemSize = str((shipSheet.cell_value(row, 9)))
            deployPoint = str((shipSheet.cell_value(row, 9)))
            securityTest = str((shipSheet.cell_value(row, 9)))
            testResult = str((shipSheet.cell_value(row, 9)))
            systemType = str((shipSheet.cell_value(row, 9)))
            defensivePower = str((shipSheet.cell_value(row, 9)))
            systemStatus = str((shipSheet.cell_value(row, 9)))
            accessURL = str((shipSheet.cell_value(row, 9)))
            developmentCompany = str((shipSheet.cell_value(row, 9)))
            extranetAccess = str((shipSheet.cell_value(row, 9)))
            businessPeople = str((shipSheet.cell_value(row, 9)))
            businessPhone = str((shipSheet.cell_value(row, 9)))
            DevelopPeople = str((shipSheet.cell_value(row, 9)))
            DevelopPhone = str((shipSheet.cell_value(row, 9)))
            systemCommon = str((shipSheet.cell_value(row, 9)))
            systemDescribe = str((shipSheet.cell_value(row, 9)))
            deployTime = str((shipSheet.cell_value(row, 9)))
            createTime = str((shipSheet.cell_value(row, 9)))
            updateTime = str((shipSheet.cell_value(row, 9)))
            createPeople = str((shipSheet.cell_value(row, 9)))
            systemUsername = str((shipSheet.cell_value(row, 9)))
            systemPassword = str((shipSheet.cell_value(row, 9)))

            # for j in range(colNum):
            #     # # 获取单元格内容为日期的数据
            #     # date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(i, j), workbook.datemode)
            #     # print(date_value)
            #     print(ecsSheet.cell_value(row, j))
            #     # print(list[i][j], '\t\t', end="")
            #
            # ecsIPS = re.compile(r'((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)')

            copartnershipobj = CopartnershipManage()
            copartnershipobj.companyName = companyName
            copartnershipobj.systemName = systemName
            copartnershipobj.IP = IP
            copartnershipobj.domain = domain
            copartnershipobj.portService = portService
            copartnershipobj.information = information
            copartnershipobj.isdesensitization = isdesensitization
            copartnershipobj.securityPeopleNum = securityPeopleNum
            copartnershipobj.testCycle = testCycle
            copartnershipobj.userSize = userSize
            copartnershipobj.systemSize = systemSize
            copartnershipobj.deployPoint = deployPoint
            copartnershipobj.securityTest = securityTest
            copartnershipobj.testResult = testResult
            copartnershipobj.systemType = systemType
            copartnershipobj.defensivePower = defensivePower
            copartnershipobj.systemStatus = systemStatus
            copartnershipobj.accessURL = accessURL
            copartnershipobj.developmentCompany = developmentCompany
            copartnershipobj.extranetAccess = extranetAccess
            copartnershipobj.businessPeople = businessPeople
            copartnershipobj.businessPhone = businessPhone
            copartnershipobj.DevelopPeople = DevelopPeople
            copartnershipobj.DevelopPhone = DevelopPhone
            copartnershipobj.systemCommon = systemCommon
            copartnershipobj.systemDescribe = systemDescribe
            copartnershipobj.deployTime = deployTime
            copartnershipobj.createTime = createTime
            copartnershipobj.updateTime = updateTime
            copartnershipobj.createPeople = createPeople
            copartnershipobj.systemUsername = systemUsername
            copartnershipobj.systemPassword = systemPassword

            copartnershipobj.save()

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
def addcopartnershipsubmit(request):
    try:
        print(request.POST)
        print(dict(request.POST).keys())

        if request.POST.get('systemName') == "":
            result = "系统名禁止为空"
            print("[ log ] -> ", result)

            return JsonResponse(result, safe=False)

        if CopartnershipManage.objects.filter(systemName__iexact=request.POST.get('systemName').replace(" ", "")):
            result = "该系统名已存在"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        copartnershipobj = CopartnershipManage()

        copartnershipobj.companyName = request.POST.get('companyName')
        copartnershipobj.systemName = request.POST.get('systemName')
        copartnershipobj.IP = request.POST.get('IP')
        copartnershipobj.domain = request.POST.get('domain')
        copartnershipobj.portService = request.POST.get('portService')
        copartnershipobj.information = request.POST.get('information')
        copartnershipobj.securityPeopleNum = request.POST.get('securityPeopleNum')
        copartnershipobj.testCycle = request.POST.get('testCycle')
        copartnershipobj.userSize = request.POST.get('userSize')
        copartnershipobj.systemSize = request.POST.get('systemSize')
        copartnershipobj.deployPoint = request.POST.get('deployPoint')
        copartnershipobj.securityTest = request.POST.get('securityTest')
        copartnershipobj.testResult = request.POST.get('testResult')
        copartnershipobj.systemType = request.POST.get('systemType')
        copartnershipobj.defensivePower = request.POST.get('defensivePower')
        copartnershipobj.accessURL = request.POST.get('accessURL')
        copartnershipobj.developmentCompany = request.POST.get('developmentCompany')
        copartnershipobj.businessPeople = request.POST.get('businessPeople')
        copartnershipobj.businessPhone = request.POST.get('businessPhone')
        copartnershipobj.DevelopPeople = request.POST.get('DevelopPeople')
        copartnershipobj.DevelopPhone = request.POST.get('DevelopPhone')
        copartnershipobj.systemCommon = request.POST.get('systemCommon')
        copartnershipobj.systemDescribe = request.POST.get('systemDescribe')
        copartnershipobj.deployTime = request.POST.get('deployTime')
        copartnershipobj.systemUsername = request.POST.get('systemUsername')
        copartnershipobj.systemPassword = request.POST.get('systemPassword')



        if request.POST.get('systemStatus') == "true":
            copartnershipobj.systemStatus = "使用中"
        elif request.POST.get('systemStatus') == "false":
            copartnershipobj.systemStatus = "已下线"


        if request.POST.get('extranetAccess') == "true":
            copartnershipobj.extranetAccess = "开放访问"
        elif request.POST.get('extranetAccess') == "false":
            copartnershipobj.extranetAccess = "本地访问"


        if request.POST.get('isdesensitization') == "true":
            copartnershipobj.extranetAccess = "已脱敏"
        elif request.POST.get('isdesensitization') == "false":
            copartnershipobj.extranetAccess = "未脱敏"




        copartnershipobj.CreateTime = datetime.datetime.now()
        copartnershipobj.updateTime = datetime.datetime.now()
        copartnershipobj.CreatePeople = request.user


        copartnershipobj.save()

        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def editCopartnershipsubmit(request):
    # try:
    print(request.POST)
    companyName = request.POST.get('companyName')
    systemName = request.POST.get('systemName')
    IP = request.POST.get('IP')
    domain = request.POST.get('domain')
    systemType = request.POST.get('systemType')

    obj1 = CopartnershipManage.objects.filter(companyName=companyName
                                              ,systemName=systemName
                                              ,IP=IP
                                              ,domain=domain
                                              ,systemType=systemType
                                              )
    if obj1:

        if request.POST.get('systemStatus') == "true":
            status = "使用中"
        elif request.POST.get('systemStatus') == "false":
            status = "已下线"

        if request.POST.get('extranetAccess') == "true":
            extranetAccess = "开放访问"
        elif request.POST.get('extranetAccess') == "false":
            extranetAccess = "本地访问"

        if request.POST.get('isdesensitization') == "true":
            isdesensitization = "已脱敏"
        elif request.POST.get('isdesensitization') == "false":
            isdesensitization = "未脱敏"




        obj1.update(

            systemStatus=status,
            extranetAccess=extranetAccess,
            isdesensitization=isdesensitization,

            companyName=request.POST.get('companyName'),
            systemName=request.POST.get('systemName'),
            IP=request.POST.get('IP'),
            domain=request.POST.get('domain'),
            portService=request.POST.get('portService'),
            information=request.POST.get('information'),
            securityPeopleNum=request.POST.get('securityPeopleNum'),
            testCycle=request.POST.get('testCycle'),
            userSize=request.POST.get('userSize'),
            systemSize=request.POST.get('systemSize'),
            deployPoint=request.POST.get('deployPoint'),
            securityTest=request.POST.get('securityTest'),
            testResult=request.POST.get('testResult'),
            systemType=request.POST.get('systemType'),
            defensivePower=request.POST.get('defensivePower'),
            accessURL=request.POST.get('accessURL'),
            developmentCompany=request.POST.get('developmentCompany'),
            businessPeople=request.POST.get('businessPeople'),
            businessPhone=request.POST.get('businessPhone'),
            DevelopPeople=request.POST.get('DevelopPeople'),
            DevelopPhone=request.POST.get('DevelopPhone'),
            systemCommon=request.POST.get('systemCommon'),
            systemDescribe=request.POST.get('systemDescribe'),
            deployTime=request.POST.get('deployTime'),
            updateTime=datetime.datetime.now(),
            createPeople=str(request.user),
            systemUsername=request.POST.get('systemUsername'),
            systemPassword=request.POST.get('systemPassword'),
        )



        result = "success"

    else:
        result = "该资产不存在,无法修改</br>提示 :禁止对系统名进行编辑"
    # except Exception as e:
    #     print(str(e))
    #     result = "failed"

    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deleteCopartnershipall(request):
    try:
        CopartnershipManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def searchCopartnership(request):
    # print(request.GET)

    systemName = request.GET.get('systemName', None).strip(" ")
    companyName = request.GET.get('companyName', None).strip(" ")
    IP = request.GET.get('IP', None).strip(" ")
    systemType = request.GET.get('systemType', None).strip(" ")
    domain = request.GET.get('domain', None).strip(" ")

    # 方法一：
    copartnershipobj = CopartnershipManage.objects.all()

    if systemName:
        copartnershipobj = copartnershipobj.filter(systemName__iexact=systemName)
    if companyName:
        copartnershipobj = copartnershipobj.filter(companyName__iexact=companyName)
    if IP:
        copartnershipobj = copartnershipobj.filter(IP__iexact=IP)

    if systemType:
        copartnershipobj = copartnershipobj.filter(systemType__iexact=systemType)
    if domain:
        copartnershipobj = copartnershipobj.filter(domain__iexact=domain)




    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)



    total = copartnershipobj.count()
    print("total:", total)
    list1 = []
    for ship in copartnershipobj:
        dict = {}

        dict['companyName'] = ship.companyName
        dict['systemName'] = ship.systemName
        dict['IP'] = ship.IP
        dict['domain'] = ship.domain
        dict['portService'] = ship.portService
        dict['information'] = ship.information
        dict['isdesensitization'] = ship.isdesensitization
        dict['securityPeopleNum'] = ship.securityPeopleNum
        dict['testCycle'] = ship.testCycle
        dict['userSize'] = ship.userSize
        dict['systemSize'] = ship.systemSize
        dict['deployPoint'] = ship.deployPoint
        dict['securityTest'] = ship.securityTest
        dict['testResult'] = ship.testResult
        dict['systemType'] = ship.systemType
        dict['defensivePower'] = ship.defensivePower
        dict['systemStatus'] = ship.systemStatus
        dict['accessURL'] = ship.accessURL
        dict['developmentCompany'] = ship.developmentCompany
        dict['extranetAccess'] = ship.extranetAccess
        dict['businessPeople'] = ship.businessPeople
        dict['businessPhone'] = ship.businessPhone
        dict['DevelopPeople'] = ship.DevelopPeople
        dict['DevelopPhone'] = ship.DevelopPhone
        dict['systemCommon'] = ship.systemCommon
        dict['systemDescribe'] = ship.systemDescribe
        dict['deployTime'] = ship.deployTime
        dict['createTime'] = ship.createTime
        dict['updateTime'] = ship.updateTime
        dict['createPeople'] = ship.createPeople
        dict['systemUsername'] = ship.systemUsername
        dict['systemPassword'] = ship.systemPassword

        list1.append(dict)

    try:
        # list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
        list1.sort(key=lambda k: (k.get('companyName')), reverse=False)
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
def deleteshipForLine(request):
    try:
        # print(request.POST)
        if request.POST:
            delete = request.POST.get('delete')
            companyName = request.POST.get('companyName')
            systemName = request.POST.get('systemName')
            IP = request.POST.get('IP')
            domain = request.POST.get('domain')
            systemType = request.POST.get('systemType')



            if delete == "yes":
                CopartnershipManage.objects.filter(companyName=companyName
                                                   ,systemName=systemName
                                                   ,domain=domain
                                                   ,IP=IP
                                                   ,systemType=systemType
                                                   ).delete()

                result = "success"
                print(result)

            else:
                result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse(str(e), safe=False)




@login_required
@csrf_exempt
def downloadCopartnershipTemplateFile(request):
    file = open('static/upload/CopartnershipManage/CopartnershipTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="CopartnershipTemplate_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response





@login_required
@csrf_exempt
def downloadCopartnershipAllToFile(request):

    filepath = os.path.join(settings.UPLOAD_DIR, "CopartnershipManage/copartnershipAssetAll.xls")
    # print(filepath)

    dirpath = os.path.join(settings.UPLOAD_DIR, "CopartnershipManage/bak/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if os.path.exists(filepath):
        new_filepath = dirpath + "copartnershipAssetAll_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls"
        # print(filepath)
        # print(new_filepath)
        shutil.move(filepath, new_filepath)
        # os.rename(filepath, new_filepath)
        # print("ok")



    copartnershipobj = CopartnershipManage.objects.all()


    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    shipSheet = workbook.add_sheet('shipAll')

    #生成第一行
    row0 = ['公司名称', '系统名称', 'IP地址', '域名', '端口及服务', '敏感信息', '是否脱敏', '安全人数', '检查周期', '用户规模', '系统规模', '部署位置', '安全测评', '测评结果', '系统类型', '安全防御能力', '系统状态', '访问URL', '开发单位', '外网访问', '业务联系人', '业务联系方式', '开发联系人', '开发联系方式', '备注', '系统简介', '部署时间', '创建时间', '修改时间', '创建人', '账号', '密码']

    for i in range(0, len(row0)):
        shipSheet.write(0, i, row0[i])

    rownum = 0

    for ship in copartnershipobj:
        # if ship.systemStatus == "已下线":
        #     continue
        rownum = rownum + 1

        shipSheet.write(rownum, 0, ship.companyName)
        shipSheet.write(rownum, 1, ship.systemName)
        shipSheet.write(rownum, 2, ship.IP)
        shipSheet.write(rownum, 3, ship.domain)
        shipSheet.write(rownum, 4, ship.portService)
        shipSheet.write(rownum, 5, ship.information)
        shipSheet.write(rownum, 6, ship.isdesensitization)
        shipSheet.write(rownum, 7, ship.securityPeopleNum)
        shipSheet.write(rownum, 8, ship.testCycle)
        shipSheet.write(rownum, 9, ship.userSize)
        shipSheet.write(rownum, 10, ship.systemSize)
        shipSheet.write(rownum, 11, ship.deployPoint)
        shipSheet.write(rownum, 12, ship.securityTest)
        shipSheet.write(rownum, 13, ship.testResult)
        shipSheet.write(rownum, 14, ship.systemType)
        shipSheet.write(rownum, 15, ship.defensivePower)
        shipSheet.write(rownum, 16, ship.systemStatus)
        shipSheet.write(rownum, 17, ship.accessURL)
        shipSheet.write(rownum, 18, ship.developmentCompany)
        shipSheet.write(rownum, 19, ship.extranetAccess)
        shipSheet.write(rownum, 20, ship.businessPeople)
        shipSheet.write(rownum, 21, ship.businessPhone)
        shipSheet.write(rownum, 22, ship.DevelopPeople)
        shipSheet.write(rownum, 23, ship.DevelopPhone)
        shipSheet.write(rownum, 24, ship.systemCommon)
        shipSheet.write(rownum, 25, ship.systemDescribe)
        shipSheet.write(rownum, 26, ship.deployTime)
        shipSheet.write(rownum, 27, str(ship.createTime))
        shipSheet.write(rownum, 28, str(ship.updateTime))
        shipSheet.write(rownum, 29, ship.createPeople)
        shipSheet.write(rownum, 30, ship.systemUsername)
        shipSheet.write(rownum, 31, ship.systemPassword)

        # print(rownum)

    workbook.save(filepath)


    file = open(filepath, 'rb')


    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="copartnershipAssetAll__%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response





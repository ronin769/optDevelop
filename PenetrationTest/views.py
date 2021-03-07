# codding = utf8

import datetime
import shutil
import xml
import time

import xlwt as xlwt
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


def index(request):
    return render(request, 'PenetrationTest/overhaul.html')



def overhaulManage(request):
    return render(request, 'PenetrationTest/overhaul.html')



def troubleManage(request):
    return render(request, 'PenetrationTest/trouble.html')



def supervisionManage(request):
    return render(request, 'PenetrationTest/supervision.html')



@login_required
def addoverhauldata(request):
    return render(request, 'PenetrationTest/addoverhaul.html')





@csrf_exempt
@login_required
def getoverhaullist(request):
    trialobj = PenetrationTestOverhaulManage.objects.all()

    total = trialobj.count()
    resultdict = {}
    list1 = []
    for trial in trialobj:
        dict = {}
        dict['overhaulId'] = trial.overhaulId
        dict['testStyle'] = trial.testStyle
        dict['systemName'] = trial.systemName
        dict['systemVersion'] = trial.systemVersion
        dict['functionNum'] = trial.functionNum
        dict['vulnNum'] = trial.vulnNum
        dict['vulnDetail'] = trial.vulnDetail
        dict['functionList'] = trial.functionList
        dict['overhaulContent'] = trial.overhaulContent
        dict['developCompany'] = trial.developCompany
        dict['applyName'] = trial.applyName
        dict['applyPhone'] = trial.applyPhone
        dict['projectBossName'] = trial.projectBossName
        dict['projectBossPhone'] = trial.projectBossPhone
        dict['functionTestName'] = trial.functionTestName
        dict['PenetrationTestName'] = trial.PenetrationTestName
        dict['testUserName'] = trial.testUserName
        dict['testPassword'] = trial.testPassword
        dict['testURL'] = trial.testURL
        dict['functionReportPath'] = trial.functionReportPath
        dict['reportPath'] = trial.reportPath
        dict['recordPath'] = trial.recordPath
        dict['functionReportIsExist'] = trial.functionReportIsExist
        dict['reportIsExist'] = trial.reportIsExist
        dict['recordIsExist'] = trial.recordIsExist
        dict['testIsOK'] = trial.testIsOK
        dict['applyTime'] = trial.applyTime
        dict['testTime'] = trial.testTime
        dict['releaseTime'] = trial.releaseTime
        dict['createTime'] = trial.createTime
        dict['updateTime'] = trial.updateTime
        dict['updatePeople'] = trial.updatePeople
        list1.append(dict)


    print(list1)

    try:
        list1.sort(key=lambda k: (k.get('overhaulId')), reverse=True)
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
def searchoverhaulsubmit(request):



    searchoverhaulIdId = request.GET.get('searchoverhaulIdId', None)
    searchtestStyleId = request.GET.get('searchtestStyleId', None)
    searchsystemNameId = request.GET.get('searchsystemNameId', None)
    searchPenetrationTestNameId = request.GET.get('searchPenetrationTestNameId', None)
    searchapplyNameId = request.GET.get('searchapplyNameId', None)
    searchprojectBossNameId = request.GET.get('searchprojectBossNameId', None)

    # 方法一：
    penetrationTestobj = PenetrationTestOverhaulManage.objects.all()

    if searchoverhaulIdId:
        penetrationTestobj = penetrationTestobj.filter(overhaulId__iexact=searchoverhaulIdId)
    if searchtestStyleId:
        penetrationTestobj = penetrationTestobj.filter(testStyle__iexact=searchtestStyleId)
    if searchsystemNameId:
        penetrationTestobj = penetrationTestobj.filter(systemName__iexact=searchsystemNameId)
    if searchPenetrationTestNameId:
        penetrationTestobj = penetrationTestobj.filter(PenetrationTestName__iexact=searchPenetrationTestNameId)
    if searchapplyNameId:
        penetrationTestobj = penetrationTestobj.filter(applyName__iexact=searchapplyNameId)
    if searchprojectBossNameId:
        penetrationTestobj = penetrationTestobj.filter(projectBossName__iexact=searchprojectBossNameId)


    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = penetrationTestobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for trial in penetrationTestobj:
        dict = {}

        dict['overhaulId'] = trial.overhaulId
        dict['testStyle'] = trial.testStyle
        dict['systemName'] = trial.systemName
        dict['systemVersion'] = trial.systemVersion
        dict['functionNum'] = trial.functionNum
        dict['functionList'] = trial.functionList
        dict['vulnNum'] = trial.vulnNum
        dict['vulnDetail'] = trial.vulnDetail
        dict['overhaulContent'] = trial.overhaulContent
        dict['developCompany'] = trial.developCompany
        dict['applyName'] = trial.applyName
        dict['applyPhone'] = trial.applyPhone
        dict['projectBossName'] = trial.projectBossName
        dict['projectBossPhone'] = trial.projectBossPhone
        dict['functionTestName'] = trial.functionTestName
        dict['PenetrationTestName'] = trial.PenetrationTestName
        dict['testUserName'] = trial.testUserName
        dict['testPassword'] = trial.testPassword
        dict['testURL'] = trial.testURL
        dict['functionReportPath'] = trial.functionReportPath
        dict['reportPath'] = trial.reportPath
        dict['recordPath'] = trial.recordPath
        dict['functionReportIsExist'] = trial.functionReportIsExist
        dict['reportIsExist'] = trial.reportIsExist
        dict['recordIsExist'] = trial.recordIsExist
        dict['testIsOK'] = trial.testIsOK
        dict['applyTime'] = trial.applyTime
        dict['testTime'] = trial.testTime
        dict['releaseTime'] = trial.releaseTime
        dict['createTime'] = trial.createTime
        dict['updateTime'] = trial.updateTime
        dict['updatePeople'] = trial.updatePeople


        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('overhaulId')), reverse=True)
    except TypeError as e:
        pass

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
def addOverhaulSubmit(request):
    # print(request.POST)
    print("-------------------")
    print(request.POST.dict())
    #
    overhaulId = request.POST.get('overhaulId')


    # 编号是必填值,不允许为空
    if overhaulId == "":
        result = "渗透编号禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    # 编号必须为整数
    if not overhaulId.isdigit():
        result = "渗透编号必须是数字"
        print("[ log ] -> ", result)
        if not isinstance(overhaulId, int):
            result = "渗透编号必须为整数"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)



    # 功能个数必须为整数
    if not request.POST.get('functionNum').isdigit():
        result = "功能个数必须是数字"
        print("[ log ] -> ", result)
        if not isinstance(request.POST.get('functionNum'), int):
            result = "功能个数必须为整数"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)



    # 编号不存在
    if not PenetrationTestOverhaulManage.objects.filter(overhaulId__iexact=overhaulId).exists():

        penetrationTestobj = PenetrationTestOverhaulManage()

        penetrationTestobj.overhaulId = request.POST.get('overhaulId')
        penetrationTestobj.functionNum = request.POST.get('functionNum')
        penetrationTestobj.vulnNum = request.POST.get('vulnNum')
        penetrationTestobj.vulnDetail = request.POST.get('vulnDetail')
        penetrationTestobj.testStyle = request.POST.get('testStyle')
        penetrationTestobj.systemName = request.POST.get('systemName')
        penetrationTestobj.systemVersion = request.POST.get('systemVersion')
        penetrationTestobj.releaseTime = request.POST.get('releaseTime')
        penetrationTestobj.applyName = request.POST.get('applyName')
        penetrationTestobj.applyPhone = request.POST.get('applyPhone')
        penetrationTestobj.applyTime = request.POST.get('applyTime')
        penetrationTestobj.projectBossName = request.POST.get('projectBossName')
        penetrationTestobj.projectBossPhone = request.POST.get('projectBossPhone')
        penetrationTestobj.testTime = request.POST.get('testTime')
        penetrationTestobj.functionTestName = request.POST.get('functionTestName')
        penetrationTestobj.PenetrationTestName = request.POST.get('PenetrationTestName')
        penetrationTestobj.developCompany = request.POST.get('developCompany')
        penetrationTestobj.testUserName = request.POST.get('testUserName')
        penetrationTestobj.testPassword = request.POST.get('testPassword')
        penetrationTestobj.testURL = request.POST.get('testURL')
        penetrationTestobj.overhaulContent = request.POST.get('overhaulContent')

        penetrationTestobj.createTime = datetime.datetime.now()
        penetrationTestobj.updateTime = datetime.datetime.now()

        if not request.POST.get('releaseTime'):
            penetrationTestobj.releaseTime = datetime.datetime.now().strftime('%Y-%m-%d')
        if not request.POST.get('applyTime'):
            penetrationTestobj.applyTime = datetime.datetime.now().strftime('%Y-%m-%d')
        if not request.POST.get('testTime'):
            penetrationTestobj.testTime = datetime.datetime.now().strftime('%Y-%m-%d')



        if request.POST.get('functionReportIsExist'):
            penetrationTestobj.functionReportIsExist = "on"
        else:
            penetrationTestobj.reportIsExist = "off"

        if request.POST.get('reportIsExist'):
            penetrationTestobj.reportIsExist = "on"
        else:
            penetrationTestobj.reportIsExist = "off"

        if request.POST.get('recordIsExist'):
            penetrationTestobj.recordIsExist = "on"
        else:
            penetrationTestobj.recordIsExist = "off"

        if request.POST.get('testIsOK'):
            penetrationTestobj.testIsOK = "on"
        else:
            penetrationTestobj.testIsOK = "off"


        penetrationTestobj.save()


        result = "success"
        return JsonResponse(result, safe=False)

    # 编号存在
    else:
        result = "编号已存在"

        # except Exception as e:
        # print(str(e))
        # result = "failed"

    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def editOverhaulSubmit(request):
    try:
        # print(request.POST)
        print("----------/**********************---------")
        print(request.POST.dict())
        print(request.POST.dict().keys())
        overhaulId = request.POST.get('overhaulId')
        print([overhaulId])


        # 编号是必填值,不允许为空
        if overhaulId == "":
            result = "渗透测试编号禁止为空"
            return JsonResponse(result, safe=False)

        # 编号必须为整数
        if not overhaulId.isdigit():
            result = "渗透测试编号必须是数字"
            if not isinstance(overhaulId, int):
                result = "渗透测试编号必须为整数"
                return JsonResponse(result, safe=False)


        # 功能个数必须为整数
        if not request.POST.get('functionNum').isdigit():
            result = "功能个数必须是数字"
            if not isinstance(request.POST.get('functionNum'), int):
                result = "功能个数必须为整数"
            return JsonResponse(result, safe=False)

        # PenetrationTestOverhaulManage.objects.filter(overhaulId__iexact=overhaulId).delete()

        # print(PenetrationTestOverhaulManage.objects.filter(overhaulId__iexact=overhaulId).exists())
        # print("++++++++++++++++++++++")

        # 编号存在
        if PenetrationTestOverhaulManage.objects.filter(overhaulId__iexact=overhaulId).exists():


            if request.POST.get('reportIsExist'):
                reportIsExist = "on"
            else:
                reportIsExist = "off"

            if request.POST.get('recordIsExist'):
                recordIsExist = "on"
            else:
                recordIsExist = "off"

            if request.POST.get('testIsOK'):
                testIsOK = "on"
            else:
                testIsOK = "off"

            PenetrationTestOverhaulManage.objects.filter(overhaulId__iexact=overhaulId).update(
                functionNum=request.POST.get('functionNum'),
                testStyle=request.POST.get('testStyle'),
                releaseTime=request.POST.get('releaseTime'),
                systemName=request.POST.get('systemName'),
                systemVersion=request.POST.get('systemVersion'),
                applyName=request.POST.get('applyName'),
                applyPhone=request.POST.get('applyPhone'),
                projectBossName=request.POST.get('projectBossName'),
                projectBossPhone=request.POST.get('projectBossPhone'),
                functionTestName=request.POST.get('functionTestName'),
                PenetrationTestName=request.POST.get('PenetrationTestName'),
                testUserName=request.POST.get('testUserName'),
                testPassword=request.POST.get('testPassword'),
                testURL=request.POST.get('testURL'),
                developCompany=request.POST.get('developCompany'),
                applyTime=request.POST.get('applyTime'),
                testTime=request.POST.get('testTime'),
                overhaulContent=request.POST.get('overhaulContent'),
                reportIsExist=reportIsExist,
                recordIsExist=recordIsExist,
                testIsOK=testIsOK,
                updateTime=datetime.datetime.now()
            )



            result = "success"
            return JsonResponse(result, safe=False)

        # 编号不存在
        else:
            result = "渗透标号编号不存在"
            print("[ log ] -> ", result)

    except Exception as e:
        print(str(e))
        result = "failed"

    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def uploadFunctionReportFile(request):
    print(request.FILES)
    print(request.POST)

    textFile = request.FILES['file']
    overhaulId = request.POST.get('overhaulId')  # 编号

    if request.method != 'POST':
        resultdict = {"code": "1", "msg": "请求方式不正确"}
        return JsonResponse(resultdict)
    if overhaulId == "":
        resultdict = {"code": "1", "msg": "编号禁止为空"}
        return JsonResponse(resultdict)
    # if not re.search("doc", os.path.splitext(textFile.name)[1], re.IGNORECASE):
    #     resultdict = {"code": "1", "msg": "文件类型(后缀名)不正确, 仅支持.doc/.docx"}
    #     return JsonResponse(resultdict)



    filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/功能报告/" + textFile.name)
    dirpath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/功能报告/")
    savefilepath = filepath.split("PenetrationTestOverhaulManage")[1]  # APP防护方案大纲.docx
    # savefilepath = filepath.split("optDevelop")[1]  # /static/upload/PenetrationTestOverhaulManage/测试报告/APP防护方案大纲.docx

    # 存入文件
    if os.path.exists(filepath):  # 文件已存在,创建新路径,备份
        new_filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/bak/功能报告/" + os.path.splitext(textFile.name)[
            0] + "_" + time.strftime('%Y_%b_%d-%H_%M_%S') + "." + os.path.splitext(textFile.name)[1])
        new_dirpath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/bak/功能报告/")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        shutil.move(filepath, new_filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'wb') as f:
        for text in textFile.chunks():  # 分包写入
            f.write(text)

    try:
        penetrationTestobj = PenetrationTestOverhaulManage.objects.get(overhaulId__iexact=overhaulId)
        penetrationTestobj.functionReportPath = savefilepath
        resultdict = {"code": "0", "msg": "发现存在文件路径并已更新"}

    except PenetrationTestOverhaulManage.DoesNotExist:
        penetrationTestobj = PenetrationTestOverhaulManage()
        penetrationTestobj.overhaulId = overhaulId
        penetrationTestobj.functionReportPath = savefilepath
        resultdict = {"code": "0", "msg": "已新增上传路径和编号"}

    penetrationTestobj.updatePeople = str(request.user)
    penetrationTestobj.updateTime = datetime.datetime.now()
    penetrationTestobj.save()

    print(resultdict)

    return JsonResponse(resultdict)



@login_required
@csrf_exempt
def uploadReportFile(request):
    print(request.FILES)
    print(request.POST)

    textFile = request.FILES['file']
    overhaulId = request.POST.get('overhaulId')  # 编号

    if request.method != 'POST':
        resultdict = {"code": "1", "msg": "请求方式不正确"}
        return JsonResponse(resultdict)
    if overhaulId == "":
        resultdict = {"code": "1", "msg": "编号禁止为空"}
        return JsonResponse(resultdict)
    # if not re.search("doc", os.path.splitext(textFile.name)[1], re.IGNORECASE):
    #     resultdict = {"code": "1", "msg": "文件类型(后缀名)不正确, 仅支持.doc/.docx"}
    #     return JsonResponse(resultdict)



    filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/测试报告/" + textFile.name)
    dirpath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/测试报告/")
    savefilepath = filepath.split("PenetrationTestOverhaulManage")[1]  # APP防护方案大纲.docx
    # savefilepath = filepath.split("optDevelop")[1]  # /static/upload/PenetrationTestOverhaulManage/测试报告/APP防护方案大纲.docx

    # 存入文件
    if os.path.exists(filepath):  # 文件已存在,创建新路径,备份
        new_filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/bak/测试报告/" + os.path.splitext(textFile.name)[
            0] + "_" + time.strftime('%Y_%b_%d-%H_%M_%S') + "." + os.path.splitext(textFile.name)[1])
        new_dirpath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/bak/测试报告/")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        shutil.move(filepath, new_filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'wb') as f:
        for text in textFile.chunks():  # 分包写入
            f.write(text)

    try:
        penetrationTestobj = PenetrationTestOverhaulManage.objects.get(overhaulId__iexact=overhaulId)
        penetrationTestobj.reportPath = savefilepath
        resultdict = {"code": "0", "msg": "发现存在文件路径并已更新"}

    except PenetrationTestOverhaulManage.DoesNotExist:
        penetrationTestobj = PenetrationTestOverhaulManage()
        penetrationTestobj.overhaulId = overhaulId
        penetrationTestobj.reportPath = savefilepath
        resultdict = {"code": "0", "msg": "已新增上传路径和编号"}

    penetrationTestobj.updatePeople = str(request.user)
    penetrationTestobj.updateTime = datetime.datetime.now()
    penetrationTestobj.save()

    print(resultdict)

    return JsonResponse(resultdict)




@login_required
@csrf_exempt
def uploadRecordFile(request):
    print(request.FILES)
    print(request.POST)

    textFile = request.FILES['file']
    overhaulId = request.POST.get('overhaulId')  # 编号

    if request.method != 'POST':
        resultdict = {"code": "1", "msg": "请求方式不正确"}
        return JsonResponse(resultdict)
    if overhaulId == "":
        resultdict = {"code": "1", "msg": "编号禁止为空"}
        return JsonResponse(resultdict)
    if not re.search("doc", os.path.splitext(textFile.name)[1], re.IGNORECASE):
        resultdict = {"code": "1", "msg": "文件类型(后缀名)不正确, 仅支持.doc/.docx"}
        return JsonResponse(resultdict)



    filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/测试记录/" + textFile.name)
    dirpath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/测试记录/")
    savefilepath = filepath.split("PenetrationTestOverhaulManage")[1]  # APP防护方案大纲.docx
    # savefilepath = filepath.split("optDevelop")[1]  # /static/upload/PenetrationTestOverhaulManage/测试报告/APP防护方案大纲.docx

    # 存入文件
    if os.path.exists(filepath):  # 文件已存在,创建新路径,备份
        new_filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/bak/测试记录/" + os.path.splitext(textFile.name)[
            0] + "_" + time.strftime('%Y_%b_%d-%H_%M_%S') + "." + os.path.splitext(textFile.name)[1])
        new_dirpath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/bak/测试记录/")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        shutil.move(filepath, new_filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'wb') as f:
        for text in textFile.chunks():  # 分包写入
            f.write(text)

    try:
        penetrationTestobj = PenetrationTestOverhaulManage.objects.get(overhaulId__iexact=overhaulId)
        penetrationTestobj.recordPath = savefilepath
        resultdict = {"code": "0", "msg": "发现存在文件路径并已更新"}

    except PenetrationTestOverhaulManage.DoesNotExist:
        penetrationTestobj = PenetrationTestOverhaulManage()
        penetrationTestobj.overhaulId = overhaulId
        penetrationTestobj.recordPath = savefilepath
        resultdict = {"code": "0", "msg": "已新增上传路径和编号"}

    penetrationTestobj.updatePeople = str(request.user)
    penetrationTestobj.updateTime = datetime.datetime.now()
    penetrationTestobj.save()

    print(resultdict)

    return JsonResponse(resultdict)






@login_required
@csrf_exempt
def editfunctionReportIsExist(request):
    print(request.POST)
    # dict = request.POST.dict()
    # print(dict)
    overhaulId = request.POST.get('overhaulId')  # 编号
    functionReportIsExist = request.POST.get('functionReportIsExist')  # 整改通知单
    print(overhaulId)
    print(functionReportIsExist)

    penetrationTestobj = PenetrationTestOverhaulManage.objects.get(overhaulId__iexact=overhaulId)
    print(penetrationTestobj.functionReportIsExist)
    if functionReportIsExist == "off":
        penetrationTestobj.functionReportIsExist = "on"
    else:
        penetrationTestobj.functionReportIsExist = "off"
    penetrationTestobj.updateTime = datetime.datetime.now()

    print(penetrationTestobj.functionReportIsExist)
    penetrationTestobj.save()

    result = {"status": penetrationTestobj.functionReportIsExist}
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def editreportIsExist(request):
    print(request.POST)
    # dict = request.POST.dict()
    # print(dict)
    overhaulId = request.POST.get('overhaulId')  # 编号
    reportIsExist = request.POST.get('reportIsExist')  # 整改通知单
    print(overhaulId)
    print(reportIsExist)

    penetrationTestobj = PenetrationTestOverhaulManage.objects.get(overhaulId__iexact=overhaulId)
    print(penetrationTestobj.reportIsExist)
    if reportIsExist == "off":
        penetrationTestobj.reportIsExist = "on"
    else:
        penetrationTestobj.reportIsExist = "off"
    penetrationTestobj.updateTime = datetime.datetime.now()

    print(penetrationTestobj.reportIsExist)
    penetrationTestobj.save()

    result = {"status": penetrationTestobj.reportIsExist}
    return JsonResponse(result, safe=False)






@login_required
@csrf_exempt
def editrecordIsExist(request):
    print(request.POST)
    # dict = request.POST.dict()
    # print(dict)
    overhaulId = request.POST.get('overhaulId')  # 编号
    recordIsExist = request.POST.get('recordIsExist')  # 整改通知单
    print(overhaulId)
    print(recordIsExist)

    penetrationTestobj = PenetrationTestOverhaulManage.objects.get(overhaulId__iexact=overhaulId)
    print(penetrationTestobj.recordIsExist)
    if recordIsExist == "off":
        penetrationTestobj.recordIsExist = "on"
    else:
        penetrationTestobj.recordIsExist = "off"
    penetrationTestobj.updateTime = datetime.datetime.now()

    print(penetrationTestobj.recordIsExist)
    penetrationTestobj.save()

    result = {"status": penetrationTestobj.recordIsExist}
    return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def edittestIsOK(request):
    print(request.POST)
    # dict = request.POST.dict()
    # print(dict)
    overhaulId = request.POST.get('overhaulId')  # 编号
    testIsOK = request.POST.get('testIsOK')  # 整改通知单
    print(overhaulId)
    print(testIsOK)

    penetrationTestobj = PenetrationTestOverhaulManage.objects.get(overhaulId__iexact=overhaulId)
    print(penetrationTestobj.testIsOK)
    if testIsOK == "off":
        penetrationTestobj.testIsOK = "on"
    else:
        penetrationTestobj.testIsOK = "off"


    penetrationTestobj.updateTime = datetime.datetime.now()
    print(penetrationTestobj.testIsOK)
    penetrationTestobj.save()

    result = {"status": penetrationTestobj.testIsOK}
    return JsonResponse(result, safe=False)





@login_required
@csrf_exempt
def deleteoverhaulforline(request):
    overhaulId = request.POST.get('overhaulId')  # 编号
    PenetrationTestOverhaulManage.objects.filter(overhaulId__iexact=overhaulId).delete()
    result = "success"
    return JsonResponse(result, safe=False)





@login_required
@csrf_exempt
def downloadOverhaulTemplateFile(request):

    try:
        filePath = "static/upload/PenetrationTestOverhaulManage/overhaulTemplate.xls"
        file = open(filePath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="overhaulTemplate_%s.xls"' % int(time.time())
        return response
    except Exception as e:
        print(str(e))
        resultdict = "模板文件下载失败"
        return JsonResponse(resultdict, safe=False)





@login_required
@csrf_exempt
def uploadoverhaulfile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/overhaul.xls")
        # print(filepath)

        dirpath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "PenetrationTestOverhaulManage/bak/overhaul_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")
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
def initoverhaul(request):
    # try:

    PenetrationTestOverhaulManage.objects.all().delete()

    # 设置路径
    path = 'static/upload/PenetrationTestOverhaulManage/overhaul.xls'

    # 打开execl
    workbook = xlrd.open_workbook(path)

    # 输出Excel文件中所有sheet的名字
    # print(workbook.sheet_names())

    # 根据sheet索引或者名称获取sheet内容
    # overhaulSheet = workbook.sheets()[0]  # 通过索引获取
    overhaulSheet = workbook.sheet_by_index(0)  # 通过索引获取
    # overhaulSheet = workbook.sheet_by_name('ECS')  # 通过名称获取

    # print(overhaulSheet.name)  # 获取sheet名称
    rowNum = overhaulSheet.nrows  # sheet行数
    colNum = overhaulSheet.ncols  # sheet列数

    firstLineValue = ['渗透编号', '测试类型', '系统名称', '系统版本', '功能个数', '功能列表', '漏洞个数', '漏洞描述', '渗透内容', '开发单位', '申请人', '申请人联系方式', '项目经理', '项目经理联系方式', '功能测试联系人', '渗透测试联系人', '测试账号', '测试密码', '测试地址', '测试报告', '测试记录', '功能是否存在', '报告是否存在', '记录是否存在', '是否通过', '申请时间', '测试时间', '计划上线时间', '创建时间', '修改时间']


    if overhaulSheet.row_values(0) != firstLineValue:
        result = "文件列名不正确,请参考模板文件"
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
        #     print(overhaulSheet.cell_value(row, j))
        #     # print(list[i][j], '\t\t', end="")


        overhaulId = str(overhaulSheet.cell_value(row, 0)).replace(".0", "")
        testStyle = overhaulSheet.cell_value(row, 1)
        systemName = overhaulSheet.cell_value(row, 2)
        systemVersion = overhaulSheet.cell_value(row, 3)
        functionNum = str(overhaulSheet.cell_value(row, 4)).replace(".0", "")
        functionList = overhaulSheet.cell_value(row, 5)
        vulnNum = overhaulSheet.cell_value(row, 6).replace(".0", "")
        vulnDetail = overhaulSheet.cell_value(row, 7)
        overhaulContent = overhaulSheet.cell_value(row, 8)
        developCompany = overhaulSheet.cell_value(row, 9)
        applyName = overhaulSheet.cell_value(row, 10)
        applyPhone = str(overhaulSheet.cell_value(row, 11)).replace(".0", "")
        projectBossName = overhaulSheet.cell_value(row, 12)
        projectBossPhone = str(overhaulSheet.cell_value(row, 13)).replace(".0", "")
        functionTestName = overhaulSheet.cell_value(row, 14)
        PenetrationTestName = overhaulSheet.cell_value(row, 15)
        testUserName = overhaulSheet.cell_value(row, 16)
        testPassword = overhaulSheet.cell_value(row, 17)
        testURL = overhaulSheet.cell_value(row, 18)
        reportPath = overhaulSheet.cell_value(row, 19)
        recordPath = overhaulSheet.cell_value(row, 20)
        functionReportIsExist = overhaulSheet.cell_value(row, 21)
        reportIsExist = overhaulSheet.cell_value(row, 22)
        recordIsExist = overhaulSheet.cell_value(row, 23)
        testIsOK = overhaulSheet.cell_value(row, 24)
        applyTime = overhaulSheet.cell_value(row, 25)
        testTime = overhaulSheet.cell_value(row, 26)
        releaseTime = overhaulSheet.cell_value(row, 27)
        createTime = overhaulSheet.cell_value(row, 28)
        updateTime = overhaulSheet.cell_value(row, 29)




        overhaulobj = PenetrationTestOverhaulManage()
        overhaulobj.overhaulId = overhaulId
        overhaulobj.testStyle = testStyle
        overhaulobj.systemName = systemName
        overhaulobj.systemVersion = systemVersion
        overhaulobj.functionNum = functionNum
        overhaulobj.functionList = functionList
        overhaulobj.vulnNum = vulnNum
        overhaulobj.vulnDetail = vulnDetail
        overhaulobj.overhaulContent = overhaulContent
        overhaulobj.developCompany = developCompany
        overhaulobj.applyName = applyName
        overhaulobj.applyPhone = applyPhone
        overhaulobj.projectBossName = projectBossName
        overhaulobj.projectBossPhone = projectBossPhone
        overhaulobj.functionTestName = functionTestName
        overhaulobj.PenetrationTestName = PenetrationTestName
        overhaulobj.testUserName = testUserName
        overhaulobj.testPassword = testPassword
        overhaulobj.testURL = testURL
        overhaulobj.reportPath = reportPath
        overhaulobj.recordPath = recordPath
        overhaulobj.functionReportIsExist = functionReportIsExist
        overhaulobj.reportIsExist = reportIsExist
        overhaulobj.recordIsExist = recordIsExist
        overhaulobj.testIsOK = testIsOK
        overhaulobj.applyTime = applyTime
        overhaulobj.testTime = testTime
        overhaulobj.releaseTime = releaseTime
        overhaulobj.createTime = createTime
        overhaulobj.updateTime = updateTime
        overhaulobj.save()

    print("---------ok---------")
    result = "success"
    # except Exception as e:
    #     print(str(e))
    #     result = "failed"

    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def deleteoverhaulall(request):
    PenetrationTestOverhaulManage.objects.filter().delete()
    result = "success"
    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def downloadOverhaulAllToFile(request):


    filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/overhaulAll.xls")
    # print(filepath)

    dirpath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage/bak/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if os.path.exists(filepath):
        new_filepath = dirpath + "overhaulAll_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls"
        # print(filepath)
        # print(new_filepath)
        shutil.move(filepath, new_filepath)
        # os.rename(filepath, new_filepath)
        # print("ok")



    overhaulobj = PenetrationTestOverhaulManage.objects.all()


    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    overhaulSheet = workbook.add_sheet('overhaulAll')

    #生成第一行
    # row0 = ['编号', '系统名称', '系统版本', '功能个数', '存在报告', '存在记录', '测试通过', '测试报告', '测试记录', '开发单位', '功能列表', '渗透内容', '申请人', '审核人', '操作人', '创建时间', '修改时间']

    row0 = ['渗透编号', '测试类型', '系统名称', '系统版本', '功能个数', '功能列表', '漏洞个数', '漏洞描述', '渗透内容', '开发单位', '申请人', '申请人联系方式', '项目经理', '项目经理联系方式', '功能测试联系人', '渗透测试联系人', '测试账号', '测试密码', '测试地址', '测试报告', '测试记录', '功能是否存在', '报告是否存在', '记录是否存在', '是否通过', '申请时间', '测试时间', '计划上线时间', '创建时间', '修改时间']

    for i in range(0,len(row0)):
        overhaulSheet.write(0, i, row0[i])


    rownum = 0

    for overhaul in overhaulobj:
        rownum = rownum + 1
        overhaulSheet.write(rownum, 0, overhaul.overhaulId)
        overhaulSheet.write(rownum, 1, overhaul.testStyle)
        overhaulSheet.write(rownum, 2, overhaul.systemName)
        overhaulSheet.write(rownum, 3, overhaul.systemVersion)
        overhaulSheet.write(rownum, 4, overhaul.functionNum)
        overhaulSheet.write(rownum, 5, overhaul.functionList)
        overhaulSheet.write(rownum, 6, overhaul.vulnNum)
        overhaulSheet.write(rownum, 7, overhaul.vulnDetail)
        overhaulSheet.write(rownum, 8, overhaul.overhaulContent)
        overhaulSheet.write(rownum, 9, overhaul.developCompany)
        overhaulSheet.write(rownum, 10, overhaul.applyName)
        overhaulSheet.write(rownum, 11, overhaul.applyPhone)
        overhaulSheet.write(rownum, 12, overhaul.projectBossName)
        overhaulSheet.write(rownum, 13, overhaul.projectBossPhone)
        overhaulSheet.write(rownum, 14, overhaul.functionTestName)
        overhaulSheet.write(rownum, 15, overhaul.PenetrationTestName)
        overhaulSheet.write(rownum, 16, overhaul.testUserName)
        overhaulSheet.write(rownum, 17, overhaul.testPassword)
        overhaulSheet.write(rownum, 18, overhaul.testURL)
        overhaulSheet.write(rownum, 19, overhaul.reportPath)
        overhaulSheet.write(rownum, 20, overhaul.recordPath)
        overhaulSheet.write(rownum, 21, overhaul.functionReportIsExist)
        overhaulSheet.write(rownum, 22, overhaul.reportIsExist)
        overhaulSheet.write(rownum, 23, overhaul.recordIsExist)
        overhaulSheet.write(rownum, 24, overhaul.testIsOK)
        overhaulSheet.write(rownum, 25, overhaul.applyTime)
        overhaulSheet.write(rownum, 26, overhaul.testTime)
        overhaulSheet.write(rownum, 27, overhaul.releaseTime)
        overhaulSheet.write(rownum, 28, str(overhaul.createTime))
        overhaulSheet.write(rownum, 29, str(overhaul.updateTime))
        # print(rownum)

    workbook.save(filepath)


    file = open(filepath, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="overhaulAll_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response



@login_required
@csrf_exempt
def downloadFunctionReportPath(request):

    print(request.POST.dict())
    # dict = request.POST.dict()
    # print(dict)
    functionReportPath = request.POST.get('functionReportPath')
    # print("--------------------")
    # print(recordPath)
    # print([recordPath])
    # print(type(recordPath))

    if functionReportPath:
        filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage" + functionReportPath)
        # print(filepath)

        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="functionReport_%s.%s"' % (int(time.time()), functionReportPath.split(".")[-1])
        return response
    else:
        result = "文件不存在,下载失败"
        return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def downloadReportPath(request):

    # print(request.POST.dict())
    # dict = request.POST.dict()
    # print(dict)
    reportPath = request.POST.get('reportPath')
    # print("--------------------")
    # print(reportPath)
    # print(testIsOK)


    if reportPath:
        filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage" + reportPath)
        # print(filepath)

        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="testReport_%s.%s"' % (int(time.time()), reportPath.split(".")[-1])
        return response
    else:
        result = "文件不存在,下载失败"
        return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def downloadRecordPath(request):

    print(request.POST.dict())
    # dict = request.POST.dict()
    # print(dict)
    recordPath = request.POST.get('recordPath')
    # print("--------------------")
    # print(recordPath)
    # print([recordPath])
    # print(type(recordPath))

    if recordPath:
        filepath = os.path.join(settings.UPLOAD_DIR, "PenetrationTestOverhaulManage" + recordPath)
        # print(filepath)

        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="testRecord_%s.%s"' % (int(time.time()), recordPath.split(".")[-1])
        return response
    else:
        result = "文件不存在,下载失败"
        return JsonResponse(result, safe=False)


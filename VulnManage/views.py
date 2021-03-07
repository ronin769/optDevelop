import shutil
import xml
import datetime
import time

import xlrd
import xlwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Max, F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.core.paginator import Paginator
# from Assets.models import *
from Assets import models as AssetsModels

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
    return render(request, 'VulnManage/vulnlist.html')


@login_required
def vulnlist(request):
    return render(request, 'VulnManage/vulnlist.html')


@login_required
def vulhubList(request):
    return render(request, 'VulnManage/vulhublist.html')


@login_required
def cnvdvuln(request):
    return render(request, 'VulnManage/cnvdvuln.html')


@login_required
def addVulnData(request):
    return render(request, 'VulnManage/addvuln.html')


@login_required
def createCnvdVuln(request):
    return render(request, 'VulnManage/createcnvdvuln.html')


@login_required
@csrf_exempt
def deleteCnvdVulnAll(request):
    try:
        print(request.POST.get('deleteAll'))
        if request.POST.get('deleteAll') == "yes":
            # 删除表中数据
            CnvdManage.objects.all().delete()
            result = "success"
            return JsonResponse(result, safe=False)
        else:
            # print("删除确认")
            result = "failed"
            return JsonResponse(result, safe=False)
    except Exception as e:
        result = str(e)
        return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def deleteVulhubAll(request):
    try:
        # print(request.POST.get('deleteAll'))
        if request.POST.get('deleteAll') == "yes":
            # 删除表中数据
            VulhubManage.objects.all().delete()
            result = "success"
            return JsonResponse(result, safe=False)
        else:
            # print("删除确认")
            result = "failed"
            return JsonResponse(result, safe=False)
    except Exception as e:
        result = str(e)
        return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def deleteTroubleall(request):
    try:
        if request.POST.get('deleteAll') == "yes":
            # 删除表中数据
            VulnerabilityManage.objects.all().delete()
            result = "success"
            return JsonResponse(result, safe=False)
        else:
            result = "failed"
            return JsonResponse(result, safe=False)
    except Exception as e:
        result = str(e)
        return JsonResponse(result, safe=False)







# 通过 www.vulhub.com 网站下载最新漏洞目录
@login_required
@csrf_exempt
def initVulhubList(request):
    try:
        if request.POST.get('init') == "yes":
            response = httpGet()
            contentList = re.findall('\(a\.Link,t,e\)\}},function\(t,e\){t\.exports=(.*?)},function\(t,e,n\)', response)

            # 删除表中数据
            VulhubManage.objects.all().delete()

            contentStr = contentList[0].strip("[").strip("]").replace("},{", "}~{").replace('name', '\"name\"').replace(
                'app', '\"app\"').replace('cve', '\"cve\"').replace('path', '\"path\"').replace('"app"web', 'appweb')
            contentStrList = contentStr.split("~")
            print(contentStrList)

            for num in range(len(contentStrList)):
                # print(contentStrList[num])

                vulhubJson = json.loads(contentStrList[num])
                # print(vulnJson)
                # print(type(vulnJson))
                vulhubObj = VulhubManage()
                vulhubObj.vulhubApp = vulhubJson["app"]
                vulhubObj.vulhubName = vulhubJson["name"]
                vulhubObj.vulhubPath = vulhubJson["path"]
                vulhubObj.vulhubCVE = vulhubJson["cve"]
                vulhubObj.save()
            print("success")
            result = "success"
            return JsonResponse(result, safe=False)
        else:
            print("删除确认")
            result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse(str(e), safe=False)


def httpGet():
    url = "https://vulhub.org/js/bundle.js"
    headers = {

        "Host": "vulhub.org",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; DUK-AL20 Build/MXC89K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36",
    }

    response = requests.get(url=url, headers=headers, timeout=5)
    # print(response.url)
    # print(response.text)
    return response.text







@login_required
@csrf_exempt
def initTroubleAll(request):
    # try:

    VulnerabilityManage.objects.all().delete()

    path = os.path.join(settings.UPLOAD_DIR, "VulnManage/vulnManage.xls")

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

    firstLineValue = ['编号', '通知单名称', '系统名称', '级别', '漏洞域名', '是否通知', '是否反馈', '是否复测', '是否修复', '个数', '漏洞类型', '测试人员', '项目经理', '研发负责人', '整改通知单WORD', '整改通知单PDF', '整改反馈单', '复测报告', '开发单位', '漏洞描述', '创建人员', '修改人员', '创建时间', '更新时间']

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
        vulnNoticeFileId = domainSheet.cell_value(row, 0)
        vulnNoticeFileName = domainSheet.cell_value(row, 1).replace('"', '^').replace(".0", "")
        vulnSystemName = domainSheet.cell_value(row, 2).replace('"', '^').replace(".0", "")
        vulnLevel = domainSheet.cell_value(row, 3).replace('"', '^').replace(".0", "")
        vulnDomain = domainSheet.cell_value(row, 4)
        vulnIsNotice = domainSheet.cell_value(row, 5).replace('"', '^').replace(".0", "")
        vulnIsFeedback = domainSheet.cell_value(row, 6).replace('"', '^').replace(".0", "")
        vulnIsRetest = domainSheet.cell_value(row, 7).replace('"', '^').replace(".0", "")
        vulnIsEepair = domainSheet.cell_value(row, 8).replace('"', '^').replace(".0", "")
        vulnCount = str(domainSheet.cell_value(row, 9)).replace('"', '^').replace(".0", "")
        vulnType = domainSheet.cell_value(row, 10).replace('"', '^').replace(".0", "")
        vulnTestName = domainSheet.cell_value(row, 11).replace('"', '^').replace(".0", "")
        businessPeople = domainSheet.cell_value(row, 12).replace('"', '^').replace(".0", "")
        DevelopPeople = domainSheet.cell_value(row, 13).replace('"', '^').replace(".0", "")
        vulnNoticeWordPath = domainSheet.cell_value(row, 14)
        vulnNoticePdfPath = domainSheet.cell_value(row, 15)
        vulnFeedbackPath = domainSheet.cell_value(row, 16)
        vulnRetestPath = domainSheet.cell_value(row, 17)
        vulnDevelopCompany = domainSheet.cell_value(row, 18).replace('"', '^').replace(".0", "")
        vulnDetail = domainSheet.cell_value(row, 19).replace('"', '^').replace(".0", "")
        vulncreatePeople = domainSheet.cell_value(row, 20).replace('"', '^').replace(".0", "")
        vulnupdatePeople = domainSheet.cell_value(row, 21).replace('"', '^').replace(".0", "")
        vulncreateTime = str(domainSheet.cell_value(row, 22))
        vulnupdateTime = str(domainSheet.cell_value(row, 23))


        vulnobj = VulnerabilityManage()
        vulnobj.vulnNoticeFileId = vulnNoticeFileId
        vulnobj.vulnNoticeFileName = vulnNoticeFileName
        vulnobj.vulnSystemName = vulnSystemName
        vulnobj.vulnLevel = vulnLevel
        vulnobj.vulnDomain = vulnDomain
        vulnobj.vulnIsNotice = vulnIsNotice
        vulnobj.vulnIsFeedback = vulnIsFeedback
        vulnobj.vulnIsRetest = vulnIsRetest
        vulnobj.vulnIsEepair = vulnIsEepair
        vulnobj.vulnCount = vulnCount
        vulnobj.vulnType = vulnType
        vulnobj.vulnTestName = vulnTestName
        vulnobj.businessPeople = businessPeople
        vulnobj.DevelopPeople = DevelopPeople
        vulnobj.vulnNoticeWordPath = vulnNoticeWordPath
        vulnobj.vulnNoticePdfPath = vulnNoticePdfPath
        vulnobj.vulnFeedbackPath = vulnFeedbackPath
        vulnobj.vulnRetestPath = vulnRetestPath
        vulnobj.vulnDevelopCompany = vulnDevelopCompany
        vulnobj.vulnDetail = vulnDetail
        vulnobj.vulncreatePeople = vulncreatePeople
        vulnobj.vulnupdatePeople = vulnupdatePeople
        vulnobj.vulncreateTime = vulncreateTime
        vulnobj.vulnupdateTime = vulnupdateTime
        vulnobj.save()

    print("[ log ] -> 初始化成功")
    result = "success"
    # except xlrd.biffh.XLRDError as e:
    #     print("[ Exception ] -> ", str(e))
    #     result = "文件损坏,请重新创建文件"
    #     return JsonResponse(result, safe=False)
    #
    # except Exception as e:
    #     print("[ Exception ] -> ", str(e))
    #     result = "创建失败"

    return JsonResponse(result, safe=False)





@login_required
@csrf_exempt
def addCnvdVulnDetail(request):
    # vulNum=&vulName=&vulType=&vulStatus=on&vulOption=%E6%9C%AA%E5%A4%84%E7%90%86&vulDetail=
    try:
        cnvdobj = CnvdManage()
        cnvdobj.cnvdNumber = request.POST.get('cnvdNumber')
        cnvdobj.cveNumber = request.POST.get('cveNumber')
        cnvdobj.cveUrl = request.POST.get('cveUrl')
        cnvdobj.cnvdTitle = request.POST.get('cnvdTitle')
        cnvdobj.cnvdServerity = request.POST.get('cnvdServerity')
        cnvdobj.cnvdProducts = request.POST.get('cnvdProducts')
        cnvdobj.cnvdIsEvent = request.POST.get('cnvdIsEvent')
        cnvdobj.cnvdSubmitTime = request.POST.get('cnvdSubmitTime')
        cnvdobj.cnvdOpenTime = request.POST.get('cnvdOpenTime')
        cnvdobj.cnvdDiscovererName = request.POST.get('cnvdDiscovererName')
        cnvdobj.cnvdReferenceLink = request.POST.get('cnvdReferenceLink')
        cnvdobj.cnvdFormalWay = request.POST.get('cnvdFormalWay')
        cnvdobj.cnvdDescription = request.POST.get('cnvdDescription')
        cnvdobj.save()
        result = "success"
        return JsonResponse(result, safe=False)
    except Exception as e:
        result = str(e)
        return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def addVulnsubmit(request):
    # try:
    # print(request.POST)
    # print("-------------------")
    print(request.POST.dict())

    vulnNoticeFileIdTemp = request.POST.get('vulnNoticeFileId')
    # vulnNoticeFileNameTemp = "电动网安-" + vulnNoticeFileIdTemp + "-" + request.POST.get('vulnNoticeFileName') + "-整改通知单"
    vulnDomain = request.POST.get('vulnDomain')

    # 通知单编号是必填值,不允许为空
    if request.POST.get('vulnNoticeFileId') == "":
        result = "通知单编号禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    # 知单编号必须为整数
    if not request.POST.get('vulnNoticeFileId').isdigit():
        result = "通知单编号必须是数字"
        print("[ log ] -> ", result)
        if not isinstance(request.POST.get('vulnNoticeFileId'), int):
            result = "通知单编号必须为整数"
            print("[ log ] -> ", result)

            return JsonResponse(result, safe=False)

    # 漏洞涉及域名为必填值
    if vulnDomain == "":
        result = "漏洞涉及域名禁止为空"
        print("[ log ] -> ", result)
        return JsonResponse(result, safe=False)

    if VulnerabilityManage.objects.filter(vulnNoticeFileId__iexact=vulnNoticeFileIdTemp).exists():
        result = "通知单编号已存在,不可以重复添加"
        return JsonResponse(result, safe=False)

    # 开始逻辑
    Vulnerabilityobj = VulnerabilityManage()
    Vulnerabilityobj.vulnNoticeFileId = vulnNoticeFileIdTemp
    Vulnerabilityobj.vulnNoticeFileName = request.POST.get('vulnNoticeFileName')
    Vulnerabilityobj.vulnSpecialTime = request.POST.get('vulnSpecialTime')
    Vulnerabilityobj.vulnDomain = request.POST.get('vulnDomain')
    Vulnerabilityobj.vulnLevel = request.POST.get('vulnLevel')
    Vulnerabilityobj.vulnDetail = request.POST.get('vulnDetail')
    Vulnerabilityobj.vulnTestName = request.POST.get('vulnTestName')
    Vulnerabilityobj.vulnCount = request.POST.get('vulnCount')


    if request.POST.get('vulnIsNotice'):
        Vulnerabilityobj.vulnIsNotice = request.POST.get('vulnIsNotice')
    else:
        Vulnerabilityobj.vulnIsNotice = "off"
    if request.POST.get('vulnIsFeedback'):
        Vulnerabilityobj.vulnIsFeedback = request.POST.get('vulnIsFeedback')
    else:
        Vulnerabilityobj.vulnIsFeedback = "off"
    if request.POST.get('vulnIsRetest'):
        Vulnerabilityobj.vulnIsRetest = request.POST.get('vulnIsRetest')
    else:
        Vulnerabilityobj.vulnIsRetest = "off"
    if request.POST.get('vulnIsEepair'):
        Vulnerabilityobj.vulnIsEepair = request.POST.get('vulnIsEepair')
    else:
        Vulnerabilityobj.vulnIsEepair = "off"



    assetsModelsObj = AssetsModels.DomainManage.objects.all()
    # 获取资产表中域名对应的部门名称
    if request.POST.get('vulnDomain'):
        assetsModelsObj = assetsModelsObj.filter(domainName__iexact=request.POST.get('vulnDomain'))
    #
    # if assetsModelsObj.count() == 0:
    #     Vulnerabilityobj.vulnDepartmentName = None
    #     result = "非公司资产"
    #     print("[ log ] -> ", result)
    #
    # 获取资产表中域名对应的系统名
    for assetsModel in assetsModelsObj:  # 如果为多个就覆盖取最后一个
        Vulnerabilityobj.vulnSystemName = assetsModel.systemName
        Vulnerabilityobj.businessPeople = assetsModel.businessPeople
        Vulnerabilityobj.DevelopPeople = assetsModel.DevelopPeople



    Vulnerabilityobj.vulnType = request.POST.get('vulnType')
    # print(Vulnerabilityobj.vulnType)

    # 形如: 用户名遍历漏洞,任意文件上传漏洞,支付逻辑漏洞

    # print(str(request.user))

    Vulnerabilityobj.vulncreateTime = datetime.datetime.now()
    Vulnerabilityobj.vulnupdateTime = datetime.datetime.now()
    Vulnerabilityobj.vulncreatePeople = str(request.user)
    Vulnerabilityobj.vulnupdatePeople = str(request.user)


    Vulnerabilityobj.save()
    result = "success"
    return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def editVulnsubmit(request):
    # try:
    # print("-------------------")
    print(request.POST.dict())


    noticeFileId = request.POST.get('vulnNoticeFileIdOpenForm')  # 003




    # 通知单编号是必填值,不允许为空
    if noticeFileId == "":
        result = "通知单编号禁止为空"
        print("[ log ] -> ", result)

        return JsonResponse(result, safe=False)


    # 通知单编号必须为整数
    if not noticeFileId.isdigit():
        result = "通知单编号必须是数字"
        print("[ log ] -> ", result)
        if not isinstance(noticeFileId, int):
            result = "通知单编号必须为整数"
            print("[ log ] -> ", result)

            return JsonResponse(result, safe=False)

    # 通知单编号必须为整数
    if not request.POST.get('vulnCountOpenForm').isdigit():
        result = "漏洞个数必须是数字"
        print("[ log ] -> ", result)
        if not isinstance(noticeFileId, int):
            result = "漏洞个数必须为整数"
            print("[ log ] -> ", result)

            return JsonResponse(result, safe=False)

    # 域名是必填值,不允许为空
    if request.POST.get('noticeFileId') == "":
        result = "漏洞涉及域名禁止为空"
        print("[ log ] -> ", result)

        return JsonResponse(result, safe=False)

    if request.POST.get('vulnIsNoticeOpenForm'):
        vulnIsNotice = request.POST.get('vulnIsNoticeOpenForm')
    else:
        vulnIsNotice = "off"
    if request.POST.get('vulnIsFeedbackOpenForm'):
        vulnIsFeedback = request.POST.get('vulnIsFeedbackOpenForm')
    else:
        vulnIsFeedback = "off"
    if request.POST.get('vulnIsRetestOpenForm'):
        vulnIsRetest = request.POST.get('vulnIsRetestOpenForm')
    else:
        vulnIsRetest = "off"
    if request.POST.get('vulnIsEepairOpenForm'):
        vulnIsEepair = request.POST.get('vulnIsEepairOpenForm')
    else:
        vulnIsEepair = "off"




    assetsModelsObj = AssetsModels.DomainManage.objects.all()
    # 获取资产表中域名对应的部门名称
    assetsModelsObj = assetsModelsObj.filter(domainName__iexact=request.POST.get('vulnDomainOpenForm'))
    if assetsModelsObj.count() == 0:
        result = "非公司资产"
        vulnSystemName = request.POST.get('vulnSystemNameOpenForm')
        vulnDevelopCompany = request.POST.get('vulnDevelopCompanyOpenForm')
        print("[ log ] -> ", result)

    else:
        print("查到域名--------------")
        # 获取资产表中域名对应的系统名
        for assetsModel in assetsModelsObj:  # 如果为多个就覆盖取最后一个
            vulnSystemName = assetsModel.systemName

        # 获取资产表中域名对应的开发单位
        for assetsModel in assetsModelsObj:  # 如果为多个就覆盖取最后一个
            vulnDevelopCompany = assetsModel.developmentCompany



    VulnerabilityManage.objects.filter(vulnNoticeFileId__iexact=noticeFileId).update(
        vulnDomain=request.POST.get('vulnDomainOpenForm'),
        vulnType=request.POST.get('vulnLevelOpenForm'),
        vulnLevel=request.POST.get('vulnLevelOpenForm'),
        vulnTestName=request.POST.get('vulnTestNameOpenForm'),
        vulnCount=request.POST.get('vulnCountOpenForm'),
        vulnSystemName=vulnSystemName,
        vulnDevelopCompany=vulnDevelopCompany,
        vulnNoticeFileName=request.POST.get('vulnNoticeFileNameOpenForm'),
        vulnDetail=request.POST.get('vulnDetailOpenForm'),
        vulnIsNotice=vulnIsNotice,
        vulnIsFeedback=vulnIsFeedback,
        vulnIsRetest=vulnIsRetest,
        vulnIsEepair=vulnIsEepair,
        vulnupdateTime=datetime.datetime.now(),
        vulnupdatePeople=str(request.user),
        )

    result = "success"
    return JsonResponse(result, safe=False)


@csrf_exempt
def getCnvdList(request):
    cnvdobj = CnvdManage.objects.all()

    total = cnvdobj.count()
    resultdict = {}
    list1 = []
    for cnvd in cnvdobj:
        dict = {}
        dict['cveNumber'] = cnvd.cveNumber
        dict['cnvdNumber'] = cnvd.cnvdNumber
        dict['cveUrl'] = cnvd.cveUrl
        dict['cnvdTitle'] = cnvd.cnvdTitle
        dict['cnvdServerity'] = cnvd.cnvdServerity
        dict['cnvdProducts'] = cnvd.cnvdProducts
        dict['cnvdSubmitTime'] = cnvd.cnvdSubmitTime
        dict['cnvdOpenTime'] = cnvd.cnvdOpenTime
        dict['cnvdDiscovererName'] = cnvd.cnvdDiscovererName
        dict['cnvdReferenceLink'] = cnvd.cnvdReferenceLink
        dict['cnvdFormalWay'] = cnvd.cnvdFormalWay
        dict['cnvdDescription'] = cnvd.cnvdDescription
        dict['cnvdPatchName'] = cnvd.cnvdPatchName
        dict['cnvdPatchDescription'] = cnvd.cnvdPatchDescription
        dict['cnvdIsEvent'] = cnvd.cnvdIsEvent
        list1.append(dict)
    # print(list1)

    try:
        list1.sort(key=lambda k: (k.get('cnvdNumber')), reverse=True)
    except TypeError as e:
        print(str(e))

    # list1 = list1 + list2
    # print(dict)
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

    # cnvdobj = VulhubManage.objects.all()
    # return render(request, 'VulnManage/cnvdvuln.html', {'li':cnvdobj})
    # return render(request, 'VulnManage/cnvdvuln.html')


@login_required
@csrf_exempt
def initCnvdVuln(request):
    try:
        print("starting...")
        # print(request.POST.get('init'))
        if request.POST.get('init') == "yes":
            # 删除表中数据
            CnvdManage.objects.all().delete()

            # 多线程存储到数据库
            executor = ThreadPoolExecutor(max_workers=500)
            # dirname = os.getcwd()
            # print(settings.UPLOAD_DIR)
            dirname = settings.UPLOAD_DIR + '/cnvdfile/'
            # print(dirname)
            fileList = os.listdir(dirname)
            # print(fileList)
            fillPathList = []
            for fileName in fileList:
                if os.path.splitext(fileName)[1] == '.xml':
                    fillPathList.append(fileName)
            print(fillPathList)
            for filename in fillPathList:
                # print("sss",filename)
                # print("ddd",dirname)
                task1 = executor.submit(createCnvdToMysql, dirname, filename)
                # print(task1.result())    # result方法可以获取task的执行结果
                # createCnvdToMysql(dirname, filename)

            # 删除cnvdNumber 为空 的字段
            CnvdManage.objects.filter(Q(cnvdNumber='')).delete()
            CnvdManage.objects.filter(Q(cnvdNumber=None)).delete()

            result = "success"
            print(result)
            print("CNVD 初始化完成！")
            return JsonResponse(result, safe=False)


        else:
            print("初始化确认")
            result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        print(str(e))
        return JsonResponse(str(e), safe=False)


def createCnvdToMysql(dirname, filename):
    os.chdir(dirname)
    # print(os.getcwd())
    # print(filename)
    DOMTree = xml.dom.minidom.parse(filename)
    # print("-----------assssssssssss----------------")

    collection = DOMTree.documentElement
    # print(collection)
    # if collection.hasAttribute('title'):
    #     print('ok: %s' % collection.getAttribute('title'))
    # print("-----------------------------------------------------------")
    Vulnerabities_in = collection.getElementsByTagName('vulnerability')

    for vulnerabit in Vulnerabities_in:
        cnvdNumber = vulnerabit.getElementsByTagName('number')[0].childNodes[0].data
        # print("cnvdNumber: ", cnvdNumber)
        # print('number: %s' % number.childNodes[0].data)
        try:
            cveNumber = vulnerabit.getElementsByTagName('cveNumber')[0].childNodes[0].data
            # print(cveNumber.childNodes)
        except:
            cveNumber = None
        try:
            cveUrl = vulnerabit.getElementsByTagName('cveUrl')[0].childNodes[0].data
            # print(cveUrl.childNodes[0].data)
        except:
            cveUrl = None
        try:
            cnvdTitle = vulnerabit.getElementsByTagName('title')[0].childNodes[0].data
        except:
            cnvdTitle = None
        try:
            cnvdServerity = vulnerabit.getElementsByTagName('serverity')[0].childNodes[0].data
        except:
            cnvdServerity = None
        try:
            cnvdIsEvent = vulnerabit.getElementsByTagName('isEvent')[0].childNodes[0].data
        except:
            cnvdIsEvent = None
        try:
            cnvdProducts = ""
            products = vulnerabit.getElementsByTagName('product')
            for product in products:
                if cnvdProducts == "":
                    cnvdProducts = cnvdProducts + product.childNodes[0].data
                else:
                    if len(cnvdProducts) < 2:
                        cnvdProducts = cnvdProducts + product.childNodes[0].data
                    else:
                        cnvdProducts = cnvdProducts + ",\r\n" + product.childNodes[0].data
            cnvdProducts = cnvdProducts[:1000]

            # print(cnvdProducts)
            # print(len(cnvdProducts))
        except:
            cnvdProducts = None
        try:
            cnvdSubmitTime = vulnerabit.getElementsByTagName('submitTime')[0].childNodes[0].data
        except:
            cnvdSubmitTime = None
        try:
            cnvdOpenTime = vulnerabit.getElementsByTagName('openTime')[0].childNodes[0].data
        except:
            cnvdOpenTime = None
        try:
            cnvdReferenceLink = vulnerabit.getElementsByTagName('referenceLink')[0].childNodes[0].data
        except:
            cnvdReferenceLink = None
        try:
            cnvdDiscovererName = vulnerabit.getElementsByTagName('discovererName')[0].childNodes[0].data
        except:
            cnvdDiscovererName = None
        try:
            cnvdDescription = vulnerabit.getElementsByTagName('description')[0].childNodes[0].data
        except:
            cnvdDescription = None
        try:
            cnvdFormalWay = vulnerabit.getElementsByTagName('formalWay')[0].childNodes[0].data
        except:
            cnvdFormalWay = None
        try:
            cnvdPatchName = vulnerabit.getElementsByTagName('patchName')[0].childNodes[0].data
        except:
            cnvdPatchName = None
        try:
            cnvdPatchDescription = vulnerabit.getElementsByTagName('patchDescription')[0].childNodes[0].data
        except:
            cnvdPatchDescription = None

        # print(cnvdPatchDescription)
        try:
            cnvdObj = CnvdManage()
            cnvdObj.cnvdNumber = cnvdNumber
            cnvdObj.cveNumber = cveNumber
            cnvdObj.cveUrl = cveUrl
            cnvdObj.cnvdTitle = cnvdTitle
            cnvdObj.cnvdServerity = cnvdServerity
            cnvdObj.cnvdProducts = cnvdProducts
            cnvdObj.cnvdSubmitTime = cnvdSubmitTime
            cnvdObj.cnvdOpenTime = cnvdOpenTime
            cnvdObj.cnvdDiscovererName = cnvdDiscovererName
            cnvdObj.cnvdReferenceLink = cnvdReferenceLink
            cnvdObj.cnvdDescription = cnvdDescription
            cnvdObj.cnvdFormalWay = cnvdFormalWay
            cnvdObj.cnvdPatchName = cnvdPatchName
            cnvdObj.cnvdPatchDescription = cnvdPatchDescription
            cnvdObj.cnvdIsEvent = cnvdIsEvent

            cnvdObj.save()
        except Exception as e:
            f = open("output.log", "a")
            f.write(str(e))
            f.close()
            print(str(e))
            print(cnvdProducts)
            continue
    print("filename: %s, success!" % filename)

    # print("num:", count)


@login_required
@csrf_exempt
def deleteCnvdvulForLine(request):
    try:
        # print(request.POST.get('delete'))
        # print(request.POST.get('cnvdNumber'))

        delete = request.POST.get('delete')
        cnvdNumber = request.POST.get('cnvdNumber')

        # print(type(deleteStr))
        # print(cnvdNumberStr)

        if delete == "yes":
            result = "success"
            print(result)
            # print(CnvdManage.objects.filter(cnvdNumber="CNVD-2019-09856"))
            CnvdManage.objects.filter(cnvdNumber=cnvdNumber).delete()
            # cnvdObj.save()

            result = "success"
            print(result)
            return JsonResponse(result, safe=False)

        else:
            print("删除确认")
            result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse(str(e), safe=False)


@login_required
@csrf_exempt
def deletevulnforline(request):
    print(request.POST)
    try:
        # print(request.POST.get('delete'))
        # print(request.POST.get('cnvdNumber'))

        delete = request.POST.get('delete')
        vulnNoticeFileId = request.POST.get('vulnNoticeFileId')

        # print(type(deleteStr))
        # print(cnvdNumberStr)

        if delete == "yes":
            result = "success"
            # print(result)
            # vulnNoticeFileId = vulnNoticeFileId.replace("电动网安[","").replace("]","")
            # print(vulnNoticeFileId)
            # print(VulnerabilityManage.objects.filter(vulnNoticeFileId__iexact=vulnNoticeFileId))
            VulnerabilityManage.objects.filter(vulnNoticeFileId__iexact=vulnNoticeFileId).delete()
            # cnvdObj.save()

            result = "success"
            print(result)
            return JsonResponse(result, safe=False)

        else:
            print("删除确认")
            result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse(str(e), safe=False)


@login_required
@csrf_exempt
def editCnvdvulForLine(request):
    cnvdObj = CnvdManage()
    try:
        # print(request.POST.get('delete'))
        # print(request.POST.get('cnvdNumber'))

        edit = request.POST.get('edit')
        cnvdNumber = request.POST.get('cnvdNumber')
        cnvdTitle = request.POST.get('cnvdTitle')
        cveNumber = request.POST.get('cveNumber')

        # print(type(deleteStr))
        # print(cnvdNumberStr)

        if edit == "yes":
            result = "success"
            print(result)
            CnvdManage.objects.filter(cnvdNumber=cnvdNumber).update(cnvdTitle=cnvdTitle, cveNumber=cveNumber)

            result = "success"
            print(result)
            return JsonResponse(result, safe=False)

        else:
            print("编辑确认")
            result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse(str(e), safe=False)


@login_required
@csrf_exempt
def searchcnvdpath(request):
    cnvdNumberId = request.GET.get('cnvdNumberId', None)
    cveNumberId = request.GET.get('cveNumberId', None)
    cnvdTitleId = request.GET.get('cnvdTitleId', None)
    cnvdProductsId = request.GET.get('cnvdProductsId', None)
    cnvdDescriptionId = request.GET.get('cnvdDescriptionId', None)

    # 方法一：
    cnvdobj = CnvdManage.objects.all()

    if cnvdNumberId:
        cnvdobj = cnvdobj.filter(cnvdNumber__iexact=cnvdNumberId)
    if cveNumberId:
        cnvdobj = cnvdobj.filter(cveNumber__iexact=cveNumberId)
    if cnvdTitleId:
        cnvdobj = cnvdobj.filter(cnvdTitle__iexact=cnvdTitleId)
    if cnvdProductsId:
        cnvdobj = cnvdobj.filter(cnvdProducts__iexact=cnvdProductsId)
    if cnvdDescriptionId:
        cnvdobj = cnvdobj.filter(cnvdDescription__iexact=cnvdDescriptionId)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = cnvdobj.count()
    print("total:", total)
    resultdict = {}
    list1 = []
    for cnvdvuln in cnvdobj:
        dict = {}
        dict['cveNumber'] = cnvdvuln.cveNumber
        dict['cnvdNumber'] = cnvdvuln.cnvdNumber
        dict['cveUrl'] = cnvdvuln.cveUrl
        dict['cnvdTitle'] = cnvdvuln.cnvdTitle
        dict['cnvdServerity'] = cnvdvuln.cnvdServerity
        dict['cnvdProducts'] = cnvdvuln.cnvdProducts
        dict['cnvdSubmitTime'] = cnvdvuln.cnvdSubmitTime
        dict['cnvdOpenTime'] = cnvdvuln.cnvdOpenTime
        dict['cnvdDiscovererName'] = cnvdvuln.cnvdDiscovererName
        dict['cnvdReferenceLink'] = cnvdvuln.cnvdReferenceLink
        dict['cnvdFormalWay'] = cnvdvuln.cnvdFormalWay
        dict['cnvdDescription'] = cnvdvuln.cnvdDescription
        dict['cnvdPatchName'] = cnvdvuln.cnvdPatchName
        dict['cnvdPatchDescription'] = cnvdvuln.cnvdPatchDescription
        dict['cnvdIsEvent'] = cnvdvuln.cnvdIsEvent

        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('cnvdNumber')), reverse=True)
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


#

@login_required
@csrf_exempt
def searchvulnsubmit(request):
    print(request.GET)


    vulnNoticeFileId = request.GET.get('vulnNoticeFileId', None).strip(" ")
    vulnSystemName = request.GET.get('vulnSystemName', None).strip(" ")
    vulnLevel = request.GET.get('vulnLevel', None).strip(" ")
    vulnType = request.GET.get('vulnType', None).strip(" ")
    vulnDomain = request.GET.get('vulnDomain', None).strip(" ")
    vulnTestName = request.GET.get('vulnTestName', None).strip(" ")


    # print("vulnNoticeFileId")
    # print("vulnSystemName")
    # print("vulnType")
    # print("vulnLevel")
    # print("vulnDomain")
    # print("vulnTestName")

    # 方法一：
    vulnerabilityobj = VulnerabilityManage.objects.all()
    if vulnerabilityobj:
        vulnerabilityobj = vulnerabilityobj.filter(vulnNoticeFileId__iexact=vulnNoticeFileId)
    if vulnerabilityobj:
        vulnerabilityobj = vulnerabilityobj.filter(vulnSystemName__iexact=vulnSystemName)
    if vulnerabilityobj:
        vulnerabilityobj = vulnerabilityobj.filter(vulnType__iexact=vulnType)
    if vulnerabilityobj:
        vulnerabilityobj = vulnerabilityobj.filter(vulnLevel__iexact=vulnLevel)
    if vulnerabilityobj:
        vulnerabilityobj = vulnerabilityobj.filter(vulnDomain__iexact=vulnDomain)
    if vulnerabilityobj:
        vulnerabilityobj = vulnerabilityobj.filter(vulnTestName__iexact=vulnTestName)

    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)

    total = vulnerabilityobj.count()
    # print("total:", total)
    resultdict = {}
    list1 = []
    for vulnerability in vulnerabilityobj:
        dict = {}

        dict['vulnNoticeFileId'] = vulnerability.vulnNoticeFileId
        dict['vulnNoticeFileName'] = vulnerability.vulnNoticeFileName
        dict['vulnDomain'] = vulnerability.vulnDomain
        dict['vulnSystemName'] = vulnerability.vulnSystemName
        dict['businessPeople'] = vulnerability.businessPeople
        dict['DevelopPeople'] = vulnerability.DevelopPeople
        dict['vulnTestName'] = vulnerability.vulnTestName
        dict['vulnType'] = vulnerability.vulnType
        dict['vulnLevel'] = vulnerability.vulnLevel
        dict['vulnCount'] = vulnerability.vulnCount
        dict['vulnDetail'] = vulnerability.vulnDetail
        dict['vulnDevelopCompany'] = vulnerability.vulnDevelopCompany
        dict['vulnIsNotice'] = vulnerability.vulnIsNotice
        dict['vulnIsFeedback'] = vulnerability.vulnIsFeedback
        dict['vulnNoticeWordPath'] = vulnerability.vulnNoticeWordPath
        dict['vulnNoticePdfPath'] = vulnerability.vulnNoticePdfPath
        dict['vulnFeedbackPath'] = vulnerability.vulnFeedbackPath
        dict['vulnRetestPath'] = vulnerability.vulnRetestPath
        dict['vulnIsRetest'] = vulnerability.vulnIsRetest
        dict['vulnIsEepair'] = vulnerability.vulnIsEepair
        dict['vulncreateTime'] = vulnerability.vulncreateTime
        dict['vulnupdateTime'] = vulnerability.vulnupdateTime
        dict['vulncreatePeople'] = vulnerability.vulncreatePeople
        dict['vulnupdatePeople'] = vulnerability.vulnupdatePeople

        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('vulnNoticeFileId')), reverse=True)
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


# Create your views here.

@login_required
@csrf_exempt
def getVulnDetail(request):
    # # 删除表中数据
    # VulhubManage.objects.all().delete()
    # # 创建数据
    # createVuln()

    vulnerabilityobj = VulnerabilityManage.objects.all()

    total = vulnerabilityobj.count()
    resultdict = {}
    list1 = []
    for vulnerability in vulnerabilityobj:
        dict = {}
        dict['vulnNoticeFileId'] = vulnerability.vulnNoticeFileId
        dict['vulnNoticeFileName'] = vulnerability.vulnNoticeFileName
        dict['vulnDomain'] = vulnerability.vulnDomain
        dict['vulnSystemName'] = vulnerability.vulnSystemName
        dict['businessPeople'] = vulnerability.businessPeople
        dict['DevelopPeople'] = vulnerability.DevelopPeople
        dict['vulnTestName'] = vulnerability.vulnTestName
        dict['vulnType'] = vulnerability.vulnType
        dict['vulnLevel'] = vulnerability.vulnLevel
        dict['vulnCount'] = vulnerability.vulnCount
        dict['vulnDetail'] = vulnerability.vulnDetail
        dict['vulnDevelopCompany'] = vulnerability.vulnDevelopCompany
        dict['vulnIsNotice'] = vulnerability.vulnIsNotice
        dict['vulnIsFeedback'] = vulnerability.vulnIsFeedback
        dict['vulnNoticeWordPath'] = vulnerability.vulnNoticeWordPath
        dict['vulnNoticePdfPath'] = vulnerability.vulnNoticePdfPath
        dict['vulnFeedbackPath'] = vulnerability.vulnFeedbackPath
        dict['vulnRetestPath'] = vulnerability.vulnRetestPath
        dict['vulnIsRetest'] = vulnerability.vulnIsRetest
        dict['vulnIsEepair'] = vulnerability.vulnIsEepair
        dict['vulncreateTime'] = vulnerability.vulncreateTime
        dict['vulnupdateTime'] = vulnerability.vulnupdateTime
        dict['vulncreatePeople'] = vulnerability.vulncreatePeople
        dict['vulnupdatePeople'] = vulnerability.vulnupdatePeople

        list1.append(dict)

    # print(list1)

    try:
        # list1.sort(key=lambda k: (k.get('vulnNoticeFileId')), reverse=False)
        list1.sort(key=lambda k: (k.get('vulnNoticeFileId')), reverse=True)
    except TypeError as e:
        print(str(e))

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, limit, list1)

    res = []  # 最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


# Create your views here.
def getVulhubDetail(request):
    vulhubobj = VulhubManage.objects.all()

    total = vulhubobj.count()
    resultdict = {}
    list1 = []
    for vulhub in vulhubobj:
        dict = {}
        # dict['vulStatus'] = vulhub.vulStatus
        # dict['vulOption'] = vulhub.vulOption
        dict['vulhubCVE'] = vulhub.vulhubCVE
        dict['vulhubName'] = vulhub.vulhubName
        dict['vulhubApp'] = vulhub.vulhubApp
        dict['vulhubPath'] = vulhub.vulhubPath

        list1.append(dict)

    # resultdict['code'] = 0
    # resultdict['msg'] = ""
    # resultdict['count'] = total
    # resultdict['data'] = list1

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
def uploadWordVulnNoticeFile(request):
    print(request.FILES)
    print(request.POST)

    textFile = request.FILES['file']
    # print(textFile.name.split(".")[0])
    # print(textFile.name.split(".")[1])


    vulnNoticeFileId = request.POST.get('vulnNoticeFileIdOpenForm')


    if request.method != 'POST':
        resultdict = {"code": "1", "msg": "请求方式不正确"}
        return JsonResponse(resultdict)

    if vulnNoticeFileId == "":
        resultdict = {"code": "1", "msg": "通知单编号禁止为空"}
        return JsonResponse(resultdict)

    if not re.search("doc|pdf", os.path.splitext(textFile.name)[1], re.IGNORECASE):
        resultdict = {"code": "1", "msg": "文件类型(后缀名)不正确, 仅支持.pdf/.doc/.docx"}
        return JsonResponse(resultdict)


    textFileName = "电动网安-" + vulnNoticeFileId + "-" + textFile.name.split(".")[0] + "-整改通知单" + "." + textFile.name.split(".")[1]


    # /src/optDevelop/static/upload/VulnManage/整改通知单WORD/GitHub.docx
    filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage/整改通知单WORD/" + textFileName)
    dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/整改通知单WORD/")
    savefilepath = filepath.split("VulnManage")[1]  # APP防护方案大纲.docx

    # savefilepath = filepath.split("optDevelop")[1]  # /static/upload/VulnManage/整改通知单WORD/APP防护方案大纲.docx

    print(filepath)

    # 存入文件
    if os.path.exists(filepath):  # 文件已存在,创建新路径,备份
        new_filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage/bak/整改通知单WORD/" + os.path.splitext(textFile.name)[
            0] + "_" + time.strftime('%Y_%b_%d-%H_%M_%S') + "." + os.path.splitext(textFile.name)[1])
        new_dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/bak/整改通知单WORD/")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        shutil.move(filepath, new_filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'wb') as f:
        for text in textFile.chunks():  # 分包写入
            f.write(text)


    VulnerabilityManage.objects.filter(vulnNoticeFileId__iexact=vulnNoticeFileId).update(
        vulnNoticeWordPath=savefilepath,
        vulnupdatePeople=str(request.user),
        vulnupdateTime=datetime.datetime.now()
    )

    resultdict = {"code": "0", "msg": "已新增上传路径和通知单编号"}

    return JsonResponse(resultdict)


@login_required
@csrf_exempt
def uploadPdfVulnNoticeFile(request):
    print(request.FILES)
    print(request.POST)

    textFile = request.FILES['file']

    vulnNoticeFileId = request.POST.get('vulnNoticeFileIdOpenForm')
    print(vulnNoticeFileId)

    if request.method != 'POST':
        resultdict = {"code": "1", "msg": "请求方式不正确"}
        return JsonResponse(resultdict)

    if vulnNoticeFileId == "":
        resultdict = {"code": "1", "msg": "通知单编号禁止为空"}
        return JsonResponse(resultdict)

    if not re.search("doc|pdf", os.path.splitext(textFile.name)[1], re.IGNORECASE):
        resultdict = {"code": "1", "msg": "文件类型(后缀名)不正确, 仅支持.pdf/.doc/.docx"}
        return JsonResponse(resultdict)



    textFileName = "电动网安-" + vulnNoticeFileId + "-" + textFile.name.split(".")[0] + "-整改通知单" + "." + textFile.name.split(".")[1]

    # /src/optDevelop/static/upload/VulnManage/整改通知单PDF/GitHub.docx
    filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage/整改通知单PDF/" + textFileName)
    dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/整改通知单PDF/")
    savefilepath = filepath.split("VulnManage")[1]  # APP防护方案大纲.docx
    # savefilepath = filepath.split("optDevelop")[1]  # /static/upload/VulnManage/整改通知单WORD/APP防护方案大纲.docx
    print(filepath, savefilepath)

    # 存入文件
    if os.path.exists(filepath):  # 文件已存在,创建新路径,备份
        new_filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage/bak/整改通知单PDF/" + os.path.splitext(textFile.name)[
            0] + "_" + time.strftime('%Y_%b_%d-%H_%M_%S') + "." + os.path.splitext(textFile.name)[1])
        new_dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/bak/整改通知单PDF/")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        shutil.move(filepath, new_filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'wb') as f:
        for text in textFile.chunks():  # 分包写入
            f.write(text)


    VulnerabilityManage.objects.filter(vulnNoticeFileId__iexact=vulnNoticeFileId).update(
        vulnNoticePdfPath=savefilepath,
        vulnupdatePeople=str(request.user),
        vulnupdateTime=datetime.datetime.now()
    )

    resultdict = {"code": "0", "msg": "已新增上传路径和通知单编号"}

    print(resultdict)

    return JsonResponse(resultdict)


@login_required
@csrf_exempt
def uploadVulnFeedbackFile(request):
    print(request.FILES)
    print(request.POST)

    textFile = request.FILES['file']


    vulnNoticeFileId = request.POST.get('vulnNoticeFileIdOpenForm')
    print(vulnNoticeFileId)


    if request.method != 'POST':
        resultdict = {"code": "1", "msg": "请求方式不正确"}
        return JsonResponse(resultdict)
    if vulnNoticeFileId == "":
        resultdict = {"code": "1", "msg": "通知单编号禁止为空"}
        return JsonResponse(resultdict)

    if not re.search("pdf|doc", os.path.splitext(textFile.name)[1], re.IGNORECASE):
        resultdict = {"code": "1", "msg": "文件类型(后缀名)不正确, 仅支持.pdf/.doc/.docx"}
        return JsonResponse(resultdict)



    textFileName = "电动网安-" + vulnNoticeFileId + "-" + textFile.name.split(".")[0] + "-整改反馈单" + "." + textFile.name.split(".")[1]


    # /src/optDevelop/static/upload/VulnManage/整改通知单PDF/GitHub.docx
    filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage/整改反馈单/" + textFileName)
    dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/整改反馈单/")
    savefilepath = filepath.split("VulnManage")[1]  # APP防护方案大纲.docx
    # savefilepath = filepath.split("optDevelop")[1]  # /static/upload/VulnManage/整改通知单WORD/APP防护方案大纲.docx
    print(filepath, savefilepath)

    # 存入文件
    if os.path.exists(filepath):  # 文件已存在,创建新路径,备份
        new_filepath = os.path.join(settings.UPLOAD_DIR,
                                    "VulnManage/bak/整改反馈单/" + os.path.splitext(textFile.name)[0] + "_" + time.strftime(
                                        '%Y_%b_%d-%H_%M_%S') + "." + os.path.splitext(textFile.name)[1])
        new_dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/bak/整改反馈单/")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        shutil.move(filepath, new_filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'wb') as f:
        for text in textFile.chunks():  # 分包写入
            f.write(text)




    VulnerabilityManage.objects.filter(vulnNoticeFileId__iexact=vulnNoticeFileId).update(
        vulnFeedbackPath=savefilepath,
        vulnupdatePeople=str(request.user),
        vulnupdateTime=datetime.datetime.now()
    )


    resultdict = {"code": "0", "msg": "已新增上传路径和通知单编号"}

    print(resultdict)

    return JsonResponse(resultdict)


@login_required
@csrf_exempt
def uploadVulnRetestFile(request):
    print(request.FILES)
    print(request.POST)

    textFile = request.FILES['file']

    vulnNoticeFileId = request.POST.get('vulnNoticeFileIdOpenForm')


    if request.method != 'POST':
        resultdict = {"code": "1", "msg": "请求方式不正确"}
        return JsonResponse(resultdict)
    if vulnNoticeFileId == "":
        resultdict = {"code": "1", "msg": "通知单编号禁止为空"}
        return JsonResponse(resultdict)
    if not re.search("doc|pdf", os.path.splitext(textFile.name)[1], re.IGNORECASE):
        resultdict = {"code": "1", "msg": "文件类型(后缀名)不正确, 仅支持.pdf/.doc/.docx"}
        return JsonResponse(resultdict)


    textFileName = "电动网安-" + vulnNoticeFileId + "-" + textFile.name.split(".")[0] + "-复测报告" + "." + textFile.name.split(".")[1]

    # /src/optDevelop/static/upload/VulnManage/整改通知单PDF/GitHub.docx
    filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage/复测报告/" + textFileName)
    dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/复测报告")
    savefilepath = filepath.split("VulnManage")[1]  # APP防护方案大纲.docx
    # savefilepath = filepath.split("optDevelop")[1]  # /static/upload/VulnManage/整改通知单WORD/APP防护方案大纲.docx
    print(dirpath, "----", filepath, "----", savefilepath)

    # 存入文件
    if os.path.exists(filepath):  # 文件已存在,创建新路径,备份
        new_filepath = os.path.join(settings.UPLOAD_DIR,
                                    "VulnManage/bak/复测报告/" + os.path.splitext(textFile.name)[0] + "_" + time.strftime(
                                        '%Y_%b_%d-%H_%M_%S') + "." + os.path.splitext(textFile.name)[1])
        new_dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/bak/复测报告/")
        if not os.path.exists(new_dirpath):
            os.makedirs(new_dirpath)
        shutil.move(filepath, new_filepath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(filepath, 'wb') as f:
        for text in textFile.chunks():  # 分包写入
            f.write(text)

    VulnerabilityManage.objects.filter(vulnNoticeFileId__iexact=vulnNoticeFileId).update(
        vulnRetestPath=savefilepath,
        vulnupdatePeople=str(request.user),
        vulnupdateTime=datetime.datetime.now()
    )


    resultdict = {"code": "0", "msg": "已新增上传路径和通知单编号"}

    print(resultdict)

    return JsonResponse(resultdict)





@login_required
@csrf_exempt
def uploadTroubleFileAll(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage/vulnManage.xls")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "VulnManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "VulnManage/bak/vulnManage%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")

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
def editVulnIsNotice(request):
    print(request.POST)
    # dict = request.POST.dict()
    # print(dict)
    vulnNoticeFileId = request.POST.get('vulnNoticeFileId')  # 整改通知单
    vulnIsNotice = request.POST.get('vulnIsNotice')  # 整改通知单
    print(vulnNoticeFileId)
    print(vulnIsNotice)

    vulnerabilityobj = VulnerabilityManage.objects.get(vulnNoticeFileId__iexact=vulnNoticeFileId)
    print(vulnerabilityobj.vulnIsNotice)
    if vulnIsNotice == "off":
        vulnerabilityobj.vulnIsNotice = "on"
    else:
        vulnerabilityobj.vulnIsNotice = "off"

    print(vulnerabilityobj.vulnIsNotice)
    vulnerabilityobj.save()

    result = {"status": vulnerabilityobj.vulnIsNotice}
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def editVulnIsFeedback(request):
    print(request.POST)
    # dict = request.POST.dict()
    # print(dict)
    vulnNoticeFileId = request.POST.get('vulnNoticeFileId')  # 整改通知单
    vulnIsFeedback = request.POST.get('vulnIsFeedback')  # 整改通知单
    print(vulnNoticeFileId)
    print(vulnIsFeedback)

    vulnerabilityobj = VulnerabilityManage.objects.get(vulnNoticeFileId__iexact=vulnNoticeFileId)
    print(vulnerabilityobj.vulnIsFeedback)
    if vulnIsFeedback == "off":
        vulnerabilityobj.vulnIsFeedback = "on"
    else:
        vulnerabilityobj.vulnIsFeedback = "off"

    print(vulnerabilityobj.vulnIsFeedback)
    vulnerabilityobj.save()

    result = {"status": vulnerabilityobj.vulnIsFeedback}
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def editVulnIsRetest(request):
    print(request.POST)
    # dict = request.POST.dict()
    # print(dict)
    vulnNoticeFileId = request.POST.get('vulnNoticeFileId')  # 整改通知单
    vulnIsRetest = request.POST.get('vulnIsRetest')  # 整改通知单
    print(vulnNoticeFileId)
    print(vulnIsRetest)

    vulnerabilityobj = VulnerabilityManage.objects.get(vulnNoticeFileId__iexact=vulnNoticeFileId)
    print(vulnerabilityobj.vulnIsRetest)
    if vulnIsRetest == "off":
        vulnerabilityobj.vulnIsRetest = "on"
    else:
        vulnerabilityobj.vulnIsRetest = "off"

    print(vulnerabilityobj.vulnIsRetest)
    vulnerabilityobj.save()

    result = {"status": vulnerabilityobj.vulnIsRetest}
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def editVulnIsRepire(request):
    print(request.POST)
    # dict = request.POST.dict()
    # print(dict)
    vulnNoticeFileId = request.POST.get('vulnNoticeFileId')  # 整改通知单
    vulnIsEepair = request.POST.get('vulnIsEepair')  # 整改通知单
    print(vulnNoticeFileId)
    print(vulnIsEepair)

    vulnerabilityobj = VulnerabilityManage.objects.get(vulnNoticeFileId__iexact=vulnNoticeFileId)
    print(vulnerabilityobj.vulnIsEepair)
    if vulnIsEepair == "off":
        vulnerabilityobj.vulnIsEepair = "on"
    else:
        vulnerabilityobj.vulnIsEepair = "off"

    print(vulnerabilityobj.vulnIsEepair)
    vulnerabilityobj.save()

    result = {"status": vulnerabilityobj.vulnIsEepair}
    return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def downloadVulnNoticeWordPath(request):

    print(request.POST.dict())
    # dict = request.POST.dict()
    # print(dict)
    vulnNoticeWordPath = request.POST.get('vulnNoticeWordPath')
    # print("--------------------")
    # print(recordPath)
    # print([recordPath])
    # print(type(recordPath))

    if vulnNoticeWordPath:
        filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage" + vulnNoticeWordPath)
        # print(filepath)

        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="vulnNoticeWord_%s.%s"' % (vulnNoticeWordPath.split("-")[1], vulnNoticeWordPath.split(".")[-1])
        return response
    else:
        result = "文件不存在,下载失败"
        return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def downloadVulnNoticePdfPath(request):

    print(request.POST.dict())
    # dict = request.POST.dict()
    # print(dict)
    vulnNoticePdfPath = request.POST.get('vulnNoticePdfPath')
    # print("--------------------")
    # print(recordPath)
    # print([recordPath])
    # print(type(recordPath))

    if vulnNoticePdfPath:
        filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage" + vulnNoticePdfPath)
        # print(filepath)

        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="vulnNoticePdf_%s.%s"' % (vulnNoticePdfPath.split("-")[1], vulnNoticePdfPath.split(".")[-1])
        return response
    else:
        result = "文件不存在,下载失败"
        return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def downloadVulnFeedbackPath(request):

    print(request.POST.dict())
    # dict = request.POST.dict()
    # print(dict)
    vulnFeedbackPath = request.POST.get('vulnFeedbackPath')
    # print("--------------------")
    # print(recordPath)
    # print([recordPath])
    # print(type(recordPath))

    if vulnFeedbackPath:
        filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage" + vulnFeedbackPath)
        # print(filepath)

        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="vulnFeedback_%s.%s"' % (vulnFeedbackPath.split("-")[1], vulnFeedbackPath.split(".")[-1])
        return response
    else:
        result = "文件不存在,下载失败"
        return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def downloadVulnRetestPath(request):

    print(request.POST.dict())
    # dict = request.POST.dict()
    # print(dict)
    vulnRetestPath = request.POST.get('vulnRetestPath')
    # print("--------------------")
    # print(recordPath)
    # print([recordPath])
    # print(type(recordPath))
    # print(vulnRetestPath.split("/")[-1])

    if vulnRetestPath:
        filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage" + vulnRetestPath)
        # print(filepath)

        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/msword'
        response['Content-Disposition'] = 'attachment;filename="vulnRetest_%s.%s"' % (vulnRetestPath.split("-")[1], vulnRetestPath.split(".")[-1])
        return response
    else:
        result = "文件不存在,下载失败"
        return JsonResponse(result, safe=False)




@login_required
@csrf_exempt
def downloadTroubleTemplateFile(request):

    # print(request.POST.dict())


    troubleTemplate = os.path.join(settings.UPLOAD_DIR, "VulnManage/troubleTemplate.xls")


    if os.path.exists(troubleTemplate):

        file = open(troubleTemplate, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = 'attachment;filename="vulnTemplate_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
        return response
    else:
        result = "文件不存在,下载失败"
        return JsonResponse(result, safe=False)





@login_required
@csrf_exempt
def downloadTroubleAllToFile(request):

    filepath = os.path.join(settings.UPLOAD_DIR, "VulnManage/vulnManage.xls")
    # print(filepath)

    dirpath = os.path.join(settings.UPLOAD_DIR, "AssetsManage/bak/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if os.path.exists(filepath):
        new_filepath = dirpath + "vulnManageAll_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls"
        # print(filepath)
        # print(new_filepath)
        shutil.move(filepath, new_filepath)
        # os.rename(filepath, new_filepath)
        # print("ok")



    vulnobj = VulnerabilityManage.objects.all()


    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    vulnSheet = workbook.add_sheet('domainAll')

    #生成第一行
    row0 = ['编号', '通知单名称', '系统名称', '级别', '漏洞域名', '是否通知', '是否反馈', '是否复测', '是否修复', '个数', '漏洞类型', '测试人员', '项目经理', '研发负责人', '整改通知单WORD', '整改通知单PDF', '整改反馈单', '复测报告', '开发单位', '漏洞描述', '创建人员', '修改人员', '创建时间', '更新时间']

    for i in range(0, len(row0)):
        vulnSheet.write(0, i, row0[i])


    rownum = 0

    for vuln in vulnobj:
        # if domain.systemStatus == "已下线":
        #     continue
        rownum = rownum + 1
        vulnSheet.write(rownum, 0, vuln.vulnNoticeFileId)
        vulnSheet.write(rownum, 1, vuln.vulnNoticeFileName)
        vulnSheet.write(rownum, 2, vuln.vulnSystemName)
        vulnSheet.write(rownum, 3, vuln.vulnLevel)
        vulnSheet.write(rownum, 4, vuln.vulnDomain)
        vulnSheet.write(rownum, 5, vuln.vulnIsNotice)
        vulnSheet.write(rownum, 6, vuln.vulnIsFeedback)
        vulnSheet.write(rownum, 7, vuln.vulnIsRetest)
        vulnSheet.write(rownum, 8, vuln.vulnIsEepair)
        vulnSheet.write(rownum, 9, vuln.vulnCount)
        vulnSheet.write(rownum, 10, vuln.vulnType)
        vulnSheet.write(rownum, 11, vuln.vulnTestName)
        vulnSheet.write(rownum, 12, vuln.businessPeople)
        vulnSheet.write(rownum, 13, vuln.DevelopPeople)
        vulnSheet.write(rownum, 14, vuln.vulnNoticeWordPath)
        vulnSheet.write(rownum, 15, vuln.vulnNoticePdfPath)
        vulnSheet.write(rownum, 16, vuln.vulnFeedbackPath)
        vulnSheet.write(rownum, 17, vuln.vulnRetestPath)
        vulnSheet.write(rownum, 18, vuln.vulnDevelopCompany)
        vulnSheet.write(rownum, 19, vuln.vulnDetail)
        vulnSheet.write(rownum, 20, vuln.vulncreatePeople)
        vulnSheet.write(rownum, 21, vuln.vulnupdatePeople)
        vulnSheet.write(rownum, 22, str(vuln.vulncreateTime))
        vulnSheet.write(rownum, 23, str(vuln.vulnupdateTime))
        # print(rownum)

    workbook.save(filepath)


    file = open(filepath, 'rb')


    response = FileResponse(file)
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="vulnManageAll_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response










    # file = open(filepath, 'rb')
    #
    #
    # response = FileResponse(file)
    # response['Content-Type'] = 'application/octet-stream'
    # response['Content-Disposition'] = 'attachment;filename="domainAll_%s.xls"' % int(time.time())
    # return response



# def cnvdxmlHandle(filename):
#     f = open(filename, "r", encoding='utf-8')
#     fcontent = f.read()
#     # print(type(fcontent))
#     # print(type(fcontent))
#     soup = fcontent.strip("\r\n")
#
#     soup = BeautifulSoup(str(fcontent), "lxml")
#     print(soup.title)
#
#     if type(soup.title.string) == element.Comment:
#         print(soup.title.string)
#
#
#     vulnList = soup.find_all('vulnerability')
#     for vulnPerLine in vulnList:
#         soup1 = BeautifulSoup(str(vulnPerLine), "lxml")
#         # exit()
#         # print(str(soup1.select("title")).replace("\n", ""))
#         # exit()
#
#         # print(soup1.cvenumber)
#         # print(soup1.cveurl)
#         cnvdNumber = soup1.number.string
#         try:
#             cveNumber = soup1.cvenumber.string
#         except AttributeError as e:
#             cveNumber = None
#         try:
#             cveUrl = soup1.cveurl.string
#         except AttributeError as e:
#             cveUrl = None
#
#         # print(vulnPerLine)
#
#         cveTitle = soup1.title.string
#         cveServerity = soup1.serverity.string
#         products = soup1.select("product")
#
#
#         cveProducts = []
#         for perPro in products:
#             soup2 = BeautifulSoup(str(perPro), "lxml")
#             cveProducts.append(soup2.product.string)
#         cveIsEvent = soup1.isevent.string
#         cveSubmitTime = soup1.submittime.string
#         cveOpenTime = soup1.opentime.string
#         try:
#             cveDiscovererName = soup1.discoverername.string
#         except AttributeError as e:
#             cveDiscovererName = None
#         try:
#             cveReferenceLink = soup1.referencelink.string
#         except AttributeError as e:
#             cveReferenceLink = None
#
#         try:
#             cveFormalWay = soup1.formalway.string
#         except AttributeError as e:
#             cveFormalWay = None
#         cveDescription = soup1.description.string
#
#         print(cnvdNumber)
#         print(cveNumber)
#         print(cveUrl)
#         print(cveTitle)
#         print(cveServerity)
#         print(cveProducts)
#         print(cveIsEvent)
#         print(cveSubmitTime)
#         print(cveOpenTime)
#         print(cveDiscovererName)
#         print(cveReferenceLink)
#         print(cveFormalWay)
#         print(cveDescription)
#     return cnvdNumber
#
#
#
#
#
#
#
#     # 以下为查询，有专用的方式，比如
#     # 实现where子名，作为方法filter()、exclude()、get()的参数
#     # 语法：属性名称__比较运算符=值
#     # 表示两个下划线，左侧是属性名称，右侧是比较类型
#     # 对于外键，使用“属性名_id”表示外键的原始值
#     # 转义：like语句中使用了%与，匹配数据中的%与，在过滤器中直接写，例如：filter(title__contains="%")=>where title like '%\%%'，表示查找标题中包含%的
#
#
#     # 返回列表
#     # list  = BookInfo.books1.filter(heroinfo__hcontent__contains="六")    # 包含 六 的书
#     # 等价于 select * from bookinfo inner join booktest_heroinfo on bookinfo.id=book_id;
#     # 是查 heroinfo 的 hcontent 中包含 六 的英雄对应的书 （BookInfo）
#     # list = BookInfo.books1.aggregate(Max('id'))
#     # context = {'list': list}
#     # return render(request, 'booktest/index.html', context)
#
#     # list = BookInfo.books1.filter(pk__lt=3).
#
#     # context = {'list': list}
#     # return render(request, 'booktest/index.html', context)
#
#     # 使用aggregate()函数返回聚合函数的值
#     # 函数：Avg，Count，Max，Min，Sum
#     Max1 = BookInfo.books1.aggregate(Max('id'))           # id 的最大值
#     Max1 = BookInfo.books1.aggregate(Max('bpub_data'))      # bpub_data 的最大值
#     Max1 = BookInfo.books1.aggregate(Sum('id'))
#
#
#     list1 = BookInfo.books1.filter(bread__gt=10)            # 阅读量大于10
#
#
#     # 两个列做自己算使用 F 对象，列比较，列计算等
#     list1 = BookInfo.books1.filter(bread__gt=F('bcommet'))  # 阅读量大于评论量
#
#
#     # 逻辑与关系
#     list1 = BookInfo.books1.filter(pk__lt=4, btitle__contains='1')
#     list1 = BookInfo.books1.filter(pk__lt=4).filter(btitle__contains='1')
#
#     # 逻辑或使用 Q 对象
#
#     list1 = BookInfo.books1.filter(( Q(pk__lt=6) | Q(bcommet__gt=10) ))
#     context = {'list1': list1
#         , 'Max1': Max1
#                }
#     return render(request, 'booktest/index.html', context)
#
#
# def detail(request, re1):
#     # return HttpResponse(re1)
#     # return HttpResponse(request.path)
#     return HttpResponse(request.method)
#     # return HttpResponse(request.FILES)
#     # return HttpResponse(request.GET)
#     # return HttpResponse(request.is_ajax())

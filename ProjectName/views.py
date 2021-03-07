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
    return render(request, 'ProjectName/projectName.html')


@login_required
def projectName(request):
    return render(request, 'ProjectName/projectName.html')


@login_required
def addProjectNamepage(request):
    return render(request, 'ProjectName/addProjectName.html')




@login_required
@csrf_exempt
def getProjectNamelist(request):
    projectnameobj = ProjectNameManage.objects.all()

    # total = shipManage.objects.filter(systemStatus__contains="使用中").count()
    total = 0
    resultdict = {}
    list1 = []
    for project in projectnameobj:
        # print("--")
        total = total + 1
        dict = {}
        dict['projectName'] = project.projectName
        dict['projectDesc'] = project.projectDesc
        dict['businessPeople'] = project.businessPeople
        dict['businessPhone'] = project.businessPhone
        dict['developPeople'] = project.developPeople
        dict['developPhone'] = project.developPhone
        dict['developmentCompany'] = project.developmentCompany
        dict['common'] = project.common
        dict['createTime'] = project.createTime
        dict['updateTime'] = project.updateTime
        dict['createPeople'] = project.createPeople

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
def uploadProjectNamefile(request):
    # print(request.FILES)
    if request.method == 'POST':
        textFile = request.FILES['file']
        # filepath = os.path.join(settings.UPLOAD_DIR, textFile.name)
        filepath = os.path.join(settings.UPLOAD_DIR, "projectNameManage/projectNameAsset.xls")
        # print(filepath)
        dirpath = os.path.join(settings.UPLOAD_DIR, "projectNameManage/bak/")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        if os.path.exists(filepath):
            new_filepath = os.path.join(settings.UPLOAD_DIR,
                                        "projectNameManage/bak/projectNameAsset%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls")

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
def initProjectName(request):
    try:

        ProjectNameManage.objects.all().delete()

        path = 'static/upload/projectNameManage/projectNameAsset.xls'
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

        firstLineValue = ['项目名称', '项目描述', '业务联系人', '业务联系方式', '开发联系人', '开发联系方式', '开发单位', '备注', '创建时间', '修改时间', '创建人']

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
            projectName = str((shipSheet.cell_value(row, 0)))
            projectDesc = str((shipSheet.cell_value(row, 1)))
            businessPeople = str((shipSheet.cell_value(row, 2)))
            businessPhone = str((shipSheet.cell_value(row, 3))).replace(".0", "")
            developPeople = str((shipSheet.cell_value(row, 4)))
            developPhone = str((shipSheet.cell_value(row, 5))).replace(".0", "")
            developmentCompany = str((shipSheet.cell_value(row, 6)))
            common = str((shipSheet.cell_value(row, 7)))
            createTime = str((shipSheet.cell_value(row, 8)))
            updateTime = str((shipSheet.cell_value(row, 9)))
            createPeople = str((shipSheet.cell_value(row, 10)))

            # for j in range(colNum):
            #     # # 获取单元格内容为日期的数据
            #     # date_value = xlrd.xldate_as_tuple(Data_sheet.cell_value(i, j), workbook.datemode)
            #     # print(date_value)
            #     print(ecsSheet.cell_value(row, j))
            #     # print(list[i][j], '\t\t', end="")
            #
            # ecsIPS = re.compile(r'((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)')

            projectNameobj = ProjectNameManage()
            projectNameobj.projectName = projectName
            projectNameobj.projectDesc = projectDesc
            projectNameobj.businessPeople = businessPeople
            projectNameobj.businessPhone = businessPhone
            projectNameobj.developPeople = developPeople
            projectNameobj.developPhone = developPhone
            projectNameobj.developmentCompany = developmentCompany
            projectNameobj.common = common
            projectNameobj.createTime = createTime
            projectNameobj.updateTime = updateTime
            projectNameobj.createPeople = createPeople
            projectNameobj.save()

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
def addProjectNamesubmit(request):
    try:
        # print(request.POST)
        # print(dict(request.POST).keys())

        if request.POST.get('projectName') == "":
            result = "项目名禁止为空"
            print("[ log ] -> ", result)

            return JsonResponse(result, safe=False)

        if ProjectNameManage.objects.filter(projectName__iexact=request.POST.get('projectName').replace(" ", "")):
            result = "该项目名已存在"
            print("[ log ] -> ", result)
            return JsonResponse(result, safe=False)

        projectNameobj = ProjectNameManage()
        projectNameobj.projectName = request.POST.get('projectName')
        projectNameobj.projectDesc = request.POST.get('projectDesc')
        projectNameobj.businessPeople = request.POST.get('businessPeople')
        projectNameobj.businessPhone = request.POST.get('businessPhone')
        projectNameobj.developPeople = request.POST.get('developPeople')
        projectNameobj.developPhone = request.POST.get('developPhone')
        projectNameobj.developmentCompany = request.POST.get('developmentCompany')
        projectNameobj.common = request.POST.get('common')
        projectNameobj.createTime = datetime.datetime.now()
        projectNameobj.updateTime = datetime.datetime.now()
        projectNameobj.createPeople = request.user

        projectNameobj.save()

        result = "success"
    except Exception as e:
        print(str(e))
        result = "failed"

    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def editProjectNamesubmit(request):
    try:
        # print(request.POST.dict())
        projectName = request.POST.get('projectName')
        projectDesc = request.POST.get('projectDesc')

        obj1 = ProjectNameManage.objects.filter(projectName=projectName, projectDesc=projectDesc)
        if obj1:
            obj1.update(
                projectName=request.POST.get('projectName'),
                projectDesc=request.POST.get('projectDesc'),
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
def deleteProjectNameall(request):
    try:
        ProjectNameManage.objects.all().delete()
        result = "success"
    except:
        result = "failed"
    return JsonResponse(result, safe=False)



@login_required
@csrf_exempt
def searchProjectName(request):
    # print(request.GET)

    projectName = request.GET.get('projectName', None).strip(" ")
    projectDesc = request.GET.get('projectDesc', None).strip(" ")
    businessPeople = request.GET.get('businessPeople', None).strip(" ")
    developPeople = request.GET.get('developPeople', None).strip(" ")

    # 方法一：
    projectNameobj = ProjectNameManage.objects.all()

    if projectName:
        projectNameobj = projectNameobj.filter(projectName__icontains=projectName)
    if projectDesc:
        projectNameobj = projectNameobj.filter(projectDesc__icontains=projectDesc)
    if businessPeople:
        projectNameobj = projectNameobj.filter(businessPeople__icontains=businessPeople)
    if developPeople:
        projectNameobj = projectNameobj.filter(developPeople__icontains=developPeople)


    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)



    total = projectNameobj.count()
    print("total:", total)
    list1 = []
    for ship in projectNameobj:
        dict = {}

        dict['projectName'] = ship.projectName
        dict['projectDesc'] = ship.projectDesc
        dict['businessPeople'] = ship.businessPeople
        dict['businessPhone'] = ship.businessPhone
        dict['developPeople'] = ship.developPeople
        dict['developPhone'] = ship.developPhone
        dict['developmentCompany'] = ship.developmentCompany
        dict['common'] = ship.common

        list1.append(dict)

    try:
        # list1.sort(key=lambda k: (k.get('serviceName')), reverse=False)
        list1.sort(key=lambda k: (k.get('projectName')), reverse=False)
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
def deleteProjectNameforline(request):
    try:
        if request.POST:
            delete = request.POST.get('delete')
            projectName = request.POST.get('projectName')
            projectDesc = request.POST.get('projectDesc')

            if delete == "yes":
                ProjectNameManage.objects.filter(projectName__iexact=projectName, projectDesc__iexact=projectDesc).delete()
                result = "success"
                print(result)
            else:
                result = "failed"
            return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse(str(e), safe=False)


@login_required
@csrf_exempt
def downloadProjectNameTemplateFile(request):
    file = open('static/upload/projectNameManage/projectNameTemplate.xls', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="projectNameTemplate_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response


@login_required
@csrf_exempt
def downloadProjectNameAllToFile(request):

    filepath = os.path.join(settings.UPLOAD_DIR, "projectNameManage/projectNameAssetAll.xls")
    # print(filepath)

    dirpath = os.path.join(settings.UPLOAD_DIR, "projectNameManage/bak/")
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    if os.path.exists(filepath):
        new_filepath = dirpath + "projectNameAssetAll_%s" % time.strftime('%Y_%b_%d-%H_%M_%S') + ".xls"
        # print(filepath)
        # print(new_filepath)
        shutil.move(filepath, new_filepath)
        # os.rename(filepath, new_filepath)
        # print("ok")

    projectNameobj = ProjectNameManage.objects.all()


    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    projectSheet = workbook.add_sheet('projectAll')

    #生成第一行
    row0 = ['项目名称', '项目描述', '业务联系人', '业务联系方式', '开发联系人', '开发联系方式', '开发单位', '备注', '创建时间', '修改时间', '创建人']

    for i in range(0, len(row0)):
        projectSheet.write(0, i, row0[i])

    rownum = 0

    for project in projectNameobj:
        # if ship.systemStatus == "已下线":
        #     continue
        rownum = rownum + 1
        projectSheet.write(rownum, 0, project.projectName)
        projectSheet.write(rownum, 1, project.projectDesc)
        projectSheet.write(rownum, 2, project.businessPeople)
        projectSheet.write(rownum, 3, project.businessPhone)
        projectSheet.write(rownum, 4, project.developPeople)
        projectSheet.write(rownum, 5, project.developPhone)
        projectSheet.write(rownum, 6, project.developmentCompany)
        projectSheet.write(rownum, 7, project.common)
        projectSheet.write(rownum, 8, str(project.createTime))
        projectSheet.write(rownum, 9, str(project.updateTime))
        projectSheet.write(rownum, 10, project.createPeople)

        # print(rownum)

    workbook.save(filepath)


    file = open(filepath, 'rb')


    response = FileResponse(file)
    response['Content-Type'] = '.xls,application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="projectNameAssetAll_%s.xls"' % time.strftime('%Y_%b_%d-%H_%M_%S')
    return response





from django.db import models
import mongoengine

# apt install mysql
# from tinymce.models import HTMLField
# pip3 install django-tinymce
# 先生成应用 python3 manage.py startapp FireWall
# 设置数据里 setting
# 创建空数据库 create schema  `optmanager` DEFAULT CHARACTER SET utf8;
# setting 中加入应用名'booktest'
# 定义以下类之后生成迁移 python3 manage.py makemigrations ，自动生成 00001_initial.py，为数据库
# 迁移 python3 manage.py migrate
# 当执行 python manage.py makemigrations 出现错误：TypeError: init() missing 1 required positional argument: ‘on_delete’
#   添加 book = models.ForeignKey('BookInfo', on_delete = models.CASCADE)
# 提示decode错误 query = query.decode(errors=‘replace’) 将decode修改为encode即可
# 定义url: index类
# from django.urls import path
# from . import views
# # 定义自己的 URL
# urlpatterns = [path('', views.index, name='index'),]
# 创建模板文件,index.html
# views 中修改返回值,会返回给index.html
# 运行 python3 manage.py runserver

# 富文本编辑器需要安装 pip3 install django-tinymce

class PenetrationTestOverhaulManage(models.Model):

    overhaulId = models.CharField(max_length=100, primary_key=True, unique=True)   # 渗透编号
    testStyle = models.CharField(max_length=100, null=True)                 # 测试类型
    systemName = models.CharField(max_length=100, null=True)               # 系统名称
    systemVersion = models.CharField(max_length=100, null=True)            # 系统版本
    functionNum = models.IntegerField(null=True)                           # 功能个数
    functionList = models.CharField(max_length=100, null=True)             # 功能列表
    vulnNum = models.CharField(max_length=100, null=True)                  # 漏洞个数
    vulnDetail = models.CharField(max_length=100, null=True)               # 漏洞描述
    overhaulContent = models.CharField(max_length=100, null=True)          # 检修内容
    developCompany = models.CharField(max_length=200, null=True)           # 开发单位
    applyName = models.CharField(max_length=200, null=True)                 # 申请人
    applyPhone = models.CharField(max_length=200, null=True)                # 申请人联系方式
    projectBossName = models.CharField(max_length=200, null=True)           # 项目经理
    projectBossPhone = models.CharField(max_length=200, null=True)          # 项目经理联系方式
    functionTestName = models.CharField(max_length=200, null=True)          # 功能测试联系人
    PenetrationTestName = models.CharField(max_length=200, null=True)       # 渗透测试联系人
    testUserName = models.CharField(max_length=200, null=True)              # 测试账号
    testPassword = models.CharField(max_length=200, null=True)              # 测试密码
    testURL = models.CharField(max_length=200, null=True)                   # 测试地址
    functionReportPath = models.CharField(max_length=1000, null=True)       # 功能报告
    reportPath = models.CharField(max_length=1000, null=True)               # 测试报告
    recordPath = models.CharField(max_length=1000, null=True)               # 测试记录
    functionReportIsExist = models.CharField(max_length=1000, null=True)    # 功能报告是否存在
    reportIsExist = models.CharField(max_length=1000, null=True)            # 报告是否存在
    recordIsExist = models.CharField(max_length=1000, null=True)            # 记录是否存在
    testIsOK = models.CharField(max_length=1000, null=True)                 # 是否通过
    applyTime = models.CharField(max_length=200, null=True)                 # 申请时间
    testTime = models.CharField(max_length=200, null=True)                  # 测试时间
    releaseTime = models.CharField(max_length=200, null=True)               # 计划上线时间
    createTime = models.DateTimeField(db_column='createTime', null=True)    # 创建时间，前端过滤当年的
    updateTime = models.DateTimeField(db_column='updateTime', null=True)    # 修改时间
    updatePeople = models.CharField(max_length=200, null=True)              # 修改人
    isDelete = models.CharField(max_length=100)   # 是否可删除


# class ApplyManage(models.Model):
#
#     overhaulId = models.CharField(max_length=100, primary_key=True, unique=True)   # 渗透编号
#     testStyle = models.CharField(max_length=100, null=True)                 # 测试类型
#     systemName = models.CharField(max_length=100, null=True)               # 系统名称
#     systemVersion = models.CharField(max_length=100, null=True)            # 系统版本
#     functionNum = models.IntegerField(null=True)                           # 功能个数
#     functionList = models.CharField(max_length=100, null=True)             # 功能列表
#     vulnNum = models.CharField(max_length=100, null=True)                  # 漏洞个数
#     vulnDetail = models.CharField(max_length=100, null=True)               # 漏洞描述
#     overhaulContent = models.CharField(max_length=100, null=True)          # 检修内容
#     developCompany = models.CharField(max_length=200, null=True)           # 开发单位
#     applyName = models.CharField(max_length=200, null=True)                 # 申请人
#     applyPhone = models.CharField(max_length=200, null=True)                # 申请人联系方式
#     projectBossName = models.CharField(max_length=200, null=True)           # 项目经理
#     projectBossPhone = models.CharField(max_length=200, null=True)          # 项目经理联系方式
#     functionTestName = models.CharField(max_length=200, null=True)          # 功能测试联系人
#     PenetrationTestName = models.CharField(max_length=200, null=True)       # 渗透测试联系人
#     testUserName = models.CharField(max_length=200, null=True)              # 测试账号
#     testPassword = models.CharField(max_length=200, null=True)              # 测试密码
#     testURL = models.CharField(max_length=200, null=True)                   # 测试地址
#     functionReportPath = models.CharField(max_length=1000, null=True)       # 功能报告
#     reportPath = models.CharField(max_length=1000, null=True)               # 测试报告
#     recordPath = models.CharField(max_length=1000, null=True)               # 测试记录
#     functionReportIsExist = models.CharField(max_length=1000, null=True)    # 功能报告是否存在
#     reportIsExist = models.CharField(max_length=1000, null=True)            # 报告是否存在
#     recordIsExist = models.CharField(max_length=1000, null=True)            # 记录是否存在
#     testIsOK = models.CharField(max_length=1000, null=True)                 # 是否通过
#     applyTime = models.CharField(max_length=200, null=True)                 # 申请时间
#     testTime = models.CharField(max_length=200, null=True)                  # 测试时间
#     releaseTime = models.CharField(max_length=200, null=True)               # 计划上线时间
#     createTime = models.DateTimeField(db_column='createTime', null=True)    # 创建时间，前端过滤当年的
#     updateTime = models.DateTimeField(db_column='updateTime', null=True)    # 修改时间
#     updatePeople = models.CharField(max_length=200, null=True)              # 修改人
#     isDelete = models.CharField(max_length=100)   # 是否可删除




# class TroubleManage(models.Model):
#     vulhubName = models.CharField(max_length=100, null=True)
#
#     isDelete = models.BooleanField(default=False)   # 是否可删除
#
#
#
# class SupervisionManage(models.Model):
#     cnvdNumber = models.CharField(max_length=1000, null=True)
#
#     isDelete = models.BooleanField(default=False)   # 是否可删除

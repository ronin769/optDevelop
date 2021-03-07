from django.shortcuts import render

# Create your views here.
from django.db import models
import mongoengine


# apt install mysql
# from tinymce.models import HTMLField
# pip3 install django-tinymce
# 先生成应用 python3 manage.py startapp Assets --fake
# 设置数据里 setting
# 创建空数据库 create schema  `optmanager` DEFAULT CHARACTER SET utf8;
# setting 中加入应用名'booktest'
# 定义以下类之后生成迁移 python3 manage.py makemigrations ，自动生成 00001_initial.py，为数据库
# 迁移 python3 manage.py migrate
# 当执行 python manage.py makemigrations 出现错误：TypeError: init() missing 1 required positional argument: ‘on_delete’
#   添加 book = models.ForeignKey('BookInfo', on_delete=models.CASCADE)
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


class CopartnershipManage(models.Model):
    companyName = models.CharField(max_length=1000, null=True)      # 公司名称
    systemName = models.CharField(max_length=100, null=True)        # 系统名称  主键
    IP = models.CharField(max_length=100, null=True)                # IP地址
    domain = models.CharField(max_length=100, null=True)            # 域名
    portService = models.CharField(max_length=2000, null=True)      # 端口及服务
    information = models.CharField(max_length=100, null=True)       # 敏感信息
    isdesensitization = models.CharField(max_length=100, null=True) # 是否脱敏
    securityPeopleNum = models.CharField(max_length=100, null=True) # 安全人数
    testCycle = models.CharField(max_length=100, null=True)         # 检查周期
    userSize = models.CharField(max_length=100, null=True)          # 用户规模
    systemSize = models.CharField(max_length=100, null=True)        # 系统规模
    deployPoint = models.CharField(max_length=100, null=True)       # 部署位置
    securityTest = models.CharField(max_length=1000, null=True)     # 安全测评
    testResult = models.CharField(max_length=1000, null=True)       # 测评结果
    systemType = models.CharField(max_length=100, null=True)        # 系统类型
    defensivePower = models.CharField(max_length=100, null=True)    # 安全防御能力
    systemStatus = models.CharField(max_length=100, null=True)      # 系统状态
    accessURL = models.CharField(max_length=1000, null=True)        # 访问URL
    developmentCompany = models.CharField(max_length=1000, null=True)  # 开发单位
    extranetAccess = models.CharField(max_length=100, null=True)    # 外网访问
    businessPeople = models.CharField(max_length=100, null=True)    # 业务联系人
    businessPhone = models.CharField(max_length=100, null=True)     # 业务联系方式
    DevelopPeople = models.CharField(max_length=100, null=True)     # 开发联系人
    DevelopPhone = models.CharField(max_length=100, null=True)      # 开发联系方式
    systemCommon = models.CharField(max_length=2000, null=True)     # 备注
    systemDescribe = models.CharField(max_length=2000, null=True)   # 系统简介
    deployTime = models.CharField(max_length=200, null=True)        # 部署时间
    createTime = models.DateTimeField(max_length=100, null=True)    # 创建时间
    updateTime = models.DateTimeField(max_length=100, null=True)    # 修改时间
    createPeople = models.CharField(max_length=100, null=True)      # 创建人
    systemUsername = models.CharField(max_length=100, null=True)    # 账号
    systemPassword = models.CharField(max_length=100, null=True)    # 密码
    isDelete = models.BooleanField(default=False)                   # 是否可删除

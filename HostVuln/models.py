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


class HostVulnManage(models.Model):
    vulnName = models.CharField(max_length=1000, null=True)   # 漏洞名称
    urgent = models.CharField(max_length=1000, null=True)   # 修复紧急度
    assetId = models.CharField(max_length=1000, null=True)   # 影响资产ID
    assetPublicIP = models.CharField(max_length=1000, null=True)   # 影响资产IP（公网）
    assetPrivateIP = models.CharField(max_length=1000, null=True)   # 影响资产IP（私网）
    assetRemarks = models.CharField(max_length=1000, null=True)   # 影响资产备注名称
    firstFindTime = models.DateTimeField(max_length=100, null=True)   # 首次发现时间
    lastFindTime = models.DateTimeField(max_length=100, null=True)   # 最近一次发现时间
    vulnExplain = models.CharField(max_length=2000, null=True)   # 漏洞说明
    vulnStatus = models.CharField(max_length=1000, null=True)   # 漏洞状态
    repairCommand = models.CharField(max_length=1000, null=True)   # 修复命令
    CVEID = models.CharField(max_length=2000, null=True)   # CVE编号
    label = models.CharField(max_length=1000, null=True)   # 标签
    createTime = models.DateTimeField(max_length=100, null=True)        # 创建时间
    updateTime = models.DateTimeField(max_length=100, null=True)        # 修改时间
    createPeople = models.CharField(max_length=100, null=True)          # 创建人
    isDelete = models.BooleanField(default=False)                       # 是否可删除




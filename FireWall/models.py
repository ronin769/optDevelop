from django.db import models

# apt install mysql
# from tinymce.models import HTMLField
# pip3 install django-tinymce
# 先生成应用 python3 manage.py startapp NewFireWall
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

class FireWallFile(models.Model):
    filePath = models.CharField(max_length=500, null=True)     # 文件路径
    fileName = models.CharField(max_length=1000, null=True)     # 文件名字
    fileData = models.CharField(max_length=1000, null=True)     # 文件上传时间
    fileType = models.CharField(max_length=1000, null=True)     # 文件类型
    isDelete = models.BooleanField(default=False)   # 是否可删除

class PolicyManage(models.Model):
    ruleId = models.CharField(max_length=1000, null=True)           # 序号
    ruleName = models.CharField(max_length=1000, null=True)         # 规则名
    ruleSa = models.CharField(max_length=1000, null=True)           # 源地址
    ruleDa = models.CharField(max_length=1000, null=True)           # 目的地址
    ruleIzone = models.CharField(max_length=1000, null=True)        # 流入安全域
    ruleOzone = models.CharField(max_length=1000, null=True)        # 流出安全域
    ruleService = models.CharField(max_length=1000, null=True)      # 服务
    ruleOpentime = models.CharField(max_length=1000, null=True)     # 开通时间
    ruleStatus = models.CharField(max_length=1000, null=True)       # 生效
    ruleActive = models.CharField(max_length=1000, null=True)       # 动作
    ruleComment = models.CharField(max_length=1000, null=True)      # 操作
    ruleAccount = models.CharField(max_length=1000, null=True)      # 命中数
    isDelete = models.BooleanField(default=False)       # 是否可删除

class AddrgrpName(models.Model):
    addrgrpName = models.CharField(max_length=1000, null=True)
    addrgrpMember = models.CharField(max_length=1000, null=True)
    addrgrpComment = models.CharField(max_length=1000, null=True)
    isDelete = models.BooleanField(default=False)   # 是否可删除

class AddressName(models.Model):
    addressName = models.CharField(max_length=1000, null=True)
    addressIP = models.CharField(max_length=10000, null=True)
    addressComment = models.CharField(max_length=1000, null=True)
    isDelete = models.BooleanField(default=False)   # 是否可删除

class ServiceName(models.Model):
    serviceName = models.CharField(max_length=1000, null=True)
    serviceProtocol = models.CharField(max_length=1000, null=True)
    serviceComment = models.CharField(max_length=1000, null=True)
    isDelete = models.BooleanField(default=False)   # 是否可删除




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

class NewFireWallFile(models.Model):
    newFilePath = models.CharField(max_length=500, null=True)     # 文件路径
    newFileName = models.CharField(max_length=1000, null=True)     # 文件名字
    newFileData = models.CharField(max_length=1000, null=True)     # 文件上传时间
    newFileType = models.CharField(max_length=1000, null=True)     # 文件类型
    isDelete = models.BooleanField(default=False)   # 是否可删除

class NewPolicyManage(models.Model):
    newRuleId = models.CharField(max_length=1000, null=True)           # 序号
    newRuleName = models.CharField(max_length=1000, null=True)         # 规则名
    newRuleSa = models.CharField(max_length=1000, null=True)           # 源地址
    newRuleDa = models.CharField(max_length=1000, null=True)           # 目的地址
    newRuleIzone = models.CharField(max_length=1000, null=True)        # 流入安全域
    newRuleOzone = models.CharField(max_length=1000, null=True)        # 流出安全域
    newRuleService = models.CharField(max_length=1000, null=True)      # 服务
    newRuleOpentime = models.CharField(max_length=1000, null=True)     # 开通时间
    newRuleStatus = models.CharField(max_length=1000, null=True)       # 生效
    newRuleActive = models.CharField(max_length=1000, null=True)       # 动作
    newRuleComment = models.CharField(max_length=1000, null=True)      # 操作
    newRuleAccount = models.CharField(max_length=1000, null=True)      # 命中数
    isDelete = models.BooleanField(default=False)       # 是否可删除

class NewAddrgrpName(models.Model):
    newAddrgrpName = models.CharField(max_length=1000, null=True)
    newAddrgrpMember = models.CharField(max_length=1000, null=True)
    newAddrgrpComment = models.CharField(max_length=1000, null=True)
    isDelete = models.BooleanField(default=False)   # 是否可删除

class NewAddressName(models.Model):
    newAddressName = models.CharField(max_length=1000, null=True)
    newAddressIP = models.CharField(max_length=10000, null=True)
    newAddressComment = models.CharField(max_length=1000, null=True)
    isDelete = models.BooleanField(default=False)   # 是否可删除

class NewServiceName(models.Model):
    newServiceName = models.CharField(max_length=1000, null=True)
    newServiceProtocol = models.CharField(max_length=1000, null=True)
    newServiceComment = models.CharField(max_length=1000, null=True)
    isDelete = models.BooleanField(default=False)   # 是否可删除




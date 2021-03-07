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

class VulnerabilityManage(models.Model):

    # 我们在前端显示的是"男"、"女"、"保密"，而不是1、2、3，则需要拿到这张表的对象（obj），使用 obj.get_字段名_display() 即可。
    # gender_choices = (
    #     (1, "男"),
    #     (2, "女"),
    #     (3, "保密"))
    # gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    # obj = models.UserInfo.objects.filter(pk=1).first()
    # obj.get_gender_display()
    vulnNoticeFileId = models.CharField(max_length=100, primary_key=True, unique=True)            # 通知单编号，后台调取
    vulnNoticeFileName = models.CharField(max_length=100, null=True)            # 通知单名称，后台调取
    vulnDomain = models.CharField(max_length=200, null=True)                    # 漏洞域名
    vulnSystemName = models.CharField(max_length=100, null=True)                # 系统名称，后台调取
    businessPeople = models.CharField(max_length=100, null=True)                # 项目经理，后台调取
    DevelopPeople = models.CharField(max_length=100, null=True)                 # 开发人员，后台调取
    vulnTestName = models.CharField(max_length=100, null=True)                  # 测试人员
    vulnType = models.CharField(max_length=100, null=True)                      # 漏洞名称
    vulnLevel = models.CharField(max_length=100, null=True)                     # 漏洞级别，和漏洞名称绑定
    vulnCount = models.IntegerField(null=True)                                  # 漏洞个数，由后台计算
    vulnDetail = models.CharField(max_length=1000, null=True)                   # 漏洞描述，由漏洞个数，漏洞名称和漏洞类型计算得到
    vulnDevelopCompany = models.CharField(max_length=200, null=True)            # 开发单位，后台调取
    vulnIsNotice = models.CharField(max_length=100, null=True)                  # 是否下发通知单，按钮，由是否存在文件判断
    vulnIsFeedback = models.CharField(max_length=100, null=True)                # 是否收到反馈，按钮，由是否存在文件判断
    vulnNoticeWordPath = models.CharField(max_length=1000, null=True)           # 通知单路径
    vulnNoticePdfPath = models.CharField(max_length=1000, null=True)            # 通知单路径
    vulnFeedbackPath = models.CharField(max_length=1000, null=True)             # 反馈单路径
    vulnRetestPath = models.CharField(max_length=1000, null=True)               # 复测报告路径
    vulnIsRetest = models.CharField(max_length=100, null=True)                  # 是否进行复测，按钮，由是否存在文件判断
    vulnIsEepair = models.CharField(max_length=100, null=True)                  # 复测是否通过，按钮
    vulncreateTime = models.DateTimeField(db_column='createTime', null=True)    # 创建时间，前端过滤当年的
    vulnupdateTime = models.DateTimeField(db_column='updateTime', null=True)    # 修改时间
    vulncreatePeople = models.CharField(max_length=100, null=True)              # 创建人员
    vulnupdatePeople = models.CharField(max_length=100, null=True)              # 修改人员
    isDelete = models.CharField(max_length=100)   # 是否可删除

class VulhubManage(models.Model):
    vulhubName = models.CharField(max_length=100, null=True)
    vulhubApp = models.CharField(max_length=100, null=True)   # 中间件名称
    vulhubCVE = models.CharField(max_length=100, null=True)   # CVE编号
    vulhubPath = models.CharField(max_length=100, null=True)  # 漏洞路径
    vulhubOption = models.BooleanField(default=False, null=True)  # 漏洞处理
    vulhubdetail = models.CharField(max_length=500, null=True)    # 漏洞详情
    vulhubStatus = models.BooleanField(default=False, null=True)  # 漏洞开启状态
    isDelete = models.BooleanField(default=False)   # 是否可删除

class CnvdManage(models.Model):
    cnvdNumber = models.CharField(max_length=1000, null=True)
    cveNumber = models.CharField(max_length=1000, null=True)
    cveUrl = models.CharField(max_length=1000, null=True)
    cnvdTitle = models.CharField(max_length=1000, null=True)
    cnvdServerity = models.CharField(max_length=100, null=True)
    cnvdProducts = models.TextField(max_length=65535, null=True)
    cnvdIsEvent = models.CharField(max_length=1000, null=True)
    cnvdSubmitTime = models.CharField(max_length=1000, null=True)
    cnvdOpenTime = models.CharField(max_length=1000, null=True)
    cnvdDiscovererName = models.CharField(max_length=1000, null=True)
    cnvdReferenceLink = models.CharField(max_length=1000, null=True)
    cnvdFormalWay = models.TextField(max_length=65535, null=True)
    cnvdDescription = models.CharField(max_length=1000, null=True)
    cnvdPatchName = models.CharField(max_length=1000, null=True)
    cnvdPatchDescription = models.CharField(max_length=1000, null=True)
    isDelete = models.BooleanField(default=False)   # 是否可删除

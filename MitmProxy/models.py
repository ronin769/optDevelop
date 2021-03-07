# from tinymce.models import HTMLField
import mongoengine
# from mongoengine import Document, StringField

# from __future__ import unicode_literals

# from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField


# apt install mongodb
# pip3 install mongoengine
# pip3 install django-tinymce
# 先生成应用 python3 manage.py startapp MitmProxy
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



# Create your models here.

# mongoengine.connect('optmongodb',host = '127.0.0.1',port = 27017)
from rest_framework import serializers, viewsets, response


# apt install postgresql-server-dev-all
# apt install postgresql-client
# apt install postgresql-server-dev-10
# Python 3 versions from 3.4 to 3.8
# PostgreSQL server versions from 7.4 to 12
# PostgreSQL client library version from 9.1
# apt-get install python3.6-dev




class RequestManage(mongoengine.Document):
    try:
        text = mongoengine.StringField(max_length=1000000, null=True)
    except ValidationError as e:
        text = None
    try:
        cookies = mongoengine.DictField(max_length=1000, null=True)
    except ValidationError as e:
        cookies = None
    try:
        get_state = mongoengine.DictField(max_length=5000, null=True)
    except ValidationError as e:
        get_state = None
    try:
        method = mongoengine.StringField(max_length=1000, null=True)
    except ValidationError as e:
        method = None
    try:
        port = mongoengine.IntField(max_length=1000, null=True)
    except ValidationError as e:
        port = None
    try:
        pretty_url = mongoengine.StringField(max_length=10000, null=True)
    except ValidationError as e:
        pretty_url = None
    try:
        pretty_host = mongoengine.StringField(max_length=1000, null=True)
    except ValidationError as e:
        pretty_host = None
    try:
        path = mongoengine.StringField(max_length=10000, null=True)
    except ValidationError as e:
        path = None
    try:
        path_components = mongoengine.ListField(max_length=1000, null=True)
    except ValidationError as e:
        path_components = None
    # try:
    #     query = mongoengine.DictField(max_length=1000, null=True)
    # except ValidationError as e:
    #     query = None
    try:
        raw_content = mongoengine.BinaryField(max_length=1000, null=True)
    except ValidationError as e:
        raw_content = None
    try:
        stream = mongoengine.StringField(max_length=1000, null=True)
    except ValidationError as e:
        stream = None
    try:
        timestamp_end = mongoengine.FloatField(max_length=1000, null=True)
    except ValidationError as e:
        timestamp_end = None
    try:

        timestamp_start = mongoengine.FloatField(max_length=1000, null=True)
    except ValidationError as e:
        timestamp_start = None
    try:
        urlencoded_form = mongoengine.DictField(max_length=10000, null=True)
    except ValidationError as e:
        urlencoded_form = {}

    # 指明连接的数据表名
    meta = {'collection': 'RequestModel'}
    # def __unicode__(self):
    #     return self.name

class ResponseManage(mongoengine.Document):

    timestamp_start = mongoengine.FloatField(max_length=1000, null=True)
    timestamp_end = mongoengine.FloatField(max_length=1000, null=True)
    stream = mongoengine.StringField(max_length=1000, null=True)
    is_replay = mongoengine.BooleanField(max_length=1000, null=True)
    http_version = mongoengine.StringField(max_length=1000, null=True)
    headers = mongoengine.DictField(max_length=5000, null=True)
    reason = mongoengine.StringField(max_length=1000, null=True)
    status_code = mongoengine.IntField(max_length=1000, null=True)
    text = mongoengine.StringField(max_length=500000, null=True)

    # url = models.ForeignKey(
    #     RequestModel,
    #     related_name="inputs",
    #     on_delete=models.CASCADE )
    # 指明连接的数据表名
    meta = {'collection': 'ResponseModel'}
    # def __unicode__(self):
    #     return self.name


# class Post(models.Model):
#     # ....省略之前的字段
#     # 添加 author 字段，author 我们使用 django 自带的 User 类，
#     # 我们通过 ForeignKey 进行关联两个 Model，related_name 为反向引用，
#     # 即我们在 RequestModel 表内可以通过 related_name 的值来引用 post 对象
#     author = models.ForeignKey(RequestModel, related_name='posts', on_delete=models.CASCADE)
#

# class Tool(models.Model):
#     label = models.CharField(
#         max_length=1024,
#         null=True,
#         blank=True
#     )
#
#     description = models.TextField(null=True, blank=True)
#
#
# class ToolInput(models.Model):
#     tool = models.ForeignKey(
#         Tool,
#         related_name="inputs",
#         on_delete=models.CASCADE )
#
#     # name = models.CharField(max_length=1024, null=True, blank=True)
#
#     value = JSONField(null=True, blank=True)
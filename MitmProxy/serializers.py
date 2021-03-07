#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''

# pip3 install django-rest-framework-mongoengine
# pip3 install djangorestframework


from rest_framework import serializers
from .models import *

class RequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RequestManage
        fields = '__all__'

class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    inputs = RequestSerializer(many=True)

    class Meta:
        model = ResponseManage
        fields = ('label', 'description', 'inputs')
#
# class UserSerializer(serializers.ModelSerializer):
#     # posts 字段是反向引用，必须要显示声明出来才可以
#     posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'posts']
#
# class PostSerializer(serializer.ModelSerializer):
#     # 显示 author 中的某个字段，例如 username，我们可以通过 source 参数设置
#     author = serializer.ReadOnlyField(source='author.usernam')
#
#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'body', 'excerpt', 'author', 'create_time', 'modified_time']
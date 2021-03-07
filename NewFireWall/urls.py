from django.urls import path, re_path, include
from . import views

# 定义自己的 URL
urlpatterns = [
    # path('/', views.index, name='index'),
    # 第二个参数叫 name，是为了给当前 path 起名字，用于反向解析
    path('/', views.newService, name='NewFirewall'),  # path 不识别正则
    path('newService/', views.newService, name='newService'),  # path 不识别正则
    path('newAddress/', views.newAddress, name='newAddress'),  # path 不识别正则
    path('newPolicy/', views.newPolicy, name='newPolicy'),  # path 不识别正则
    path('uploadnewService/', views.uploadnewService, name='uploadnewService'),  # path 不识别正则
    path('uploadnewAddress/', views.uploadnewAddress, name='uploadnewAddress'),  # path 不识别正则
    path('uploadnewPolicy/', views.uploadnewPolicy, name='uploadnewPolicy'),  # path 不识别正则
    path('uploadhitnumber/', views.uploadhitnumber, name='uploadhitnumber'),  # path 不识别正则
    path('getnewServicelist/', views.getnewServicelist, name='getnewServicelist'),  # path 不识别正则
    path('getnewAddresslist/', views.getnewAddresslist, name='getnewAddresslist'),  # path 不识别正则
    path('getnewPolicylist/', views.getnewPolicylist, name='getnewPolicylist'),  # path 不识别正则
    path('getsourceip/', views.getsourceip, name='getsourceip'),  # path 不识别正则
    path('getdirectionip/', views.getdirectionip, name='getdirectionip'),  # path 不识别正则
    path('getrulenewService/', views.getrulenewService, name='getrulenewService'),  # path 不识别正则
    path('deletenewServiceall/', views.deletenewServiceall, name='deleteNewFirewallall'),  # path 不识别正则
    path('deletenewAddressall/', views.deletenewAddressall, name='deletenewAddressall'),  # path 不识别正则
    path('deletenewPolicyall/', views.deletenewPolicyall, name='deletenewPolicyall'),  # path 不识别正则
    path('initnewService/', views.initnewService, name='initNewFirewall'),  # path 不识别正则
    path('initnewAddress/', views.initnewAddress, name='initnewAddress'),  # path 不识别正则
    path('initnewPolicy/', views.initnewPolicy, name='initnewPolicy'),  # path 不识别正则
    path('searchnewService/', views.searchnewService, name='searchnewService'),  # path 不识别正则
    path('searchnewAddress/', views.searchnewAddress, name='searchnewAddress'),  # path 不识别正则
    path('searchnewPolicy/', views.searchnewPolicy, name='searchnewPolicy'),  # path 不识别正则
    path('downloadNewFireWallTemplateFile/', views.downloadNewFirewallTemplateFile, name='downloadNewFirewallTemplateFile'),  # path 不识别正则


]

from django.urls import path, re_path, include
from FireWall import views

# 定义自己的 URL
urlpatterns = [
    # path('/', views.index, name='index'),
    # 第二个参数叫 name，是为了给当前 path 起名字，用于反向解析
    path('/', views.service, name='firewall'),  # path 不识别正则
    path('service/', views.service, name='service'),  # path 不识别正则
    path('address/', views.address, name='address'),  # path 不识别正则
    path('policy/', views.policy, name='policy'),  # path 不识别正则
    path('uploadService/', views.uploadService, name='uploadService'),  # path 不识别正则
    path('uploadaddress/', views.uploadaddress, name='uploadaddress'),  # path 不识别正则
    path('uploadpolicy/', views.uploadpolicy, name='uploadpolicy'),  # path 不识别正则
    path('uploadhitnumber/', views.uploadhitnumber, name='uploadhitnumber'),  # path 不识别正则
    path('getservicelist/', views.getservicelist, name='getservicelist'),  # path 不识别正则
    path('getaddresslist/', views.getaddresslist, name='getaddresslist'),  # path 不识别正则
    path('getpolicylist/', views.getpolicylist, name='getpolicylist'),  # path 不识别正则
    path('getsourceip/', views.getsourceip, name='getsourceip'),  # path 不识别正则
    path('getdirectionip/', views.getdirectionip, name='getdirectionip'),  # path 不识别正则
    path('getruleservice/', views.getruleservice, name='getruleservice'),  # path 不识别正则
    path('deleteserviceall/', views.deleteserviceall, name='deletefirewallall'),  # path 不识别正则
    path('deleteaddressall/', views.deleteaddressall, name='deleteaddressall'),  # path 不识别正则
    path('deletepolicyall/', views.deletepolicyall, name='deletepolicyall'),  # path 不识别正则
    path('initservice/', views.initservice, name='initfirewall'),  # path 不识别正则
    path('initaddress/', views.initaddress, name='initaddress'),  # path 不识别正则
    path('initpolicy/', views.initpolicy, name='initpolicy'),  # path 不识别正则
    path('searchservice/', views.searchservice, name='searchservice'),  # path 不识别正则
    path('searchaddress/', views.searchaddress, name='searchaddress'),  # path 不识别正则
    path('searchpolicy/', views.searchpolicy, name='searchpolicy'),  # path 不识别正则
    path('downloadFirewallTemplateFile/', views.downloadFirewallTemplateFile, name='downloadFirewallTemplateFile'),  # path 不识别正则


]

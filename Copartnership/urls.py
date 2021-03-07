from django.urls import path, re_path, include
from Copartnership import views

# 定义自己的 URL
urlpatterns = [
    # path('/', views.index, name='index'),
    # 第二个参数叫 name，是为了给当前 path 起名字，用于反向解析
    path('/', views.index, name='index'),
    path('copartnership/', views.copartnershipManage, name='copartnership'),
    path('addCopartnershippage/', views.addCopartnershippage, name='addCopartnershippage'),

    path('getCopartnershiplist/', views.getCopartnershiplist, name='getCopartnershiplist'),
    # path('getdomainlist/', views.getDomainlist, name='getdomainlist'),
    path('deleteCopartnershipall/', views.deleteCopartnershipall, name='deleteCopartnershipall'),
    # path('deletedomainall/', views.deleteDomainAll, name='deletedomainall'),
    # path('deletevulnall/', views.deleteVulnall, name='deletevulnall'),
    path('uploadCopartnershipfile/', views.uploadCopartnershipfile, name='uploadCopartnershipfile'),
    # path('uploadvulnfile/', views.uploadVulnfile, name='uploadvulnfile'),
    # path('uploaddomainfile/', views.uploadDomainfile, name='uploaddomainfile'),
    path('searchCopartnership/', views.searchCopartnership, name='searchCopartnership'),
    # path('searchvuln/', views.searchvuln, name='searchvuln'),
    # path('searchdomain/', views.searchDomain, name='searchdomain'),
    # path('initecs/', views.initECSfile, name='initecs'),
    # path('initvuln/', views.initVulnfile, name='initvuln'),
    # path('initdomain/', views.initDomainfile, name='initdomain'),
    # path('deletedomainforline/', views.deleteDomainForLine, name='deletedomainforline'),
    path('editCopartnershipsubmit/', views.editCopartnershipsubmit, name='editCopartnershipsubmit'),
    path('downloadCopartnershipTemplateFile/', views.downloadCopartnershipTemplateFile, name='downloadCopartnershipTemplateFile'),
    path('downloadCopartnershipAllToFile/', views.downloadCopartnershipAllToFile, name='downloadCopartnershipAllToFile'),
    # path('downloadDomainTemplateFile/', views.downloadDomainTemplateFile, name='downloadDomainTemplateFile'),
    # path('downloadDomainAllToFile/', views.downloadDomainAllToFile, name='downloadDomainAllToFile'),


    #
    path('addcopartnershipsubmit/', views.addcopartnershipsubmit, name='addcopartnershipsubmit'),





]

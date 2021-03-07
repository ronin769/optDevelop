from django.urls import path, re_path, include
from HostVuln import views

# 定义自己的 URL
urlpatterns = [
    # path('/', views.index, name='index'),
    # 第二个参数叫 name，是为了给当前 path 起名字，用于反向解析
    path('/', views.index, name='index'),
    path('hostVuln/', views.hostVuln, name='hostVuln'),
    path('getHostVulnlist/', views.getHostVulnlist, name='getHostVulnlist'),
    path('deleteHostVulnall/', views.deleteHostVulnall, name='deleteHostVulnall'),
    path('uploadHostVulnfile/', views.uploadHostVulnfile, name='uploadHostVulnfile'),
    path('searchHostVuln/', views.searchHostVuln, name='searchHostVuln'),
    path('initHostVuln/', views.initHostVuln, name='initHostVuln'),
    path('deleteHostVulnforline/', views.deleteHostVulnforline, name='deleteHostVulnforline'),
    path('downloadHostVulnTemplateFile/', views.downloadHostVulnTemplateFile, name='downloadHostVulnTemplateFile'),
    path('downloadHostVulnAllToFile/', views.downloadHostVulnAllToFile, name='downloadHostVulnAllToFile'),
    path('addHostVulnsubmit/', views.addHostVulnsubmit, name='addHostVulnsubmit'),
    path('editHostVulnsubmit/', views.editHostVulnsubmit, name='editHostVulnsubmit'),


]

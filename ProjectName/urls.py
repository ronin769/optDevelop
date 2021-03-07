from django.urls import path, re_path, include
from ProjectName import views

# 定义自己的 URL
urlpatterns = [
    # path('/', views.index, name='index'),
    # 第二个参数叫 name，是为了给当前 path 起名字，用于反向解析
    path('/', views.index, name='index'),
    path('projectName/', views.projectName, name='project'),
    path('addProjectNamepage/', views.addProjectNamepage, name='addProjectNamepage'),

    path('getProjectNamelist/', views.getProjectNamelist, name='getProjectNamelist'),
    # path('getdomainlist/', views.getDomainlist, name='getdomainlist'),
    path('deleteProjectNameall/', views.deleteProjectNameall, name='deleteProjectNameall'),
    # path('deletedomainall/', views.deleteDomainAll, name='deletedomainall'),
    # path('deletevulnall/', views.deleteVulnall, name='deletevulnall'),
    path('uploadProjectNamefile/', views.uploadProjectNamefile, name='uploadProjectNamefile'),
    # path('uploadvulnfile/', views.uploadVulnfile, name='uploadvulnfile'),
    # path('uploaddomainfile/', views.uploadDomainfile, name='uploaddomainfile'),
    path('searchProjectName/', views.searchProjectName, name='searchProjectName'),
    # path('searchvuln/', views.searchvuln, name='searchvuln'),
    # path('searchdomain/', views.searchDomain, name='searchdomain'),
    path('initProjectName/', views.initProjectName, name='initProjectName'),
    # path('initvuln/', views.initVulnfile, name='initvuln'),
    # path('initdomain/', views.initDomainfile, name='initdomain'),
    path('deleteProjectNameforline/', views.deleteProjectNameforline, name='deleteProjectNameforline'),
    path('downloadProjectNameTemplateFile/', views.downloadProjectNameTemplateFile, name='downloadProjectNameTemplateFile'),
    path('downloadProjectNameAllToFile/', views.downloadProjectNameAllToFile, name='downloadProjectNameAllToFile'),
    # path('downloadDomainTemplateFile/', views.downloadDomainTemplateFile, name='downloadDomainTemplateFile'),
    # path('downloadDomainAllToFile/', views.downloadDomainAllToFile, name='downloadDomainAllToFile'),


    path('addProjectNamesubmit/', views.addProjectNamesubmit, name='addProjectNamesubmit'),
    path('editProjectNamesubmit/', views.editProjectNamesubmit, name='editProjectNamesubmit'),





]

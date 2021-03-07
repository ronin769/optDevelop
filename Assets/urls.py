from django.urls import path, re_path, include
from Assets import views

# 定义自己的 URL
urlpatterns = [
    # path('/', views.index, name='index'),
    # 第二个参数叫 name，是为了给当前 path 起名字，用于反向解析
    path('/', views.index, name='index'),
    path('ecs/', views.ecsManage, name='ecs'),
    path('vuln/', views.vulnManage, name='vuln'),
    path('domain/', views.domainManage, name='domain'),
    path('produceFirewall/', views.produceFirewallManage, name='produceFirewall'),
    path('workFirewall/', views.workFirewallManage, name='workFirewall'),


    path('getvulnlist/', views.getVulnlist, name='getvulnlist'),
    path('deleteecsall/', views.deleteECSall, name='deleteecsall'),
    path('deletevulnall/', views.deleteVulnall, name='deletevulnall'),
    path('uploadecsfile/', views.uploadecsfile, name='uploadecsfile'),
    path('uploadvulnfile/', views.uploadVulnfile, name='uploadvulnfile'),
    path('searchECS/', views.searchECS, name='searchECS'),
    path('searchvuln/', views.searchvuln, name='searchvuln'),
    path('initecs/', views.initECSfile, name='initecs'),
    path('initvuln/', views.initVulnfile, name='initvuln'),
    path('deletedomainforline/', views.deleteDomainForLine, name='deletedomainforline'),
    path('downloadVulnTemplateFile/', views.downloadVulnTemplateFile, name='downloadVulnTemplateFile'),
    path('downloadEcsTemplateFile/', views.downloadEcsTemplateFile, name='downloadEcsTemplateFile'),

    path('getecsslbip/', views.getEcsSLBIP, name='getecsslbip'),
    path('getvulslbipanddomain/', views.getVulSLBipAndDomain, name='getvulslbipanddomain'),




    path('getEcsList/', views.getEcsList, name='getEcsList'),


    path('getProduceFirewallPolicyList/', views.getProduceFirewallPolicyList, name='getProduceFirewallPolicyList'),
    path('addProduceFirewallPolicySubmit/', views.addProduceFirewallPolicySubmit, name='addProduceFirewallPolicySubmit'),
    path('addProduceFirewallIPGroupSubmit/', views.addProduceFirewallIPGroupSubmit, name='addProduceFirewallIPGroupSubmit'),
    path('addProduceFirewallServiceGroupSubmit/', views.addProduceFirewallServiceGroupSubmit, name='addProduceFirewallServiceGroupSubmit'),
    path('downloadProduceFirewallPolicyAllToFile/', views.downloadProduceFirewallPolicyAllToFile, name='downloadProduceFirewallPolicyAllToFile'),
    path('downloadProduceFirewallPolicyTemplateFile/', views.downloadProduceFirewallPolicyTemplateFile, name='downloadProduceFirewallPolicyTemplateFile'),
    path('uploadproducefirewallpolicyfile/', views.uploadproducefirewallpolicyfile, name='uploadproducefirewallpolicyfile'),
    path('deleteProducefirewallpolicyfileAll/', views.deleteProducefirewallpolicyfileAll, name='deleteProducefirewallpolicyfileAll'),
    path('initproducefirewallpolicyfile/', views.initproducefirewallpolicyfile, name='initproducefirewallpolicyfile'),
    path('searchProduceFirewallPolicy/', views.searchProduceFirewallPolicy, name='searchProduceFirewallPolicy'),
    path('deleteProduceFirewallPolicyAll/', views.deleteProduceFirewallPolicyAll, name='deleteProduceFirewallPolicyAll'),


    path('getWorkFirewallPolicyList/', views.getWorkFirewallPolicyList, name='getWorkFirewallPolicyList'),
    path('addWorkFirewallPolicySubmit/', views.addWorkFirewallPolicySubmit, name='addWorkFirewallPolicySubmit'),
    path('downloadWorkFirewallPolicyAllToFile/', views.downloadWorkFirewallPolicyAllToFile, name='downloadWorkFirewallPolicyAllToFile'),
    path('downloadWorkFirewallPolicyTemplateFile/', views.downloadWorkFirewallPolicyTemplateFile, name='downloadWorkFirewallPolicyTemplateFile'),
    path('uploadworkfirewallpolicyfile/', views.uploadworkfirewallpolicyfile, name='uploadworkfirewallpolicyfile'),
    path('deleteWorkfirewallpolicyfileAll/', views.deleteWorkfirewallpolicyfileAll, name='deleteWorkfirewallpolicyfileAll'),
    path('initworkfirewallpolicyfile/', views.initworkfirewallpolicyfile, name='initworkfirewallpolicyfile'),


    path('getdomainlist/', views.getDomainlist, name='getdomainlist'),
    path('addDomainpage/', views.addDomainpage, name='addDomainpage'),
    path('addDomainsubmit/', views.addDomainSubmit, name='addDomainsubmit'),
    path('editDomainsubmit/', views.editDomainForLine, name='editDomainsubmit'),
    path('searchdomain/', views.searchDomain, name='searchdomain'),
    path('initdomain/', views.initDomainfile, name='initdomain'),
    path('deletedomainall/', views.deleteDomainAll, name='deletedomainall'),
    path('downloadDomainTemplateFile/', views.downloadDomainTemplateFile, name='downloadDomainTemplateFile'),
    path('downloadDomainAllToFile/', views.downloadDomainAllToFile, name='downloadDomainAllToFile'),
    path('uploaddomainfile/', views.uploadDomainfile, name='uploaddomainfile'),
    path('domainPocicyInit/', views.domainPocicyInit, name='domainPocicyInit'), # 初始化域名表中的防火墙策略, 必须在中再大厦访问


    path('addV2EcsSubmit/', views.addV2EcsSubmit, name='addV2EcsSubmit'),
    path('addV2SlbSubmit/', views.addV2SlbSubmit, name='addV2SlbSubmit'),
    path('addV3EcsSubmit/', views.addV3EcsSubmit, name='addV3EcsSubmit'),
    path('addV3SlbSubmit/', views.addV3SlbSubmit, name='addV3SlbSubmit'),



]

from django.urls import path, re_path, include
from VulnManage import views

# 定义自己的 URL
urlpatterns = [
    # path('', views.index, name='index'),
    # 第二个参数叫 name，是为了给当前 path 起名字，用于反向解析
    path('', views.index, name='index'),  # path 不识别正则
    path('vulnlist/', views.vulnlist, name='vulnlist'),  # path 不识别正则
    path('vulhublist/', views.vulhubList, name='vulhublist'),  # path 不识别正则
    path('cnvdvuln/', views.cnvdvuln, name='cnvdvuln'),  # path 不识别正则
    path('addvulndata/', views.addVulnData, name='addvulndata'),  # path 不识别正则
    path('addVulnsubmit/', views.addVulnsubmit, name='addVulnsubmit'),  # path 不识别正则
    path('addCnvdVulnDetail/', views.addCnvdVulnDetail, name='addCnvdVulnDetail'),  # path 不识别正则
    path('editvulnsubmit/', views.editVulnsubmit, name='editvulnsubmit'),  # path 不识别正则
    path('getvulndetail/', views.getVulnDetail, name='getvulndetail'),  # path 不识别正则
    path('getvulhubdetail/', views.getVulhubDetail, name='getvulhubdetail'),  # path 不识别正则
    path('getcnvdlist/', views.getCnvdList, name='getcnvdlist'),  # path 不识别正则


    path('createcnvdvuln/', views.createCnvdVuln, name='createcnvdvuln'),  # path 不识别正则
    path('initcnvdvuln/', views.initCnvdVuln, name='initcnvdvuln'),  # path 不识别正则
    path('initvulhublist/', views.initVulhubList, name='initvulhublist'),  # path 不识别正则
    path('initTroubleAll/', views.initTroubleAll, name='initTroubleall'),  # path 不识别正则



    path('deleteCnvdVulnAll/', views.deleteCnvdVulnAll, name='deleteCnvdVulnAll'),  # path 不识别正则
    path('deleteVulhubAll/', views.deleteVulhubAll, name='deleteVulhubAll'),  # path 不识别正则
    path('deletecnvdvulforline/', views.deleteCnvdvulForLine, name='deletecnvdvulforline'),  # path 不识别正则
    path('deletevulnforline/', views.deletevulnforline, name='deletevulnforline'),  # path 不识别正则


    path('deleteTroubleall/', views.deleteTroubleall, name='deleteTroubleall'),  # path 不识别正则



    path('editcnvdvulforline/', views.editCnvdvulForLine, name='editcnvdvulforline'),  # path 不识别正则
    path('searchcnvdpath/', views.searchcnvdpath, name='searchcnvdpath'),  # path 不识别正则
    path('searchvulnsubmit/', views.searchvulnsubmit, name='searchvulnsubmit'),  # path 不识别正则

    path('uploadWordVulnNoticeFile/', views.uploadWordVulnNoticeFile, name='uploadWordVulnNoticeFile'),  # path 不识别正则
    path('uploadPdfVulnNoticeFile/', views.uploadPdfVulnNoticeFile, name='uploadPdfVulnNoticeFile'),  # path 不识别正则
    path('uploadVulnFeedbackFile/', views.uploadVulnFeedbackFile, name='uploadVulnFeedbackFile'),  # path 不识别正则
    path('uploadVulnRetestFile/', views.uploadVulnRetestFile, name='uploadVulnRetestFile'),  # path 不识别正则
    path('uploadTroubleFileAll/', views.uploadTroubleFileAll, name='uploadTroubleFile'),  # path 不识别正则


    path('editvulnisnotice/', views.editVulnIsNotice, name='editvulnssnotice'),  # path 不识别正则
    path('editvulnisfeeedback/', views.editVulnIsFeedback, name='editvulnisfeeedback'),  # path 不识别正则
    path('editvulnisretest/', views.editVulnIsRetest, name='editvulnisretest'),  # path 不识别正则
    path('editvulnisrepire/', views.editVulnIsRepire, name='editvulnisrepire'),  # path 不识别正则

    path('downloadVulnNoticeWordPath/', views.downloadVulnNoticeWordPath, name='downloadVulnNoticeWordPath'),  # path 不识别正则
    path('downloadVulnNoticePdfPath/', views.downloadVulnNoticePdfPath, name='downloadVulnNoticePdfPath'),  # path 不识别正则
    path('downloadVulnFeedbackPath/', views.downloadVulnFeedbackPath, name='downloadVulnFeedbackPath'),  # path 不识别正则
    path('downloadVulnRetestPath/', views.downloadVulnRetestPath, name='downloadVulnRetestPath'),  # path 不识别正则
    path('downloadTroubleTemplateFile/', views.downloadTroubleTemplateFile, name='downloadTroubleTemplateFile'),  # path 不识别正则
    path('downloadTroubleAllToFile/', views.downloadTroubleAllToFile, name='downloadTroubleAllToFile'),  # path 不识别正则



    # path('content/', views.content, name='content'),  # path 不识别正则
    # path('editor/', views.editor, name='editor'),  # path 不识别正则
    # path('redisCache/', views.redisCache, name='redisCache'),  # path 不识别正则
    # path('cachetest1/', views.cachetest1, name='cachetest1'),  # path 不识别正则
    #
    # # path('mysearch/', views.mysearch, name='mysearch'),  # path 不识别正则
    # path('mysearch/', views.mysearch, name='mysearch'),  # path 不识别正则
    # path('search/', include('haystack.urls'))

    # path('myExp/', views.myExp, name='myExp'),  # path 不识别正则

    # re_path(r'(\d+)', views.detail, name='detail'),  # 正则需要用 re_path
    # re_path(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),   # 正则命名组
    # path('', views.home, name='home'),
]

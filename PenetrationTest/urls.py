from django.urls import path, re_path, include
from PenetrationTest import views

# 定义自己的 URL
urlpatterns = [
    # path('/', views.index, name='index'),
    # 第二个参数叫 name，是为了给当前 path 起名字，用于反向解析
    path('/', views.index, name='index'),  # path 不识别正则
    path('overhaul/', views.overhaulManage, name='overhaul'),  # path 不识别正则
    path('trouble/', views.troubleManage, name='trouble'),  # path 不识别正则
    path('supervision/', views.supervisionManage, name='supervision'),  # path 不识别正则


    path('getoverhaullist/', views.getoverhaullist, name='supervision'),  # path 不识别正则
    path('addoverhauldata/', views.addoverhauldata, name='addoverhauldata'),  # path 不识别正则
    path('addOverhaulSubmit/', views.addOverhaulSubmit, name='addOverhaulSubmit'),  # path 不识别正则
    path('editOverhaulSubmit/', views.editOverhaulSubmit, name='editOverhaulSubmit'),  # path 不识别正则
    path('uploadReportFile/', views.uploadReportFile, name='uploadReportFile'),  # path 不识别正则
    path('uploadFunctionReportFile/', views.uploadFunctionReportFile, name='uploadFunctionReportFile'),  # path 不识别正则
    path('uploadRecordFile/', views.uploadRecordFile, name='uploadRecordFile'),  # path 不识别正则
    path('uploadoverhaulfile/', views.uploadoverhaulfile, name='uploadoverhaulfile'),  # path 不识别正则
    path('editfunctionReportIsExist/', views.editfunctionReportIsExist, name='editfunctionReportIsExist'),  # path 不识别正则
    path('editreportIsExist/', views.editreportIsExist, name='editreportIsExist'),  # path 不识别正则
    path('editrecordIsExist/', views.editrecordIsExist, name='editrecordIsExist'),  # path 不识别正则
    path('edittestIsOK/', views.edittestIsOK, name='edittestIsOK'),  # path 不识别正则
    path('deleteoverhaulforline/', views.deleteoverhaulforline, name='deleteoverhaulforline'),  # path 不识别正则
    path('searchoverhaulsubmit/', views.searchoverhaulsubmit, name='searchoverhaulsubmit'),  # path 不识别正则
    path('deleteoverhaulall/', views.deleteoverhaulall, name='deleteoverhaulall'),  # path 不识别正则
    path('initoverhaul/', views.initoverhaul, name='initoverhaul'),  # path 不识别正则
    path('downloadOverhaulTemplateFile/', views.downloadOverhaulTemplateFile, name='downloadOverhaulTemplateFile'),  # path 不识别正则
    path('downloadOverhaulAllToFile/', views.downloadOverhaulAllToFile, name='downloadOverhaulAllToFile'),  # path 不识别正则
    path('downloadReportPath/', views.downloadReportPath, name='downloadReportPath'),  # path 不识别正则
    path('downloadRecordPath/', views.downloadRecordPath, name='downloadRecordPath'),  # path 不识别正则
    path('downloadFunctionReportPath/', views.downloadFunctionReportPath, name='downloadFunctionReportPath'),  # path 不识别正则



    # path('/', views.home, name='home'),
]

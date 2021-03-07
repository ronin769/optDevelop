from django.contrib import admin
from django.urls import path, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers


from django.urls import path, re_path, include
from MitmProxy import views
# from course.view import CourseView
from rest_framework.routers import DefaultRouter
# from rest_framework_mongoengine.routers import MongoRouterMixin
from rest_framework import routers, serializers, viewsets


# this is DRF router for REST API viewsets
router = routers.DefaultRouter()

# register REST API endpoints with DRF router
router.register(r'tool/', views.ToolViewSet, r"tool")



# 定义自己的 URL
urlpatterns = [

    path('api/', include((router.urls, "api"), namespace='api')),



    path('/', views.index, name='mitmstatus'),
    path('mitmstatus/', views.index, name='mitmstatus'),
    # path('openmimt/', views.OpenMimtAndWriteToMondodb, name='openmimt'),
    path('catchpathlist/', views.catchPathList, name='catchpathlist'),
    path('getpathjson/', views.getPathJson, name='getpathjson'),
    path('searchpath/', views.searchPathJson, name='searchpath'),
    path('pathlistremoveduplicate/', views.pathListRemoveDuplicate, name='pathlistremoveduplicate'),
    path('getpathjsonremoveduplicate/', views.getPathJsonRemoveDuplicate, name='getpathjsonremoveduplicate'),

]
"""optDevelop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path, re_path
from django.views import static     ##新增
from django.conf import settings    ##新增
from django.conf.urls import url    ##新增
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('RBAC.urls')),
    # path('index/', include('RBAC.urls')),
    path('user/', include('RBAC.urls')),
    path('VulnManage/', include('VulnManage.urls')),
    path('MitmProxy/', include('MitmProxy.urls')),
    path('FireWall/', include('FireWall.urls')),
    path('NewFireWall/', include('NewFireWall.urls')),
    path('Assets/', include('Assets.urls')),
    path('PenetrationTest/', include('PenetrationTest.urls')),
    path('Copartnership/', include('Copartnership.urls')),
    path('ProjectName/', include('ProjectName.urls')),
    path('HostVuln/', include('HostVuln.urls')),



    # # 以下是新增
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),



]
handler403 = views.forbidden
handler404 = views.notFount
handler500 = views.serverError

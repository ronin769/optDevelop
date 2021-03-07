from django.urls import path, re_path, include
from RBAC import views

# 定义自己的 URL
urlpatterns = [
    path('', views.index, name='index'),    # index 页面是大框
    path('index/', views.index, name='index'),    # index 页面是大框
    path('welcome/', views.welcome1, name='welcome1'),  # 首页是 welcome1


    path('accounts/login/', views.login, name='login'),


    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('registersubmit/', views.registerSubmit, name='registersubmit'),
    path('loginsubmit/', views.loginSubmit, name='loginsubmit'),
    path('logoutsubmit/', views.logoutSubmit, name='logoutsubmit'),
    path('logoutsubmit/', views.logoutSubmit, name='logoutsubmit'),
    path('changepasswd/', views.changePasswd, name='changepasswd'),
    path('changepasswdsubmit/', views.changePasswdSubmit, name='changepasswdsubmit'),
    path('loginRequired/', views.loginRequired, name='loginRequired'),
    path('changeusersetting/', views.changeUserSetting, name='changeusersetting'),




    path('tecentmap/', views.tecentmap, name='tecentmap'),
    path('luckincoffee/', views.luckincoffee, name='luckincoffee'),
    path('getPhone/', views.getPhone, name='getPhone'),
    path('getTecentMap/', views.getTecentMap, name='getTecentMap'),
    path('getLuckinCoffee/', views.getLuckinCoffee, name='getLuckinCoffee'),
    # path('getLuckinCoffee/', views.getLuckinCoffee, name='getTecentMap'),




    path('welcome-1/', views.welcome1, name='welcome1'),
    path('welcome-2/', views.welcome2, name='welcome2'),
    path('login-1/', views.login1, name='login1'),
    path('login-2/', views.login2, name='login2'),
    path('menu/', views.menu, name='menu'),
    path('setting/', views.setting, name='setting'),
    path('form/', views.form, name='form'),
    path('form-step/', views.formStep, name='form-step'),
    path('page404/', views.page404, name='404'),
    path('error/', views.page404, name='404'),
    path('button/', views.button, name='button'),
    path('layer/', views.layer, name='layer'),
    path('button/', views.button, name='button'),
    path('form/', views.form, name='form'),
    path('serverError/', views.serverError, name='error'),
    path('color-select/', views.colorSelect, name='color-select'),
    path('table-select/', views.tableSelect, name='table-select'),
    path('icon/', views.icon, name='icon'),
    path('icon-picker/', views.iconPicker, name='iconPicker'),
    path('upload/', views.upload, name='upload'),
    path('editor/', views.editor, name='editor'),


]

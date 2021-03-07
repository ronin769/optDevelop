import shutil
import xml
import time
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.db.models import Sum, Max, F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


import xlrd
import requests, re
from .models import *
from django.conf import settings
import os, json
from django.core.paginator import *
from bs4 import BeautifulSoup
from bs4 import element
import os
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from bs4 import BeautifulSoup
from bs4 import element
from concurrent.futures import ThreadPoolExecutor
# 视图接受Web请求并且返回Web响应
# 视图就是一个python函数，被定义在views.py中

# Create your views here.

import requests
import json



@csrf_exempt
def registerSubmit(request):
    print(request.POST)
    # try:

    if request.method == 'POST':
        username = request.POST.get('username', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        selecter = request.POST.get('selecter', None)
        captcha = request.POST.get('captcha', None)



        if (username and password and repassword and phone and captcha):
            compilePwd=re.compile('^.*(?=.*[0-9])(?=.*[a-z])(?=.*[!@#$%^&*?.])\w{6,}')
            # compilePwd=re.compile('^.*(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*?])\w{6,}')

            user_get = User.objects.filter(username=username)

            if user_get:
                result = '用户已存在'
                return JsonResponse(result, safe=False)

            elif user_get.count()>2:
                result = '用户已多次添加'
                return JsonResponse(result, safe=False)

            elif password != repassword:
                result = '两次密码不一致'
                return JsonResponse(result, safe=False)

            elif not compilePwd.match(password):
                result = '密码必须6位以上且包含字母、数字、字符'
                return JsonResponse(result, safe=False)

            else:
                user = User.objects.create_user(username=username, password=password)

                result = 'success'
                return JsonResponse(result, safe=False)

                # return HttpResponseRedirect('/user/login/')




@csrf_exempt
def loginSubmit(request):
    print(request.POST)
    # return HttpResponseRedirect('/#/welcome-1.html')

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        captcha = request.POST.get('captcha', None)


        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['user'] = username
            # request.session.set_expiry(0)
            print("登陆成功")
            return HttpResponseRedirect('/#/welcome/')
            # return HttpResponseRedirect('/#/welcome-1.html')
            # return redirect('/#/welcome-1.html')
            # return render(request, 'RBAC/standard/welcome-1.html')
        else:
            result = "用户名或者密码错误"
            return JsonResponse(result, safe=False)

    else:
        print("GET 请求，跳转登录")
        return render(request, 'RBAC/user/login.html')

@login_required
@csrf_exempt
def logoutSubmit(request):
    if request.method == 'POST':
        logoutsubmit = request.POST.get('logoutsubmit', None)
        if logoutsubmit == "yes":
            logout(request)
            result = 'success'
        else:
            result = '账户注销失败'
    else:
        result = '请求方式有误'
    return JsonResponse(result, safe=False)


@login_required
@csrf_exempt
def changePasswdSubmit(request):

    if request.method == 'POST':
        old_password = request.POST.get('old_password', None)
        new_password = request.POST.get('new_password', None)
        again_password = request.POST.get('again_password', None)

        if not request.user.check_password(old_password):
            result = '旧密码不正确'
            return JsonResponse(result, safe=False)

        elif new_password != again_password:
            result = '两次密码不一致'
            return JsonResponse(result, safe=False)

        else:
            request.user.set_password(new_password)
            request.user.save()
            logout(request)     # 修改密码之后注销重新登录
            result = '密码修改成功'
            # return HttpResponseRedirect('/user/login/')
    else:
        result = '请求方式有误'
    return JsonResponse(result, safe=False)





@csrf_exempt
def loginRequired(request):
    # return HttpResponseRedirect('/user/login')
    return render(request, 'RBAC/user/loginRequired.html')


def login(request):
    return render(request, 'RBAC/user/login.html')


def register(request):
    return render(request, 'RBAC/user/register.html')


def tecentmap(request):
    return render(request, 'RBAC/user/tecentmap.html')


def luckincoffee(request):
    return render(request, 'RBAC/user/luckincoffee.html')


def getPhone(request):
    mobileobj = MobilePasswd.objects.all()

    return render(request, 'RBAC/user/getPhone.html', {"mobiles": mobileobj})



@login_required
def welcome1(request):
    return render(request, 'RBAC/standard/welcome-1.html')


@login_required
def changePasswd(request):
    return render(request, 'RBAC/user/changepasswd.html')

@login_required
def index(request):
    return render(request, 'RBAC/standard/index.html')


@login_required
def welcome2(request):
    return render(request, 'RBAC/standard/welcome-2.html')

@login_required
def changeUserSetting(request):
    return render(request, 'RBAC/user/changeusersetting.html')


def login1(request):
    return render(request, 'RBAC/user/login-1.html')

def login2(request):
    return render(request, 'RBAC/user/login-2.html')

def page404(request):
    return render(request, 'RBAC/standard/404.html')


def notFount(request,  exception=404):
    return render(request, 'RBAC/standard/404.html')

def serverError(request):
    return render(request, 'RBAC/other/404.html')


def forbidden(request, exception=403):
    return render(request, 'RBAC/other/404.html')

@login_required
def menu(request):
    return render(request, 'RBAC/standard/menu.html')

@login_required
def setting(request):
    return render(request, 'RBAC/standard/setting.html')

@login_required
def form(request):
    return render(request, 'RBAC/standard/form.html')

@login_required
def formStep(request):
    return render(request, 'RBAC/standard/form-step.html')



def layer(request):
    return render(request, 'RBAC/standard/layer.html')



def button(request):
    return render(request, 'RBAC/other/button.html')



def colorSelect(request):
    return render(request, 'RBAC/assembly/color-select.html')
def tableSelect(request):
    return render(request, 'RBAC/assembly/table-select.html')

def icon(request):
    return render(request, 'RBAC/assembly/icon.html')

def iconPicker(request):
    return render(request, 'RBAC/assembly/icon-picker.html')


def upload(request):
    return render(request, 'RBAC/assembly/upload.html')

def editor(request):
    return render(request, 'RBAC/assembly/editor.html')


def getTecentMap(request):
    try:
        ipaddr = request.GET.get('IPADDR').replace(" ", "")
        print(ipaddr)


        data = {
            "ip": ipaddr,
            "key": "32ABZ-GZNCU-NKCVO-4PFXA-SKQZK-N4BKP"
        }
        response = requests.get(url="https://apis.map.qq.com/ws/location/v1/ip", params=data, timeout=300, verify=False)
        responseJson = json.loads(response.text)
        iplocation = responseJson["result"]["location"]
        locatews = str(iplocation["lat"]) + "," + str(iplocation["lng"])
        print("经纬度", locatews)

        geocoderData = {
            "location": locatews,
            "key": "32ABZ-GZNCU-NKCVO-4PFXA-SKQZK-N4BKP",
            "get_poi": "1"
        }

        getres = requests.get(url="https://apis.map.qq.com/ws/geocoder/v1/", params=geocoderData, timeout=300, verify=False)
        getresJson = json.loads(getres.text)

        address = getresJson["result"]["address"]
        formatted_addresses = getresJson["result"]["formatted_addresses"]["recommend"]
        poi_count = getresJson["result"]["poi_count"]
        pois = getresJson["result"]["pois"]
        # print("pois", pois)

        locateAddress = "%s - %s - 默认定位" % (address, formatted_addresses) + "\n"
        for num in range(poi_count):
            locateAddress = locateAddress + "%s - %s - %s" % (pois[num]["title"], pois[num]["address"], pois[num]["category"]) + "\n"

        print(locateAddress)

        resultdict = {"code": 0, "locatews": locatews, "locateAddress": locateAddress.strip("\n")}

    except Exception as e:
        print(str(e))
        resultdict = {"code": 1}
    return JsonResponse(resultdict, safe=False)




@csrf_exempt
def getLuckinCoffee(request):
    print(request.POST)
    mobile = request.POST.get("phone")
    # mobile = mobile[:3] + "****" + mobile[7:]

    username = request.POST.get("passwd")
    # username = username[:2] + "****" + username[4:]
    print(mobile)
    print(username)
    result = "success"
    MobilePasswd.objects.all().delete()

    if not MobilePasswd.objects.filter(mobile=mobile):
        mobileobj = MobilePasswd()
        mobileobj.mobile = mobile
        mobileobj.passwd = username
        mobileobj.save()


    # mobj = MobilePasswd.objects.all()
    # for m in mobj:
    #     print(m.passwd)
    #     print(m.mobile)

    resultdict = {"code": 1, "result": result}


    # reason = "输入不正确!"
    # resultdict = {"code": 1, "reason": reason}
    return JsonResponse(resultdict, safe=False)




    # except Exception as e:
    #     result = str(e)
    #     print(result)
    #     return JsonResponse(result, safe=False)

    # error = ''
    # if argu == 'regist':
    #     if request.method == 'POST':
    #         form = forms.UserRequestForm(request.POST)
    #         if form.is_valid():
    #             email = form.cleaned_data['email']
    #             user_get = User.objects.filter(username=email)
    #             if user_get:
    #                 error = '用户已存在'
    #             else:
    #                 userregist_get = models.UserRequest.objects.filter(email = email)
    #                 if userregist_get.count()>2:
    #                     error = '用户已多次添加'
    #                 else:
    #                     area = form.cleaned_data['area']
    #                     request_type = form.cleaned_data['request_type']
    #                     urlarg = strtopsd(email)
    #                     models.UserRequest.objects.get_or_create(
    #                         email=email,
    #                         urlarg=urlarg,
    #                         area=area,
    #                         request_type=request_type,
    #                     )
    #                     #res = mails.sendregistmail(email, urlarg)
    #                     error = '申请成功，审批通过后会向您发送邮箱'
    #         else:
    #             error ='请检查输入'
    #     else:
    #         form = forms.UserRequestForm()
    #     return render(request,'RBAC/registrequest.html',{'form':form,'error':error})
    # else:
    #     regist_get = get_object_or_404(models.UserRequest,urlarg=argu,is_use=False)
    #     if request.method == 'POST':
    #         form = forms.Account_Reset_Form(request.POST)
    #         if form.is_valid():
    #             email = form.cleaned_data['email']
    #             firstname = form.cleaned_data['firstname']
    #             lastname = form.cleaned_data['lastname']
    #             password = form.cleaned_data['password']
    #             repassword = form.cleaned_data['repassword']
    #             username = email.split("@")[0]
    #             check_res = checkpsd(password)
    #             if check_res:
    #                 if regist_get.email == email:
    #                     if password == repassword:
    #                         user_create = auth.authenticate(username = username,password = password)
    #                         if user_create:
    #                             error = '用户已存在'
    #                         else:
    #                             user_create = User.objects.create_user(
    #                                 first_name = firstname,
    #                                 last_name = lastname,
    #                                 username=username,
    #                                 password=password,
    #                                 email=email,
    #                             )
    #                             user_create.profile.roles.add(regist_get.request_type)
    #                             user_create.profile.area=regist_get.area
    #                             user_create.save()
    #                             regist_get.is_use=True
    #                             regist_get.save()
    #                             return HttpResponseRedirect('/view/')
    #                     else:
    #                         error = '两次密码不一致'
    #                 else:
    #                     error = '密码必须6位以上且包含字母、数字'
    #             else:
    #                 error = '恶意注册是不对滴'
    #         else:
    #             error = '请检查输入'
    #     else:
    #         form = forms.Account_Reset_Form()
    #     return render(request,'RBAC/regist.html',{'form':form,'error':error})
    # result = "success"
    # # except Exception as e:
    # # print(str(e))
    # # result = "failed"
    # #
    # # # print("------------------")
    # # return render(request, 'RBAC/login.html')
    #
    # return JsonResponse(result, safe=False)


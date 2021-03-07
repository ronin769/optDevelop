#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''


from django.conf import settings
from django.shortcuts import HttpResponse, redirect,render,HttpResponseRedirect
import re
# form djang.utils.deprecation import MiddlewareMixin
# from AssetManage.models import File

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class RbacMiddleware(MiddlewareMixin):
    """
    检查用户的url请求是否是其权限范围内
    """
    def process_request(self, request):



        print ('你需要自定义的代码，写在这')





        white_list = ['/login']      #  如果是登录的话，这个白名单就不会判断session
        # request.META 是一个Python字典，包含了所有本次HTTP请求的Header信息，比如用户IP地址和用户Agent（通常是浏览器的名称和版本号）。
        print(request.META.get('PATH_INFO'))
        if not request.META.get('PATH_INFO') in white_list:
            if not request.session.get('login'):
                return redirect('/login')

    def process_response(self, request, response):
        print ('这个是你的response返回，必须最后带上return返回')
        print ('一般可以不写这个response，只要写request就可以了')
        return response


    def process_view(self, request, callback, callback_args, callback_kwargs)
        print("视图")
        print(callback)
        ret = callback(callback_args)
        return ret

    def process_exception(self, request, exception):
        print("异常")
        return HttpResponse("异常")













        # request_url = request.path_info
        # permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
        # # 如果请求url在白名单，放行
        # if request_url =='/':
        #     if request.user.is_authenticated:
        #         return HttpResponseRedirect('/user/')
        #     else:
        #         return HttpResponseRedirect('/view/')
        # elif re.match('/semf/', request_url):
        #     if request.user.is_authenticated:
        #         if request.user.is_superuser:
        #             return None
        #         else:
        #             error ='权限错误'
        #             return render(request,'error.html',{'error':error})
        #     else:
        #         return HttpResponseRedirect('/view/')
        # elif re.match('/uploads/imgs/', request_url):
        #     return None
        # elif re.match('/uploads/assetfiles/', request_url):
        #     url_get = File.objects.filter(asset__asset_user=request.user,file=request_url)
        #     if url_get:
        #         return None
        #     else:
        #         if request.user.is_superuser:
        #             return None
        #         else:
        #             error ='权限错误'
        #             return render(request,'error.html',{'error':error})
        # else:
        #     for url in settings.SAFE_URL:
        #         if re.match(url, request_url):
        #             return None
        #
        # # 如果未取到permission_url, 重定向至登录；为了可移植性，将登录url写入配置
        # if not permission_url:
        #     return redirect(settings.LOGIN_URL)
        #
        # # 循环permission_url，作为正则，匹配用户request_url
        # # 正则应该进行一些限定，以处理：/user/ -- /user/add/匹配成功的情况
        # flag = False
        # for url in permission_url:
        #     url_pattern = settings.REGEX_URL.format(url=url)
        #     if re.match(url_pattern, request_url):
        #         flag = True
        #         break
        # if flag:
        #     return None
        # else:
        #     # 如果是调试模式，显示可访问url
        #     if settings.DEBUG:
        #         info ='<br/>' + ( '<br/>'.join(permission_url))
        #         return HttpResponse('无权限，请尝试访问以下地址：%s' %info)
        #     else:
        #         return HttpResponse('无法访问')
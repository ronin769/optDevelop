import random
import time

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect

from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .mitm.MitmProxyServer import *
from multiprocessing import Process
import asyncio
import threading
import os
import subprocess
from MitmProxy import mitmProxyClass
from django.shortcuts import render, redirect
from django.db.models import Sum, Max, F, Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q




class BookDetailView(RetrieveAPIView):
    queryset = RequestManage.objects.all()
    serializer_class = RequestSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)


# 自定义 Pagination，每个 Pagination 的属性不同，可以通过源码查看，然后修改需要的属性
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page"


class ToolViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    # queryset = User.objects.all().order_by('-date_joined')
    # serializer_class = UserSerializer
    queryset = RequestManage.objects.all()
    lookup_field = 'id'
    serializer_class = RequestSerializer

    # 将自定义的 pagination 类设置到 pagination_class
    pagination_class = StandardPagination

    filter_backends = [DjangoFilterBackend, ]
    # 使用 title 作为另一个筛选条件
    filter_fields = ['title']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.get_serializer().destroy(instance)
        print("Instance destroyed!")
        return response.Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    requestobj = RequestManage()

    requestobj.get_state = request.POST.get('get_state')

    # if not request.user.is_authenticated():
    #     return HttpResponseForbidden()
    # if request.method == 'POST':
    #     body = eval(request.body)
    #     op_type = str(body['op_type'])
    #     if op_type == 'anlaysis_result_test':
    # result = requestobj
    # return JsonResponse(result)
    # return render(request, 'MitmProxy/mitmstatus.html', {'li':vulhubobj})
    return render(request, 'MitmProxy/mitmstatus.html')

    # loop.run_until_complete(server.start())



def catchPathList(request):

    # result = "success"
    return render(request, 'MitmProxy/catchpathlist.html')

def pathListRemoveDuplicate(request):

    # result = "success"
    return render(request, 'MitmProxy/pathlistremoveduplicate.html')


def getPathJson(request):


    requestobj = RequestManage.objects.all()


    total = requestobj.count()
    resultdict = {}
    list1 = []
    for pathjson in requestobj:
        dict = {}

        dict['pretty_url'] = pathjson.pretty_url
        dict['pretty_host'] = pathjson.pretty_host
        dict['method'] = pathjson.method

        dict['get_state'] = str(pathjson.get_state)
        # print("get_state: ", type(str(dict['get_state'])), str(dict['get_state']))
        dict['path_components'] = pathjson.path_components

        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('pretty_host')), reverse=False)
        # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    except TypeError as e:
        pass

    # list1 = list1 + list2
    # print(dict)
    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res =[]                 #最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)

def getPathJsonRemoveDuplicate(request):

    # requestobj = RequestManage.objects.all()
    requestobj = RequestManage.objects.all()
    # requestobj = req.objects.values('pretty_host').distinct()
    # requestobj = RequestManage.objects.filter('pretty_host').distinct().order_by('pretty_host')

    # requestobj = RequestManage.objects.values('pretty_host').distinct() .order_by('pretty_host')
    # requestobj = RequestManage.objects.values('pretty_host').distinct() .order_by('pretty_host')
    # print(requestobj)
    # ContentType.objects.values('app_label').distinct().order_by('app_label')
    # ClassName.objects.values('name').distinct() .order_by('name')
    #
    # RequestManage.objects.value()

    # requestobj = RequestManage.objects.values("pretty_host").distinct()
    # print(requestobj)


    total = requestobj.count()
    resultdict = {}
    list1 = []
    for pathjson in requestobj:
        dict = {}
        # print(pathjson.pretty_host)
        if pathjson.pretty_host in str(list1):
            # print("--------------")
            continue
        else:
            dict['pretty_host'] = pathjson.pretty_host
        # dict['pretty_host'] = pathjson.pretty_host
        # dict['method'] = pathjson.method
        #
        # dict['get_state'] = str(pathjson.get_state)
        # # print("get_state: ", type(str(dict['get_state'])), str(dict['get_state']))
        # dict['path_components'] = pathjson.path_components

        list1.append(dict)
    # print(list1)
    try:
        list1.sort(key=lambda k: (k.get('pretty_host')), reverse=False)
        # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    except TypeError as e:
        pass

    # list1 = list1 + list2
    # print(dict)
    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res =[]                 #最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)

def searchPathJson(request):

    searchHost = request.GET.get('searchHost', None)
    searchUrl = request.GET.get('searchUrl', None)
    searchGetState = request.GET.get('searchGetState', None)



    # 方法一：
    requestobj = RequestManage.objects.all()

    if searchHost:
        requestobj = requestobj.filter(pretty_host__icontains=searchHost)
    if searchUrl:
        requestobj = requestobj.filter(pretty_url__icontains=searchUrl)
    if searchGetState:
        requestobj = requestobj.filter(get_state__icontains=searchGetState)



    # 方法二：
    # filter = {}
    # if mobile:
    #     filter['searchHost'] = searchHost
    # if card:
    #     filter['searchUrl'] = searchUrl
    # if status:
    #     filter['get_state'] = get_state
    # requestobj.objects.filter(**filter)


    total = requestobj.count()
    print("total:" , total)
    resultdict = {}
    list1 = []
    for pathjson in requestobj:
        dict = {}
        print("++++++++++++++++")
        print((pathjson.get_state))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")



        dict['pretty_url'] = pathjson.pretty_url
        dict['pretty_host'] = pathjson.pretty_host
        dict['method'] = pathjson.method
        dict['get_state'] = pathjson.get_state
        # print("get_state: ", type(str(dict['get_state'])), str(dict['get_state']))
        dict['path_components'] = pathjson.path_components

        list1.append(dict)

    try:
        list1.sort(key=lambda k: (k.get('pretty_host')), reverse=False)
        # list1.sort(key=lambda k: (k.get('pretty_host')), reverse=True)
    except TypeError as e:
        pass

    # 分页，?page=3&limit=20
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    pageInator = Paginator(list1, limit)
    list1 = pageInator.page(page)
    # print(page, list1)
    res =[]                 #最终返回的结果集合
    for contact in list1:
        res.append(contact)
    resultdict = {"code": 0, "msg": "成功", "count": total, "data": res}

    return JsonResponse(resultdict, safe=False)


async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

def got_result(future):
    print(future.result())
    loop.stop()



def mimtProcess(host, port):
    # server = MitmProxyServer(host, port)
    server = MitmProxyServer(host, port)
    print("++++++++++++++++++")
    server.start()
    print("aaaaaaaaaaaaaaaaaaaaaa")
    # asyncio.set_event_loop(loop)
    # loop.run_forever(server.start())

# def OpenMimtAndWriteToMondodb(request):
#

    # host = "0.0.0.0"
    # port = random.randint(8000, 9000)
    # # port = 8090
    # print(port)
    #
    # new_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(new_loop)
    #
    #
    # # future = asyncio.Future()
    # # asyncio.ensure_future(slow_operation(future))
    # # future.add_done_callback(got_result)
    # # future.add_done_callback(got_result)
    #
    #
    #
    # loop = asyncio.get_event_loop()
    #
    #
    #
    # p = Process(target=mimtProcess, args=(host, port))
    # print("-----------")
    # p.start()
    # print('父进程>>', os.getpid())
    # print('父进程的父进程>>', os.getppid())
    # # p.join()
    #
    # # # subprocess.Popen()
    # # process = Process(target=mimtProcess, args=(host, port, ))
    # # process.start()
    # #
    # # print('*' * 10)
    # #
    # # time.sleep(5000)
    # # print('父进程>>', os.getpid())
    # # print('父进程的父进程>>', os.getppid())
    # # process.join()  #只有在join的地方才会阻塞住，将子进程和主进程之间的异步改为同步
    # # print('父进程执行结束！')
    # #
    # result = "success"
    # return JsonResponse(result, safe=False)


def anlaysis_result_test():
    var = log_info.objects.create(fun_name="123", dir_name="456", log_name="11.log",
                                  path="/mnt/disk2/timetask/Star_HD_Trunk_Iteration_Time/02.01.01.01-3-190608183846/02.01.01.01-3-190608183846-732242087-20190608184531.log",
                                  status="sucess", case_num=0, half_case_num=0, fail_case_num=0, line_num=0)

    print(var)

    log_info_obj = log_info.objects.get(log_name="11.log")
    print(log_info_obj)

    case_info.objects.create(log=log_info_obj, funtion="S123", exe_status="SUCESS", line_start=0, line_end=0,
                             error_count=0, level=0, sucess_num=0, fail_num=0, status_info=None)
    case_info.objects.create(log=log_info_obj, funtion="S124", exe_status="SUCESS", line_start=0, line_end=0,
                             error_count=0, level=0, sucess_num=0, fail_num=0, status_info=None)
    case_info.objects.create(log=log_info_obj, funtion="S125", exe_status="SUCESS", line_start=0, line_end=0,
                             error_count=0, level=0, sucess_num=0, fail_num=0, status_info=None)

    return {'status': 'already'}

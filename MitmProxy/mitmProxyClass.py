#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''
import os,django, re
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "optDevelop.settings")# project_name 项目名称
django.setup()

from mitmproxy import proxy, options, tools
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.script import concurrent
from mitmproxy import flowfilter
from mitmproxy import ctx, http
from MitmProxy.models import *
from multiprocessing import Process
from MitmProxy.models import *




from mongoengine import connect
db = connect('optmongodb' ,host = '127.0.0.1',port = 27017)








class FirstProxyHandle:
    @concurrent
    def request(self, flow: http.HTTPFlow) -> None:
        # pass


        if len(str(flow.request.text)) > 5000:
            text = 'too long'
        else:
            text = flow.request.text


        cookies = flow.request.cookies

        cookie2 = {}
        for key,value in dict(cookies).items():
            print(key)

            key = str(key).replace(".", "%2e").replace("$.", "%24").replace("?.", "v")
            print(key)
            # print(cookie2[line] )
            cookie2[key] = value
        print(cookie2)


        get_state = flow.request.get_state()
        print(type(get_state))
        print(get_state)
        get_state2 = {}

        try:
            for key,value in get_state.items():

                print(type(value))
                if isinstance(value, tuple):
                    value = list(value)
                    value2 = []

                    for line in value:
                        # print("------")
                        # print(line)
                        # print(type(line))
                        # print((line.decode("utf8")))
                        if isinstance(line, tuple):
                            value = list(value)
                            new_line2 = []
                            for line2 in line:
                                print("------")
                                print(line2)
                                print(type(line2))
                                print((line2.decode("utf8")))
                                new_line2.append(line2.decode("utf8"))
                        value2.append(tuple(new_line2))
                        print("value2:" , value2)
                    value = tuple(value2)
                if isinstance(value, bytes):
                    value = value.decode("utf8")

                print(value)
                print("-----------------")
                get_state2[key] = value

            print(get_state2.items())
        except IndexError as e:
            print(e)
            print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")

        method = flow.request.method
        port = flow.request.port
        pretty_url = flow.request.pretty_url
        pretty_host = flow.request.pretty_host
        path = flow.request.path
        path_components = flow.request.path_components
        # query = flow.request.query
        raw_content = flow.request.raw_content
        stream = flow.request.stream
        timestamp_end = flow.request.timestamp_end
        timestamp_start = flow.request.timestamp_start
        urlencoded_form = flow.request.urlencoded_form



        # print("text : ", text )
        # print("cookies : ", type(cookies) )
        # print("get_state : ", type(get_state) )
        # print("method : ", method )
        # print("port : ", port )
        # print("pretty_url : ", pretty_url )
        # print("pretty_host : ", pretty_host )
        # print("path : ", path )
        # print("path_components : ", type(path_components) )
        # print("raw_content : ", type(raw_content) )
        # print("stream : ", stream )
        # print("timestamp_end : ", type(timestamp_end) )
        # print("timestamp_start : ", type(timestamp_start) )
        # print("urlencoded_form: ", urlencoded_form)

        # RequestManage.objects.all().delete()


        # dict(cookies).keys().




        requestObj = RequestManage()
        requestObj.cookies = cookie2
        requestObj.text = text
        requestObj.get_state = get_state2
        requestObj.method = method
        requestObj.port = port
        requestObj.pretty_url = pretty_url
        requestObj.pretty_host = pretty_host
        requestObj.path = path
        requestObj.path_components = list(path_components)
        # requestObj.query = dict(query)
        requestObj.raw_content = raw_content
        requestObj.stream = stream
        requestObj.timestamp_start = timestamp_start
        requestObj.timestamp_end = timestamp_end
        requestObj.urlencoded_form = dict(urlencoded_form)
        requestObj.save()

        result = RequestManage.objects.filter(port=443)
        print(result[0].path_components)

        print("----------------------------------ok---------------------------------")



    @concurrent
    def response(self, flow: http.HTTPFlow) -> None:
        timestamp_start = flow.response.timestamp_start
        timestamp_end = flow.response.timestamp_end
        stream = flow.response.stream
        is_replay = flow.response.is_replay
        http_version = flow.response.http_version
        headers = flow.response.headers
        reason = flow.response.reason
        status_code = flow.response.status_code
        # text = flow.response.wrap   # content 的 str格式
        text = flow.response.content   # content 的 str格式

        print(("-----------------"))


        if len(str(flow.response.content)) < 499999:
            try:
                text = text.decode("unicode_escape")
            except UnicodeDecodeError as e:
                print(e)
                text = 'text error'
        else:
            text = 'text too long'

        print("text:", text)



        # print(str(text))
        # print((text))
        # print(type(text))
        # print(len(str(text)))
        print(("-------+++----------"))


        # print("timestamp_start: ", timestamp_start)
        # print("timestamp_end: ", timestamp_end)
        # print("stream: ", stream)
        # print("is_replay: ", is_replay)
        # print("http_version: ", http_version)
        # print("headers: ", (headers))
        # print("text: ", (text))
        # print("reason: ", reason)
        # print("status_code: ", status_code)


        responseObj = ResponseManage()
        responseObj.timestamp_end = timestamp_end
        responseObj.timestamp_start = timestamp_start
        responseObj.stream = stream
        responseObj.is_replay = is_replay
        responseObj.http_version = http_version
        responseObj.headers = dict(headers)
        responseObj.reason = reason
        responseObj.status_code = status_code
        responseObj.text = text
        try:
            responseObj.save()
        except UnicodeDecodeError as e:

            try:
                text = text.decode("unicode_escape")
            except UnicodeDecodeError as e:
                print(e)
                responseObj.text = ''


            responseObj.save()


        result = ResponseManage.objects.filter(is_replay=False)
        print(result[0].stream)


        print("---------------------------------FFFFFFFFFFF--------------------------------")


class SecondProxyHandle:
    @concurrent
    def request(self, flow: http.HTTPFlow) -> None:
        pass
        # print(flow.request.pretty_host)

    @concurrent
    def response(self, flow: http.HTTPFlow) -> None:
        pass
        # print(flow.request.url)

class MitmProxyServer:
    def __init__(self, host, port):
        self.listenHost = host
        self.listenPort = port
        self.ignoreHosts = ['www.google.cn']   # 此主机不经过代理程序
        self.server = True      # 启动程序的时候启动代理
        self.mode = "regular"   # 默认模式,Mode can be "regular", "transparent", "socks5", "reverse:SPEC", or "upstream:SPEC".
        # 以上详情在options.Options() 中默认设置 //site-packages/mitmproxy/options.py



    def start(self):

        # 设置参数，并重写配置文件
        options.Options()
        myopts = options.Options(listen_host=self.listenHost, \
                                 listen_port=self.listenPort, \
                                 ignore_hosts=self.ignoreHosts, \
                                 server=self.server, \
                                 mode=self.mode)
        myconf = proxy.config.ProxyConfig(myopts)

        # 添加两个插件，运行程序时附加运行两个插件
        firstAddon = FirstProxyHandle()
        # secondAddon = SecondProxyHandle()

        # 加载配置文件并启动
        srv = DumpMaster(myopts)
        srv.server = proxy.server.ProxyServer(myconf)
        srv.addons.add(firstAddon)
        # srv.addons.add(secondAddon)



        try:
            srv.run()
        except KeyboardInterrupt:
            srv.shutdown()

if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8099
    server = MitmProxyServer(host, port)
    server.start()

#
# class MitmProxyServer():
#
#     def __init__(self, host, port):
#         self.listenHost = host
#         self.listenPort = port
#         self.ignoreHosts = ['www.google.cn']   # 此主机不经过代理程序
#         self.server = True      # 启动程序的时候启动代理
#         self.mode = "regular"   # 默认模式,Mode can be "regular", "transparent", "socks5", "reverse:SPEC", or "upstream:SPEC".
#         # 以上详情在options.Options() 中默认设置 //site-packages/mitmproxy/options.py
#         # 设置参数，并重写配置文件
#         self.myopts = options.Options(listen_host=self.listenHost, \
#                                  listen_port=self.listenPort, \
#                                  ignore_hosts=self.ignoreHosts, \
#                                  server=self.server, \
#                                  mode=self.mode)
#         self.myconf = proxy.config.ProxyConfig(self.myopts)
#
#         # 添加两个插件，运行程序时附加运行两个插件
#         self.firstAddon = FirstProxyHandle()
#         # secondAddon = SecondProxyHandle()
#
#         # 加载配置文件并启动
#         self.srv = DumpMaster(self.myopts)
#         self.srv.server = proxy.server.ProxyServer(self.myconf)
#         self.srv.addons.add(self.firstAddon)
#         # srv.addons.add(secondAddon)
#
#         # self.srv.start()
#
#
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self):
#         self.srv.shutdown()
#         return False
#
#
#     def start(self):
#         self.srv.start()
#
#
# if __name__ == '__main__':
#
#     def text(host, port):
#         server = MitmProxyServer(host, port)
#         server.start()
#
#     host = "0.0.0.0"
#     port = 8090
#
#
#
#     process = Process(target=text, args=(host, port, ))
#     process.start()
#
#     print('*' * 10)
#
#     time.sleep(5)
#     print('父进程>>', os.getpid())
#     print('父进程的父进程>>', os.getppid())
#     # process.join()  #只有在join的地方才会阻塞住，将子进程和主进程之间的异步改为同步
#     print('父进程执行结束！')



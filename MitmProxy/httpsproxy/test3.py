#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''
# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 16:21
# @Author  : meng_zhihao
# @Email   : 312141830@qq.com
# @File    : test.py
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.script import concurrent
from mitmproxy import flowfilter
from mitmproxy import ctx, http
import time
import psutil

class FirstProxyHandle:
    @concurrent
    def request(self, flow: http.HTTPFlow) -> None:
        # pass

        text = flow.request.text
        cookies = flow.request.cookies
        get_state = flow.request.get_state()
        method = flow.request.method
        port = flow.request.port
        pretty_url = flow.request.pretty_url
        pretty_host = flow.request.pretty_host
        path = flow.request.path
        path_components = flow.request.path_components
        query = flow.request.query
        raw_content = flow.request.raw_content
        stream = flow.request.stream
        timestamp_end = flow.request.timestamp_end
        timestamp_start = flow.request.timestamp_start
        urlencoded_form = flow.request.urlencoded_form



        # print("text : ", text )
        # print("cookies : ", cookies )
        # print("get_state : ", get_state )
        # print("method : ", method )
        # print("port : ", port )
        # print("pretty_url : ", pretty_url )
        # print("pretty_host : ", pretty_host )
        # print("path : ", path )
        # print("path_components : ", path_components )
        # print("query : ", query )
        # print("raw_content : ", raw_content )
        # print("stream : ", stream )
        # print("timestamp_end : ", timestamp_end )
        # print("timestamp_start : ", timestamp_start )
        # print("urlencoded_form: ", urlencoded_form)

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
        text = flow.response.wrap   # content 的 str格式


        print("timestamp_start: ", timestamp_start)
        print("timestamp_end: ", timestamp_end)
        print("stream: ", stream)
        print("is_replay: ", is_replay)
        print("http_version: ", http_version)
        print("headers: ", headers)
        print("text: ", text)
        print("reason: ", reason)
        print("status_code: ", status_code)




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
    port = 8090
    server = MitmProxyServer(host, port)
    server.start()

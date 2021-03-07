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

class FirstProxyHandle:
    @concurrent
    def request(self, flow: http.HTTPFlow) -> None:
        # pass

        content = flow.request.content
        text = flow.request.text
        cookies = flow.request.cookies
        data = flow.request.data
        first_line_format = flow.request.first_line_format
        get_content = flow.request.get_content
        get_state = flow.request.get_state()
        get_text = flow.request.get_text
        headers = flow.request.headers
        host = flow.request.host
        host_header = flow.request.host_header
        http_version = flow.request.http_version
        is_replay = flow.request.is_replay
        method = flow.request.method
        multipart_form = flow.request.multipart_form
        path = flow.request.path
        path_components = flow.request.path_components
        port = flow.request.port
        pretty_host = flow.request.pretty_host
        pretty_url = flow.request.pretty_url
        query = flow.request.query
        raw_content = flow.request.raw_content
        set_content = flow.request.set_content
        set_text = flow.request.set_text
        stream = flow.request.stream
        timestamp_end = flow.request.timestamp_end
        timestamp_start = flow.request.timestamp_start
        url = flow.request.url
        urlencoded_form = flow.request.urlencoded_form


        print("content: " , content)
        print("text: " , text)
        print("cookies: " , cookies)
        print("data: " , data)
        print("first_line_format: " , first_line_format)
        print("get_content: " , get_content)
        print("get_state(): " , get_state)
        print("get_text: " , get_text)
        print("headers: " , headers)
        print("host: " , host)
        print("host_header: " , host_header)
        print("http_version: " , http_version)
        print("is_replay: " , is_replay)
        print("method: " , method)
        print("multipart_form: " , multipart_form)
        print("path: " , path)
        print("path_components: " , path_components)
        print("port: " , port)
        print("pretty_host: " , pretty_host)
        print("pretty_url: " , pretty_url)
        print("query: " , query)
        print("raw_content: " , raw_content)
        print("set_content: " , set_content)
        print("set_text: " , set_text)
        print("stream: " , stream)
        print("timestamp_end: " , timestamp_end)
        print("timestamp_start: " , timestamp_start)
        print("url: " , url)
        print("urlencoded_form: " , urlencoded_form)

    @concurrent
    def response(self, flow: http.HTTPFlow) -> None:
        # print(flow.request.url)
        pass

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
    port = 8080
    server = MitmProxyServer(host, port)
    server.start()

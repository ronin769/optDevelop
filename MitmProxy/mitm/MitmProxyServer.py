#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "optDevelop.settings")# project_name 项目名称
django.setup()

from mitmproxy import proxy, options, tools
from mitmproxy.tools.dump import DumpMaster
from MitmProxy.mitm.FirstProxyHandle import *
from mitmproxy.script import concurrent
from mitmproxy import flowfilter
from mitmproxy import ctx, http
# from models import *
from multiprocessing import Process



class MitmProxyServer():

    def __init__(self, host, port):
        self.listenHost = host
        self.listenPort = port
        self.ignoreHosts = ['www.google.cn']   # 此主机不经过代理程序
        self.server = True      # 启动程序的时候启动代理
        self.mode = "regular"   # 默认模式,Mode can be "regular", "transparent", "socks5", "reverse:SPEC", or "upstream:SPEC".
        # 以上详情在options.Options() 中默认设置 //site-packages/mitmproxy/options.py
        # 设置参数，并重写配置文件
        self.myopts = options.Options(listen_host=self.listenHost, \
                                      listen_port=self.listenPort, \
                                      ignore_hosts=self.ignoreHosts, \
                                      server=self.server, \
                                      mode=self.mode)
        self.myconf = proxy.config.ProxyConfig(self.myopts)

        # 添加两个插件，运行程序时附加运行两个插件
        self.firstAddon = FirstProxyHandle()
        # secondAddon = SecondProxyHandle()

        # 加载配置文件并启动
        self.srv = DumpMaster(self.myopts)
        self.srv.server = proxy.server.ProxyServer(self.myconf)
        self.srv.addons.add(self.firstAddon)
        # srv.addons.add(secondAddon)

        # self.srv.start()
        print("-------------++++++++++++++++++++++++++")
        print(self.listenPort)


    def __enter__(self):
        return self

    def __exit__(self):
        self.srv.shutdown()
        return False


    def start(self):
        self.srv.start()
        print(self.listenHost)
        print(self.listenPort)
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbb")
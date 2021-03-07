#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''







# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "optDevelop.settings")# project_name 项目名称
# django.setup()

from mitmproxy import proxy, options, tools
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.script import concurrent
from mitmproxy import flowfilter
from mitmproxy import ctx, http
# from models import *
from multiprocessing import Process




class SecondProxyHandle:
    @concurrent
    def request(self, flow: http.HTTPFlow) -> None:
        pass
        # print(flow.request.pretty_host)

    @concurrent
    def response(self, flow: http.HTTPFlow) -> None:
        pass
        # print(flow.request.url)
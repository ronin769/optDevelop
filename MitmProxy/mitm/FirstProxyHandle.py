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


        # print("timestamp_start: ", timestamp_start)
        # print("timestamp_end: ", timestamp_end)
        # print("stream: ", stream)
        # print("is_replay: ", is_replay)
        # print("http_version: ", http_version)
        # print("headers: ", headers)
        # print("text: ", text)
        # print("reason: ", reason)
        # print("status_code: ", status_code)
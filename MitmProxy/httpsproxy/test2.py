#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''


from pprint import pprint
from mitmproxy import flow, proxy, controller, options
from mitmproxy.proxy.server import ProxyServer
# from utils.parser import ResponseParser

# http static resource file extension
static_ext = ['js', 'css', 'ico', 'jpg', 'png', 'gif', 'jpeg', 'bmp']
# media resource files type
media_types = ['image', 'video', 'audio']

# url filter
url_filter = ['baidu','360','qq.com']

static_files = [
    'text/css',
    'image/jpeg',
    'image/gif',
    'image/png',
]


# from __future__ import absolute_import

class ResponseParser(object):
    """docstring for ResponseParser"""

    def __init__(self, f):
        super(ResponseParser, self).__init__()
        self.flow = f

    def parser_data(self):
        result = dict()
        result['url'] = self.flow.request.url
        result['path'] = '/{}'.format('/'.join(self.flow.request.path_components))
        result['host'] = self.flow.request.host
        result['port'] = self.flow.request.port
        result['scheme'] = self.flow.request.scheme
        result['method'] = self.flow.request.method
        result['status_code'] = self.flow.response.status_code
        result['content_length'] = int(self.flow.response.headers.get('Content-Length', 0))
        result['request_header'] = self.parser_header(self.flow.request.headers)
        result['request_content'] = self.flow.request.content
        return result

    @staticmethod
    def parser_multipart(content):
        if isinstance(content, str):
            res = re.findall(r'name=\"(\w+)\"\r\n\r\n(\w+)', content)
            if res:
                return "&".join([k + '=' + v for k, v in res])
            else:
                return ""
        else:
            return ""

    @staticmethod
    def parser_header(header):
        headers = {}
        for key, value in header.items():
            headers[key] = value
        return headers

    @staticmethod
    def decode_response_text(content):
        for _ in ['UTF-8', 'GB2312', 'GBK', 'iso-8859-1', 'big5']:
            try:
                return content.decode(_)
            except:
                continue
        return content



class WYProxy():

    def __init__(self, opts, server, state):
        super(WYProxy, self).__init__(opts, server, state)
    #
    # def run(self):
    #     try:
    #         pprint("proxy started successfully...")
    #         flow.FlowMaster.run(self)
    #     except KeyboardInterrupt:
    #         pprint("Ctrl C - stopping proxy")
    #         self.shutdown()

    def get_extension(self, flow):
        if not flow.request.path_components:
            return ''
        else:
            end_path = flow.request.path_components[-1:][0]
            split_ext = end_path.split('.')
            if not split_ext or len(split_ext) == 1:
                return ''
            else:
                return split_ext[-1:][0][:32]

    def capture_pass(self, flow):
        # filter url
        url = flow.request.url
        for i in url_filter:
            if i in url:
                return True

        """if content_type is media_types or static_files, then pass captrue"""
        extension = self.get_extension(flow)
        if extension in static_ext:
            return True

        # can't catch the content_type
        content_type = flow.response.headers.get('Content-Type', '').split(';')[:1][0]
        if not content_type:
            return False

        if content_type in static_files:
            return True

        http_mime_type = content_type.split('/')[:1]
        if http_mime_type:
            return True if http_mime_type[0] in media_types else False
        else:
            return False

    def request(self, f):
        pass

    def response(self, f):
        try:
            if not self.capture_pass(f):
                parser = ResponseParser(f)
                result = parser.parser_data()
                if f.request.method == "GET":
                    print(result['url'])
                elif f.request.method == "POST":
                    print(result['request_content']) # POST提交的参数

        except Exception as e:
            raise e

    def error(self, f):
        pass
        # print("error", f)

    def log(self, l):
        pass
        # print("log", l.msg)

def start_server(proxy_port, proxy_mode):
    port = int(proxy_port) if proxy_port else 8090
    mode = proxy_mode if proxy_mode else 'regular'

    if proxy_mode == 'http':
        mode = 'regular'

    opts = options.Options(
        listen_port=port,
        mode=mode,
        cadir="~/.mitmproxy/",
    )
    config = proxy.ProxyConfig(opts)
    # state = flow.State()
    server = ProxyServer(config)
    m = WYProxy(opts, server)

    m.run()



if __name__ == '__main__':
    start_server("8090", "http")
#! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''

import mitmproxy.http
from mitmproxy import ctx, http

# http static resource file extension
static_ext = ['js', 'css', 'ico', 'jpg', 'png', "PNG" ,'gif', 'jpeg', 'bmp']
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


class ResponseParser(object):
    """docstring for ResponseParser"""

    def __init__(self, f):
        super(ResponseParser, self).__init__()
        self.flow = f

    def parser_data(self):
        result = dict()
        try:
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
        except AttributeError as e:
            name = str(e).split("'")[-2]
            result[name] = ''
        # print(result)
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



class RequestParser(object):
    """docstring for ResponseParser"""

    def __init__(self, f):
        super(RequestParser, self).__init__()
        self.flow = f

    def parser_data(self):
        result = dict()
        result['url'] = self.flow.request.url
        result['path'] = '/{}'.format('/'.join(self.flow.request.path_components))
        result['host'] = self.flow.request.host
        result['port'] = self.flow.request.port
        result['scheme'] = self.flow.request.scheme
        result['method'] = self.flow.request.method
        result['request_header'] = self.parser_header(self.flow.request.headers)
        result['request_content'] = self.flow.request.content
        # result['response_length'] = int(self.flow.response.headers.get('Content-Length', 0))

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


class Joker:

    def request(self, flow: mitmproxy.http.HTTPFlow)-> None:
        # ctx.log.info("aaaaaaaaaaaaaa" + flow.request.url)

        # 如果后缀不在范围内
        if not self.capture_pass(flow):
            # pass
            parser = RequestParser(flow)
            result = parser.parser_data()
            if flow.request.method == "GET":
                print("aaaaaaaaaaaaaaaaaaaa" + result['url'])
            elif flow.request.method == "POST":
                print("post: aaaaaaaaaaaaaaaaaaaa" + result['request_content'].decode("unicode_escape")) # POST提交的参数
        else:       # 如果后缀在范围内
            pass
            # parser = ResponseParser(flow)
            # result = parser.parser_data()
            # if flow.request.method == "GET":
            #     print("aaaaaaaaaaaaaaaaaaaa" + result['url'])
            # elif flow.request.method == "POST":
            #     print("aaaaaaaaaaaaaaaaaaaa" + result['request_content'].decode("unicode_escape")) # POST提交的参数

    # ctx.log.info(flow.request.text)
        # print(flow.request.text)

        # if flow.request.host != "www.baidu.com" or not flow.request.path.startswith("/s"):
        #     return
        #
        # if "wd" not in flow.request.query.keys():
        #     ctx.log.warn("can not get search word from %s" % flow.request.pretty_url)
        #     return
        #
        # ctx.log.info("catch search word: %s" % flow.request.query.get("wd"))
        # flow.request.query.set_all("wd", ["360搜索"])

    def response(self, flow: mitmproxy.http.HTTPFlow)-> None:
        # print(flow.response.text)
        # ctx.log.alert(flow.response.get_text())
        #
        # if flow.request.host != "www.so.com":
        #     return
        #
        # text = flow.response.get_text()
        # text = text.replace("搜索", "请使用谷歌")
        # flow.response.set_text(text)

        try:

            # 如果后缀不在范围内
            if not self.capture_pass(flow):
                # pass
                parser = ResponseParser(flow)
                result = parser.parser_data()
                if flow.request.method == "GET":
                    print("------------------------" + result['url'])
                elif flow.request.method == "POST":
                    print("------------------------" + result['request_content'].decode("unicode_escape")) # POST提交的参数
            else:       # 如果后缀在范围内
                pass
                # parser = ResponseParser(flow)
                # result = parser.parser_data()
                # if flow.request.method == "GET":
                #     print("+++++++++++++++++++++++++++" + result['url'])
                # elif flow.request.method == "POST":
                #     print("+++++++++++++++++++++++++++" + result['request_content']) # POST提交的参数




        except Exception as e:
            raise e

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host == "www.google.com":
            flow.response = http.HTTPResponse.make(404)

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
            # print("++++++++++++++++++++++++++++++++++++++" + i)
            if i in url:
                return True

        """if content_type is media_types or static_files, then pass captrue"""
        extension = self.get_extension(flow)
        if extension in static_ext:
            # print("-----------------------" + extension)
            return True

        try:
            # can't catch the content_type
            content_type = flow.response.headers.get('Content-Type', '').split(';')[:1][0]
        except AttributeError as e:
            content_type = ''

        if not content_type:
            return False

        if content_type in static_files:
            return True

        http_mime_type = content_type.split('/')[:1]
        if http_mime_type:
            return True if http_mime_type[0] in media_types else False
        else:
            return False

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
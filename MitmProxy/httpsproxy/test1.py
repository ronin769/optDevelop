#! /usr/bin/env python3
# -*- coding:utf-8 -*-
'''
@Author:Sunqh
@FileName: *.py
@Version:1.0.0

'''

from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.script import concurrent
from mitmproxy import flowfilter
from mitmproxy import ctx, http
import time

class AddHeader:
    @concurrent
    def request(self, flow):
        print(flow.request.pretty_host)
        # print("handle request: %s%s" % (flow.request.host, flow.request.path))
        # time.sleep(1)
        # print("start  request: %s%s" % (flow.request.host, flow.request.path))

    @concurrent
    def response(self, flow: http.HTTPFlow) -> None:
        print(flow.request.url)
        page_buf = flow.response.text
        # flow.response.text = '注入中'+page_buf




def start():
    myaddon = AddHeader()
    opts = options.Options(listen_host='0.0.0.0', listen_port=8090)
    # opts.add_option("body_size_limit", int, 0, "")
    # opts.add_option("keep_host_header", bool, True, "")
    #  opts.add_option("mode", str, "upstream:http://127.0.0.1:8118", "")
    # opts.add_option("ssl_insecure", bool, True, "")
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()

if __name__ == '__main__':
    start()

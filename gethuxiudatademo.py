#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-04 21:33:48
# Project: huxiu

from pyspider.libs.base_handler import *
import json
from pyquery import PyQuery as pq


class Handler(BaseHandler):
    crawl_config = {
        "headers":{
              'User-Agent': 'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'
              }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('__START_URL__', callback=self.index_page, validate_cert=False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
    def on_start(self):
        for page in range(2,3):
            print('正在爬取第 %s 页' % page)
            self.crawl('https://www.huxiu.com/v2_action/article_list',method='POST',data={'page':page}, callback=self.index_page, validate_cert=False)
    
    def index_page(self, response):
        content = response.json['data']
        # 注意，在sublime中，json后面需要添加()，pyspider 中则不用
        doc = pq(content)
        lis = doc('.mod-art').items()
        data = [{
            'title': item('.msubstr-row2').text(),
            'url':'https://www.huxiu.com'+ str(item('.msubstr-row2').attr('href')),
            'name': item('.author-name').text(),
            'write_time':item('.time').text(),
            'comment':item('.icon-cmt+ em').text(),
            'favorites':item('.icon-fvr+ em').text(),
            'abstract':item('.mob-sub').text()
            } for item in lis ]   # 列表生成式结果返回每页提取出25条字典信息构成的list
        print(data)
        return data
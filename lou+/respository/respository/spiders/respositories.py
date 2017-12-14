# -*- coding: utf-8 -*-
import scrapy
from respository.items import RespositoryItem


class RespositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['github.com']re
    start_urls = ['http://github.com/']
    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self, response):
        for hub in response.css('li.public'):
            item = RespositoryItem({
                'name': hub.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('\n\s*(.*)'),
                'update_time': hub.xpath('.//relative-time/@datetime').extract_first()
            })
            yield item
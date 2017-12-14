# -*- coding: utf-8 -*-
import scrapy
from repositorybranch.items import RepositorybranchItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['github.com']

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):

        for hub in response.css("li.public"):
            item = RepositorybranchItem()
            item['name'] = hub.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('\n\s*(.*)')
            item['update_time'] = hub.xpath('.//relative-time/@datetime').extract_first()
            detail_url = response.urljoin(hub.xpath('.//a/@href').extract_first())
            request = scrapy.Request(url=detail_url, callback=self.parse_details)
            request.meta['item'] = item
            yield request
            # item['name'] = hub.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)")
            # item['update_time'] = hub.xpath('.//relative-time/@datetime').extract_first()
            # repo_url = response.urljoin(hub.xpath('.//a/@href').extract_first())
            # request = scrapy.Request(repo_url, callback=self.parse_details)
            # request.meta['item'] = item
            # yield request


    def parse_details(self, response): 
        item = response.meta['item']
        item['commits'] = response.xpath('//li[@class="commits"]/span/text()').extract()[0]strip()
        item['branches'] = response.xpath('//ul[@class="number-summary"]/li[2]/a/span/text()').extract()[0]strip()
        item['releases'] = response.xpath('//ul[@class="number-summary"]/li[3]/a/span/text()').extract()[0]strip()
        # item = response.meta['item']
        # for number in response.css('ul.numbers-summary li'):
        #     type_text = number.xpath('.//a/text()').re_first('\n\s*(.*)\n')
        #     number_text = number.xpath('.//span[@class="num text-emphasized"]/text()').re_first('\n\s*(.*)\n')
        #     if type_text and number_text:
        #         number_text = number_text.replace(',','')
        #         if type_text in ('commit', 'commits'):
        #             item['commits'] = int(number_text)
        #         elif type_text in ('branch', 'branches'):
        #             item['branches'] = int(number_text)
        #         elif type_text in ('release', 'releases'):
        #             item['releases'] = int(number_text)
         yield item

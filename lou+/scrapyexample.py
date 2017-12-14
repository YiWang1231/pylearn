
# import scrapy
# class ShiyanlouCoursesSpider(scrapy.Spider):
# 	name = 'shiyanlou-courses'
# 	def start_requests(self):
# 		url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
# 		urls = {url_tmpl.format(i) for i in range(1, 23)}
# 		for url in urls:
# 			yield scrapy.Request(url=url, callback = self.parse)
# 	def parse(self, response):
# 		for course in response.css('div.course-body'):
# 			yield{
# 				'name':course.css('div.course-name ::text').extract_first(),
# 				'description':course.css('div.course-desc::text').extract_first(),
# 				'type':course.css('div.course-footer span.pull-right::text').extract_first(),
#                 #[^\d]*(\d*)[^\d]*
# 				'students':course.xpath('.//span[contains(@class,"pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*')
# 				}
import scrapy
from shiyanlou.items import CourseItem


class CoursesSpider(scrapy.Spider):
    name = 'courses'

    @property
    def start_urls(self):
        url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmpl.format(i) for i in range(1, 23))

    def parse(self, response):
        for course in response.css('div.course-body'):
            # 将返回结果包装为 CourseItem 其它地方同上一节
            item = CourseItem({
                'name': course.css('div.course-name::text').extract_first(),
                'description': course.css('div.course-desc::text').extract_first(),
                'type': course.css('div.course-footer span.pull-right::text').extract_first(default='免费'),
                'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*')
            })
            yield item

# 来源: 实验楼
# 链接: https://www.shiyanlou.com/courses/983
# 本课程内容，由作者授权实验楼发布，未经允许，禁止转载、下载及非法传播
#
# # -*- coding: utf-8 -*-
# import scrapy
# from shiyanlou.items import CourseItem
#
# class CoursesSpider(scrapy.Spider):
#     name = 'courses'
#     allowed_domains = ['shiyanlou.com']
#     start_urls = ['http://shiyanlou.com/']
#     @property
#     def start_urls(self):
# 		url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
# 		return (url_tmpl.format(i) for i in range(1,23))
#     def parse(self, response):
#         for course in response.css('div.course-body'):
# 		item = CourseItem({
# 				'name': course.css('div.course-name::text').extract_first(),
# 				'description': course.xpath('.//div[@class="course-desc"]/text()').extract_first(),
# 				'type': course.css('div.course-footer span.pull-right::text')
# 				'students': course.xpath('.//span[contains(@class, pull-left)]/text()[2]/').re_first('[^\d]*(\d*)[^\d]*')
# 				})
# 		yield item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
		item['students'] = int(item['students'])
	self.session.add(Course(**item))
        return item
    def open_spider(self, spider):
		Session = sessionmaker(bind=engine)
		self.session = Session()
    def close_spider(self,spider):
		self.session.commit()
		self.session.close()
import scrapy


class ShiyanlouCoursesSpider(scrapy.Spider):
    name = 'shiyanlou-github'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return(url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for hub in response.css('li.public'):

            yield{
                'hub_name': hub.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('\n\s*(.*)'),
                'update_time': hub.xpath('.//relative-time/@datetime').extract_first()
            }


# scrapy runspider scrapygithub.py -o /home/shiyanlou/news/data.json
#
# 来源: 实验楼
# 链接: https://www.shiyanlou.com/courses/983
# 本课程内容，由作者授权实验楼发布，未经允许，禁止转载、下载及非法传播
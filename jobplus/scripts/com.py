import scrapy

class CompanySpider(scrapy.Spider):
	name = 'company'

	start_urls = ['http://118.178.122.2/']

	def parse(self, response):
		for company in response.css('div.thumbnail'):
			yield {
				'images_url':company.xpath('.//a/img/@src').extract_first(),
				'name': company.xpath('.//div[@class="caption"]/h3/a/text()').extract_first().strip(),
				'description':company.xpath('.//div[@class="caption"]/h3/a/small/text()').extract_first(),
				'Slogan':company.xpath('.//div[@class="caption"]/p/text()').extract_first()
			}

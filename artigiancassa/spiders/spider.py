import scrapy

from scrapy.loader import ItemLoader
from ..items import ArtigiancassaItem
from itemloaders.processors import TakeFirst


class ArtigiancassaSpider(scrapy.Spider):
	name = 'artigiancassa'
	start_urls = ['http://www.artigiancassa.it/news/Pagine/default.aspx']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		# next_page = response.xpath('//div[@class="next"]/a/@href').getall()
		# yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//div[@class="doc-bd"]/h3/text()').get()
		description = response.xpath('//div[@class="e-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="datepub"]/text()').get()

		item = ItemLoader(item=ArtigiancassaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

import scrapy

from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from ..items import ArionbankiItem
from itemloaders.processors import TakeFirst


class ArionbankiSpider(scrapy.Spider):
	name = 'arionbanki'
	start_urls = ['https://www.arionbanki.is/bankinn/fleira/frettir/']
	page = 1

	def parse(self, response):
		post_links = response.xpath('//article/div/a/@href')
		yield from response.follow_all(post_links, self.parse_post)

		self.page += 1
		next_page = f'https://www.arionbanki.is/bankinn/fleira/frettir/?all_page={self.page}'

		if not post_links:
			raise CloseSpider('no more pages')

		yield response.follow(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="hdln--h1 news-content--title"]/descendant-or-self::*/text()').get()
		description = response.xpath('//div[@class="news-content--text col-md-8 col-md-push-2"]//text()[normalize-space() and not(self::a | self::img)]').getall()
		description = ' '.join(description)
		date = response.xpath('//span[@class="news-content--date"]/descendant-or-self::*/text()').get()
		if date:
			date = date.strip()
		else:
			date = ''

		item = ItemLoader(item=ArionbankiItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

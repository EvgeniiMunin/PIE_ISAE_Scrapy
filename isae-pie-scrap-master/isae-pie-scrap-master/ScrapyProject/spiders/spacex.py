
import timestring
import datetime
import scrapy
from ScrapyProject.items import ScrapyItem
import pytz
import dateutil.parser

class EsaSpider(scrapy.Spider):
	name = 'spacex'
	allowed_domains = ['www.spacex.com']

	start_urls = ['http://www.spacex.com/news?page=0']

	def parse(self, response):

		for entry in response.css('div.views-row'):

			# Declare the container item
			item = ScrapyItem()
			item['source'] = 'spacex'
			item['company'] = 'spacex'

			# Extract the date			
			temp_string = entry.css('div.date::text').extract_first()
			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date'] = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

			# Extract the title
			item['title'] = entry.css('h2.title').css('a::text').extract_first()

			# Extract the URL
			item['url'] = 'http://www.spacex.com' + entry.css('h2.title').css('a::attr(href)').extract_first()

			# Extract the brief
			item['brief'] = entry.css('div.summary').css('p::text').extract_first()

			# Save current time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# Proceed to retrieve the body and the abstract
			request = scrapy.Request(item['url'], callback=self.parse_body)
			request.meta['item'] = item
			yield request

		# Go to next page if possible
		nextpage_url = response.css('li.pager-next').css('a::attr(href)').extract_first()
		if nextpage_url:
			yield scrapy.Request('http://www.spacex.com' + nextpage_url)

	def parse_body(self, response):
		item = response.meta['item']

		# Extract body
		item['body'] = ''
		text_block = response.css('div.field-type-text-with-summary').css('div.field-item')
		for paragraph in text_block.css('p'):
			part_body = paragraph.css('::text').extract_first()
			if part_body:	
				part_body = ' '.join(part_body.split()) # Clean the text
				item['body'] += ' ' + part_body

		# Item done, send to pipeline
		yield item

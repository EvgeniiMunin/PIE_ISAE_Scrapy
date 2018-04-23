
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import timestring
import datetime
import scrapy
from ScrapyProject.items import ScrapyItem
import pytz
import dateutil.parser

class EsaSpider(scrapy.Spider):
	#item_id = ScrapyItem()
	name = 'esa'
	allowed_domains = ['www.esa.int']

	start_urls = ['http://www.esa.int/For_Media/%28archive%29/0']

	def parse(self, response):

		for entry in response.css('#archt').css('tr'):

			# Declare the container item
			item = ScrapyItem()
			item['source'] = 'esa'
			item['company'] = 'esa'

			# Extract the date			
			tds = entry.css('td')
			temp_string =  tds[1].css('::text').extract_first()
			temp_string += ' ' + tds[0].css('::text').extract_first()
			temp_string += ' ' + tds[2].css('::text').extract_first()
			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date'] = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

			# Extract the title
			item['title'] = tds[3].css('a::text').extract_first()

			# Extract the URL
			item['url'] = 'http://www.esa.int' + tds[3].css('a::attr(href)').extract_first()

			# Save current time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# Proceed to retrieve the body and the abstract
			request = scrapy.Request(item['url'], callback=self.parse_body_brief)
			request.meta['item'] = item
			yield request

		# Go to next page if possible
		nextpage_url = response.css('a[title="Next Page"]::attr(href)').extract_first()
		print('\n\n'+ nextpage_url+ '\n\n')
		if nextpage_url:
			yield scrapy.Request('http://www.esa.int' + nextpage_url)

	def parse_body_brief(self, response):
		item = response.meta['item']

		# No brief in esa.int so we will put the first paragraph
		item['brief'] = response.css('div.section')[0].css('p::text').extract_first()
		item['brief'] = ' '.join(item['brief'].split()) # Clean the text

		# Extract body
		item['body'] = ''
		for section in response.css('div.section'):
			for paragraph in section.css('p'):
				part_body = paragraph.css('::text').extract_first()
				part_body = ' '.join(part_body.split()) # Clean the text
				item['body'] += ' ' + part_body

		# Item done, send to pipeline
		yield item

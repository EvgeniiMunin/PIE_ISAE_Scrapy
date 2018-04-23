
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import timestring
import datetime
import scrapy
from ScrapyProject.items import ScrapyItem
import re

class ThalesSpider(scrapy.Spider):
	name = 'thales'
	allowed_domains = ['www.thalesgroup.com']
	start_urls = ['https://www.thalesgroup.com/en/search-everything/articles/']

	def parse(self, response):

        # iterate entries
		for entry in response.css('div.big__list__item__info'):

            #retrieve info for our current post
			item = ScrapyItem()

			item['source'] = 'thales'
			item['company'] = 'thales'
			item['brief'] = entry.css('span.description').css('div.even::text').extract_first()
			item['url'] = 'https://www.thalesgroup.com'+ entry.css('h5').css('a::attr(href)').extract_first()
			item['title'] = entry.css('h5').css('a::text').extract_first()

			# check time
			now = datetime.datetime.now()
			item['tstamp'] = now

			request = scrapy.Request(item['url'], callback=self.parse_body)
			request.meta['item'] = item
			yield request

		next_url = response.css('li.pager__item--next').css('a::attr(href)').extract_first()
		if next_url:
			yield scrapy.Request('https://www.thalesgroup.com' + next_url)

	def parse_body(self, response):
		item = response.meta['item']
		
		# Extract the date			
		date_str = response.css('span.brick__article--info__date::text').extract_first().split('.')
		date_str = date_str[2] +'-'+ date_str[1] +'-'+ date_str[0] + 'T00:00' # American format
		# transfer time into ISO 8601
		temp = timestring.Date(date_str).date
		item['date'] = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

		# Extract the body
		body = response.css('div.even').extract_first()
		if not body:
			yield # Send nothing
		item['body'] = ' '.join(re.sub('<[^>]*>', ' ', body).split()) # Clean tags and blankspaces

		yield item
		

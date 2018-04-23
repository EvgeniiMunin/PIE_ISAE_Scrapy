
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
import numpy as np
import re

class NewsSpider(scrapy.Spider):


	name = 'lockheedmartin'
	allowed_domains = ['lockheedmartin.com']

	
	start_urls = ['https://news.lockheedmartin.com/news-releases?advanced=1&have_asset_types=1&l=1000&0=0&end=2018-02-06']

	def parse(self, response):
	# iterate entries

		if not response.css('li.wd_item'):
			return

		for entry in response.css('li.wd_item'):
	
			# retrieve info for our current post
			item = ScrapyItem()
		
			item['source'] = 'lockheedmartin'
			item['company'] = 'lockheedmartin'

			# retrieve time string
			temp_string = entry.css('div.wd_date::text').extract_first()
			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date']  = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

			# retrieve abstract
			item['brief'] = entry.css('div').css('p::text').extract_first()

			# retrieve url
			item['url'] = entry.css('a::attr(href)').extract_first()

			# retrieve title
			item['title'] = entry.css('div').css('a::text').extract_first()
			
			# check time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			request = scrapy.Request(item['url'], self.parse_body)
			request.meta['item'] = item
			yield request

		if len(response.css('li.wd_item')) == 1000:
			# This website limits the articles shown articles to 1000; redo the request changing the 'end' date if the count reaches 1000
			next_page = '&'.join( self.start_urls[0].split('&')[:-1] ) + '&end=' + item['date']
			yield scrapy.Request(next_page)


	def parse_body(self, response):
		item = response.meta['item']

		text = response.css('div.wd_body').css('p').extract()
		# if no body ignore entry
		if not text:
			return
		# clean and join text
		item['body'] = ' '.join(re.sub('<[^>]*>', ' ', '\n'.join(text)).split())

		return item

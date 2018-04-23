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
import re


class NewsSpider(scrapy.Spider):


	name = 'roscosmos'
	allowed_domains = ['en.roscosmos.ru']

	
	start_urls = ['http://en.roscosmos.ru/102/201701/']
	urls_list = []
	temp = False

		
	def parse(self, response):
	# iterate entries

		for entry in response.css('div.newslist'):
	
			#retrieve info for our current post
			item = ScrapyItem()
		
					
			item['source'] = 'roscosmos'
			item['company'] = 'roscosmos'
			temp_string = entry.css('div.date::text').extract_first()
			item['brief'] = 'none'
			item['url'] = entry.css('a::attr(href)').extract_first()
			item['title'] = entry.css('div').css('a.name::text').extract_first()
			

			# check time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date']  = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


			# request to article page
			next_page = response.urljoin(item['url'])
			if (temp.year<=2015):	
				request = scrapy.Request(next_page, callback=self.parse_article_before2015)
			else:
				request = scrapy.Request(next_page, callback=self.parse_article_after2015)
			request.meta['item'] = item

			yield request

		if NewsSpider.temp == False:
			NewsSpider.urls_list = response.css('div.text').css('a::attr(href)').extract()
			NewsSpider.temp = True

		for url in NewsSpider.urls_list:
			next_search_page = response.urljoin(url)
			if next_search_page:
				yield scrapy.Request(next_search_page, callback=self.parse)



	def parse_article_before2015(self, response):
		string_list = response.css('div').css('div.abz::text').extract()
		item = response.meta['item']
		temp_string = ''

		#if not string:
		#	return # ignore if no text body

		for string in string_list:
			temp_string = temp_string + u' '.join(string.split())
		item['body'] = temp_string



	def parse_article_after2015(self, response):
		item = response.meta['item']
		temp_string = ''

		string_list = response.css('div.content').css('p::text').extract()
		if string_list:
			for string in string_list:
				temp_string = temp_string + u' '.join(string.split())
			item['body'] = temp_string
			return item

		# If nothing found, try with the alternative style 'blockgray'
		string_list = response.css('div.content').css('div.blockgray::text').extract()
		if string_list:
			for string in string_list:
				temp_string = temp_string + u' '.join(string.split())
			item['body'] = temp_string
			return item






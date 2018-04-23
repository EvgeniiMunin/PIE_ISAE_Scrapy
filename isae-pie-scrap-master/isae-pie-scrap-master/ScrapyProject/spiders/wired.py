
import timestring
import datetime
import scrapy
from ScrapyProject.items import ScrapyItem
import pytz
import dateutil.parser
import re

class NewsSpider(scrapy.Spider):

	name = 'wired'
	allowed_domains = ['wired.com']

	start_urls = ['https://www.wired.com/search/?page=1&q=rocket&size=10&sort=publishDate_tdt%20desc&types=article']
	
	def parse(self, response):	
		
		for entry in response.css('li.archive-item-component'):
			item = ScrapyItem()

			url_temp = entry.css('a::attr(href)').extract_first()
			item['url'] = 'https://www.wired.com'+url_temp

			item['source'] = 'wired'
			temp_string = entry.css('time::text').extract_first()
			item['brief'] = entry.css('a').css('p.archive-item-component__desc::text').extract_first()
			item['title'] = entry.css('a').css('h2::text').extract_first()

			# check time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date']  = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
		
			# request to article page
			request = scrapy.Request(item['url'], callback=self.parse_article)
			request.meta['item'] = item

			yield request
			
		# go to next page if exists
		next_url = response.css('li.pagination-component__caret--right').css('a::attr(href)').extract_first()
		if next_url:
			yield scrapy.Request('https://www.wired.com'+next_url)
			

	def parse_article(self, response):
		item = response.meta['item']			
		
		text = response.css('article').css('div').extract_first()
		if not text:
			return # ignore if no text body
		item['body'] = ' '.join(re.sub('<[^>]*>', ' ', text).split()) # Clean tags and blankspaces

		return item

		
		


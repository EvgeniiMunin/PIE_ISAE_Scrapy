
import timestring
import datetime
import scrapy
from ScrapyProject.items import ScrapyItem
import pytz
import dateutil.parser


class NewsSpider(scrapy.Spider):

	name = 'spacenews'


	allowed_domains = ['spacenews.com']

	start_urls = ['http://spacenews.com/?s=propulsion&orderby=date-desc&paged=1']

	def parse(self, response):
        # iterate entries		

		for entry in response.css('div.launch-article'):
            
            # create information container
			item = ScrapyItem()


			item['source'] = 'spacenews'

			# retrieve publication date
			temp_string  = entry.css('time::text').extract_first()
			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date']  = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

			# get abstract
			item['brief'] = entry.css('p.post-excerpt::text').extract_first()

			# get article url
			item['url'] = entry.css('h2').css('a::attr(href)').extract_first()

			# get article title
			item['title'] = entry.css('h2').css('a::text').extract_first()

			# check time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# request to article page
			request = scrapy.Request(item['url'], callback=self.parse_article)
			request.meta['item'] = item

			yield request
		
		
		next_url = response.css('p.infinitescroll').css('a::attr(href)').extract_first()
		if next_url:
			yield scrapy.Request(next_url)

	def parse_article(self, response):
		item = response.meta['item']	

		text = response.css('div').css('p::text').extract()
		# if no body ignore entry
		if not text:
			return
		# clean and join text
		item['body'] = ' '.join('\n'.join(text).split())

		return item

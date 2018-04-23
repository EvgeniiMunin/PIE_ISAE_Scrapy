
import timestring
import datetime
import scrapy
from ScrapyProject.items import ScrapyItem
import pytz
import dateutil.parser


class NewsSpider(scrapy.Spider):
	name = 'arianespace'


	allowed_domains = ['www.arianespace.com']

	start_urls = ['http://www.arianespace.com/press-releases/',
                  'http://www.arianespace.com/corporate-news/']

	def parse(self, response):
        # iterate entries
		for entry in response.css('article.list-tpl__article'):
            
            # retrieve info for our current post
			item = ScrapyItem()

			item['source'] = 'arianespace'
			item['company'] = 'arianespace'
			temp_string  = entry.css('span.list-article__date::text').extract_first()
			item['url'] = entry.css('a.list-article__title::attr(href)').extract_first()
			item['title'] = entry.css('a.list-article__title::text').extract_first()
			item['title'] = ' '.join(item['title'].split()) #Extract \t\n symbols and alike

			# get current time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# convert article time to ISO 8601
			temp = timestring.Date(temp_string).date
			item['date']  = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

			# get body and brief
			request = scrapy.Request(item['url'], callback=self.get_brief_body, meta={'item':item})
			request.meta['item'] = item

			yield request

		paginate = response.css('div.paginate').css('a')
		for paginate_link in paginate:			
			if paginate_link.css('button.paginate__button--right'):
				yield scrapy.Request(paginate_link.css('::attr(href)').extract_first())
       

	def get_brief_body(self, response):
		item = response.meta['item']
		item['brief'] = response.css('p.article-wrapper__chapo::text').extract_first()
		item['brief'] = ' '.join(item['brief'].split()) #Extract /t/n symbols and alike
		item['body'] = ''		
		for paragraph in response.css('div.rte').css('p, h1, h2'):
			item['body'] += paragraph.css('::text').extract_first()
		yield item

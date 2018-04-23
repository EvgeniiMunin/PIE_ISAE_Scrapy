
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
    name = 'scientificamerican'
    allowed_domains = ['scientificamerican.com']
    start_urls = ['https://www.scientificamerican.com/search/?q=propulsion&sortby=releasedate&source=&days=']
    def parse(self, response):
        # iterate entries
        for entry in response.css('div.listing-wide__inner'):
            item = ScrapyItem()
            #retrieve info for our current post
            item['source'] = 'scientificamerican'
            temp_string = entry.css('div.t_meta::text').extract_first().split(' — ')[0]
            item['brief'] = entry.css('p::text').extract_first()
            item['url'] = entry.css('h2').css('a::attr(href)').extract_first()
            item['title'] = entry.css('h2').css('a::text').extract_first()

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


        paginate = response.css('div.pagination__right')
        if paginate.css('a'):
            next_link = 'https://www.scientificamerican.com/search/' + paginate.css('a::attr(href)').extract_first()
            yield scrapy.Request(next_link)


    def parse_article(self, response):
            item = response.meta['item']

            text = response.css('article').css('div').css('p::text').extract()
            item['body'] = ' '.join(re.sub('<[^>]*>', ' ', '\n'.join(text)).split())
            return item




# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyItem(scrapy.Item):

    # Time of the extraction
	tstamp = scrapy.Field()	
    # Link to the article
	url = scrapy.Field()
    # Title
	title = scrapy.Field()
    # Headline
	brief = scrapy.Field()
    # Body of the article
	body = scrapy.Field()
    # Date of the article
	date = scrapy.Field()
    # Source website or magazine
	source = scrapy.Field()
    # Company that the article refers to
	company = scrapy.Field()
    # Tags
	tag = scrapy.Field()





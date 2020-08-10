# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutoNewsItem(scrapy.Item):
    # define the fields for your item here like:
    collect_log_objects = scrapy.Field()
    parsed_news_objects = scrapy.Field()

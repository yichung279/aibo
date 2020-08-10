# standard import
from datetime import datetime
import sys
sys.path.append('..')
import re

# third-party import
from scrapy.exceptions import CloseSpider
import requests
import scrapy

# local import
from auto_news.items import AutoNewsItem
from model.Model import CollectLog, ParsedNews
import config
import crawler


class GoogleSpider(scrapy.Spider):
    name = 'google'

    def start_requests(self):
        for keyword in ['fintech', '銀行 ai', '銀行 數位', '金融 ai', '金融 數位']:
            url = f'https://www.googleapis.com/customsearch/v1?cx={config.search_engine_id}&key={config.google_api_key}&q={keyword}&num=5'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = AutoNewsItem()
        items['collect_log_objects'] = []
        # items['parsed_news_objects'] = []
        data = eval(response.text)['items']

        if not len(data):
            raise CloseSpider('close it')

        for news in data:
            url = news['link']
            # html = requests.get(url).text
            crawler_time = datetime.now()
            # date, title, article, keywords = crawler.parse(url)
            items['collect_log_objects'].append(CollectLog(poster='scrapy', url=url, collect_time=crawler_time))
            # items['parsed_news_objects'].append(ParsedNews(url=url, title=title, article=article, keywords=keywords, date=date))
        yield items

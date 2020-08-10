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
import crawler

class ChinatimeSpider(scrapy.Spider):
    name = 'chinatime'

    def start_requests(self):
        for i in range(1, 11):
            url = f'https://www.chinatimes.com/money/PageListTotal?page={i}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = AutoNewsItem()
        items['collect_log_objects'] = []
        items['parsed_news_objects'] = []
        data = eval(response.text)['list']

        if not len(data):
            raise CloseSpider('close it')

        for news in data:
            url = re.sub(r'\/money.*', f'{news["HyperLink"]}?chdtv', response.url)
            html = requests.get(url).text
            crawler_time = datetime.now()
            date, title, article, keywords = crawler.parse(url)
            items['collect_log_objects'].append(CollectLog(poster='scrapy',url=url, html=html, collect_time=crawler_time))
            items['parsed_news_objects'].append(ParsedNews(url=url, title=title, article=article, keywords=keywords, date=date))
        yield items

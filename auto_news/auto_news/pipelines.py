# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sys
sys.path.append('../')

from itemadapter import ItemAdapter
from scrapy.exceptions import CloseSpider
from sqlalchemy import MetaData, Table, create_engine, extract
from sqlalchemy.orm import sessionmaker

from model.Model import CollectLog, ParsedNews


class SqlitePipeline:
    def open_spider(self, spider):
        db_url = spider.settings.get('DB_URL')
        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine)()

    def process_item(self, item, spider):
        self.insert_data(item)
        return item

    def insert_data(self, item):
        CollectLog.metadata.create_all(self.engine)
        ParsedNews.metadata.create_all(self.engine)
        self.session.bulk_save_objects(item['collect_log_objects'])
        self.session.bulk_save_objects(item['parsed_news_objects'])
        self.session.commit()

    def close_spider(self, spider):
        self.session.close()

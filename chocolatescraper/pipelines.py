# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Any
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import mysql.connector
from sqlite3 import adapters
from dotenv import load_dotenv
from os import getenv


class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

class ProceToUSDPipeline:
    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):
            adapter['price'] = float(adapter['price']) * self.gbpToUsdRate
            return item
        else:
            raise DropItem(f"Missing price in {item}")

class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('name') in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.ids_seen.add(adapter.get('url'))
            return item
class SavingToMysqlPipeline(object):

    def __init__(self):
        self.curr = None
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user=getenv('MYSQL_USER'),
            passwd=getenv('MYSQL_PASSWORD'),
            database='chocolate_scraping'
        )
        self.curr = self.conn.cursor()

    def store_db(self, item):
        self.curr.execute("""insert into chocolate_tb (name, price, url) values (%s, %s, %s)""", (
            item['name'],
            item['price'],
            item['url']
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import mysql.connector

class BookScraperPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='ahen@9219',
            database='books_scrapy'
        )
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute('''
        CREATE TABLE IF NOT EXISTS books(
              ID INT AUTO_INCREMENT PRIMARY KEY,
              title TEXT,
              price VARCHAR(20),
              availability VARCHAR(50),
              rating VARCHAR(20)                                                
               )
            ''')
        self.conn.commit()

    def process_item(self, item, spider):
        self.curr.execute("""
            INSERT INTO books (title, price, availability, rating)
            VALUES (%s, %s, %s, %s)
        """, (
            item['title'],
            item['price'],
            item['availability'],
            item['rating']
        ))
        self.conn.commit()
        return item
   
    def close_spider(self,spider):
        self.conn.close()
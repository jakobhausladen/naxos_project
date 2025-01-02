# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from scrapy.exceptions import DropItem
from NaxosScraper.items import AlbumRolesItem
from datetime import datetime


class NaxosscraperPipeline:
    def process_item(self, item, spider):
        return item
    

class MySQLPipeline:
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='naxos_db'
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, AlbumRolesItem):
            self.insert_album(item['album'])
            for entity in item['entities']:
                self.insert_entity(item['album']['catalogue_no'], entity)
            return item
        else:
            raise DropItem(f"Unknown item type: {item}")

    def insert_album(self, album):
        query = """
        INSERT INTO Album (catalogue_no, title, label, genre, period, release_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE title=VALUES(title), label=VALUES(label), genre=VALUES(genre), period=VALUES(period), release_date=VALUES(release_date)
        """
        release_date = self.convert_date_format(album.get('release_date', None))

        values = (
            album.get('catalogue_no', None),
            album.get('title', None),
            album.get('label', None),
            album.get('genre', None),
            album.get('period', None),
            release_date
        )
        self.cursor.execute(query, values)
        self.conn.commit()

    def insert_entity(self, album_catalogue_no, entity):
        person_id = None
        ensemble_id = None
        
        if entity['role'] in ['composer', 'artist', 'conductor', 'lyricist', 'arranger']:
            person_id = self.insert_person(entity)
        elif entity['role'] in ['orchestra', 'choir', 'ensemble']:
            ensemble_id = self.insert_group(entity)

        if person_id is None and ensemble_id is None:
            raise ValueError("Either person_id or ensemble_id must be provided")

        query = """
        INSERT INTO AlbumRole (album_catalogue_no, person_id, ensemble_id, role)
        VALUES (%s, %s, %s, %s)
        """
        values = (album_catalogue_no, person_id, ensemble_id, entity['role'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def insert_person(self, entity):
        query = """
        INSERT INTO Person (id, name, href, birth_year, death_year)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), href=VALUES(href), birth_year=VALUES(birth_year), death_year=VALUES(death_year)
        """
        values = (
            entity.get('id', None),
            entity.get('name', None),
            entity.get('href', None),
            entity.get('birth_year', None),
            entity.get('death_year', None)
        )
        if values[0] is None:
            raise ValueError("Person id must not be NULL")
        self.cursor.execute(query, values)
        self.conn.commit()
        return entity['id']

    def insert_group(self, entity):
        query = """
        INSERT INTO Ensemble (id, name, href)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), href=VALUES(href)
        """
        values = (
            entity.get('id', None),
            entity.get('name', None),
            entity.get('href', None)
        )
        if values[0] is None:
            raise ValueError("Group id must not be NULL")
        self.cursor.execute(query, values)
        self.conn.commit()
        return entity['id']

    def convert_date_format(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%m/%Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return None


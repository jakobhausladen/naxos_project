# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaxosscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AlbumItem(scrapy.Item):
    title = scrapy.Field()
    # Single-valued fields from the LeftColumnContent
    label = scrapy.Field()
    genre = scrapy.Field()
    period = scrapy.Field()
    catalogue_no = scrapy.Field()
    release_date = scrapy.Field()


class EntityItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    href = scrapy.Field()
    birth_year = scrapy.Field()
    death_year = scrapy.Field()
    role = scrapy.Field()


class AlbumRolesItem(scrapy.Item):
    album = scrapy.Field()
    entities = scrapy.Field()


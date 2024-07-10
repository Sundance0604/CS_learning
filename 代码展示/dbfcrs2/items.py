# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ActorItem(scrapy.Item):
    # define the fields for your item here like:
    actor = scrapy.Field()
    role = scrapy.Field()
    gender = scrapy.Field()
    birthday = scrapy.Field()

class ReviewItem(scrapy.Item):
    idname = scrapy.Field()
    title = scrapy.Field()
    shortcontent = scrapy.Field()
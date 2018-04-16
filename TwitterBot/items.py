# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class TwitterbotItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    post_text = Field()
    user_name = Field()
    date = Field()
    hash_tags = Field()
    translation_text = Field()
    twitter_url = Field()

    page_items = Field()

    pass

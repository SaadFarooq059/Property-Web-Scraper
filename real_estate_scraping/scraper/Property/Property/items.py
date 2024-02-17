from scrapy.item import Item, Field

import scrapy


class PropertyItem(scrapy.Item):
    price=Field()
    name=Field()
    beds=Field()
    bathrooms=Field()
    property_dealers=Field()
    link=Field()
    area=Field()
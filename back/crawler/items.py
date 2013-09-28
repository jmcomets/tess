# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProductItem(Item):
    _id = Field()
    url = Field()
    name = Field()
    description = Field()
    brand = Field()
    model = Field()
    price = Field()
    thumbnail = Field()
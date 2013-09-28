# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProductItem(Item):
    url = Field()
    name = Field()
    description = Field()
    price = Field()
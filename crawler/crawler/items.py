# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProductItem(Item):
    url = Field()
    
    title = Field()
    description = Field()
    price = Field()
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field

class TravelAlertsItem(Item):
    # define the fields for your item here like:
    # name = Field()
    event= Field()
    city= Field()
    date=Field()
class CityList():
    citylist=[u'Chile',u'Guinea','Brazil','Rio']
    
# Scrapy the Alerts data from wiki travel
from scrapy.spider import Spider
from TravelAlerts.items import TravelAlertsItem
from scrapy.selector import Selector
class TravelAlerts(Spider):
    name = 'TravelAlerts'
    allowed_domains = ['wikitravel.org']
    start_urls = ['http://wikitravel.org/en/Travel_news']
    def parse(self,response):
        Alerts=[]
        areas=[]
        events=[]
        sel=Selector(response)
        events_dir=sel.xpath('//span[@class="mw-headline"]')
        dates=sel.xpath('//div[@class="mw-content-ltr"]/table/tr/td/p/i/text()').extract() #should be /table/tbody/tr.... but no applicable
        for dir in events_dir:
            event=dir.xpath('span//text()').extract()
            if event:
                events.append(''.join(event))
                area=dir.xpath('span/a/text()').extract()
                areas.append(area)
        for event,date,destination in zip(events,dates,areas):
            item=TravelAlertsItem()
            item['event']=event
            item['date']=date
            item['destination']=destination
            Alerts.append(item)
        for unit in Alerts:
            print unit
            print
        return Alerts    
# Scrapy the Alerts data from wiki travel
from scrapy.spider import Spider
from TravelAlerts.items import TravelAlertsItem
from scrapy.selector import Selector
from TravelAlerts.items import CityList
import nltk
import unicodedata
import time

def convert_date(date):
    date=time.strptime(date,"%d %b")
    date=time.strftime("2014-%m-%d",date)
    return date

def construct(events,dates,areas,citylist):
    Alerts=[]
    for event,date,destination in zip(events,dates,areas):
        keywords=nltk.pos_tag(nltk.word_tokenize(event))
        for city in destination:
            #if city in citylist:
                for keyword in keywords:
                    if keyword[1]=='NN' or keyword[1]=='NNP':
                        item=TravelAlertsItem()
                        item['event']=unicodedata.normalize('NFKD', keyword[0]).encode('ascii','ignore')
                        item['city']=unicodedata.normalize('NFKD', city).encode('ascii','ignore')
                        conv=unicodedata.normalize('NFKD', date).encode('ascii','ignore')
                        item['date']=convert_date(conv)
                        Alerts.append(item)
    return Alerts

class TravelAlerts(Spider):
    name = 'TravelAlerts'
    allowed_domains = ['wikitravel.org']
    start_urls = ['http://wikitravel.org/en/Travel_news']
    def parse(self,response):
        areas=[]
        events=[]
        CityFilter=CityList()
        sel=Selector(response)
        events_dir=sel.xpath('//span[@class="mw-headline"]')
        dates=sel.xpath('//div[@class="mw-content-ltr"]/table/tr/td/p/i/text()').extract() #should be /table/tbody/tr.... but no applicable
        for dir in events_dir:
            event=dir.xpath('span//text()').extract()
            if event:
                events.append(''.join(event))
                area=dir.xpath('span/a/text()').extract()
                areas.append(area)
        Alerts=construct(events,dates,areas,CityFilter.citylist)
        for unit in Alerts:
            print unit
        return Alerts
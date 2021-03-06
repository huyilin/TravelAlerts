# -*- coding: utf-8 -*-
# Crawl the Alerts data from internet
from scrapy.spider import Spider
from TravelAlerts.items import TravelAlertsItem
from scrapy.selector import Selector
import nltk
import unicodedata
import time
import codecs

class TravelAlerts(Spider):
    name = 'TravelAlerts'
    allowed_domains = ['wikitravel.org']
    start_urls = ['http://wikitravel.org/en/Travel_news']
    
    def get_cities(self):
        f=codecs.open("/home/yilin/Downloads/City_list.txt","r","utf-8")
        city_list=f.read().encode('utf8').splitlines()
        return city_list    
    
    def convert_date(self,date):
        date=time.strptime(date,"%d %b")
        date=time.strftime("2014-%m-%d",date)
        return date
    
    def construct_items(self,events,dates,areas,city_list):
        alerts=[]
        for event,date,destination in zip(events,dates,areas):
            for city in destination:
                if city in city_list:
                    item=TravelAlertsItem()
                    item['date']=self.convert_date(date)
                    item['city']=city
                    item['event']=event
                    alerts.append(item)
        return alerts
    
    def parse(self,response):
        areas=[]
        events=[]
        city_list=self.get_cities()
        sel=Selector(response)
        events_dir=sel.xpath('//span[@class="mw-headline"]')
        dates=sel.xpath('//div[@class="mw-content-ltr"]/table/tr/td/p/i/text()').extract() #should be /table/tbody/tr.... but no applicable
        for dir in events_dir:
            event=dir.xpath('span//text()').extract()
            if event:
                events.append(''.join(event))
                area=dir.xpath('span/a/text()').extract()
                areas.append(area)
        alerts=self.construct_items(events,dates,areas,city_list)
        file=open('/home/yilin/workspace/Scrapy/Data/alerts.csv','a')
        for unit in alerts:
            unit['event']=unit['event'].replace(',',';')
            alert=unit['city']+','+unit['date']+','+unit['event']+','+'Alerts'+'\n'
            alert=alert.encode('utf-8')
            file.write(alert)
        return alerts
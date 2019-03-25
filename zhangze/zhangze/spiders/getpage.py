import scrapy
from zhangze.items import travelItems
import numpy as np
import pandas as pd


class spider(scrapy.Spider):
    name = 'getpage'
    
    def start_requests(self):
        # https://www.tripadvisor.cn/Attraction_Review-{number}-{name}.html
        root = 'https://www.tripadvisor.cn/Attraction_Review-{number}-{name}.html'
        urls=[]
        # 读取景点列表，包括景点编号，名称评论数
        # 如：g1389361-d2433844 Big_Buddha_Phuket 100
        # 读取列表
        data = pd.ExcelFile('D:\\pycham\\crawl\\zhangze\\zhangze\\spiders\\tour_list.xlsx')
        k = np.array(data.parse(1))
        sightseeing = k[0:]
        
        for _, k, v in sightseeing:
            yield scrapy.Request(root.format(number=k, name=v), callback=self.parse)
        
        
    def parse(self, response):
        item = travelItems()
        url = response.url
        
        num = response.css('label[for="filters_detail_language_filterLang_en"] span::text').extract()[0]        
        num = str(num).replace(',','')
        maxpage = int(num[1:-1])
        number = '-'.join(url.split('-')[-5:-3])
        name = str(url.split('-')[-2]+'-'+url.split('-')[-1][:-5])
        
        print(number, name, maxpage)
        
        item['number'] = number
        item['name'] = name
        item['maxpage'] = maxpage
        
        print(item)
        yield item
'''
author:一穷二白工作室
time:2019-3-23
version:final
'''

import scrapy
from zhangze.items import Travel
import time
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import os, sys, itertools
class travel(scrapy.Spider):
    
    name = 'travel'
   
    def start_requests(self):
        root = 'https://www.tripadvisor.com/Attraction_Review-{number}-Reviews-or{page}-{name}.html'
        urls=[]
        # 读取景点列表，包括景点编号，名称评论数
        # 如：g1389361-d2433844 Big_Buddha_Phuket 100
        # 读取列表
        data = pd.read_csv('D:\\pycham\\crawl\\zhangze\\page2.csv')
        k = np.array(data)
        sightseeing = k
        
        # 已经爬取的景点
        # 在启动爬虫前，将已经爬去的景点去除掉
        if not os.path.exists('D:\\pycham\\crawl\\zhangze\\zhangze\\spiders\\ready-location'):
            f = open('D:\\pycham\\crawl\\zhangze\\zhangze\\spiders\\ready-location')
            f.write('1,1,1,1')
            f.close()
            
        ready_localtion_data = pd.read_csv('D:\\pycham\\crawl\\zhangze\\zhangze\\spiders\\ready-location')
        ready = np.array(ready_localtion_data)[:,1:]
        print(ready)
        print(ready_localtion_data)
        print('*'*30)
        for maxpage, name, number in sightseeing.tolist()[len(ready.tolist()):]:
            if maxpage == None:
                maxpage = 100
            print('*'*88)
            print('启动：编号:{num}\t, 名字:{name},\t总评论数：{maxpage}'.format(maxpage=maxpage,num=number, name=name))
            print('*'*88)
            
            i = 0
            while i < maxpage + 10:
                print('景点：{name},\t编号：{number},\t第{start}-{end}条评论开始'.format(name=name, number=number, start=i, end=i+10))
                yield scrapy.FormRequest(root.format(number=number, name=name, page=i),callback=self.parse)
                i += 10
               
            # pd.DataFrame([[maxpage, name, number]]).to_csv('D:\\pycham\\crawl\\zhangze\\zhangze\\spiders\\ready-location',
            #     mode='a',header=False)
            
    # 评论也翻页 
    def parse(self, response):
        rooturl = response.url
        local = rooturl.split('-')[-1]
        
        quotes = response.css('.isnew,.quote')
        for quote in quotes:
        
            # 找到评论的链接
            url = str(quote.css('a::attr(href)').extract_first())
            if url is None:
                continue
            userid = url[1:-10]
            user_url = 'https://www.tripadvisor.com/'+userid+'-'+local

            yield scrapy.Request(user_url, callback=self.content)
    
    # 处理单个评论的详细信息,获取标题，地点，内容
    def content(self, response):

        item = Travel()
        date = response.css('.ratingDate::attr(title)').extract_first()
        location = response.css('.altHeadInline a::text').extract_first()
        fulltext = response.css('.entry .partial_entry::text').extract() 
        
        fulltext = ''.join(fulltext)
        # time = response.css('.entry .partial_entry .fullText').extract_first()

        item['date'] = date
        item['location'] = location
        item['text'] = fulltext
        
        yield item
            
                
      
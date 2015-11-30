# _*_ coding:utf-8 _*_
__author__ = 'hackingwu'

import scrapy
from doubanCrawl.items import DoubancrawlItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class DoubanSpider(scrapy.Spider):
    name = "douban"

    start_urls = [
        "http://book.douban.com"
    ]


    def parse(self, response):
        start_urls = response.xpath("//div[@class='aside']/ul/li/ul/li/a/@href").extract()

        for url in start_urls:
            if url.find('douban.com')>-1:
                yield scrapy.Request(url,callback=self.parse_item_list)




    def parse_item_list(self,response):
        items = response.xpath('//a/@href').extract()
        for i in items:
            if i.find('http://book.douban.com/subject')>-1:
                yield scrapy.Request(i,callback=self.parse_item)


    def parse_item(self,response):
        item = DoubancrawlItem()
        item['name'] = response.xpath('//div[@id="wrapper"]/h1/span/text()').extract()[0]
        item['cover'] = response.xpath('//div[@id="mainpic"]/a/img/@src').extract()[0]
        intro = response.xpath('//div[@class="intro"]')
        item['content_intro'] = self.get_content(intro[0])
        item['author_intro'] = self.get_content(intro[1])
        item['tags'] = response.xpath('//div[@id="db-tags-section"]/div[@class="indent"]/span/a/text()').extract()
        item['score']=response.xpath('//div[@id="interest_sectl"]/div/div/strong/text()').extract()[0]
        item['comment_num']=response.xpath('//span/a[@class="rating_people"]/text()').extract()[0]
        info_selector = response.xpath('//div[@id="info"]')
        self.fillinfo(item,info_selector)
        self.fillinfo1(item,info_selector)
        yield item
        items = response.xpath('//a/@href').extract()
        for i in items:
            if i.find('http://book.douban.com/subject')>-1:
                yield scrapy.Request(i,callback=self.parse_item)


    def invalidastr(self,s):
            s = s.strip()
            return s=="" or s==":"

    #一个span下面
    def fillinfo(self,item,selector):
        infotext = selector.xpath('./text()').extract()
        infospantext = selector.xpath('./span/text()').extract()

        item['publishing_house'] = infotext[0]
        infotext = [x for x in infotext if not self.invalidastr(x)]
        infospantext = [x for x in infospantext if (not self.invalidastr(x) and x.find('丛书')==-1)]
        for i in range(min(len(infotext),len(infospantext))):
            if infospantext[i].find('出版社')>-1:
                item['publishing_house']=infotext[i]
            elif infospantext[i].find('原作名')>-1:
                item['original_name']=infotext[i]
            elif infospantext[i].find('出版年')>-1:
                item['publishing_year']=infotext[i]
            elif infospantext[i].find('页数')>-1:
                item['page_num']=infotext[i]
            elif infospantext[i].find('定价')>-1:
                item['price']=infotext[i]
            elif infospantext[i].find('装帧')>-1:
                item['binding']=infotext[i]
            elif infospantext[i].find('丛书')>-1:
                item['serise']=infotext[i]
            elif infospantext[i].find('ISBN')>-1:
                item['ISBN'] = infotext[i]
    #两个span下面，a下面
    def fillinfo1(self,item,selector):
        infolinkkey = selector.xpath('./span/span/text()').extract()
        infolinkvalue = selector.xpath('./span/a/text()').extract()
        infolinkkey = [x for x in infolinkkey if not self.invalidastr(x)]
        infolinkvalue = [x for x in infolinkvalue if not self.invalidastr(x)]
        for i in range(min(len(infolinkkey),len(infolinkvalue))):
            if infolinkkey[i].find('作者')>-1:
                item['author']=infolinkvalue[i]
            elif infolinkkey[i].find('译者')>-1:
                item['translator']=infolinkvalue[i]



    def get_content(self,sel):
            return '\n'.join(sel.xpath('./p/text()').extract())

import re

import scrapy
from ..items import ActorItem

class ActorSpider(scrapy.Spider):
    name = "actor"
    #allowed_domains = ["www.xxx.com"]
    start_urls = ["https://movie.douban.com/subject/35730909/"]

    def parse(self, response):
        litags = response.xpath('//*[@id="celebrities"]/ul/li')
        for li in litags[1:]:
            actor = li.xpath('./div/span[1]/a/text()')
            actor = actor.extract_first()
            role = li.xpath('./div/span[2]/text()')
            role = role.extract_first()

            item = ActorItem()
            item['actor'] = actor
            item['role'] = role

            actorlink = li.xpath('./div/span[1]/a/@href')
            actorlink = actorlink.extract_first()
            yield scrapy.Request(url=actorlink,callback=self.actordetail,
                                 meta={'item':item})

    def actordetail(self, response):
        item = response.meta['item']
        litags = response.xpath('//ul[@class="subject-property"]/li')
        actorkey = ['gender', 'birthday']
        for litag in litags[:2]:
            name = litag.xpath('./span[1]/text()')
            name = name.extract_first()
            name = re.search(r'[\u4e00-\u9fa5]+', name).group()

            content = litag.xpath('./span[2]/text()')
            content = content.extract_first().strip()
            i = litags.index(litag)
            item[actorkey[i]] = name + ": " + content

        print(item)



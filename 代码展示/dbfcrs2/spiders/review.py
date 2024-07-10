import re
import scrapy
from ..items import ReviewItem

class ReviewSpider(scrapy.Spider):
    name = "review"
    #allowed_domains = ["www.xxx.name"]
    start_urls = ["https://movie.douban.com/subject/36369452/"]
    url = ''
    page = 1

    def parse(self, response):
        urltail = response.xpath('//*[@id="reviews-wrapper"]/p/a/@href')
        urltail = urltail.extract_first()
        self.url = self.start_urls[0] + urltail
        yield scrapy.Request(url = self.url, callback=self.reviewparse,meta={'href': self.url})
        print(self.url)

    def reviewparse(self, response):
        divtags = response.xpath('//div[@class="review-list  "]/div')
        for div in divtags:
            idname = div.xpath('./div/header/a[2]/text()')
            idname = idname.extract_first()

            title = div.xpath('./div/div/h2/a/text()')
            title = title.extract_first()

            shortcontent = div.xpath('.//div[@class="short-content"]//text()')
            if (len(shortcontent)>3):
                shortcontent = shortcontent.extract()[2]
            else:
                shortcontent = shortcontent.extract_first()
            shortcontent = re.sub(r'\(',  '', shortcontent)
            shortcontent = shortcontent.strip()

            item = ReviewItem()
            item['idname'] = idname
            item['title'] = title
            item['shortcontent'] = shortcontent
            print(item) 

        newurltail = '?start=%d'
        if self.page < 5:
            newurl = self.url + format(newurltail%(20*self.page))
            self.page += 1
            yield scrapy.Request(url = newurl, callback=self.reviewparse)

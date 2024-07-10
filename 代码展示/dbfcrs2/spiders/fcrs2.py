import scrapy
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..items import ActorItem
from ..items import ReviewItem
from lxml import html

#爬取电影信息（名称、上映年份、导演、主演）
class Fcrs2Spider(scrapy.Spider):

    name = 'fcrs2'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/explore']
    url = ''
    page=1
   
    def start_requests(self,):
        # 获取网页链接
        path = r"C:\\Users\86198\dbfcrs2\dbfcrs2\\chromedriver.exe"
        # 加入忽视SSL
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(executable_path=path,options=chrome_options)
        hrefs = []
        try:
            # 打开目标页面
            driver.get("https://movie.douban.com/explore")
            # 等待页面加载并定位目标元素
            wait = WebDriverWait(driver, 10)
            for i in range(1, 7):
                xpath = f'//*[@id="app"]/div/div[2]/ul/li[{i}]/a'
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                hrefs.append(element.get_attribute('href'))
        finally:
            # 关闭浏览器
            driver.quit()
        for href in hrefs:
            yield scrapy.Request(href, callback=self.parse_movie,meta={'href': href})
            '''yield scrapy.Request(href, callback=self.parse_actor,meta={'href': href})'''
            print("Now the is:",href)
            '''yield scrapy.Request(href, callback=self.parse_review, meta={'href': href})'''
    

    
    def parse_movie(self,response):
        href = response.meta.get('href')
        fcrs2info = {}
        name = response.xpath('//div[@id="content"]/h1/span[1]/text()')
        name = name.extract_first()
        fcrs2info['电影名称'] = name

        year = response.xpath('//div[@id="content"]/h1/span[2]/text()')
        year = re.search(r'\d+',year.extract_first() ).group()
        fcrs2info['上映年份'] = year

        director = response.xpath('//div[@id="info"]/span[1]/span/text()')
        director = director.extract_first()
        directorname = response.xpath('//div[@id="info"]//a[@rel="v:directedBy"]'
                                    '/text()')
        directorname = directorname.extract_first()
        fcrs2info[director] = directorname

        introduction = response.xpath('//*[@id="link-report-intra"]/span/text()')
        introduction = introduction.extract_first()
        fcrs2info['简介'] = introduction

        screenwriters = response.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').getall()        
        print(screenwriters)
        fcrs2info['编剧'] = screenwriters

        starring = response.xpath('//div[@id="info"]/span[3]/span[1]/text()')
        starring = starring.extract_first()
        starrings = []
        starringlist = response.xpath('//div[@id="info"]//a[@rel="v:starring"]')
        for star in starringlist[:5]:
            actor = star.xpath('./text()')
            actor = actor.extract_first()
            starrings.append(actor)
        fcrs2info[starring] = starrings
        yield fcrs2info

        print("actor_actiave")

        try:
            litags = response.xpath('//*[@id="celebrities"]/ul/li')
            if not litags:
                self.logger.warning("No actor tags found on page: %s", response.url)
                return

            for li in litags[1:]:
                actor = li.xpath('./div/span[1]/a/text()').extract_first()
                role = li.xpath('./div/span[2]/text()').extract_first()

                item = ActorItem()
                item['actor'] = actor if actor else "N/A"
                item['role'] = role if role else "N/A"

                actorlink = li.xpath('./div/span[1]/a/@href').extract_first()
                if actorlink:
                    yield scrapy.Request(url=actorlink, callback=self.actordetail, meta={'item': item,'href':href})
                else:
                    self.logger.warning("No actor link found for actor: %s", actor)
        except Exception as e:
            self.logger.error("Error in parse_actor: %s", e, exc_info=True)

        divtags = response.xpath('//div[@class="review-list  "]/div')
        self.url = response.meta.get('href')

        print("in parse_review:",self.url)
        for div in divtags:
            idname = div.xpath('./div/header/a[2]/text()').extract_first()
            title = div.xpath('./div/div/h2/a/text()').extract_first()

            shortcontent = div.xpath('.//div[@class="short-content"]//text()')
            if len(shortcontent) > 3:
                shortcontent = shortcontent.extract()[2]
            else:
                shortcontent = shortcontent.extract_first()
            shortcontent = re.sub(r'\(', '', shortcontent).strip()

            com_item = ReviewItem()
            com_item['idname'] = idname
            com_item['title'] = title
            com_item['shortcontent'] = shortcontent
            yield com_item

        newurltail = '?start=%d'
        if self.page < 5:
            newurl = str(self.url) + format(newurltail % (20 * self.page))
            self.page += 1
            yield scrapy.Request(url=newurl, callback=self.parse_review)
        

    def actordetail(self, response):
        href = response.meta.get('href')
        item = response.meta['item']
        self.logger.info("Fetching actor details from: %s", response.url)

        try:
            litags = response.xpath('//ul[@class="subject-property"]/li')
            if not litags:
                self.logger.warning("No details found for actor on page: %s", response.url)
                return

            actorkey = ['gender', 'birthday']
            for litag in litags[:2]:
                name = litag.xpath('./span[1]/text()').extract_first()
                content = litag.xpath('./span[2]/text()').extract_first()

                if name and content:
                    name = re.search(r'[\u4e00-\u9fa5]+', name).group() if re.search(r'[\u4e00-\u9fa5]+', name) else name
                    content = content.strip()
                    i = litags.index(litag)
                    item[actorkey[i]] = f"{name}: {content}"
                else:
                    self.logger.warning("Incomplete detail for tag on page: %s", response.url)

            yield item
            yield scrapy.Request(href, callback=self.parse_review, meta={'href': href})
        except Exception as e:
            self.logger.error("Error in actordetail: %s", e, exc_info=True)
    
    def parse_review(self, response):
        print(response)
        divtags = response.xpath('//div[@class="review-list  "]/div')
        self.url = response.meta.get('href')
        print("in parse_review:",self.url)
        for div in divtags:
            idname = div.xpath('./div/header/a[2]/text()').extract_first()
            title = div.xpath('./div/div/h2/a/text()').extract_first()

            shortcontent = div.xpath('.//div[@class="short-content"]//text()')
            if len(shortcontent) > 3:
                shortcontent = shortcontent.extract()[2]
            else:
                shortcontent = shortcontent.extract_first()
            shortcontent = re.sub(r'\(', '', shortcontent).strip()

            item = ReviewItem()
            item['idname'] = idname
            item['title'] = title
            item['shortcontent'] = shortcontent
            yield item

        newurltail = '?start=%d'
        if self.page < 5:
            newurl = str(self.url) + format(newurltail % (20 * self.page))
            self.page += 1
            yield scrapy.Request(url=newurl, callback=self.parse_review)
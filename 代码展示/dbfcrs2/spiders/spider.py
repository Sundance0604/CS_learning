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


def get_href():
    # 创建webdriver对象
    path = r'C:\\Users\86198\dbfcrs2\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)
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
    return hrefs



class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/explore']

    def start_requests(self):
        # 获取网页链接
        hrefs = get_href()
        for href in hrefs:
            yield scrapy.Request(href, callback=self.parse_movie)

    def parse_movie(self, response):
        fcrs2info = {}
        name = response.xpath('//div[@id="content"]/h1/span[1]/text()').extract_first()
        fcrs2info['电影名称'] = name

        year = response.xpath('//div[@id="content"]/h1/span[2]/text()').extract_first()
        year = re.search(r'\d+', year).group() if year else None
        fcrs2info['上映年份'] = year

        director = response.xpath('//div[@id="info"]/span[1]/span/text()').extract_first()
        directorname = response.xpath('//div[@id="info"]//a[@rel="v:directedBy"]/text()').extract_first()
        fcrs2info[director] = directorname

        starring = response.xpath('//div[@id="info"]/span[3]/span[1]/text()').extract_first()
        starrings = []
        starringlist = response.xpath('//div[@id="info"]//a[@rel="v:starring"]')
        for star in starringlist[:5]:
            actor = star.xpath('./text()').extract_first()
            starrings.append(actor)
        fcrs2info[starring] = starrings

        yield fcrs2info


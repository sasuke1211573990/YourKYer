import scrapy
from datetime import datetime
from ..items import EduInfoItem

class EduSpider(scrapy.Spider):
    name = "edu_spider"
    allowed_domains = ["yz.chsi.com.cn"]
    start_urls = ["https://yz.chsi.com.cn/"]

    def parse(self, response):
        # This is a sample parser. In reality, we need to inspect the target site structure.
        # Assuming we are scraping headlines from the main page
        
        for article in response.css('.news-list li'):
            item = EduInfoItem()
            item['title'] = article.css('a::text').get()
            item['link'] = response.urljoin(article.css('a::attr(href)').get())
            item['publish_date'] = datetime.now() # Mock date if not found
            item['content'] = "" # Would need to follow link to get content
            item['source'] = "yz.chsi.com.cn"
            item['category'] = "news"
            item['university'] = "General"
            yield item
            
        # Mocking finding other pages
        # next_page = ...
        # if next_page: yield response.follow(next_page, self.parse)

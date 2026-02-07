import scrapy

class EduInfoItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    publish_date = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field() # e.g., 'yz.chsi.com.cn'
    category = scrapy.Field() # e.g., 'policy', 'score_line'
    university = scrapy.Field()

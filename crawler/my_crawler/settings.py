BOT_NAME = 'my_crawler'

SPIDER_MODULES = ['my_crawler.spiders']
NEWSPIDER_MODULE = 'my_crawler.spiders'

ROBOTSTXT_OBEY = False

# Configure item pipelines
ITEM_PIPELINES = {
   'my_crawler.pipelines.PostgresPipeline': 300,
}

# DB Settings (Should match backend config)
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_SERVER = "db"
POSTGRES_PORT = "5432"
POSTGRES_DB = "edu_platform"

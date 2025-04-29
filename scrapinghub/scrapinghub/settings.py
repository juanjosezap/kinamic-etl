# Scrapy settings for scrapinghub project
BOT_NAME = "scrapinghub"

SPIDER_MODULES = ["scrapinghub.spiders"]
NEWSPIDER_MODULE = "scrapinghub.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure item pipelines
ITEM_PIPELINES = {
   "scrapinghub.pipelines.ArtworksPipeline": 300,
}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


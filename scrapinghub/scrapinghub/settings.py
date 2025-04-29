import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

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

DOWNLOADER_MIDDLEWARES = {
   "scrapinghub.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 543,
   'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#    'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
   # "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
   # "rotating_proxies.middlewares.BanDetectionMiddleware": 620
}

DOWNLOAD_DELAY = 3

# ScrapeOps
SCRAPEOPS_API_KEY = os.getenv('SCRAPEOPS_API_KEY')
SCRAPEOPS_NUM_RESULTS = 50
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = "https://headers.scrapeops.io/v1/browser-headers"
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True

PROXY_POOL_ENABLED = True
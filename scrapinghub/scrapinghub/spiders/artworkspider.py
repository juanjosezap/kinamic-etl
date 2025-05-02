import scrapy
from scrapinghub.items import ArtworkItem
class ArtworksSpider(scrapy.Spider):
    name = "artworkspider"
    allowed_domains = ["pstrial-2019-12-16.toscrape.com"]
    start_urls = ["http://pstrial-2019-12-16.toscrape.com/browse/insunsh/"]

    custom_settings = dict(
        # CLOSESPIDER_ITEMCOUNT = 10,
        RETRY_ENABLED = True,
        RETRY_TIMES = 5,
        RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429, 403],
        CONCURRENT_REQUESTS = 16,
        DOWNLOAD_DELAY = 1,
        RANDOMIZE_DOWNLOAD_DELAY = True,
        PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000,
        ITEM_PIPELINES= {
            "scrapinghub.pipelines.ArtworksPipeline": 300,
            "scrapinghub.pipelines.SaveToMySQLPipeline": 400
        },
        DOWNLOAD_HANDLERS = {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        ROBOTSTXT_OBEY = False,
        DOWNLOADER_MIDDLEWARES = {
            "scrapinghub.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 543,
            # "scrapinghub.middlewares.FreeProxyMiddleware": 749,
            # "scrapinghub.middlewares.CustomRetryMiddleware": 750
        }
    )

    def parse(self, response):
        # Extract and follow subcategory links
        subcats = response.css('div#subcats a::attr(href)').getall()
        for subcat in subcats:
            absolute_url = response.urljoin(subcat)
            yield scrapy.Request(absolute_url, meta=dict(
                    playwright = True,
                    playwright_include_page = True, 
                ), callback=self.parse)

        # Extract artwork URLs, excluding specific unwanted URLs
        artworks = response.xpath("//div[@id='subcats']/following-sibling::div[1]//a/@href").getall()
        artworks = [x for x in artworks if x != "/tarpit/die-scrapers-die"]

        # Follow each artwork URL to scrape artwork details
        for artwork_url in artworks:
            absolute_url = response.urljoin(artwork_url)
            yield scrapy.Request(absolute_url, meta=dict(
                    playwright = True,
                    playwright_include_page = True, 
                ), callback=self.parse_artwork)
        
        # If no artworks are found, return early
        if len(artworks) == 0 or not artworks:
            return

        # Follow pagination links to the next page
        next_form_action = response.css('form.nav::attr(action)').get()
        next_page_value = response.css('form.nav.next input[name="page"]::attr(value)').get()
        absolute_url = response.urljoin(next_form_action) + f"?page={next_page_value}"
        yield scrapy.Request(absolute_url, meta=dict(
                playwright = True,
                playwright_include_page = True, 
            ), callback=self.parse)

    def parse_artwork(self, response):
        item = ArtworkItem()

        item["url"] = response.url
        item["title"] = response.xpath("//h1/text()").get()
        item["artist"] = response.css('h2.artist ::text').get()
        item["description"] = response.css('div.description p ::text').get()
        item["image"] = response.url.split('/item')[0] + response.css('div#body > img::attr(src)').get()
        item["categories"] = response.request.headers.get("Referer", b"").decode("utf-8").split("browse/")[1].split(sep="/")

        rows = response.css('table.properties tr')
        for row in rows:
            key = row.css('td.key::text').get("").strip()
            value = " ".join(row.css('td.value ::text').getall()).strip()
            item_key = item.properties_mapping.get(key)
            if item_key: 
                item[item_key] = value

        yield item
import scrapy
from urllib.parse import urlparse

class ProxySpider(scrapy.Spider):
    name = "proxy_spider"
    allowed_domains = ["free-proxy-list.net", "sslproxies.org", "proxylist.geonode.com"]
    start_urls = [
        "https://free-proxy-list.net",
        "https://sslproxies.org",
        "https://proxylist.geonode.com/api/proxy-list?protocols=http%2Chttps&limit=500&page=1&sort_by=lastChecked&sort_type=desc"
    ]

    custom_settings = {
        "DOWNLOAD_HANDLERS": {},
        "ITEM_PIPELINES": {
            "scrapinghub.pipelines.ProxiesPipeline": 300
        }
    }

    def parse(self, response):

        # Extract the domain from the URL
        domain = urlparse(response.url).netloc

        # Route to the appropriate parser
        if domain == 'free-proxy-list.net' or domain == 'sslproxies.org':
            return self.parse_domain1(response)
        elif domain == 'proxylist.geonode.com':
            return self.parse_domain2(response)
        else:
            self.logger.warning(f"Unknown domain: {domain}")

    def parse_domain1(self, response):
        
        for row in response.css(".table.table-striped.table-bordered tbody tr"):
            ip = row.css("td:nth-child(1)::text").get()
            port = row.css("td:nth-child(2)::text").get()
            protocol = "https" if "yes" in row.css("td:nth-child(7)::text").get() else "http"
            last_checked = row.css("td:nth-child(8)::text").get()
            
            yield {
                "proxy": f"{protocol}://{ip}:{port}",
                "ip": ip,
                "port": port,
                "protocol": protocol,
                "last_checked": last_checked
            }

    def parse_domain2(self, response):

        data = response.json()
        for row in data['data']:
            ip = row['ip']
            port = row['port']
            if 'http' in row['protocols']:
                protocol = 'http'
            elif 'https' in row['protocols']:
                protocol = 'https'
            else:
                continue

            last_checked = "20 secs ago"
            
            yield {
                "proxy": f"{protocol}://{ip}:{port}",
                "ip": ip,
                "port": port,
                "protocol": protocol,
                "last_checked": last_checked
            }
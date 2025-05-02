# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from urllib.parse import urlencode
import random
import requests
import itertools
from scrapy.exceptions import NotConfigured
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import json

class ScrapinghubSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapinghubDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapeOpsFakeBrowserHeaderAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers?') 
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        payload = { 'api-key': self.scrapeops_api_key }
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        random_index = random.randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True

    def process_request(self, request, spider):
        random_browser_header = self._get_random_browser_header()

        request.headers['accept-language'] = random_browser_header['accept-language']
        request.headers['sec-fetch-user'] = random_browser_header.get('sec-fetch-user')
        request.headers['sec-fetch-mode'] = random_browser_header.get('sec-fetch-mode')
        request.headers['sec-fetch-site'] = random_browser_header.get('sec-fetch-site')
        request.headers['sec-ch-ua-platform'] = random_browser_header.get('sec-ch-ua-platform')
        request.headers['sec-ch-ua-mobile'] = random_browser_header.get('sec-ch-ua-mobile')
        request.headers['sec-ch-ua'] = random_browser_header.get('sec-ch-ua')
        request.headers['accept'] = random_browser_header.get('accept')
        request.headers['user-agent'] = random_browser_header.get('user-agent')
        request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests')

class ProxyRotationMiddleware:
    def __init__(self, proxy_list):
        self.proxy_cycle = itertools.cycle(proxy_list)

    @classmethod
    def from_crawler(cls, crawler):
        # Retrieve the proxy list path from settings
        proxy_list_path = crawler.settings.get('PROXY_LIST')
        if not proxy_list_path:
            raise NotConfigured('PROXY_LIST setting is missing.')
        
        # Read proxies from the file
        try:
            with open(proxy_list_path, 'r') as f:
                proxy_list = [line.strip() for line in f if line.strip()]
        except IOError:
            raise NotConfigured(f'Failed to read proxy file: {proxy_list_path}')
        
        if not proxy_list:
            raise NotConfigured('Proxy list is empty.')
        
        return cls(proxy_list)

    def process_request(self, request, spider):
        # Assign the next proxy in the cycle
        request.meta['proxy'] = next(self.proxy_cycle)



class FreeProxyMiddleware:
    """
    Middleware to use free proxies from various sources
    """
    
    def __init__(self, settings):
        # Maximum number of retries for each proxy before fetching new ones
        self.max_retry_times = settings.getint('RETRY_TIMES', 2)
        self.proxies = []
        self.proxy_index = 0
        self.retry_count = {}
        # Proxy sources configuration - customize these based on your needs
        self.proxy_sources = {
            'free_proxy_list': 'https://free-proxy-list.net/',
            'proxyscrape': 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
        }
    
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler.settings)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware
    
    def spider_opened(self, spider):
        self.fetch_proxies(spider)
    
    def fetch_proxies(self, spider):
        """Fetch proxies from free proxy services"""
        proxies = []
        
        # Method 1: Using free-proxy-list.net
        try:
            response = requests.get('https://free-proxy-list.net/')
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table', {'id': 'proxylisttable'})
                if table:
                    for row in table.tbody.find_all('tr'):
                        cols = row.find_all('td')
                        if len(cols) >= 7:
                            ip = cols[0].text.strip()
                            port = cols[1].text.strip()
                            https = cols[6].text.strip()
                            if https == 'yes':
                                proxy = f'https://{ip}:{port}'
                            else:
                                proxy = f'http://{ip}:{port}'
                            proxies.append(proxy)
                    print(f"Fetched {len(proxies)} proxies from free-proxy-list.net")
        except Exception as e:
            print(f"Error fetching proxies from free-proxy-list.net: {e}")
        
        # Method 2: Using proxyscrape.com
        try:
            response = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all')
            if response.status_code == 200:
                proxy_list = response.text.strip().split('\r\n')
                for proxy in proxy_list:
                    if proxy:
                        proxies.append(f'http://{proxy}')
                print(f"Fetched {len(proxy_list)} proxies from proxyscrape.com")
        except Exception as e:
            print(f"Error fetching proxies from proxyscrape.com: {e}")
        
        # Method 3: Using PubProxy (alternative)
        try:
            response = requests.get('http://pubproxy.com/api/proxy?limit=20&format=json&https=true')
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    for item in data['data']:
                        proxy = f"{item['type']}://{item['ip']}:{item['port']}"
                        proxies.append(proxy)
                    print(f"Fetched {len(data['data'])} proxies from pubproxy.com")
        except Exception as e:
            print(f"Error fetching proxies from pubproxy.com: {e}")
        
        if proxies:
            self.proxies = proxies
            self.proxy_index = 0
            random.shuffle(self.proxies)
            print(f"Total proxies fetched: {len(self.proxies)}")
        else:
            print("No proxies fetched from any source")
    
    def get_next_proxy(self):
        """Get the next proxy from the list"""
        if not self.proxies:
            self.fetch_proxies()
            
        if not self.proxies:
            return None
            
        proxy = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def process_request(self, request, spider):
        # Skip proxy rotation if flagged
        if 'no_proxy' in request.meta:
            return
            
        proxy = self.get_next_proxy()
        if proxy:
            request.meta['proxy'] = proxy
            request.meta['proxy_index'] = self.proxy_index
            print(f"Using proxy: {proxy}")
    
    def process_response(self, request, response, spider):
        # If the response is successful, return it
        if response.status < 400:
            return response
            
        # If we get an error, try another proxy
        proxy = request.meta.get('proxy')
        if proxy:
            # Track the number of retries for this proxy
            self.retry_count[proxy] = self.retry_count.get(proxy, 0) + 1
            
            # If we've exceeded the retry limit for this proxy, remove it
            if self.retry_count[proxy] >= self.max_retry_times:
                print(f"Removing failed proxy: {proxy}")
                if proxy in self.proxies:
                    self.proxies.remove(proxy)
                
        # Let RetryMiddleware handle the retry
        return response
    
    def process_exception(self, request, exception, spider):
        # Handle proxy errors
        proxy = request.meta.get('proxy')
        if proxy:
            print(f"Proxy error: {proxy}, Exception: {exception}")
            
            # Remove the problematic proxy
            if proxy in self.proxies:
                self.proxies.remove(proxy)
                
            # Try a new proxy
            request.meta['proxy'] = self.get_next_proxy()
            
            # Don't retry the request here, let RetryMiddleware do it
            return None


class CustomRetryMiddleware(RetryMiddleware):
    """
    Custom retry middleware that works with our proxy rotation system
    """
    

    def __init__(self, settings):
        super().__init__(settings)
        # Import the exceptions that should trigger a retry
        from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, ConnectionLost, TCPTimedOutError
        from twisted.web.client import ResponseFailed
        from scrapy.core.downloader.handlers.http11 import TunnelError
        
        self.EXCEPTIONS_TO_RETRY = (
            TimeoutError, 
            DNSLookupError, 
            ConnectionRefusedError, 
            ConnectionDone, 
            ConnectError, 
            ConnectionLost, 
            TCPTimedOutError,
            ResponseFailed, 
            TunnelError
        )

        # Define retry HTTP status codes
        self.retry_codes = settings.getlist('RETRY_HTTP_CODES', [500, 502, 503, 504, 408, 429, 403])

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
            
        if response.status in self.retry_codes:
            reason = response_status_message(response.status)
            # Remove the current proxy from meta to get a new one
            if 'proxy' in request.meta:
                del request.meta['proxy']
            return self._retry(request, reason, spider) or response
            
        return response
    
    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
            # Remove the current proxy from meta to get a new one
            if 'proxy' in request.meta:
                del request.meta['proxy']
            return self._retry(request, exception, spider)
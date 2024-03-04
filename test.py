import scrapy
from scrapy.crawler import CrawlerProcess
from db import insert_tuples
import sys
import time
from itertools import zip_longest

class TemplateSpider(scrapy.Spider):
    name = 'TemplateSpider'

    def __init__(self, start_urls=None, *args, **kwargs):
        super(TemplateSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls

    exchange_rates = []  # List to store exchange rates

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'HTTP_PROXY': 'http://localhost:55555',
        'PROXY_POOL_ENABLED': True,
        'PROXY_POOL_COUNT': 20,
        'PROXY_POOL_REFRESH_INTERVAL': 300,
        'PROXY_POOL_RETRY_TIMES': 5,
        'PROXY_POOL_FORCE_REFRESH': True,
        'RETRY_ENABLED': False,  # Disable retries
        'RETRY_TIMES': 2,
        'LOG_LEVEL': 'DEBUG',
    }

    handle_httpstatus_list = [500, 502, 503, 504, 400, 404, 429]  # Handle HTTP error codes

    def parse(self, response):
        if response.status == 200:
            exchange_rate = response.css('h3.cc__source-to-target span.text-success::text').get()
            base_currency, foreign_currency = self.extract_currencies(response.url)
            self.exchange_rates.append((base_currency, foreign_currency, exchange_rate))
        else:
            base_currency, foreign_currency = self.extract_currencies(response.url)
            alt_start_url = f"https://valuta.exchange/{base_currency.upper()}-to-{foreign_currency.upper()}?"
            yield scrapy.Request(alt_start_url, callback=self.parse_alt_link,
                                  meta={'base_currency': base_currency, 'foreign_currency': foreign_currency}, dont_filter=True)

    def extract_currencies(self, url):
        currencies = url.split('/')[-1].split('-to-')
        if len(currencies) >= 2:
            return currencies[0], currencies[1].split('-')[0]
        else:
            return None, None

    def parse_alt_link(self, response): 
        if response.status == 200:
            exchange_rate = response.css('div.UpdateTime__Container-sc-136xv3i-0.gMmDCR span.UpdateTime__ExchangeRate-sc-136xv3i-1.djCdnS::text').get()
            base_currency, foreign_currency = self.extract_currencies(response.url)
            self.exchange_rates.append((base_currency, foreign_currency, exchange_rate))
        else:
            base_currency = response.meta['base_currency']
            foreign_currency = response.meta['foreign_currency']
            alt_start_url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From={base_currency.upper()}&To={foreign_currency.upper()}"
            yield scrapy.Request(alt_start_url, callback=self.parse_xe_link,
                                  meta={'base_currency': base_currency, 'foreign_currency': foreign_currency}, dont_filter=True)
            
    def parse_xe_link(self, response):
        if response.status == 200:
            exchange_rate = response.css('main.tab-box__ContentContainer-sc-28io75-3.joNDZm p.result__BigRate-sc-1bsijpp-1.dPdXSB::text').get()
            base_currency, foreign_currency = self.extract_currencies(response.url)
            self.exchange_rates.append((base_currency, foreign_currency, exchange_rate))


    def close(self, reason):
        if self.exchange_rates:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    insert_tuples(self.exchange_rates)
                    return True  # Exit if successful
                except Exception as e:
                    self.logger.error(f"Database operation failed (attempt {attempt+1}): {e}")
                    if attempt < max_retries - 1:
                        self.logger.info(f"Retrying in 5 seconds...")
                        time.sleep(5)
            self.logger.critical("Failed to insert exchange rates after all retries")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        })
        start_urls = sys.argv[1].split(',')
        process.crawl(TemplateSpider, start_urls=start_urls)
        process.start()
    else:
        print("Please provide a list of start URLs as command-line argument separated by comma.")

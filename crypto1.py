import scrapy
from scrapy.crawler import CrawlerProcess

class InputValueSpider(scrapy.Spider):
    name = 'InputValueSpider'
    start_urls = [
        'https://www.tradingview.com/symbols/BTCUSD/',
    ]  # URL of the website to scrape
    
    exchange_rates = []  # List to store exchange rates

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }

    def parse(self, response):
        exchange_rate = response.css('h3.cc__source-to-target span.text-success::text').get()
        self.exchange_rates.append(exchange_rate)

    def close(self, reason):
        with open('exchange_rates.txt', 'w') as file:
            for rate in self.exchange_rates:
                file.write(rate + '\n')

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
})
process.crawl(InputValueSpider)
process.start()

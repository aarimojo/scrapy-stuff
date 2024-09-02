import scrapy
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemloaders import ChocolateProductLoader
from urllib.parse import urlencode
from dotenv import load_dotenv
from os import getenv

load_dotenv()

API_KEY = getenv('SCRAPEOPS_API_KEY')

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk", "proxy.scrapeops.io"]
    # start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def start_requests(self):
        start_url = "https://www.chocolate.co.uk/collections/all"
        yield scrapy.Request(url=get_scrapeops_url(start_url), callback=self.parse)

    def parse(self, response):
        products = response.css("product-item")

        for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
 
            chocolate.add_css('name', "a.product-item-meta__title::text")
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*?)</span>')
            chocolate.add_css('url', "a.product-item-meta__title::attr(href)")
            yield chocolate.load_item()

        next_page = response.css('[rel="next"]::attr("href")').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(get_scrapeops_url(next_page_url), self.parse)

import scrapy
from scrapy_playwright.page import PageMethod
from Property.items import PropertyItem
import json 
import re
from playwright.sync_api import sync_playwright
import playwright
class PropertySpider(scrapy.Spider):
       
    file_path = '/home/pbx1/Documents/Scrapy/real_estate_scraping/webapp/data.json'

    
    data_dict = {}

    
    with open(file_path, 'r') as file:
        data_dict = json.load(file)
    city = data_dict.get('city', 'default_city')
    min_price=data_dict.get('minPrice','default_min_price')
    max_price=data_dict.get('maxPrice','default_price')
    min_area=data_dict.get('minArea','default_area')
    max_area=data_dict.get('maxArea','default_area')
    beds=data_dict.get('beds','default_beds')
    bathrooms=data_dict.get('baths','default_bathrooms')
    category=data_dict.get('category','default_category')
    property_type=data_dict.get('propertyType','default_propert_type')
    words = re.split(' |_| ', property_type)
    formatted_property_type = ' '.join(word.capitalize() for word in words)
    name = "property"
    allowed_domains = ["www.zameen.com"]
    data_dict = {}
    with open(file_path, 'r') as file:
        data_dict = json.load(file)
    
    start_urls = ["https://www.zameen.com/Homes/Rawalpindi-41-1.html"]
    def start_requests(self):
        page_method_script = """
            (() => {
                const xpath = "//iframe[@id='google_ads_iframe_/31946216/Splash_660x500_0']";
                const iframe = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (iframe) {
                    // Perform your actions with the iframe here
                    // Example: Clicking a button inside the iframe (note: direct DOM access to cross-origin iframes is not allowed)
                    // iframe.contentWindow.document.querySelector('button.someButton').click();

                    // For demonstration, let's just log the iframe's presence
                    console.log('Iframe found');
                } else {
                    console.log('Iframe not found');
                }
            })();
        """


        playwright_page_methods = [
            PageMethod('wait_for_timeout', 7000),
            PageMethod('wait_for_selector', '#google_ads_iframe_\\/31946216\\/Splash_660x500_0'),
            PageMethod('evaluate', page_method_script),

            PageMethod('click','div.e7c6503c[aria-label="Category filter"]'),
            PageMethod("wait_for_selector", "li._31a8085a"),
            PageMethod('click', f"text='{self.formatted_property_type}'"),
            
               
            
            PageMethod('click', 'div.e7c6503c[aria-label="City filter"]'),
            PageMethod('wait_for_selector', 'input._37492cd0'),
            PageMethod('fill', 'input._37492cd0', self.city),
            PageMethod('click', 'button._933a9a61._5dd5033c'),
            PageMethod('wait_for_timeout', 5000),
            PageMethod('click', 'div._3a42e70b._792214e8'),
            PageMethod('wait_for_selector', "input[id='activeNumericInput']"),
            PageMethod('fill', 'input[id="activeNumericInput"]', self.min_price),
            PageMethod('fill', 'input[id="inactiveNumericInput"]', self.max_price),
            PageMethod('click', 'div._3a42e70b._792214e8'),
        ]
        
        if self.category == "homes_category":
            playwright_page_methods.extend([
                # Beds
                PageMethod('click', 'div._3a42e70b._639a776e'),
                PageMethod('wait_for_selector', "div.ede17658"),
                PageMethod('click', f'button[aria-label="{self.beds}"]'),
                PageMethod('click', 'div._3a42e70b._639a776e'),
                # Baths
                PageMethod('click', 'div._3a42e70b._81da50e2'),
                PageMethod('wait_for_selector', "div.ede17658"),
                PageMethod('click', f'button[aria-label="{self.bathrooms}"]'),
                PageMethod('click', 'div._3a42e70b._81da50e2'),
            ])
        playwright_page_methods.extend([
        PageMethod('click', 'div._3a42e70b.b24af455'),
        PageMethod('wait_for_selector', "input[id='activeNumericInput']"),
        PageMethod('fill', 'input[id="activeNumericInput"]', self.min_area),
        PageMethod('fill', 'input[id="inactiveNumericInput"]', self.max_area),
        PageMethod('click', 'div._3a42e70b.b24af455'),
        PageMethod('wait_for_timeout', 5000),
            ])
 
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods':playwright_page_methods
                },
                callback=self.parse
            )

    async def parse(self, response):
                # Scrape the page content after interaction
                listings = response.css('ul._357a9937 > li.ef447dde, article._92cbc48a')
                for listing in listings:
                    item = PropertyItem()
                    item['price'] = listing.css("span.f343d9ce::text").get()
                    item['name'] = listing.css("h2.c0df3811::text").get()
                    item['beds'] = listing.css('span.b133f61d:nth-of-type(1) > ._984949e5::text').get()
                    item['bathrooms'] = listing.css('span.b133f61d:nth-of-type(2) > ._984949e5::text').get()
                    item['area'] = listing.css('span.b133f61d:nth-of-type(3) > ._984949e5 div._7ac32433 > div._026d7bff > div > span::text').get()
                    item['link'] = listing.css("div.f74e80f3 a::attr(href)").get()
                    yield item
                next_page = response.css('a[title="Next"]::attr(href)').get()
                if next_page:
                    next_page_link = response.urljoin(next_page)
                    yield scrapy.Request(
                        next_page_link,
                        callback=self.parse
                    )
    async def parse1(self, response):
            page = response.meta['playwright_page']
            listings = response.css('ul._357a9937 > li.ef447dde, article._92cbc48a')
            for listing in listings:
                item = PropertyItem()
                item['price'] = listing.css("span.f343d9ce::text").get()
                item['name'] = listing.css("h2.c0df3811::text").get()
                item['beds'] = listing.css('span.b133f61d:nth-of-type(1) > ._984949e5::text').get()
                item['bathrooms'] = listing.css('span.b133f61d:nth-of-type(2) > ._984949e5::text').get()
                item['area'] = listing.css('span.b133f61d:nth-of-type(3) > ._984949e5 div._7ac32433 > div._026d7bff > div > span::text').get()
                item['link'] = listing.css("div.f74e80f3 a::attr(href)").get()
                yield item
            next_page = response.css('a[title="Next"]::attr(href)').get()
            if next_page:
                next_page_link = response.urljoin(next_page)
                yield scrapy.Request(
                    next_page_link,
                    callback=self.parse1
                )
            await page.close()

    async def parse1(self, response):
        listings = response.css('ul._357a9937 > li.ef447dde, article._92cbc48a')
        for listing in listings:
            item = PropertyItem()
            item['price'] = listing.css("span.f343d9ce::text").get()
            item['name'] = listing.css("h2.c0df3811::text").get()
            item['beds'] = listing.css('span.b133f61d:nth-of-type(1) > ._984949e5::text').get()
            item['bathrooms'] = listing.css('span.b133f61d:nth-of-type(2) > ._984949e5::text').get()
            item['area'] = listing.css('span.b133f61d:nth-of-type(3) > ._984949e5 div._7ac32433 > div._026d7bff > div > span::text').get()
            item['link'] = listing.css("div.f74e80f3 a::attr(href)").get()
            yield item
        next_page = response.css('a[title="Next"]::attr(href)').get()
        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(
            
                next_page_link,
               
                callback=self.parse1
            )
     
import scrapy


class Cinema21Spider(scrapy.Spider):
    name = "cinema21"
    allowed_domains = ["www.cinema21.com"]
    start_urls = ["https://www.cinema21.com"]
    for url in start_urls:
        yield scrapy.Request(url = url, callback = self.parse) 

    def parse(self, response):
        page=response.url.split('/')[-3]
        title = response.selector.xpath('//div[contains(@class, "movie-info")//h2]')

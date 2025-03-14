import scrapy


class Cinema21Spider(scrapy.Spider):
    name = "cinema21"
    allowed_domains = ["www.cinema21.com"]
    start_urls = ["https://www.cinema21.com"]
    for url in start_urls:
        yield scrapy.Request(url = url, callback = self.parse) 

    def parse(self, response):
        #Ok, so this is wrong, although my selector was mostly written correctly!
        #I'm actually pulling from a Javascript thingy. SO I would need to parse it out of javascript first.
        #title = response.css(div.movieData/title::text).getall(Default='Nothing Found')
        

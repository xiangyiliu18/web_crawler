import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        filename="wordlist.txt"
        with open(filename, 'w+') as f:
             for text in response.xpath('//body//text()').extract():
                text.strip()
                if text is None:
                    text="HAHAHAHA"
                f.write("1 "+text)
   

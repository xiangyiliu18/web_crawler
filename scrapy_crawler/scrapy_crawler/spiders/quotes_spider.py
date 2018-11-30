import scrapy

## scrapy the website: http://quotes.toscrape.com/login
class QuotesSpider(scrapy.Spider):
    ''' Identifies the Spider.  It must be unique with a project. '''

    name = "quotes" 
    ## 'strat_requests'--> return an iterable of Requests which the Spider will begin to crawl from
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/', ## the starting html page
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):  ## to handle the response dowloaded for each of the request made.
        ## 'response' -- an instance of 'TextResponses'
        ## parse() --- extract the scraped data as dicts and also finding new URLs to follow and creating new requests(Request)
        print(response)
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
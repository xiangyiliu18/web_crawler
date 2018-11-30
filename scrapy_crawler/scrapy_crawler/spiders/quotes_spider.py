import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    ''' Identifies the Spider.  It must be unique with a project. '''

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)
        ## 'response' -- an instance of 'TextResponses'
        ## parse() --- extract the scraped data as dicts and also finding new URLs to follow and creating new requests(Request)
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
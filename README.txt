cse331 SBU 11/29/18
Web Crawler + Form Brute
Cheryl

1. Basic instruction:
Start your first spider with:
	cd scrapy_crawler
	scrapy genspider example example.com

1.1 TextResponse 
	--- Objects : which support the following attributese in addition to the standard response ones:
		--- text(response body, as unicode) == result is cached after the fist call, so can access 'response.text' multiple times without extra overhead
		--- econding
		--- selector
		....
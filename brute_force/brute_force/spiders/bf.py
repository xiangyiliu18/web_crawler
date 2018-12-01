import scrapy
class LoginSpider(scrapy.Spider):
    name = 'logins'

    def start_requests(self):
        return [scrapy.FormRequest("http://ec2-18-216-197-130.us-east-2.compute.amazonaws.com/wp-login.php",
                                   formdata={'user': 'user', 'pass': 'EN9fQcC3jnsS'},
                                   callback=self.logged_in)]

    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        pass
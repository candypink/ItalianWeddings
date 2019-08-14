import scrapy


class ForumSpider(scrapy.Spider):
    name = "forum-get-body"

    def start_requests(self):
        url_list = ['https://www.matrimonio.com/forum/prova-trucco--t750941']
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        with open('test.html', 'wb') as f:
            f.write(response.body)

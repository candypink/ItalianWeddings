import scrapy


class ForumSpider(scrapy.Spider):
    name = "forum"

    def start_requests(self):
        urls = [
            'https://www.matrimonio.com/forum/recenti'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_topic(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').get()
        text = response.xpath('//div[@class="com-post-content left-center-enabled"]/text()').get()
        #text_comments = 
        yield{
            'title':title,
            'text':text
            }

    def parse(self, response):
        #filename = 'forum-recenti.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        for topic_ref in response.xpath('//div[@class="discussion-post-item "]//a[@class="discussion-post-item-title"]'):
            yield response.follow(topic_ref, callback=self.parse_topic)
        
        # questa parte funziona 
        #for a in response.xpath('//a[@class="next"]'):
        #    yield response.follow(a, callback=self.parse)
    

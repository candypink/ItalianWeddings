import scrapy


class ForumSpider(scrapy.Spider):
    name = "forum"

    def start_requests(self):
        urls = [
            'https://www.matrimonio.com/forum/recenti'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse_comment(self,response):
        print('   chiara: in test_fun!!')
        i=0
        for comment in response.xpath('//li[@class="pure-g discuss-post-comment"]'):
            # take all the text, turn it to lower case and remove extra spaces
            # ignore 'Visualizza messaggio citato'
            text = [x.strip().lower() for x in comment.xpath('div//div[contains(@class,"discuss-post-comment-content") and contains(@class,"com-discuss")]/*//text()').getall() 
                    if 'Visualizza messaggio citato' not in x]
            # remove empty strings
            text = list(filter(None, text))
            # join different paragraphs of same comment
            text = ' '.join(text)
            title = 'comment'
            print(text)
            yield{
                'title':title,
                'text':text
                }

    def parse_topic(self, response):
        print("chiara: parsing topic")
        title = response.xpath('//meta[@property="og:title"]/@content').get().strip().lower()
        text = response.xpath('//div[contains(@class,"com-post-content")]/text()').get().strip().lower()
        yield{
            'title':title,
            'text':text
            }
        # store the comments on the first page of the thread
        for comment in self.parse_comment(response):
            yield comment
        # now I follow the other pages on the same thread

    def parse(self, response):
        # from the main page, follow each comment to its own page
        for topic_ref in response.xpath('//div[@class="discussion-post-item "]//a[@class="discussion-post-item-title"]'):
            yield response.follow(topic_ref, callback=self.parse_topic)
        
        # questa parte funziona 
        #for a in response.xpath('//a[@class="next"]'):
        #    yield response.follow(a, callback=self.parse)
    

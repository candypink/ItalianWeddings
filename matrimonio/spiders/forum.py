import scrapy

def clean_time(input):
    time = input.lower().replace(',','').replace('alle ','').replace('il','').strip()
    return time

class ForumSpider(scrapy.Spider):
    name = "forum"

    def start_requests(self):
        urls = [
            'https://www.matrimonio.com/forum/recenti'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse_comments(self, parent_id, response):
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
            title = 'comment' # comments don't have title, but giving them the titile comment can help distinguish from main thread
            id = comment.xpath('div//div[@class="discussion-message-globe"]/div[@class="discuss-post-comment-header"]/@id').get(default='NA').lower().strip()
            author = comment.xpath('div/a/@data-id-user').get(default='NA').lower().strip()
            time = clean_time(comment.xpath('div//time/text()').get(default='NA'))
            yield{
                'title':title,
                'text':text,
                'id':id,
                'author':author,
                'time': time,
                'parent_id': parent_id
                }

    def parse_topic(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').get(default='NA').strip().lower()
        text = response.xpath('//div[contains(@class,"com-post-content")]/text()').get(default='NA').strip().lower()
        id = response.xpath('//div[@id="relatedDressesBox"]/@data-idtema').get(default='NA').lower().strip()
        author = response.xpath('//div[@class="wrapper main"]//div[contains(@class,"com-post-header-author")]/a/@data-id-user').get(default='NA').lower().strip()
        time = clean_time(response.xpath('//span[@class="com-post-header-meta-date"]/text()').getall()[1])
        yield{
            'title':title,
            'text':text, 
            'id':id,
            'parent_id':id, #for the initial post I set the parent id as the it of the post itself
            'author':author,
            'time':time
            }
        # store the comments on the first page of the thread
        for comment in self.parse_comments( parent_id=id, response=response):
            yield comment 
        # now I follow the other pages on the same thread
        for link in response.xpath('/html/head/link[@rel="next"]/@href').getall():
            yield response.follow(link, callback=lambda y: self.parse_comments(parent_id=id, response=y))
        

    def parse(self, response):
        # from the main page, follow each comment to its own page
        for topic_ref in response.xpath('//div[@class="discussion-post-item "]//a[@class="discussion-post-item-title"]'):
            yield response.follow(topic_ref, callback=self.parse_topic)
        # lok at pages after the first one
        for a in response.xpath('//a[@class="next"]'):
            yield response.follow(a, callback=self.parse)
    

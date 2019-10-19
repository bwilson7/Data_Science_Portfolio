import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

class UserCommentsSpider(CrawlSpider):
    name = 'user_comments_spider'
    allowed_domains = ['trailforks.com']
    start_urls = ['https://www.trailforks.com/region/united-states/trails/']

    trail_links = "//td[@class=' highlight']//a"
    next_page = "//ul//li[@class='next-page']//a"
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths=trail_links, unique=True), callback='parse_comments', follow=True),
        Rule(LinkExtractor(restrict_xpaths=next_page), follow=True)
    )

    def parse_comments(self, response):
        if response.xpath("//*[@class='ppcont']").get() is None:
            
            comment_dic = {}
            comment_dic['trail_id'] = response.xpath("/html/body/div[1]/div/div[4]/div[3]/section/div[1]/div[1]/div[2]/div[1]/div[2]/div/ul/@id").get()
            comment_dic['trail_name'] = response.xpath("//span[@id='trailtitle']/text()").get()
            comment_dic['user'] = 'NaN'
            comment_dic['posting_date'] = 'NaN'
            comment_dic['comment'] = 'NaN'
            
            yield comment_dic
        
        else:
            
            comments = response.xpath("//div[@id='comment_wrap']//div[@class='ppcont']//div[@class='comtext translate']//text()").getall() 
            user = response.xpath("//div[@id='comment_wrap']//div[@class='ppcont']//div//span[@class='link clickable']//text()").getall()  
            posting_datetime = response.xpath("//div[@id='comment_wrap']//div[@class='ppcont']//div//span[@class='time']//text()").getall()
        
            #all comment text starts with '\n' so I am skipping those when zipping the data together
            user_comments = set(zip(user, comments[1::2], posting_datetime))

            for i in user_comments:
                
                comment_dic = {}
                comment_dic['trail_id'] = response.xpath("/html/body/div[1]/div/div[4]/div[3]/section/div[1]/div[1]/div[2]/div[1]/div[2]/div/ul/@id").get()
                comment_dic['trail_name'] = response.xpath("//span[@id='trailtitle']/text()").get()
                comment_dic['user'] = i[0]
                comment_dic['posting_date'] = i[2]
                comment_dic['comment'] = i[1]
                
                yield comment_dic

process = CrawlerProcess({
    'FEED_FORMAT':'json',
    'FEED_URI':'usa_trails_user_comments.json',
    'LOG_ENABLED':True,
    'USER-AGENT':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'ROBOTSTXT_OBEY':True,
    'AUTOTHROTTLE_ENABLED':True,
    'HTTPCACHE_ENABLED':True
})

process.crawl(UserCommentsSpider)
process.start()
print('Trails Scraping Done!')

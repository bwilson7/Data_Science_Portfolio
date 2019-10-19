import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
import re

class UserRatingSpider(scrapy.Spider):
    name = 'user_rating_spider'
    start_urls = ['https://www.trailforks.com/region/united-states/trails/']
    
    def parse(self, response):
        #follow all trail links on the page
        for trail in response.xpath("//td[@class=' highlight']//a/@href").getall():
            trail_page = scrapy.Request(trail, callback=self.parse_votes_link)
            yield trail_page
        
        #follow the next_page until all trail pages are parsed
        next_page = response.xpath("//ul/li[@class='next-page']/a/@href").get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
            
    def parse_votes_link(self, response):
        if re.search('/error/', str(response)):
            print('/nError Request')
            print(response.request.meta['redirect_urls'][0])
            
        vote_link = response.xpath("/html/body/div[1]/div/div[4]/div[3]/section/div[1]/div[1]/div[2]/div[1]/div[2]/div/div[2]/span[2]/@data-url").get()
        if vote_link is not None:
            link = scrapy.Request(vote_link, callback=self.parse_votes)
            yield link
    
    def parse_votes(self, response):
        for row in response.xpath("/html/body/div[1]/div/div[4]/div[3]/section/table[1]/tbody/tr"):
            user_rating = {}
            user_rating['user'] = row.xpath("td[2]/a/text()").get()
            user_rating['rate_date'] = row.xpath("td[3]/div/div/text()").get()
            user_rating['rating'] = row.xpath("td[4]/div/ul/@rating").get()
            user_rating['trail_id'] = row.xpath("td[4]/div/ul/@id").get()

            yield user_rating

process = CrawlerProcess({
    'FEED_FORMAT':'json',
    'FEED_URI':'usa_trails_user_rankings.json',
    'LOG_ENABLED':True,
    'USER-AGENT':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'ROBOTSTXT_OBEY':True,
    'AUTOTHROTTLE_ENABLED':True,
    'HTTPCACHE_ENABLED':True
})

process.crawl(UserRatingSpider)
process.start()
print('Trails Scraping Done!')
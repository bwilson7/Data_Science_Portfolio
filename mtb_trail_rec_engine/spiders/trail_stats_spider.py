import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

def set_to_dict(set1):
    dic1 = {}
    for i in set1:
        dic1[i[0]] = i[1]
    return dic1


class TrailsSpider(CrawlSpider):

    name = 'trails_spider'

    allowed_domains = ['trailforks.com']
    start_urls = ['https://www.trailforks.com/region/united-states/trails/']

    trail_links = "//td[@class=' highlight']//a"
    next_page = "//il/li[@class='next-page']/a"

    rules = (
        Rule(LinkExtractor(restrict_xpaths=trail_links, unique=True), callback='parse_trailstats', follow=True),
        Rule(LinkExtractor(restrict_xpaths=next_page), follow=True)
    )
    
    def parse_trailstats(self, response):
                
        trail_stats = {}
        
        trail_stats['trail_id'] = response.xpath("/html/body/div[1]/div/div[4]/div[3]/section/div[1]/div[1]/div[2]/div[1]/div[2]/div/ul/@id").get()
        
        trail_stats['trail_name'] = response.xpath("//li[@id='page_title']//h1//span//text()").get(default='BUMMER')
                
        #collecting basic trail stats from first greybox on trail page
        stat = response.xpath("//div[@class='col-3']//div[@class='large']//text()").getall()
        stat_name = response.xpath("//div[@class='col-3']//div[@class='small grey']//text()").getall()
        basic_stats = set(zip(stat_name, stat))
        trail_stats.update(set_to_dict(basic_stats))

        #trail description is not in an iterable table so xpath is simpler
        trail_stats['description'] = response.xpath("//div[@class='block padding-top-30']//p//text()").get(default='BUMMER')

        #storing first part of xpath in a vairable for readability & length reasons
        more_details = "//div[@class='clearfix block']//ul[@id='trailstats_display']//li"
        title = response.xpath(more_details + "//div[@class='term']//text()").getall()
        value = response.xpath(more_details + "//div[@class='definition']//text()").getall()
        
        #title includes 'average_time' data at the end of the table where time is not in definition class
        #this will be extracted on it's own and not with the rest of the table
        topo_details = set(zip(title[:len(title)], value))
        trail_stats.update(set_to_dict(topo_details))
        trail_stats['Average time'] = response.xpath(more_details + "//div[@class='definition hovertip']//text()").get(default='BUMMER')

        #total historical rides is not in an iterable table
        trail_stats['total_rides'] = response.xpath("//div[@class='margin-bottom-15 clearfix']//div[@class='col-4 last']//li//b//text()").get(default='BUMMER')

        #this is the total # of comments for the trail
        trail_stats['comment_count'] =  response.xpath("//div[@class='comcount']//h3//text()").get(default='BUMMER')
        
        #main details table is inconsistent with class names and row in the table
        #so selecting the necessary data is not very straightforward
        terms = response.xpath("//li//div[@class='term']//text()").getall()
        main_details = ['Riding Area', 'Difficulty Rating', 'Trail Type', 'Bike Type', 'Dogs Allowed', 'TTFs on Trail', 'Global Ranking']
        special_details = ['Riding Area', 'Difficulty Rating', 'Global Ranking']
        
        for detail in main_details:
            try:
                ind = terms.index(detail) + 1
                if detail in special_details:
                    if detail == 'Riding Area':
                        trail_stats['location'] = response.xpath("//li[{}]//div[@class='definition']/br/following::text()".format(ind)).get()
                        trail_stats[detail] = response.xpath("//li[{}]//div[@class='definition']//a//text()".format(ind)).get()
                    elif detail == 'Difficulty Rating':
                        trail_stats[detail] = response.xpath("//li[{}]//div[@class='definition diffratingvoteLink']/span/@title".format(ind)).get()
                    elif detail == 'Global Ranking':
                        trail_stats[detail] = response.xpath("//li[{}]//div[@class='definition']//a//text()".format(ind)).get()
                else:        
                    trail_stats[detail] = response.xpath("//li[{}]//div[@class='definition']//text()".format(ind)).get()
            except ValueError:
                trail_stats[detail] = 'BUMMER'
                
        yield trail_stats

process = CrawlerProcess({
    'FEED_FORMAT':'json',
    'FEED_URI':'usa_trails_details_102019.json',
    'LOG_ENABLED':True,
    'USER-AGENT':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'ROBOTSTXT_OBEY':True,
    'AUTOTHROTTLE_ENABLED':True,
    'HTTPCACHE_ENABLED':True
})

#Initiate the Spider and print when it's done
process.crawl(TrailsSpider)
process.start()
print('Trails Scraping Done!')










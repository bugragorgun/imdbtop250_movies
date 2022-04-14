import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/chart/top/']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'

# , headers={'User-Agent': self.user_agent}
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250')

# , process_request='set_user_agent'

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td[@class="titleColumn"]/a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths=''), process_request='set_user_agent')
    )

    # def set_user_agent(self,request,spider):
    #     request.headers['User-Agent']=self.user_agent

    def parse_item(self, response):
        yield{
            'title': response.xpath("//div[@class='sc-94726ce4-1 iNShGo']/h1/text()").get(),
            'year': response.xpath("//span[@class='sc-8c396aa2-2 itZqyK']/text()").get(),
            'duration': response.xpath("(//li[@class='ipc-inline-list__item'])[3]/text()").get(),
            'rate': response.xpath("(//span[@class='sc-7ab21ed2-1 jGRxWM'])[2]/text()").get(),
            'movie_url': response.url,
            # 'user_agent': response.request.headers['User-Agent']
        }
        
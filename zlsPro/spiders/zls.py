import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis
from ..items import ZlsproItem


class ZlsSpider(CrawlSpider):
    name = 'zls'
    # allowed_domains = ['xxx.com']
    # start_urls = ['https://www.4567kan.com/index.php/vod/show/class/%E5%8A%A8%E4%BD%9C/id/1.html']
    # start_urls = ['https://www.4567kan.com/index.php/vod/show/class/%E7%88%B1%E6%83%85/id/1.html']
    start_urls = ['https://www.4567kan.com/index.php/vod/show/class/%E5%96%9C%E5%89%A7/id/1.html']

    # conn = Redis(host='127.0.0.1',port=6379)

    # /index.php/vod/show/class/%E5%8A%A8%E4%BD%9C/id/1/page/2.html
    link = LinkExtractor(allow=r'1/page/\d+\.html')
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 解析电影的名称+电影详情页的url
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            title = li.xpath('./div/a/@title').extract_first()
            detail_url = 'https://www.4567kan.com' + li.xpath('./div/a/@href').extract_first()

            # 用于记录爬取过的链接，如果爬取过了，就不再爬取了
            # ex = self.conn.sadd('movie_urls',detail_url)
            # ex==1插入成功，ex==0插入失败

            # if ex == 1: # detail_url表示的电影 没有存在于redis数据库的记录表中
            #     # 爬取电影数据：发起请求
            #     print('有新数据更新，正在爬取新数据......')
            #     item = ZlsproItem()
            #     item['title'] = title
            #
            #     yield scrapy.Request(url=detail_url,callback=self.parse_detail,meta={'item':item})
            # else:  # 存在于记录表中
            #     print('暂无数据更新！')

            item = ZlsproItem()
            item['title'] = title
            item['detail_url'] = detail_url

            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self,response):
        # 解析电影简介
        item = response.meta['item']
        desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
        item['desc'] = desc

        yield item
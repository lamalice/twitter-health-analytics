from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from TwitterBot.items import TwitterbotItem


class TwitterCrawler(CrawlSpider):
    name='twittercrawler'
    allowed_domains = ['twitter.com']

    start_urls = ['https://twitter.com/search?q=%23flu&src=typd']

    rules = [
        Rule(LinkExtractor(
            allow=(),
            deny=(),
        ),
            callback='parse_item',
            # process_links='filter_links',
            follow=True)
    ]

    def parse_item(self, response):
        items = []
        sel = Selector(response)
        item = TwitterbotItem()
        page_items = sel.xpath('//li[contains(@class,"js-stream-item")]').extract()

        if page_items:
            page_selector = Selector(text=page_items[0])

            item['post_text'] = page_selector.xpath('//span[contains(@class,"js-display-url")]/text()').extract() + page_selector.xpath('//p[contains(@class,"TweetTextSize")]/text()').extract() + page_selector.xpath('//a[contains(@class,"twitter-atreply")]/s/text()').extract() +  page_selector.xpath('//a[contains(@class,"twitter-atreply")]/b/text()').extract()

            item['user_name'] = '@' + page_selector.xpath('//span[contains(@class,"username")]/b/text()').extract_first()
            item['date'] = page_selector.xpath('//small/a/@title').extract_first()

            item['hash_tags'] = page_selector.xpath('//a[contains(@class,"twitter-hashtag")]/@href').extract()
            item['twitter_url'] = page_selector.xpath('//a[contains(@href,"/status/")]/@href').extract_first()
            if item['twitter_url']:
                item['twitter_url'] = 'https://twitter.com' + item['twitter_url']

            items.append(item)

        return items
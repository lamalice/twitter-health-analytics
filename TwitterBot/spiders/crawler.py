from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from TwitterBot.items import TwitterbotItem
from TwitterBot.spiders.helper import TwitterHelper as Helper
import scrapy
import re

file = open("/Users/alicelam/Kstate_Classes/CIS598/twitter-health-analytics/TwitterBot/data/file2.json", 'w')
file.write("[")

class TwitterCrawler(CrawlSpider):
    name='twittercrawler'
    allowed_domains = ['twitter.com']

    start_urls = [
        # 'https://twitter.com/ChelseaClinton'
        # 'https://twitter.com/search?q=%23fluseason&src=typd'
        'https://twitter.com/search?q=%23flu&src=typd',
        # 'https://twitter.com/search?q=%23fever&src=typd',
        # 'https://twitter.com/search?q=%23sick&src=typd',
        # 'https://twitter.com/search?q=%23commoncold&src=typd',
        # 'https://twitter.com/search?q=%23stomachache&src=typd',
        # 'https://twitter.com/search?q=%23sorethroat&src=typd',
        # 'https://twitter.com/search?q=%23runnynose&src=typd'
     ]
    rules = [
        Rule(LinkExtractor(
            restrict_xpaths='//div[contains(@class,"content-main")]',
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
        # item = TwitterbotItem()
        #
        # timeline = sel.xpath('//div[contains(@class,"content-main")]').extract()
        #
        # for x in range(len(timeline)):
        #     timeline_selector = Selector(text=timeline[x])

            # if timeline_selector:
        container = sel.xpath('//div[contains(@class,"content-main")]').extract()

        for x in range(len(container)):
            container = Selector(text=container[x])

            page_items = container.xpath('//li[contains(@class,"js-stream-item")]').extract()
            # file.write(str(page_items))

            location = Helper().cleaner(sel.xpath(
                '//span[contains(@class,"ProfileHeaderCard-locationText")]/text()').extract())
            if page_items:
                for x in range(len(page_items)):
                    page_selector = Selector(text=page_items[x])
                    item = TwitterbotItem()

                    item['twitter_url'] = page_selector.xpath('//a[contains(@href,"/status/")]/@href').extract_first()
                    if item['twitter_url']:
                        item['twitter_url'] = 'https://twitter.com' + item['twitter_url']

                        item['post_text'] = page_selector.xpath('//span[contains(@class,"js-display-url")]/text()').extract() + page_selector.xpath('//p[contains(@class,"TweetTextSize")]/text()').extract() + page_selector.xpath('//a[contains(@class,"twitter-atreply")]/s/text()').extract() +  page_selector.xpath('//a[contains(@class,"twitter-atreply")]/b/text()').extract()

                        item['user_name'] = '@' + page_selector.xpath('//span[contains(@class,"username")]/b/text()').extract_first()
                        item['date'] = Helper().translate(page_selector.xpath('//small/a/@title').extract_first())
                        item['hash_tags'] = page_selector.xpath('//a[contains(@class,"twitter-hashtag")]/@href').extract()
                        item['user_location'] = location
                        item['post_retweets'] = page_selector.xpath('//button[contains(@data-modal,"ProfileTweet-retweet")]//span[contains(@class, "ProfileTweet-actionCountForPresentation")]/text()').extract_first()
                        item['post_likes'] = page_selector.xpath(
                            '//button[contains(@class,"js-actionFavorite")]//span[contains(@class, "ProfileTweet-actionCountForPresentation")]/text()').extract_first()

                        self.jsonify(item)
                        yield (scrapy.Request(item['twitter_url']))
                    # if '/hashtag/flu?src=hash' in item['hash_tags'] or '/hashtag/fever?src=hash' in item['hash_tags'] or '/hashtag/sick?src=hash' in item['hash_tags'] or'/hashtag/commoncold?src=hash' in item['hash_tags'] or '/hashtag/stomachache?src=hash'  in item['hash_tags'] or'/hashtag/sorethroat?src=hash' in item['hash_tags'] or'/hashtag/runnynose?src=hash' in item['hash_tags'] :
                        items.append(item)
        return items

    def jsonify(self, item):
        file.write("{")

        # regex_quote_char = r'[A-Za-z]"[A-Za-z]'
        for field in item:

            if item[field] == None:
                item[field] = 'null'
            if field is 'twitter_url' or field is 'user_name' or field is 'date' or field is 'hash_tags':
                file.write('\"' + str(field) + '\"' + ': ' + '\"' + str(item[field]) + '\"' + ',\n')
            elif field is 'post_text' or field is 'user_location':
                item[field] = str(item[field]).replace("'", '\"')
                file.write('\"' + str(field) + '\"' + ': ' + str(item[field]) + ',\n')
            elif field is 'post_retweets':
                file.write('\"' + str(field) + '\"' + ': ' + str(item[field]) + ',\n')
            elif field is 'post_likes':
                file.write('\"' + str(field) + '\"' + ': ' + str(item[field]) + '\n')
                # re.sub(regex_quote_char, "", str(item[field]))

        file.write("},")
        file.write('\n')
        file.flush()
        print(item)
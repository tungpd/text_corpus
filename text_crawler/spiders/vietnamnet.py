# coding=utf8
from text_crawler.utils import TextSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class VietnamnetSprider(TextSpider):
    name = "vietnamnet"
    allowed_domains = ['vietnamnet.vn']
    start_urls = ['https://vietnamnet.vn/']
    excluded_url_pattern = r'(^http\:\/\/(english|video|tuyendung)\.vietnamnet\.vn[\S]*)|([\S]+-tag[\d]+\.html$)|([\S]+\/(su-kien|the-thao)\/[\S]+\.html$)'
    allowed_url_pattern = r'[\S]*\.html$'

    rules = (
            Rule(LinkExtractor(allow=(allowed_url_pattern, ), deny=(excluded_url_pattern,)), callback='parse_article', follow=True),
    )
    def __init__(self, *args, **kwargs):
        super(VietnamnetSprider, self).__init__()

# -*- coding: utf-8 -*-
from text_crawler import utils
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class VnexpressSpider(utils.TextSpider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = ['http://vnexpress.net/']
    excluded_url_pattern = r'(^http\:\/\/(e|video)\.vnexpress\.net[\S]*)|([\S]+\/tag-[\S]+\.html)|(http:\/\/vnexpress.net\/tac-gia\/[\S]+\.html)'
    allowed_url_pattern = r'[\S]*\.html$'

    rules = (
            Rule(LinkExtractor(allow=(allowed_url_pattern, ), deny=(excluded_url_pattern,)), callback='parse_article', follow=True),
    )


    def __init__(self, *args, **kwargs):
        super(VnexpressSpider, self).__init__()

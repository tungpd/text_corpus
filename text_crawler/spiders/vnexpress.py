# -*- coding: utf-8 -*-
from text_crawler import utils
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class VnexpressSpider(utils.TextSpider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = ['http://vnexpress.net/',
                  'https://vnexpress.net/thoi-su',
                  'https://vnexpress.net/goc-nhin',
                  'https://vnexpress.net/the-gioi',
                  'https://vnexpress.net/kinh-doanh',
                  'https://vnexpress.net/giai-tri',
                  'https://vnexpress.net/the-thao',
                  'https://vnexpress.net/phap-luat',
                  'https://vnexpress.net/suc-khoe',
                  'https://vnexpress.net/doi-song',
                  'https://vnexpress.net/du-lich',
                  'https://vnexpress.net/khoa-hoc',
                  'https://vnexpress.net/so-hoa',
                  'https://vnexpress.net/oto-xe-may',
                  'https://vnexpress.net/y-kien',
                  'https://vnexpress.net/tam-su',
                ]
    excluded_url_pattern = r'(^http\:\/\/(e|video)\.vnexpress\.net[\S]*)|([\S]+\/tag-[\S]+\.html)|([\S]+vnexpress.net\/[\S]+\/anh-video)|(http:\/\/vnexpress.net\/tac-gia\/[\S]+\.html)'
    allowed_url_pattern = r'[\S]*\.html$'
    rules = (
            # Rule(LinkExtractor(deny=(allowed_url_pattern, excluded_url_pattern)), process_links=None, callback=None, follow=True),
            Rule(LinkExtractor(allow=(allowed_url_pattern, ), deny=(excluded_url_pattern,)), process_links="process_links", callback='parse_article', follow=True),
        )
    def __init__(self, *args, **kwargs):
        super(VnexpressSpider, self).__init__()


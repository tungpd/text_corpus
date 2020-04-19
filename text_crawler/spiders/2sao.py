# coding=utf8

from text_crawler.utils import TextSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class HaiSaoSprider(TextSpider):
    name = "haisao"
    allowed_domains = ['2sao.vn']
    start_urls = ['https://2sao.vn/',
                'https://2sao.vn/sao-c-aae/',
                  'https://2sao.vn/phim-c-aaj/',
                  'https://2sao.vn/nhac-c-aap/',
                  'https://2sao.vn/dep-c-aav/',
                  'https://2sao.vn/yolo-c-aax/']
    excluded_url_pattern = r''
    allowed_url_pattern = r'[\S]*\.html$'
    rules = (
            Rule(LinkExtractor(allow=(allowed_url_pattern, ), deny=None), callback='parse_article', process_links='process_links',  follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(HaiSaoSprider, self).__init__()

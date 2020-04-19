# coding=utf8
from text_crawler.utils import TextSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class VietnamnetSprider(TextSpider):
    name = "vietnamnet"
    allowed_domains = ['vietnamnet.vn']
    start_urls = ['https://vietnamnet.vn/',
                  'https://vietnamnet.vn/vn/thoi-su/chinh-tri/',
                  'https://vietnamnet.vn/vn/talkshow/',
                  'https://vietnamnet.vn/vn/thoi-su/',
                  'https://vietnamnet.vn/vn/kinh-doanh/',
                  'https://vietnamnet.vn/vn/giai-tri/',
                  'https://vietnamnet.vn/vn/the-gioi/',
                  'https://vietnamnet.vn/vn/giao-duc/',
                  'https://vietnamnet.vn/vn/doi-song/',
                  'https://vietnamnet.vn/vn/phap-luat/',
                  'https://vietnamnet.vn/vn/the-thao/',
                  'https://vietnamnet.vn/vn/cong-nghe/',
                  'https://vietnamnet.vn/vn/suc-khoe/',
                  'https://vietnamnet.vn/vn/bat-dong-san/',
                  'https://vietnamnet.vn/vn/ban-doc/',
                  'https://vietnamnet.vn/vn/tuanvietnam/',
                  'https://vietnamnet.vn/vn/oto-xe-may/',
                  'https://infonet.vietnamnet.vn/',
                  'https://infonet.vietnamnet.vn/doi-song-3.info',
                  'https://infonet.vietnamnet.vn/thi-truong-1176.info',
                  'https://infonet.vietnamnet.vn/the-gioi-5.info',
                  'https://infonet.vietnamnet.vn/gia-dinh-8.info',
                  'https://infonet.vietnamnet.vn/gioi-tre-1185.info',
                  'https://infonet.vietnamnet.vn/chuyen-la-9.info',
                  'https://infonet.vietnamnet.vn/quan-su-58.info',
                  'https://ictnews.vietnamnet.vn/',
                  'https://ictnews.vietnamnet.vn/thoi-su',
                  'https://ictnews.vietnamnet.vn/vien-thong',
                  'https://ictnews.vietnamnet.vn/internet',
                  'https://ictnews.vietnamnet.vn/chinh-phu-dien-tu',
                  'https://ictnews.vietnamnet.vn/cntt',
                  'https://ictnews.vietnamnet.vn/kinh-doanh',
                  'https://ictnews.vietnamnet.vn/the-gioi-so',
                  'https://ictnews.vietnamnet.vn/game',
                  'https://ictnews.vietnamnet.vn/khoi-nghiep',
                  'https://ictnews.vietnamnet.vn/cong-nghe-360']
    excluded_url_pattern = r'(^http\:\/\/(english|video|tuyendung)\.vietnamnet\.vn[\S]*)|([\S]+-tag[\d]+\.html$)|([\S]+\/(su-kien|the-thao)\/[\S]+\.html$)'
    allowed_url_pattern = r'[\S]*\.(html|ict)$'
    rules = (
            Rule(LinkExtractor(allow=(allowed_url_pattern, ), deny=(excluded_url_pattern,)), callback='parse_article', process_links='process_links',  follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(VietnamnetSprider, self).__init__()

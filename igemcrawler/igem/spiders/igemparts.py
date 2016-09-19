# -*- coding: utf-8 -*-
import scrapy
from igem.items import PartItem
from scrapy.selector import Selector

MAX_YEAR = 2015

regex = "http:\/\/parts.igem.org\/wiki\/index.php\?title=Part(\S+)"

class IgempartsSpider(scrapy.Spider):
    name = "igemparts"
    allowed_domains = ["parts.igem.org", "igem.org"]
    start_urls = ([
        "http://igem.org/Team_Parts?year=%d" % year
        for year in range(2005, MAX_YEAR + 1)
    ] + [
        "http://igem.org/Lab_Parts",
        "http://igem.org/Course_Parts"
    ])

    def parse(self, response):

        xxs = Selector(response)
        parts_links = xxs.xpath('//a[contains(@href, "Part:")]/@href')
        parts_names = parts_links.re(r'Part:([^:"&#]*).*')
        for name in parts_names:
            item = PartItem()
            item['name'] = name
            yield item

        for url in xxs.xpath('//a[contains(@href, "pgroup.cgi")]/@href').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse)

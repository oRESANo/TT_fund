# -*- coding: utf-8 -*-
import scrapy
import re
from lxml import etree
from tt_fund.settings import str_now_day
from tt_fund.settings import save_item_in_csv


class ManagerSpider(scrapy.Spider):
    name = 'fund_search'
    allowed_domains = ['eastmoney.com']
    total_page = 1  # 根据此url修改总页数 http://fund.eastmoney.com/manager/
    start_urls = ["http://fund.eastmoney.com/data/fundsearch.html?spm=search&key=%e6%b6%88%e8%b4%b9#key%e6%b6%88%e8%b4%b9"]

    title_num = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers=headers_raw_to_dict(self.h),
            )

    # 1.基金当日收益排名情况（基金排名页）
    def parse(self, response):
        fund_type = re.findall(r'kf&ft=(.*?)&rs=&gs=0&sc=zzf&st=desc', response.url)[0]
        response = response.text
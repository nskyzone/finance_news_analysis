# -*- coding: utf-8 -*-

from scrapy.http.request import Request
from scrapy.spiders import CrawlSpider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from ..items import HexunResearchPaperItem


class HexunResearchPaperSpider(CrawlSpider):
    name = 'HexunResearchPaperSpider'
    allowed_domains = ['yanbao.stock.hexun.com']
    start_urls = []

    def start_requests(self):
        page_range = 4496
        # 公司研究研报url
        base_url = 'http://yanbao.stock.hexun.com/xgq/gsyj.aspx?1=1&page=%d'
        for page_index in range(1, page_range + 1):
            url = base_url % page_index
            yield Request(url, self.parse_company_list_item)
        other_url_dict = {
            'hyyj': 2937,
            'yjyc': 4559,
            'qsch': 1179,
            'clbg': 786
        }
        # 其他研究（行业研究、业绩预测、券商晨会、策略报告）研报url
        base_url = 'http://yanbao.stock.hexun.com/xgq/%s.aspx?1=1&page=%d'
        for section_short_name in other_url_dict:
            page_range = other_url_dict[section_short_name]
            for page_index in range(1, page_range + 1):
                url = base_url % (section_short_name, page_index)
                yield Request(url, self.parse_other_list_item)
        pass

    def atoi(self, a):
        try:
            a = int(a)
        except ValueError:
            a = None
        return a

    def atof(self, f):
        try:
            f = float(f)
        except ValueError:
            f = None
        return f

    def parse_other_list_item(self, response):
        base_url = get_base_url(response)
        yaobao_table_items = response.xpath(
            '//div[@class="table"]/table//tr')
        # self.logger.debug("".join(response.xpath('//div[@class="table"]').extract()))
        for i in range(1, len(yaobao_table_items)):
            yb_item = yaobao_table_items[i]
            # 股票名称
            poster_name = yb_item.xpath('./td[1]/a/text()').extract()
            poster_name = "".join(poster_name)
            # 研报标题
            title = yb_item.xpath('./td[2]/a/text()').extract()
            title = "".join(title)
            # 研报url
            url = yb_item.xpath('./td[3]/a/@href').extract()
            url = "".join(url)
            url = urljoin_rfc(base_url, url)
            # 发布时间
            a_post_time = yb_item.xpath('./td[2]/text()').extract()
            a_post_time = "".join(a_post_time)
            # self.logger.debug("a_post_time: " + a_post_time)
            scrapy_item = HexunResearchPaperItem()
            # 插入scrapy item中
            scrapy_item['url'] = url
            scrapy_item['title'] = title
            scrapy_item['poster_name'] = poster_name
            scrapy_item['a_post_time'] = a_post_time
            yield Request(
                url=url,
                meta={'item': scrapy_item},
                callback=self.parse_detail)
            pass
        pass

    def parse_company_list_item(self, response):
        # list_url = response.url
        base_url = get_base_url(response)
        yaobao_table_items = response.xpath(
            '//div[@class="table"]/table//tr')
        # self.logger.debug("".join(response.xpath('//div[@class="table"]').extract()))
        for i in range(1, len(yaobao_table_items)):
            yb_item = yaobao_table_items[i]
            # 股票名称
            ticker_name = yb_item.xpath('./td[1]/a/text()').extract()
            ticker_name = "".join(ticker_name)
            # self.logger.debug("ticker_name: " + ticker_name)
            # 股票代码
            ticker_id = yb_item.xpath('./td[1]/a/@href').re('([0-9]+)')
            ticker_id = "".join(ticker_id)
            # self.logger.debug('ticker_id: ' + ticker_id)
            # 研报标题
            title = yb_item.xpath('./td[2]/a/text()').extract()
            title = "".join(title)
            # self.logger.debug("title: " + title)
            # 研报url
            url = yb_item.xpath('./td[2]/a/@href').extract()
            url = "".join(url)
            url = urljoin_rfc(base_url, url)
            # self.logger.debug("url: " + url)
            # 研报所属行业
            industry = yb_item.xpath('./td[3]/text()').extract()
            industry = "".join(industry)
            # self.logger.debug("industry: " + industry)
            # 研报发表机构名称
            poster_name = yb_item.xpath('./td[4]//text()').extract()
            poster_name = "".join(poster_name)
            # self.logger.debug("poster_name: " + poster_name)
            # 分析师姓名
            analyst_name = yb_item.xpath('./td[5]/a/text()').extract()
            # self.logger.debug("analyst_name: " + " ".join(analyst_name))
            # 评级分类
            rating_level = yb_item.xpath('./td[6]/text()').extract()
            rating_level = "".join(rating_level)
            # self.logger.debug("rating_level: " + rating_level)
            # 评级变动
            rating_change = yb_item.xpath('./td[7]/text()').extract()
            rating_change = "".join(rating_change)
            # self.logger.debug("rating_change: " + rating_change)
            # 上涨空间
            upside = yb_item.xpath('./td[8]/text()').extract()
            upside = self.atof("".join(upside))
            self.logger.debug("upside: " + str(upside))
            # 发布时间
            a_post_time = yb_item.xpath('./td[9]/text()').extract()
            a_post_time = "".join(a_post_time)
            # self.logger.debug("a_post_time: " + a_post_time)
            scrapy_item = HexunResearchPaperItem()
            # 插入scrapy item中
            scrapy_item['url'] = url
            scrapy_item['title'] = title
            scrapy_item['ticker_name'] = ticker_name
            scrapy_item['ticker_id'] = ticker_id
            scrapy_item['industry'] = industry
            scrapy_item['poster_name'] = poster_name
            scrapy_item['analyst_name'] = analyst_name
            scrapy_item['rating_level'] = rating_level
            scrapy_item['rating_change'] = rating_change
            scrapy_item['upside'] = upside
            scrapy_item['a_post_time'] = a_post_time
            yield Request(
                url=url,
                meta={'item': scrapy_item},
                callback=self.parse_detail)
            pass
        pass

    def parse_detail(self, response):
        item = response.meta['item']
        # 研报分类
        yanbao_class = response.xpath(
            '//p[@class="text_01"]/a[1]/text()').extract()
        yanbao_class = "".join(yanbao_class)
        # self.logger.debug("yanbao_class: " + yanbao_class)
        # 摘要
        abstract = response.xpath(
            '//div[@class="yj_bglc"]/p[@class="txt_02"]/text()').extract()
        abstract = "".join(abstract).strip()
        # self.logger.debug("abstract: " + abstract)
        # 调查投票人数
        survey_voting_num = response.xpath(
            '//div[@class="vote"]/div[@class="allSum"]//span[@id="sum"]/text()').extract()
        survey_voting_num = self.atoi("".join(survey_voting_num))
        # self.logger.debug("survey_voting_num: " + str(survey_voting_num))
        good_ratio = response.xpath(
            '//div[@id="vote"]/cite[@class="henzs"]/b/text()').extract()
        good_ratio = self.atof("".join(good_ratio))
        # self.logger.debug("good_ratio: " + str(good_ratio))
        general_ratio = response.xpath(
            '//div[@id="vote"]/cite[@class="yibs"]/b/text()').extract()
        general_ratio = self.atof("".join(general_ratio))
        # self.logger.debug("general_ratio: " + str(general_ratio))
        bad_ratio = response.xpath(
            '//div[@id="vote"]/cite[@class="buzs"]/b/text()').extract()
        bad_ratio = self.atof("".join(bad_ratio))
        # self.logger.debug("bad_ratio: " + str(bad_ratio))
        # 插入scrapy item中
        item['yanbao_class'] = yanbao_class
        item['abstract'] = abstract
        item['survey_voting_num'] = survey_voting_num
        item['good_ratio'] = good_ratio
        item['general_ratio'] = general_ratio
        item['bad_ratio'] = bad_ratio
        # 除了公司研究列表中都没有研究员，需要在详情页中抓取
        if 'analyst_name' not in item:
            analyst_name = response.xpath(
                '//p[@class="text_01"]/a[3]/text()').extract()
            item['analyst_name'] = analyst_name
        return item

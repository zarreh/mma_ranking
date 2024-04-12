import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FighterCrawlSpider(CrawlSpider):
    name = "fighter_crawl"
    allowed_domains = ["www.ufcstats.com"]
    start_urls = ["http://www.ufcstats.com/statistics/fighters"]

    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'

    # def start_requests(self):
    #     yield scrapy.Request(url='http://www.ufcstats.com/statistics/fighters', headers={
    #         'User-Agent': self.user_agent
    #     })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="(//ul)[1]/li/a")),
        Rule(
            LinkExtractor(
                restrict_xpaths='(//li[@class="b-statistics__paginate-item"]/a)[last()]',
                allow=r"&page=all",
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        # print(response.url)
        rows = response.xpath(
            "//tbody/tr[@class='b-statistics__table-row' and position()>1]"
        )
        for row in rows:
            fname = row.xpath(".//td[1]/a/text()").get()
            link = row.xpath(".//td[1]/a/@href").get()
            lname = row.xpath(".//td[2]/a/text()").get()
            nname = row.xpath(".//td[3]/a/text()").get()
            ht = row.xpath("normalize-space(.//td[4]/text())").get()
            wt = row.xpath(".//td[5]/text()").get()
            reach = row.xpath("normalize-space(.//td[6]/text())").get()
            stance = row.xpath("normalize-space(.//td[7]/text())").get()
            w = row.xpath(".//td[8]/text()").get()
            l = row.xpath(".//td[9]/text()").get()
            d = row.xpath(".//td[10]/text()").get()

            # ht = re.sub(r'[^a-zA-Z0-9]', '', ht)
            wt = re.sub(r"[^a-zA-Z0-9]", "", wt)
            # reach = re.sub(r'[^a-zA-Z0-9]', '', reach)
            # stance = re.sub(r'[^a-zA-Z0-9]', '', stance)
            w = re.sub(r"[^a-zA-Z0-9]", "", w)
            l = re.sub(r"[^a-zA-Z0-9]", "", l)
            d = re.sub(r"[^a-zA-Z0-9]", "", d)

            # yield {
            #     "link": link,
            #     'Frist_name': fname,
            #     'Last_name': lname,
            #     'Nick_name': nname,
            #     'Hight': ht,
            #     'Weight': wt,
            #     'Reach': reach,
            #     'Stance': stance,
            #     'Win': w,
            #     'Loss': l,
            #     'Draw': d
            # }
            yield scrapy.Request(
                url=link,
                callback=self.parse_fither_page,
                meta={
                    "link": link,
                    "Frist_name": fname,
                    "Last_name": lname,
                    "Nick_name": nname,
                    "Hight": ht,
                    "Weight": wt,
                    "Reach": reach,
                    "Stance": stance,
                    "Win": w,
                    "Loss": l,
                    "Draw": d,
                },
            )

    def parse_fither_page(self, response):
        # print('hello')
        fname = response.request.meta["Frist_name"]
        link = response.request.meta["link"]
        lname = response.request.meta["Last_name"]
        nname = response.request.meta["Nick_name"]
        ht = response.request.meta["Hight"]
        wt = response.request.meta["Weight"]
        reach = response.request.meta["Reach"]
        stance = response.request.meta["Stance"]
        w = response.request.meta["Win"]
        l = response.request.meta["Loss"]
        d = response.request.meta["Draw"]
        yield {
            "link": link,
            "Frist_name": fname,
            "Last_name": lname,
            "Nick_name": nname,
            "Hight": ht,
            "Weight": wt,
            "Reach": reach,
            "Stance": stance,
            "Win": w,
            "Loss": l,
            "Draw": d,
            "DOB": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item b-list__box-list-item_type_block'])[4]/text())[2])"
            ).get(),
            "SLpM": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item b-list__box-list-item_type_block'])[5]/text())[2])"
            ).get(),
            "Str. Acc.": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item b-list__box-list-item_type_block'])[6]/text())[2])"
            ).get(),
            "SApM": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item b-list__box-list-item_type_block'])[7]/text())[2])"
            ).get(),
            "Str. Def.": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item  b-list__box-list-item_type_block'])[2]/text())[2])"
            ).get(),
            "TD Avg.": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item b-list__box-list-item_type_block'])[9]/text())[2])"
            ).get(),
            "TD Acc.": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item b-list__box-list-item_type_block'])[10]/text())[2])"
            ).get(),
            "TD Def.": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item b-list__box-list-item_type_block'])[11]/text())[2])"
            ).get(),
            "Sub. Avg.": response.xpath(
                "normalize-space(((//li[@class='b-list__box-list-item  b-list__box-list-item_type_block'])[3]/text())[2])"
            ).get(),
        }

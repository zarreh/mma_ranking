import re

import pandas as pd
import scrapy

# import logging


class FightersSpider(scrapy.Spider):
    name = "fighters"
    allowed_domains = ["www.ufcstats.com"]
    start_urls = ["http://www.ufcstats.com/statistics/fighters"]

    def parse(self, response):
        page_links = response.xpath("(//ul)[1]/li")
        for page_link in page_links:
            link = page_link.xpath(".//a/@href").get()
            link = link + "&page=all"
            yield response.follow(url=link, callback=self.parse_fighters)

    def parse_fighters(self, response):
        # logging.info(response.url)
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
            }

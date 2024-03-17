import scrapy
import pandas as pd


class FightersSpider(scrapy.Spider):
    name = 'fighters'
    allowed_domains = ['www.ufcstats.com/']
    start_urls = ['http://www.ufcstats.com/statistics/fighters']

    def parse(self, response):
        first_name = response.xpath("//td[@class='b-statistics__table-col' and position()=1]/a/text()").getall()
        links = response.xpath("//td[@class='b-statistics__table-col' and position()=1]/a/@href").getall()
        last_name = response.xpath("//td[@class='b-statistics__table-col' and position()=2]/a/text()").getall()
        nick_name = response.xpath("//td[@class='b-statistics__table-col' and position()=3]/a/text()").getall()
        ht = response.xpath("//td[@class='b-statistics__table-col' and position()=4]/text()").getall()
        wt = response.xpath("//td[@class='b-statistics__table-col' and position()=5]/text()").getall()
        reach = response.xpath("//td[@class='b-statistics__table-col' and position()=6]/text()").getall()
        stance = response.xpath("//td[@class='b-statistics__table-col' and position()=7]/text()").getall()
        w = response.xpath("//td[@class='b-statistics__table-col b-statistics__table-col_type_small' and position()=8]/text()").getall()
        l = response.xpath("//td[@class='b-statistics__table-col b-statistics__table-col_type_small' and position()=9]/text()").getall()
        d = response.xpath("//td[@class='b-statistics__table-col b-statistics__table-col_type_small' and position()=10]/text()").getall()
        
        yield {
            "link": links,
            'Frist_name': first_name,
            'Last_name': last_name,
            'Nick_name': nick_name,
            'Hight': ht,
            'Weight': wt,
            'reach': reach,
            'Stance': stance,
            'Win': w,
            'Loss': l,
            'Draw': d
        }
        col = ['Frist_name','Last_name','Nick_name','Hight','Weight','reach','Stance','Win','Loss','Draw', 'link']
        df = pd.DataFrame(list(zip(first_name, last_name, nick_name, ht, wt, reach, stance, w, l, d, links)), columns=col)
        df.to_csv('fighters.csv', mode='x')
        
        

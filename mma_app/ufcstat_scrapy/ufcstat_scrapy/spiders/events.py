import scrapy
from .scraping_config import BEGAN_DATE
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventsSpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['www.ufcstats.com']
    start_urls = ['http://www.ufcstats.com/statistics/events/completed?page=all']

    def parse(self, response):
        event_links = response.xpath('(//td/i)[position() >1]')
        for event in event_links:
            link = event.xpath('.//a/@href').get()
            yield scrapy.Request(url=link, callback=self.parse_event)

    def parse_event(self,response):
        date = response.xpath('normalize-space((//ul/li/text())[2])').get()
        place = response.xpath('normalize-space((//ul/li/text())[4])').get()
        fights = response.xpath('//tbody/tr')

        date_obj = datetime.strptime(date, "%B %d, %Y").date()
        if date_obj>=BEGAN_DATE:
            logger.info(f'DATE: {date} IS AFTER BEGAN DATE: {BEGAN_DATE}')
            for fight in fights:
                yield scrapy.Request(url=fight.xpath('.//@data-link').get(), callback=self.parse_fight, meta={
                    'Date': date,
                    'Place': place,
                    'link': fight.xpath('.//@data-link').get(),
                    'fighter1': fight.xpath("normalize-space(.//td[@class='b-fight-details__table-col l-page_align_left']/p[1]/a/text())").get(),
                    'fighter2': fight.xpath("normalize-space(.//td[@class='b-fight-details__table-col l-page_align_left']/p[2]/a/text())").get()
                                    
                })
            
    def parse_fight(self, response):
        date = response.request.meta['Date']
        place = response.request.meta['Place']
        link = response.request.meta['link']
        # fighter1 = response.request.meta['fighter1']
        # fighter2 = response.request.meta['fighter2']

        date_obj = datetime.strptime(date, "%B %d, %Y").date()
        if date_obj>=BEGAN_DATE:
            logger.info(f'DATE: {date} IS AFTER BEGAN DATE: {BEGAN_DATE}')
               
            yield {
                'Date': date,
                'Place': place,
                'link': link,
                # 'fighter1': fighter1,
                # 'fighter2': fighter2,
                'fighter1': response.xpath("normalize-space((.//div/h3/a)[1]/text())").get(),
                'fighter2': response.xpath("normalize-space((.//div/h3/a)[2]/text())").get(),
                'fighter1_result': response.xpath("normalize-space((.//div[@class='b-fight-details__person']/i)[1]/text())").get(),
                'fighter2_result': response.xpath("normalize-space((.//div[@class='b-fight-details__person']/i)[2]/text())").get(),
                'BELT': response.xpath("((.//div[@class='b-fight-details__fight-head']/i/img[contains(@src, 'belt')]/@src))").get(),
                'BOUNES': response.xpath("((.//div[@class='b-fight-details__fight-head']/i/img/@src)[last()])").get(),
                'Weight': response.xpath("normalize-space((.//div[@class='b-fight-details__fight-head']/i/text())[last()])").get(),
                'TIME_FORMAT': response.xpath("normalize-space(.//div[@class='b-fight-details__content']/p/i[4]/text()[2])").get(),
                'Method': response.xpath("normalize-space(.//div[@class='b-fight-details__content']/p/i[@class='b-fight-details__text-item_first' ]/i[2]/text())").get(),
                'Method_detail': response.xpath("normalize-space((.//div[@class='b-fight-details__content']/p[2]/text())[2])").get(),
                'Judge1': response.xpath("normalize-space((.//div/p[2]/i[@class='b-fight-details__text-item' ])[1]/span/text())").get(),
                'Judge1_score': response.xpath("normalize-space((.//div/p[2]/i[@class='b-fight-details__text-item' ])[1]/text()[2])").get(),
                'Judge2': response.xpath("normalize-space((.//div/p[2]/i[@class='b-fight-details__text-item' ])[2]/span/text())").get(),
                'Judge2_score': response.xpath("normalize-space((.//div/p[2]/i[@class='b-fight-details__text-item' ])[2]/text()[2])").get(),
                'Judge3': response.xpath("normalize-space((.//div/p[2]/i[@class='b-fight-details__text-item' ])[3]/span/text())").get(),
                'Judge3_score': response.xpath("normalize-space((.//div/p[2]/i[@class='b-fight-details__text-item' ])[3]/text()[2])").get(),
                'ROUND': response.xpath("normalize-space(.//div[@class='b-fight-details__content']/p[1]/i[2]/text()[2])").get(),
                'TIME': response.xpath("normalize-space(.//div[@class='b-fight-details__content']/p[1]/i[3]/text()[2])").get(),
                'REFEREE': response.xpath("normalize-space(.//div[@class='b-fight-details__content']/p[1]/i[5]/span/text())").get(),
                #-------------------------------------------Total --------------------------------------------------------------------------------
                'T_KD_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[2]/p[1]/text())").get(),
                'T_SIG_STR_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[3]/p[1]/text())").get(),
                'T_SIG_STR%_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[4]/p[1]/text())").get(),
                'TOTAL_STR_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[5]/p[1]/text())").get(),
                'T_TD_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[6]/p[1]/text())").get(),
                'T_TD%_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[7]/p[1]/text())").get(),
                'T_SUB_ATT_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[8]/p[1]/text())").get(),
                'T_REV_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[9]/p[1]/text())").get(),
                'T_CTRL_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[10]/p[1]/text())").get(),
                'T_KD_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[2]/p[2]/text())").get(),
                'T_SIG_STR_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[3]/p[2]/text())").get(),
                'T_SIG_STR%_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[4]/p[2]/text())").get(),
                'TOTAL_STR_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[5]/p[2]/text())").get(),
                'T_TD_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[6]/p[2]/text())").get(),
                'T_TD%_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[7]/p[2]/text())").get(),
                'T_SUB_ATT_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[8]/p[2]/text())").get(),
                'T_REV_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[9]/p[2]/text())").get(),
                'T_CTRL_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[1]/td[10]/p[2]/text())").get(),
                #-------------------------------------------Total per Round 1--------------------------------------------------------------------------------
                'R1_KD_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[2]/p[1]/text())").get(),
                'R1_SIG_STR_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[3]/p[1]/text())").get(),
                'R1_SIG_STR%_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[4]/p[1]/text())").get(),
                'R1_STR_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[5]/p[1]/text())").get(),
                'R1_TD_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[6]/p[1]/text())").get(),
                'R1_TD%_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[7]/p[1]/text())").get(),
                'R1_SUB_ATT_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[8]/p[1]/text())").get(),
                'R1_REV_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[9]/p[1]/text())").get(),
                'R1_CTRL_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[10]/p[1]/text())").get(),
                'R1_KD_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[2]/p[2]/text())").get(),
                'R1_SIG_STR_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[3]/p[2]/text())").get(),
                'R1_SIG_STR%_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[4]/p[2]/text())").get(),
                'R1_STR_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[5]/p[2]/text())").get(),
                'R1_TD_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[6]/p[2]/text())").get(),
                'R1_TD%_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[7]/p[2]/text())").get(),
                'R1_SUB_ATT_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[8]/p[2]/text())").get(),
                'R1_REV_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[9]/p[2]/text())").get(),
                'R1_CTRL_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[2]/td[10]/p[2]/text())").get(),
                #-------------------------------------------Total per Round 2--------------------------------------------------------------------------------
                'R2_KD_F1':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[2]/p[1]/text())").get(),
                'R2_SIG_STR_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[3]/p[1]/text())").get(),
                'R2_SIG_STR%_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[4]/p[1]/text())").get(),
                'R2_STR_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[5]/p[1]/text())").get(),
                'R2_TD_F1':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[6]/p[1]/text())").get(),
                'R2_TD%_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[7]/p[1]/text())").get(),
                'R2_SUB_ATT_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[8]/p[1]/text())").get(),
                'R2_REV_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[9]/p[1]/text())").get(),
                'R2_CTRL_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[10]/p[1]/text())").get(),
                'R2_KD_F2':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[2]/p[2]/text())").get(),
                'R2_SIG_STR_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[3]/p[2]/text())").get(),
                'R2_SIG_STR%_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[4]/p[2]/text())").get(),
                'R2_STR_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[5]/p[2]/text())").get(),
                'R2_TD_F2':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[6]/p[2]/text())").get(),
                'R2_TD%_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[7]/p[2]/text())").get(),
                'R2_SUB_ATT_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[8]/p[2]/text())").get(),
                'R2_REV_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[9]/p[2]/text())").get(),
                'R2_CTRL_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[3]/td[10]/p[2]/text())").get(),
                #-------------------------------------------Total per Round 3--------------------------------------------------------------------------------
                'R3_KD_F1':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[2]/p[1]/text())").get(),
                'R3_SIG_STR_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[3]/p[1]/text())").get(),
                'R3_SIG_STR%_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[4]/p[1]/text())").get(),
                'R3_STR_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[5]/p[1]/text())").get(),
                'R3_TD_F1':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[6]/p[1]/text())").get(),
                'R3_TD%_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[7]/p[1]/text())").get(),
                'R3_SUB_ATT_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[8]/p[1]/text())").get(),
                'R3_REV_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[9]/p[1]/text())").get(),
                'R3_CTRL_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[10]/p[1]/text())").get(),
                'R3_KD_F2':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[2]/p[2]/text())").get(),
                'R3_SIG_STR_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[3]/p[2]/text())").get(),
                'R3_SIG_STR%_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[4]/p[2]/text())").get(),
                'R3_STR_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[5]/p[2]/text())").get(),
                'R3_TD_F2':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[6]/p[2]/text())").get(),
                'R3_TD%_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[7]/p[2]/text())").get(),
                'R3_SUB_ATT_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[8]/p[2]/text())").get(),
                'R3_REV_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[9]/p[2]/text())").get(),
                'R3_CTRL_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[4]/td[10]/p[2]/text())").get(),
                #-------------------------------------------Total per Round 4--------------------------------------------------------------------------------
                'R4_KD_F1':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[2]/p[1]/text())").get(),
                'R4_SIG_STR_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[3]/p[1]/text())").get(),
                'R4_SIG_STR%_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[4]/p[1]/text())").get(),
                'R4_STR_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[5]/p[1]/text())").get(),
                'R4_TD_F1':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[6]/p[1]/text())").get(),
                'R4_TD%_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[7]/p[1]/text())").get(),
                'R4_SUB_ATT_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[8]/p[1]/text())").get(),
                'R4_REV_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[9]/p[1]/text())").get(),
                'R4_CTRL_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[10]/p[1]/text())").get(),
                'R4_KD_F2':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[2]/p[2]/text())").get(),
                'R4_SIG_STR_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[3]/p[2]/text())").get(),
                'R4_SIG_STR%_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[4]/p[2]/text())").get(),
                'R4_STR_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[5]/p[2]/text())").get(),
                'R4_TD_F2':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[6]/p[2]/text())").get(),
                'R4_TD%_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[7]/p[2]/text())").get(),
                'R4_SUB_ATT_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[8]/p[2]/text())").get(),
                'R4_REV_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[9]/p[2]/text())").get(),
                'R4_CTRL_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[5]/td[10]/p[2]/text())").get(),
                #-------------------------------------------Total per Round 5--------------------------------------------------------------------------------
                'R5_KD_F1':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[2]/p[1]/text())").get(),
                'R5_SIG_STR_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[3]/p[1]/text())").get(),
                'R5_SIG_STR%_F1': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[4]/p[1]/text())").get(),
                'R5_STR_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[5]/p[1]/text())").get(),
                'R5_TD_F1':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[6]/p[1]/text())").get(),
                'R5_TD%_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[7]/p[1]/text())").get(),
                'R5_SUB_ATT_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[8]/p[1]/text())").get(),
                'R5_REV_F1':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[9]/p[1]/text())").get(),
                'R5_CTRL_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[10]/p[1]/text())").get(),
                'R5_KD_F2':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[2]/p[2]/text())").get(),
                'R5_SIG_STR_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[3]/p[2]/text())").get(),
                'R5_SIG_STR%_F2': response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[4]/p[2]/text())").get(),
                'R5_STR_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[5]/p[2]/text())").get(),
                'R5_TD_F2':       response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[6]/p[2]/text())").get(),
                'R5_TD%_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[7]/p[2]/text())").get(),
                'R5_SUB_ATT_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[8]/p[2]/text())").get(),
                'R5_REV_F2':      response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[9]/p[2]/text())").get(),
                'R5_CTRL_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[6]/td[10]/p[2]/text())").get(),
                #-------------------------------------------SIGNIFICANT STRIKES--------------------------------------------------------------------------------
                'T_HEAD_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[4]/p[1]/text())").get(),  
                'T_BODY_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[5]/p[1]/text())").get(), 
                'T_LEG_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[6]/p[1]/text())").get(), 
                'T_DISTANCE_F1':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[7]/p[1]/text())").get(), 
                'T_CLINCH_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[8]/p[1]/text())").get(), 
                'T_GROUND_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[9]/p[1]/text())").get(), 

                'T_HEAD_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[4]/p[2]/text())").get(),  
                'T_BODY_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[5]/p[2]/text())").get(), 
                'T_LEG_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[6]/p[2]/text())").get(), 
                'T_DISTANCE_F2':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[7]/p[2]/text())").get(), 
                'T_CLINCH_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[8]/p[2]/text())").get(), 
                'T_GROUND_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[7]/td[9]/p[2]/text())").get(), 
                #-------------------------------------------SIGNIFICANT STRIKES per Round 1--------------------------------------------------------------------------------
                'R1_HEAD_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[4]/p[1]/text())").get(),  
                'R1_BODY_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[5]/p[1]/text())").get(), 
                'R1_LEG_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[6]/p[1]/text())").get(), 
                'R1_DISTANCE_F1':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[7]/p[1]/text())").get(), 
                'R1_CLINCH_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[8]/p[1]/text())").get(), 
                'R1_GROUND_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[9]/p[1]/text())").get(), 

                'R1_HEAD_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[4]/p[2]/text())").get(),  
                'R1_BODY_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[5]/p[2]/text())").get(), 
                'R1_LEG_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[6]/p[2]/text())").get(), 
                'R1_DISTANCE_F2':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[7]/p[2]/text())").get(), 
                'R1_CLINCH_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[8]/p[2]/text())").get(), 
                'R1_GROUND_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[8]/td[9]/p[2]/text())").get(), 
                
                #-------------------------------------------SIGNIFICANT STRIKES per Round 2--------------------------------------------------------------------------------
                'R2_HEAD_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[4]/p[1]/text())").get(),  
                'R2_BODY_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[5]/p[1]/text())").get(), 
                'R2_LEG_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[6]/p[1]/text())").get(), 
                'R2_DISTANCE_F1':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[7]/p[1]/text())").get(), 
                'R2_CLINCH_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[8]/p[1]/text())").get(), 
                'R2_GROUND_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[9]/p[1]/text())").get(), 
                
                'R2_HEAD_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[4]/p[2]/text())").get(),  
                'R2_BODY_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[5]/p[2]/text())").get(), 
                'R2_LEG_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[6]/p[2]/text())").get(), 
                'R2_DISTANCE_F2':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[7]/p[2]/text())").get(), 
                'R2_CLINCH_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[8]/p[2]/text())").get(), 
                'R2_GROUND_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[9]/td[9]/p[2]/text())").get(), 
                
                #-------------------------------------------SIGNIFICANT STRIKES per Round 3--------------------------------------------------------------------------------
                'R3_HEAD_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[4]/p[1]/text())").get(),  
                'R3_BODY_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[5]/p[1]/text())").get(), 
                'R3_LEG_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[6]/p[1]/text())").get(), 
                'R3_DISTANCE_F1':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[7]/p[1]/text())").get(), 
                'R3_CLINCH_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[8]/p[1]/text())").get(), 
                'R3_GROUND_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[9]/p[1]/text())").get(), 
                
                'R3_HEAD_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[4]/p[2]/text())").get(),  
                'R3_BODY_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[5]/p[2]/text())").get(), 
                'R3_LEG_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[6]/p[2]/text())").get(), 
                'R3_DISTANCE_F2':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[7]/p[2]/text())").get(), 
                'R3_CLINCH_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[8]/p[2]/text())").get(), 
                'R3_GROUND_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[10]/td[9]/p[2]/text())").get(), 
                
                #-------------------------------------------SIGNIFICANT STRIKES per Round 4--------------------------------------------------------------------------------
                'R4_HEAD_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[4]/p[1]/text())").get(),  
                'R4_BODY_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[5]/p[1]/text())").get(), 
                'R4_LEG_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[6]/p[1]/text())").get(), 
                'R4_DISTANCE_F1':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[7]/p[1]/text())").get(), 
                'R4_CLINCH_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[8]/p[1]/text())").get(), 
                'R4_GROUND_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[9]/p[1]/text())").get(), 
                
                'R4_HEAD_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[4]/p[2]/text())").get(),  
                'R4_BODY_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[5]/p[2]/text())").get(), 
                'R4_LEG_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[6]/p[2]/text())").get(), 
                'R4_DISTANCE_F2':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[7]/p[2]/text())").get(), 
                'R4_CLINCH_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[8]/p[2]/text())").get(), 
                'R4_GROUND_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[11]/td[9]/p[2]/text())").get(), 
                
                #-------------------------------------------SIGNIFICANT STRIKES per Round 5--------------------------------------------------------------------------------
                'R5_HEAD_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[4]/p[1]/text())").get(),  
                'R5_BODY_F1':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[5]/p[1]/text())").get(), 
                'R5_LEG_F1':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[6]/p[1]/text())").get(), 
                'R5_DISTANCE_F1':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[7]/p[1]/text())").get(), 
                'R5_CLINCH_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[8]/p[1]/text())").get(), 
                'R5_GROUND_F1':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[9]/p[1]/text())").get(),
                
                'R5_HEAD_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[4]/p[2]/text())").get(),  
                'R5_BODY_F2':    response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[5]/p[2]/text())").get(), 
                'R5_LEG_F2':     response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[6]/p[2]/text())").get(), 
                'R5_DISTANCE_F2':response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[7]/p[2]/text())").get(), 
                'R5_CLINCH_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[8]/p[2]/text())").get(), 
                'R5_GROUND_F2':  response.xpath("normalize-space((.//tbody/tr[@class='b-fight-details__table-row'])[12]/td[9]/p[2]/text())").get()
                
            }
        else:
            logger.info(f'DATE: {date} IS BEFORE BEGAN DATE: {BEGAN_DATE} HENCE IT WILL BE SKIPED')
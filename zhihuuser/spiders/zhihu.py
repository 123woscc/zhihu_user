# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import json
from zhihuuser.items import UserItem

class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['http://www.zhihu.com/']
    start_user='excited-vczh'
    followees_url='https://www.zhihu.com/api/v4/members/{user}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
    user_data_url='https://www.zhihu.com/api/v4/members/{user}?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'

    def start_requests(self):
        yield Request(self.followees_url.format(user=self.start_user),callback=self.parse_followees)
        yield Request(self.user_data_url.format(user=self.start_user),callback=self.parse_user)


    def parse_followees(self,response):
        result=json.loads(response.text)
        if 'data' in result.keys():
            for user in result.get('data'):
                yield Request(self.user_data_url.format(user=user.get('url_token')),callback=self.parse_user)
                yield Request(self.followees_url.format(user=user.get('url_token')), callback=self.parse_followees)

        if 'paging' in result.keys() and result.get('paging').get('is_end')==False:
            next_page=result.get('paging').get('next')
            yield Request(next_page,self.parse_followees)

    def parse_user(self,response):
        result=json.loads(response.text)
        item=UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field]=result.get(field)
        yield item



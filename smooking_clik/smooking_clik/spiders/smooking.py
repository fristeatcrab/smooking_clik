import re
import random, time, math, datetime
from bs4 import BeautifulSoup
import codecs, json
from  ..settings import  daohang,UPPOOL_one,dianziyan,curr_keyword
from scrapy import Spider
from scrapy.http import Request
import logging
from lxml import etree
from urllib import parse
logging.getLogger("requests").setLevel(logging.WARNING)
logging.captureWarnings(True)
import urllib3
urllib3.disable_warnings()
from  . import judge


class SmSpider(Spider):

    def __init__(self, *args, **kwargs):
        super(SmSpider, self).__init__(*args, **kwargs)
        super(SmSpider, self).__init__()
        # self.key_lsit = list(current_key.keys())
        self.key_index = 0
    name = "sm"


    def start_requests(self):
             # time.sleep(random.randint(2,5))
             yield Request(
                url="https://www.baidu.com",
                callback=self.page_,
                 headers={"User-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'},
                 dont_filter=True
             )

    def page_(self,response):

        user_agent = random.choice(UPPOOL_one)
        header_1 = {'User-Agent': user_agent,'Referer':None}
        header = {'User-Agent': user_agent}
        time.sleep(1)
        yield Request(
            url="http://dps.kdlapi.com/api/getdps/?orderid=956920344938769&num=1&pt=1&dedup=1&format=json&sep=1",
                callback= lambda response,data={ 'header':header,
                                 }:self._check(response,data),
                 dont_filter=True,
            headers=header_1,
             )

    def _check(self, response,data):
        porxy_dict = json.loads(str(response.text))
        if  int(porxy_dict['code']) == -1:
            time.sleep(random.randint(2, 5))
            yield Request(
                url="http://dps.kdlapi.com/api/getdps/?orderid=956920344938769&num=1&pt=1&dedup=1&format=json&sep=1",
                callback=lambda response, data={'header': data['header'],
                                                }: self.page_(response),
                dont_filter=True,
                headers=data['header']
            )
        elif int(porxy_dict['code']) == -5:
            logging.info('ipproxy_down')
        else:
            data['proxy'] ='http://'+ '%s:%s@%s'%('1813482282', 'hxm5bz2m',str( porxy_dict['data']['proxy_list'][0]))
            data['key'] = 0
            logging.info(data['proxy'])
            time.sleep(1)
            ip_status = judge.judge_ip(data['proxy'])
            if ip_status:
                yield Request(
                url=random.choice(daohang),
                callback=lambda response,
                            data=data: self.click(response,data),
                headers=data['header'],
                meta={'proxy': data['proxy']},
                dont_filter=True
                )
            else:
                yield Request(
                url='https://www.baidu.com',
                callback=self.page_,
                headers= data['header'],dont_filter=True
            )

    def click(self,response,data):
        time.sleep(random.randint(3,5))
        current_url = random.choice(dianziyan)
        # current_url = 'https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=baidu&wd=%E7%94%B5%E5%AD%90%E7%83%9F&oq=%25E7%2594%25B5%25E5%25AD%2590%25E7%2583%259F&rsv_pq=a52177d3000e0543&rsv_t=cf1eMtf%2FeUkJj2JbHoWeMXP7lw%2Fs8cbjK2Js%2FXgjx6%2BUF7dX3fyUQrykSk4&rqlang=cn&rsv_enter=0&rsv_dl=ts_0&prefixsug=%25E7%2594%25B5%25E5%25AD%2590%25E7%2583%259F&rsp=0&rsv_sug=1'

        ip_status = judge.judge_ip(data['proxy'])
        if ip_status:
            yield Request(
                url=current_url,
                callback=lambda response,
                                data=data: self.click_1(response, data),
                headers=data['header'],
                meta={'proxy': data['proxy']},
                dont_filter=True
            )
        else:
            yield Request(
                url='https://www.baidu.com',
                callback=self.page_,
                headers=data['header'], dont_filter=True
            )

    def click_1(self,response,data):
        time.sleep(random.randint(6, 15))
        soo = BeautifulSoup(response.text, 'lxml')
        # smooking_next = soo.find_all("a", class_="n")
        time.sleep(1)
        smooking_next = response.xpath("//a[@class='n']/@href")
        logging.info('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{0}<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(len(smooking_next)))
        try:
            if len(smooking_next) == 2:
                next_url = 'https://baidu.com' + str(smooking_next[1].extract())
        # elif len(smooking_next) == 0:
        #     next_url = 'https://www.baidu.com/s?wd=电子烟&pn=10&oq=电子烟&ie=utf-8'
            else:
                next_url = 'https://baidu.com' + str(smooking_next[0].extract())
            # time.sleep(1)
            # next_url = re.sub('http://', 'https://', next_url1)
            page = re.findall('&pn=(\d+)', str(response.url))
            title_list = soo.find_all("h3",class_ = "t")
            time.sleep(1)
            status = []
            for title in title_list:
                if  '兰博基尼'  in  str(title.get_text()):
                    logging.info('>>>>>>>>>>>>>>>>>>>>>>This is title ：{0}<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(title.get_text()))
                    logging.info('>>>>>>>>>>>>>>>>>>>>>>enable<<<<<<<<<<<<<<<<<<<<<<<<<<')
                    url__ = title.a['href']
                    status.append('enable')
                    ip_status = judge.judge_ip(data['proxy'])
                    if ip_status:
                        yield Request(
                    url=url__,
                    callback=lambda response,
                                    data1=data: self.click_2(response, data),
                    dont_filter=True,
                    headers=data['header'],
                    meta={'proxy': re.sub('https://', 'http://', data['proxy'])},
                )
                    else:
                        yield Request(
                    url="https://www.baidu.com",
                    callback=self.page_,
                    dont_filter=True,
                    headers=data['header'],
                    )
                else:
                    status.append('diss')
            if 'enable'  in status:
                logging.info('ok')
            elif len(page) > 0 and int(page[0]) > 200:
                time.sleep(1)
                yield Request(
                    url="http://www.baidu.com/link?url=eeSlhJLlqV2W7o8GACYxm46plhdDE5P-6RzBNNkclJsLj07Ga9-Dw3vOgGAs2N3y",
                    callback=lambda response,
                                    data1=data: self.click_2(response, data),
                    dont_filter=True,
                    headers=data['header'],
                    meta={'proxy': re.sub('https://', 'http://', data['proxy'])},
                    )

            else:
                next =   re.sub('http://', 'https://', next_url)
                next_1 =   re.sub('http://', 'https://', next)
                next_2 =   re.sub('http://', 'https://', next_1)
                ip_status = judge.judge_ip(data['proxy'])
                if ip_status:
                    yield Request(
                    url= str(next_2),
                callback=lambda response,
                            data2=data: self.click_1(response, data),
                headers=data['header'],
                meta={'proxy': data['proxy']},
                dont_filter=True
                )
                else:
                    time.sleep(1)
                    logging.info('proxy>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<erro')
                    yield Request(
                    url='https://www.baidu.com',
                    callback=self.page_,
                    headers=data['header'], dont_filter=True
                     )
        except Exception as e:
            logging.info('****************************下一ip{0}********************************'.format(e))
            yield Request(
                url="https://www.baidu.com",
                callback=self.page_,
                dont_filter=True,
                headers=data['header']
            )


    def click_2(self,response,data):
            time.sleep(random.randint(8,24))
            user_agent =data['header']
            # header = {'User-Agent': user_agent}
            meta_ = {'proxy': data['proxy']}
            data.clear()
            yield Request(
                url="https://www.baidu.com",
                callback=self.page_,
                dont_filter=True,
                meta=meta_,
                headers=user_agent,
            )
            data.clear()



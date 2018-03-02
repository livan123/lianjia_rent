# -*- coding: utf-8 -*-
import scrapy
from lianjia2.items import Lianjia2Item
from scrapy.http import Request
import urllib.request
from lxml import etree

class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    allowed_domains = ['lianjia.com']
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
    start_urls = ['http://sh.lianjia.com/zufang/pudong',
                  'http://sh.lianjia.com/zufang/minhang',
                  'http://sh.lianjia.com/zufang/baoshan',
                  'http://sh.lianjia.com/zufang/xuhui',
                  'http://sh.lianjia.com/zufang/putuo',
                  'http://sh.lianjia.com/zufang/yangpu',
                  'http://sh.lianjia.com/zufang/changning',
                  'http://sh.lianjia.com/zufang/songjiang',
                  'http://sh.lianjia.com/zufang/jiading',
                  'http://sh.lianjia.com/zufang/huangpu',
                  'http://sh.lianjia.com/zufang/jingan',
                  'http://sh.lianjia.com/zufang/zhabei',
                  'http://sh.lianjia.com/zufang/hongkou',
                  'http://sh.lianjia.com/zufang/qingpu',
                  'http://sh.lianjia.com/zufang/fengxian',
                  'http://sh.lianjia.com/zufang/jinshan',
                  'http://sh.lianjia.com/zufang/chongming',
                  'http://sh.lianjia.com/zufang/shanghaizhoubian'
                  ]

    def parse(self, response):
        shanghai = response.xpath("//div[@class='bd zufang']/dl[1]/dd[1]/div[2]/a/@href").extract()

        for i in range(1, len(shanghai)):
            # 所有分区的url
            house_url = "http://sh.lianjia.com"+shanghai[i]
            # 在divided_url中的房子数量：
            house_page = urllib.request.urlopen(house_url).read().decode("utf-8", "ignore")
            house_num = etree.HTML(house_page, parser=None, base_url=None)
            # 每一页中的数量：
            nums = house_num.xpath("//div[@class='con-box']/div[1]/h2/span/text()")
            print(nums)

            if(nums[0]!='0'):
                page_num = int(nums[0])/20
                for j in range(1, int(page_num)+2):
                    url = house_url+"/d"+str(j)
                    print(url)
                    yield Request(url, headers=self.header, meta={"url":url}, callback=self.parse_Detail)

    def parse_Detail(self, response):

        items = Lianjia2Item()

        # 标题:info-panel
        items["title"] = response.xpath("//div[@class='info-panel']/h2/a/text()").extract()

        # 小区名称:
        items["constant_company"] = response.xpath("//div[@class='info-panel']/div[@class='col-1']/div[@class='where']/a/span/text()").extract()

        # 户型
        typesss = []
        urls = []
        types = response.xpath("//div[@class='info-panel']/div[@class='col-1']/div[@class='where']/span[1]/text()").extract()
        for i in range(0, len(types)):
            typess = types[i].replace('\xa0\xa0','')
            typesss.append(typess)
            url = response.meta["url"]
            urls.append(url)
        items["house_type"] = typesss

        # url:
        items["url"] = urls

        # 面积
        areasss = []
        ii = []
        areas = response.xpath("//div[@class='info-panel']/div[@class='col-1']/div[@class='where']/span[2]/text()").extract()
        for i in range(0, len(areas)):
            ii.append(str(i))
            areass = areas[i].replace('\xa0\xa0','')
            areasss.append(areass)
        items["area"] = areasss
        items["ii"] = ii

        # 区域
        items["district"] = response.xpath("//div[@class='info-panel']/div[@class='col-1']/div[@class='other']/div[@class='con']/a[1]/text()").extract()

        # 板块
        items["plate"] = response.xpath("//div[@class='info-panel']/div[@class='col-1']/div[@class='other']/div[@class='con']/a[2]/text()").extract()

        # 楼层位置floor
        floorsssss = []
        for i in range(1, len(ii)+1):
            paths = "//*[@id='house-lst']/li["+str(i)+"]/div[2]/div[1]/div[2]/div[1]/text()"
            floors = response.xpath(paths).extract()
            floorsss = []
            for i in range(0, len(floors)):
                floorss = floors[i].replace('\n','').replace('\t','')
                floorsss.append(floorss)
            floorssss = ''.join(floorsss)
            floorsssss.append(floorssss)
        items["floor"] = floorsssss

        # 租金
        # items["rent_moeny"] = response.xpath("//div[@class='info-panel']/div[@class='col-3']/div[@class='price']/span/text()").extract()
        rent_moneysssss = []
        for i in range(1, len(ii)+1):
            rent_moneysss = []
            paths = "//*[@id='house-lst']/li["+str(i)+"]/div[2]/div[2]/div[1]//text()"
            rent_moneys = response.xpath(paths).extract()
            for j in range(0, len(rent_moneys)):
                rent_moneyss = rent_moneys[j].replace('\n','').replace('\t','')
                rent_moneysss.append(rent_moneyss)
            rent_moneyssss = ''.join(rent_moneysss)
            rent_moneysssss.append(rent_moneyssss)
        items["rent_moeny"] = rent_moneysssss
        print(items["rent_moeny"])

        # 上架时间
        sale_timesss = []
        sale_times = response.xpath("//div[@class='info-panel']/div[@class='col-3']/div[@class='price-pre']/text()").extract()
        for i in range(0, len(sale_times)):
            sale_timess = sale_times[i].replace('\n','').replace('\t','')
            sale_timesss.append(sale_timess)
        items["time_on_sale"] = sale_timesss

        # 多少人看过
        items["people_seen"] = response.xpath("//div[@class='info-panel']/div[@class='col-2']/div[@class='square']/div/span/text()").extract()

        # 一页有多少个房源：
        # ii个

        # 地铁线路
        linesssss = []
        for i in range(1, len(ii)+1):
            paths = "//*[@id='house-lst']/li["+str(i)+"]/div[2]/div[1]/div[3]/div/div//text()"
            lines = response.xpath(paths).extract()
            linesss = []
            for j in range(0, len(lines)):
                liness = lines[j].replace('\n','').replace('\t','')
                linesss.append(liness)
            linessss = ''.join(linesss)
            if(linessss==''):
                linesssss.append("没有显示地铁线")
            else:
                linesssss.append(linessss)
        items["metro_line"] = linesssss

        yield items



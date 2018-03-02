# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Lianjia2Item(scrapy.Item):
    # ii:
    ii = scrapy.Field()
    # url:
    url = scrapy.Field()
    # 名称
    title = scrapy.Field()
    # 小区名称
    constant_company = scrapy.Field()
    # 户型
    house_type = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 区域
    district = scrapy.Field()
    # 板块
    plate = scrapy.Field()
    # 楼层位置
    floor = scrapy.Field()
    # 租金
    rent_moeny = scrapy.Field()
    # 上架时间
    time_on_sale = scrapy.Field()
    # 多少人看过
    people_seen = scrapy.Field()
    # 地铁线路
    metro_line = scrapy.Field()

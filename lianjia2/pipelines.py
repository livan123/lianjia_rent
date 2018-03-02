# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import csv

class Lianjia2Pipeline(object):

    def __init__(self):
      self.csvwriter = csv.writer(open('lianjia_rent_houses.csv', 'w', newline=''), delimiter=',')
      self.csvwriter.writerow(['第几套','链接','名称','小区名称','户型','面积','区域','板块','楼层位置','租金','上架时间','多少人看过','地铁线路'])

    def process_item(self, item, spider):

        rows = zip(item['ii'],
                   item['url'],
                   item['title'],
                   item['constant_company'],
                   item['house_type'],
                   item['area'],
                   item['district'],
                   item['plate'],
                   item['floor'],
                   item['rent_moeny'],
                   item['time_on_sale'],
                   item['people_seen'],
                   item['metro_line'],
                   )

        for row in rows:
            self.csvwriter.writerow(row)

        return item

    # def process_item(self, item, spider):
    #     conn = pymysql.connect(host="localhost",
    #                            user="root",
    #                            password="123456",
    #                            db="livan",
    #                            port=3306,
    #                            charset='utf8')
    #     cur = conn.cursor()
    #     for i in range(0, len(item["ii"])):
    #         try:
    #             ii = item["ii"][i]
    #             url = item["url"][i]
    #             title = item["title"][i]
    #             constant_company = item["constant_company"][i]
    #             house_type = item["house_type"][i]
    #             area = item["area"][i]
    #             district = item["district"][i]
    #             plate = item["plate"][i]
    #             floor = item["floor"][i]
    #             rent_moeny = item["rent_moeny"][i]
    #             time_on_sale = item["time_on_sale"][i]
    #             people_seen = item["people_seen"][i]
    #             metro_line = item["metro_line"][i]
    #             print(title)
    #
    #             sql = "insert into rent_house(ii,url,title,constant_company,house_type,area,district,plate,floor,rent_moeny,time_on_sale,people_seen,metro_line) " \
    #                   "values('"+ii+"','"+url+"','"+title+"','"+constant_company+"','"+house_type+"','"+area+"','"+district+"','"+plate+"','"+floor+"','"+rent_moeny+"','"+time_on_sale+"','"+people_seen+"','"+metro_line+"')"
    #
    #             cur.execute(sql)
    #             conn.commit()
    #         except Exception as e:
    #             raise e
    #
    #     conn.close()  #关闭连接
    #
    #     return item
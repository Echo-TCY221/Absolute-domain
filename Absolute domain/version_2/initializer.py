#!/usr/bin/env python
# coding=utf-8
"""程序初始化"""
import datetime
import requests
from lxml import etree
import re
from config.data_analysis import join_db
import config.headerdata as hd


class CategoryData:
    def __init__(self, list_url):
        self.list_url = list_url
        self.headers = hd.headers
        self.category_collection = join_db()

    def get_data(self):
        try:
            with requests.Session() as session:
                response = session.get(self.list_url, headers=self.headers)
                response.raise_for_status()  # 抛出异常处理请求错误
                etree_data = etree.HTML(response.text)
                list_etree = etree_data.xpath('//div[@id="tags"]/main/ul/li')
                for index, i_xp in enumerate(list_etree, start=1):
                    list_url = i_xp.xpath('./a/@href')
                    list_name = i_xp.xpath('./a/h2/text()')
                    list_total = i_xp.xpath('./a/p/text()')
                    date_now = datetime.datetime.now()
                    formatted_date = date_now.strftime("%Y-%m-%d %H:%M:%S")
                    filte = {"_id": f"{index:05d}"}
                    existing_data = self.category_collection.find_one(filte)
                    if existing_data is None:
                        data_dict = {
                            "_id": f"{index:05d}",
                            'list_name': list_name[0],
                            'list_url': list_url[0],
                            'list_total': list_total[0],
                            'increment_data': 0,  # 新增字段
                            'put_time': formatted_date,
                            'upData_t': 0,
                            'flag': False
                        }
                        self.category_collection.insert_one(data_dict)
                    else:
                        existing_total = existing_data['list_total']
                        existing_num = int(re.findall(r'\d+', existing_total)[0])
                        new_num = int(re.findall(r'\d+', list_total[0])[0])
                        increment_data = new_num - existing_num
                        update_data = {
                            "$set": {
                                'list_total': list_total[0],
                                'increment_data': increment_data,  # 更新增量数据
                                'upData_t': formatted_date,
                                'flag': False
                            }
                        }
                        self.category_collection.update_one(filte, update_data)
                print(len(list_etree), "条数据")
        except requests.exceptions.RequestException as e:
            print("请求失败:", str(e))


def optimize_code():
    list_url = "https://www.jdlingyu.com/tags"
    category_data = CategoryData(list_url)
    category_data.get_data()


if __name__ == '__main__':
    optimize_code()

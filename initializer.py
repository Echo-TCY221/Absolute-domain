#!/usr/bin/env python
# coding=utf-8

import datetime
import requests
from lxml import etree
import re
import logging
from pymongo import MongoClient
import config.headerdata as hd


class CategoryData:
    def __init__(self, list_url, collection):
        self.list_url = list_url
        self.headers = hd.get_headers()
        self.category_collection = collection

    def update_data(self, index, list_name, list_url, list_total):
        try:
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
                    'history_data': [],  # 存储历史数据
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
                history_data = existing_data.get('history_data', [])
                history_data.append({
                    'timestamp': formatted_date,
                    'list_total': existing_total,
                })
                if increment_data != 0:
                    update_data = {
                        "$set": {
                            'list_total': list_total[0],
                            'history_data': history_data,
                            'increment_data': increment_data,
                            'upData_t': formatted_date,
                            'flag': True
                        }
                    }
                else:
                    update_data = {
                        "$set": {
                            'list_total': list_total[0],
                            'history_data': history_data,
                            'increment_data': increment_data,
                            'upData_t': formatted_date,
                            'flag': False
                        }
                    }
                self.category_collection.update_one(filte, update_data)
                if increment_data > 0:
                    logging.info(f"Incremental data found for {'_id'}: {increment_data}")
                    print(f"Incremental data found for {'_id'}: {increment_data}")
        except requests.exceptions.RequestException as e:
            logging.info("请求失败:", str(e))
            print("请求失败:", str(e))

    def get_data(self):
        try:
            with requests.Session() as session:
                response = session.get(self.list_url, headers=self.headers)
                response.raise_for_status()
                etree_data = etree.HTML(response.text)
                list_etree = etree_data.xpath('//div[@id="tags"]/main/ul/li')
                for index, i_xp in enumerate(list_etree, start=1):
                    list_url = i_xp.xpath('./a/@href')
                    list_name = i_xp.xpath('./a/h2/text()')
                    list_total = i_xp.xpath('./a/p/text()')
                    self.update_data(index, list_name, list_url, list_total)
                logging.info(f"{len(list_etree)} 条数据")
                print(f"{len(list_etree)} 条数据")
        except requests.exceptions.RequestException as e:
            logging.info(f"请求失败: {str(e)}")
            print(f"请求失败: {str(e)}")


def optimize_code():
    list_url = "https://www.jdlingyu.com/tags"
    client = MongoClient("mongodb://localhost:27017/")
    db = client["py_db"]
    collection = db["Category_list"]

    category_data = CategoryData(list_url, collection)
    category_data.get_data()

    client.close()


if __name__ == '__main__':
    optimize_code()
    logging.basicConfig(filename='db_logfile.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

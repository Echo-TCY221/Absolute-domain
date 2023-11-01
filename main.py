#!/usr/bin/env python
# coding=utf-8
# author: @ttt
# time: 2023/08/11

import json
import logging
from config.url_list import page_url_get
from config.pagedowload import DownloadImage
from config.data_analysis import run


# 将 print() 替换为日志输出函数
def log_print(message):
    logging.info(message)
    print(message)


def get_page_url_title(dir_name, total_num):
    """从JSON文件中获取页面URL和标题数据"""
    with open(dir_name, 'r', encoding='utf-8') as fp:
        dt_json = json.load(fp)
        data_list = dt_json.get('data')
        page_data = data_list[total_num]
        return page_data['url'], page_data['title']


def len_json(dir_name):
    """获取JSON文件中的数据数量"""
    with open(dir_name, 'r', encoding='utf-8') as fl:
        da_json = json.load(fl)
        return len(da_json['data'])


if __name__ == '__main__':
    logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    data_dir_name, agg_data = run()
    end_value = len_json(data_dir_name)
    save_dir = "data/page1"  # 这里设置数据保存位置
    total = 0
    while total < end_value:
        url, title = get_page_url_title(data_dir_name, total)
        page_list = page_url_get(url)
        log_print(f"{title} : {len(page_list)}")
        dp = DownloadImage
        dp.run(page_list, save_dir, total, agg_data)
        total += 1
    log_print("图片保存位置:  " + "./Absolute domain/version_2/" + save_dir)

"""
详情页请求、读取数据库、初始化数据、创建数据文件
return type: -> dir_name
"""

import datetime
import json
import time
import requests
from requests.exceptions import *
import random
from lxml import etree
from pymongo import MongoClient
from config import headerdata as hd


def send_request_get(url, headers, proxy_flag=False):
    """发送GET请求"""
    if not headers:
        headers = hd.headers
    count = 0
    while True:
        try:
            if proxy_flag:
                res = requests.get(url, headers=headers, timeout=30)
            else:
                res = requests.get(url, headers=headers, timeout=30)
            res.raise_for_status()  # 检查响应状态码
            html_str = res.text
        except (ProxyError, SSLError, HTTPError, TooManyRedirects, ConnectionError, Timeout) as e:
            count += 1
            if count <= 20:
                continue
            else:
                raise Exception('more request Exception unknow') from e
        count += 1
        if count >= 20:
            raise Exception('more request Exception unknow')
        return html_str


def get_page_list_url(url, num):
    headers = hd.headers
    response = send_request_get(url, headers)
    data_list = []
    if response is None:
        print("请求失败...")
        return None
    else:
        list_xpath_data = etree.HTML(response)
        if list_xpath_data is None:
            print("无法解析HTML数据...")
            return None
        axpath = '//div[@class="post-info"]'
        for item in list_xpath_data.xpath(axpath):
            if len(item.xpath('./h2/a/text()')) > 0 and len(item.xpath('./h2/a/@href')) > 0:
                title = item.xpath('./h2/a/text()')[0]
                url = item.xpath('./h2/a/@href')[0]
            else:
                print("xpath不适配该页面...")
                title, url = "", ""
            if len(item.xpath('./div[@class="list-footer"]/span/time/@datetime')) > 0:
                datetime_str = item.xpath('./div[@class="list-footer"]/span/time/@datetime')[0]
            else:
                datetime_str = ""
            if len(item.xpath('.//li[@class="post-list-meta-views"]/span/text()')) > 0:
                views = item.xpath('.//li[@class="post-list-meta-views"]/span/text()')[0]
            else:
                views = 0
            if len(item.xpath('.//li[@class="post-list-meta-like"]/span/text()')) > 0:
                like = item.xpath('.//li[@class="post-list-meta-like"]/span/text()')[0]
            else:
                like = 0
            data_list.append({'title': title, 'url': url, 'datetime': datetime_str, 'views': views, 'like': like})
        print(f"第{num}页..")
        return data_list


def page_turn(num, pg_num, re_url, re_list, dir_name):
    num = num
    page_num = pg_num
    req_url = re_url
    req_list = re_list
    data_list = []
    while num <= page_num:
        if num == 0 or num == 1:
            url = req_url
        else:
            url = req_list.replace('{}', str(num))
        data_list.extend(get_page_list_url(url, num))
        num += 1
        print(datetime.datetime.now())
        time.sleep(random.randint(0, 3))
    data_dic = {'data': data_list}
    print(f"共获取{len(data_list)}条数据。", dir_name)
    return data_dic


def write_data(dir_name, data_dic):
    if data_dic is None:
        print("data_dic数据为空!", data_dic)
        return None
    with open(dir_name, "w", encoding='utf-8') as ff:
        json.dump(data_dic, ff, ensure_ascii=False)
        ff.close()


def request_url_get(db_data):
    print("...参考初始化程序创建的mongodb数据库中list_name字段...")
    while True:
        list_name = input("请输入要获取的分类列表:")
        if not list_name:
            print("不能为空..")
        else:
            data_dict = db_data.find_one({'list_name': list_name})
            if not data_dict:
                print("无数据..")
            else:
                return data_dict.get('list_url')


def handle_db_connection_error(e):
    error_message = str(e)
    if "Connection refused" in error_message:
        return "无法连接到MongoDB服务器。请确保MongoDB服务器正在运行，并且已经启动。"
    elif "Authentication failed" in error_message:
        return "身份验证失败。请检查用户名和密码是否正确，并确保MongoDB服务器已启用身份验证。"
    elif "not authorized" in error_message:
        return "没有足够的权限执行指定的操作。请检查连接时使用的用户权限和数据库名称。"
    else:
        return "发生未知错误，请检查数据库连接配置和网络连接。"


def join_db():
    try:
        client = MongoClient('127.0.0.1:27017')
        db = client['py_db']  # 数据库名
        db_data = db['Category_list']  # 集合名
        print("数据库连接成功...")
        return db_data
    except ConnectionError as e:
        error_message = handle_db_connection_error(e)
        print("无法连接到MongoDB服务器")
        print("解决办法：" + error_message)
        return None


def run():
    db_data = join_db()
    dir_name = "123.json"
    request_url = request_url_get(db_data)
    request_list = request_url + "/page/{}"
    page_init = 1
    page_end = int(input("请输入获取的页数:"))
    data_dict = page_turn(page_init, page_end, request_url, request_list, dir_name)
    write_data(dir_name, data_dict)
    return dir_name

"""调用程序,获取网页链接  type：-> list"""
import requests
from lxml import etree
from config import headerdata as hdata


def page_url_get(url):
    xpath = '//div[@class="entry-content"]/p/img/@src'
    headers = hdata.headers
    response = requests.get(url, headers=headers)
    etree_data = etree.HTML(response.text)
    img_list = etree_data.xpath(xpath)
    if len(img_list) < 1:
        img_list = [""]
    return img_list

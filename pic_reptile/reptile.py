from urllib import request
from bs4 import BeautifulSoup
import lxml
import urllib
import time
import os
import struct

BASE_PAGE_HEAD='https://bangumi.bilibili.com/anime/index#p='
BASE_PAGE_TAIL='&v=0&area=&stat=0&y=0&q=0&tag=&t=1&sort=0'





url='https://bangumi.bilibili.com/web_api/season/index_global?page=1&page_size=20&version=0&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0&quarter=0'
req = urllib.request.Request(url=url)
page = request.urlopen(req).read()


print(page)

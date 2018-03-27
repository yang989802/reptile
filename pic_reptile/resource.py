# 导入 requests 库
import requests
# 从 bs4 中导入 BeautifulSoup
from bs4 import BeautifulSoup
import lxml
# 第一页的链接
url = 'https://www.doutula.com/photo/list/?page=1'
# 请求这个链接
response = requests.get(url)
# 使用返回的数据，构建一个 BeautifulSoup 对象
soup = BeautifulSoup(response.content,'lxml')
# 获取所有 class='img-responsive lazy image_dtz'的 img 标签
img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
for img in img_list:
	# 因为 src 属性刚开始获取的是 loading 的图片，因此使用 data-original 比较靠谱
	print (img['data-original'])
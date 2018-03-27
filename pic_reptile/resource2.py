from urllib import request
from bs4 import BeautifulSoup
import lxml
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
req = request.Request(url="https://www.doutula.com/photo/list/?page=1", headers=headers)
s = request.urlopen(req).read()
soup = BeautifulSoup(s.content,'lxml')
# 获取所有 class='img-responsive lazy image_dtz'的 img 标签
img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
for img in img_list:
	# 因为 src 属性刚开始获取的是 loading 的图片，因此使用 data-original 比较靠谱
	print (img['data-original'])


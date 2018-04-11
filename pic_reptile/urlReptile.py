from urllib import request
from bs4 import BeautifulSoup
import lxml
import urllib
import time
import os



def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        print('path already exists')
        return False

# url = 'http://ws2.sinaimg.cn/bmiddle/9150e4e5ly1fhpi3ysfocj205i04aa9z.jpg'
# path = 'd:/picReptile'
# mkdir(path)
# urllib.request.urlretrieve(
#     url,
#     'd:/picReptile/test.jpg',
#     cbk
# )
BASE_SAVE_PATH='d:/picReptile/'
PAGE_URL_LIST=[]  # 列表
DETAIL_IMG_URL=[] #表情包详情页
BASE_PAGE_URL ='https://www.doutula.com/article/list/?page='#主页面获取详情页
IMG_URL=[]#图片下载地址
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
start = time.time()
for x in range(1, 10):
    url = BASE_PAGE_URL + str(x)
    PAGE_URL_LIST.append(url)

for url in PAGE_URL_LIST:
    req = urllib.request.Request(url=url,headers=headers)

    try:
        page = request.urlopen(req).read()
        time.sleep(0.5)
    except:
        print('error->url'+str(url))
        continue
    else:
        page = page.decode('utf-8')
        soup = BeautifulSoup(page,'lxml')
        file_path = soup.find_all('a',attrs={'class':'list-group-item random_list'})
        for link in file_path:
            DETAIL_IMG_URL.append(link['href'])

while len(DETAIL_IMG_URL)!=0:
    url=DETAIL_IMG_URL.pop()
    req = urllib.request.Request(url=url,headers=headers)
    page = request.urlopen(req).read()
    page = page.decode('utf-8')
    soup = BeautifulSoup(page,'lxml')
    h1 = soup.h1
    h1 = h1.a
    fileName = h1.get_text()
    path = BASE_SAVE_PATH+fileName+'/'
    mkdir(path)
    imgDiv = soup.find_all('div',attrs={'class':'artile_des'})
    for img in imgDiv:
        if (img.table is None):
           continue
        else:
            IMG_URL.append(img.img['src'])
    index = 1
    while len(IMG_URL)!=0:
        url = IMG_URL.pop()
        if not (('https' in url) or ('http' in url)):
            url='http:'+url
        try:
            urllib.request.urlretrieve(
                url,
                path+str(index)+'.jpg'
            )
            index=index+1
        except:
            print('error-> '+url+'\n'+'filename:'+path)


    end = time.time()

    print('task runs %0.2f seconds.'%(end - start))



    



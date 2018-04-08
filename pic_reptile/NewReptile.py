from urllib import request
from bs4 import BeautifulSoup
import lxml
import urllib
import time
import os,random
from  multiprocessing import Process,Queue


#头
BASE_SAVE_PATH='d:/picReptile/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#主页index
PAGE_INDEX = 'https://www.doutula.com/article/list/?page='

def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        print('path already exists')
        return False
#下载图片
def downloadPic(imgDiv,path):
    IMG_URL=[]
    for img in imgDiv:
        if(img.table is None):
           print('none')
        else:
            IMG_URL.append(img.img['src'])

    index = 1
    while len(IMG_URL) != 0:
        url = IMG_URL.pop()
        if not (('https' in url) or ('http' in url)):
            url = 'http:' + url
        try:
            urllib.request.urlretrieve(
                url,
                path + str(index) + '.jpg'
            )
            index = index + 1

        except:
            print('error-> ' + url + '\n' + 'filename:' + path)
def download(link):
    print('Run download task  (%s)...' % (os.getpid()))
    req = urllib.request.Request(url=link, headers=headers)
    page = request.urlopen(req).read()
    page = page.decode('utf-8')
    soup = BeautifulSoup(page,'lxml')
    h1 = soup.h1
    h1 = h1.a
    fileName = h1.get_text()
    path = BASE_SAVE_PATH+fileName+'/'
    mkdir(path)
    imgDiv = soup.find_all('div', attrs={'class': 'artile_des'})
    downloadPic(imgDiv,path)

#记录url
def copy_url(url,num):
    req=urllib.request.Request(url = url ,headers=headers)
    try:
        page = request.urlopen(req).read()
        time.sleep(random.random() * 3)
    except:
        print('error->url:'+str(url))
    else:
        page = page.decode('utf-8')
        soup = BeautifulSoup(page,'lxml')
        file_path = soup.find_all('a', attrs={'class': 'list-group-item random_list'})
        for link in file_path:
             download(link['href'])


if __name__ == "__main__":
    start = time.time()
    for index in range(1,50):
        url = PAGE_INDEX+str(index)
        p = Process(target=copy_url,args=(url,index,))
        p.start()
    print('123')
    p.join()
    end = time.time()
    print('Task  runs %0.2f seconds.' % (end - start))



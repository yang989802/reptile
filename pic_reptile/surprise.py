import time
from urllib import request

import os
from bs4 import BeautifulSoup
from db.MysqlDB import MysqlDB
from  multiprocessing import Process,Pool
import random
connect = MysqlDB()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
def getLen():
    req = request.Request(url='https://www.doutula.com/article/list/?page=1',headers=headers)
    page = request.urlopen(req).read()
    page = page.decode('utf-8')
    soup = BeautifulSoup(page,'lxml')
    page_num = soup.find('ul',attrs={'class':'pagination'})
    page_num = page_num.contents[len(page_num.contents)-3]
    print('get len is '+page_num.get_text())
    return page_num.get_text()
def httpHead(url):
    #地址增加http
    if not (('https' in url) or ('http' in url)):
        url = 'http:' + url
    return url
def getOnError(onerror):
    #获取onError的src
    onerror = onerror.lstrip("this.src='")
    onerror = onerror.rstrip("'")
    onerror = httpHead(onerror)
    return onerror

def picNameToString(img_name):
    if img_name is None:
        return None
    else:
        string = ""
        for c in img_name:
            if c == '"':
                string += '\\\"'
            elif c == "'":
                string += "\\\'"
            elif c == "\\":
                string += "\\\\"
            else:
                string += c
        return string

def insert_pic_url(imgDiv,url_id):
    # 下载图片地址
    IMG_URL=[]
    for img in imgDiv:
        if(img.table is None):
           print('none')
           break
        else:
            onerror = getOnError(img.img['onerror'])
            img_src = img.img['src']
            img_src =httpHead(img_src)
            img_name = img.img['alt']
            img_name = picNameToString(img_name)
            connect.insertPic(img_src,onerror,url_id,img_name)
            #print('img.src = %s \n img.onerror=%s \n url_id =%s'%(img.img['src'],img.img['onerror'],url_id))



def into_pic_url(url,title,num):
    #进入下载页记录图片地址
    print('Run child process %s (%s)...' % (num, os.getpid()))
    print('title : %s  url : %s'%(title,url))
    if(connect.insertDownload(url,title)):
        req = request.Request(url=url, headers=headers)
        page = request.urlopen(req).read()
        page = page.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        imgDiv = soup.find_all('div', attrs={'class': 'artile_des'})
        url_id = connect.findUrlIdByUrl(url)
        insert_pic_url(imgDiv,url_id['ID'])
    else:
        return


#记录下载页的url
def copy_url(url,num):
    req=request.Request(url = url ,headers=headers)
    try:
        time.sleep(random.random() * 3)
        page = request.urlopen(req).read()
    except:
        print('error->url:'+str(url))
    else:
        page = page.decode('utf-8')
        soup = BeautifulSoup(page,'lxml')
        file_path = soup.find_all('a', attrs={'class': 'list-group-item random_list'})
        for link in file_path:
            into_pic_url(link['href'],link.contents[1].get_text(),num)
        file_path = soup.find_all('a', attrs={'class': 'list-group-item random_list tg-article'})
        for link in file_path:
            into_pic_url(link['href'],link.contents[1].get_text(),num)
    end =time.time()
if __name__=='__main__':
    start = time.time()
    len = int(getLen())+1#测试只用1-2页
    pool = Pool(10)
    url = connect.getUrl()
    for index in range(1,len):
       print('get :'+url+str(index))
       url_page = url+str(index)
       pool.apply_async(copy_url,args=(url_page, index,))
       # p = Process(target=copy_url, args=(url_page, index,))
       # p.start()

    pool.close()
    pool.join()

    end = time.time()
    print('task runs %0.2f seconds.'%(end - start))
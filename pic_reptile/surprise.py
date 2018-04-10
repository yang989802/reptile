import time
from urllib import request
from bs4 import BeautifulSoup
from db.MysqlDB import MysqlDB
from  multiprocessing import Process
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
    if not (('https' in url) or ('http' in url)):
        url = 'http:' + url
    return url
def getOnError(onerror):
    onerror = onerror.lstrip("this.src='")
    onerror = onerror.rstrip("'")
    onerror = httpHead(onerror)
    return onerror

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
            connect.insertPic(img_src,onerror,url_id,img.img['alt'])
            #print('img.src = %s \n img.onerror=%s \n url_id =%s'%(img.img['src'],img.img['onerror'],url_id))



def into_pic_url(url,title):
    #进入下载页记录图片地址
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
        page = request.urlopen(req).read()
        time.sleep(random.random() * 3)
    except:
        print('error->url:'+str(url))
    else:
        page = page.decode('utf-8')
        soup = BeautifulSoup(page,'lxml')
        file_path = soup.find_all('a', attrs={'class': 'list-group-item random_list'})
        for link in file_path:
            into_pic_url(link['href'],link.contents[1].get_text())

if __name__=='__main__':
    start = time.time()
    len = getLen()#测试只用1-2页
    url = connect.getUrl()
    for index in range(1,2):
       print('get :'+url+str(index))
       p = Process(target=copy_url, args=(url, index,))
       p.start()
    p.join()
    end = time.time()

    print('task runs %0.2f seconds.'%(end - start))
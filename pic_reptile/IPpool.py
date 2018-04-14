from urllib import request

import time
from bs4 import BeautifulSoup
import csv
import mysql.connector
import demjson
def insert(temp):
    start = time.time()
    connect = mysql.connector.connect(user='root', password='root', database='spider', host='127.0.0.1')
    cursor = connect.cursor(dictionary=True)
    sql = 'insert into ip_pool (ip,port) VALUES '
    for row in temp:
        sqlin = sql
        json = demjson.decode(row)
        ip = json['ip']
        port = json['port']
        sqlin += "(\'" + ip + "\'," + port + ')'
        cursor.execute(sqlin)
        connect.commit()
    connect.close()
    end = time.time()
    print('task runs %0.2f seconds.' % (end - start))
def insert_new(temp):
    start = time.time()
    connect = mysql.connector.connect(user='root', password='root', database='spider', host='127.0.0.1')
    cursor = connect.cursor(dictionary=True)
    sql='insert into ip_pool (ip,port) VALUES '
    for row in temp:
        json = demjson.decode(row)
        ip = json['ip']
        port = json['port']
        sql+="(\'"+ip+"\',"+port+'),'
    sql = sql.rstrip(',')
    cursor.execute(sql)
    connect.commit()
    connect.close()
    end = time.time()
    print('task runs %0.2f seconds.' % (end - start))
def IPspider(numpage):

    url='http://www.xicidaili.com/nn/'
    user_agent='IP'
    headers={'User-agent':user_agent}
    for num in range(1,numpage+1):
        ipurl=url+str(num)
        print('Now downloading the '+str(num*100)+' ips')
        req=request.Request(url=ipurl,headers=headers)
        content=request.urlopen(req).read()
        bs=BeautifulSoup(content,'html.parser')
        res=bs.find_all('tr')
        temp = []
        for item in res:
            try:
                tds=item.find_all('td')
                jsonStr = 'ip:"'+tds[1].get_text()+'",port:'+tds[2].get_text()
                toJson = {'ip':tds[1].get_text(),'port':tds[2].get_text()}
                json = demjson.encode(toJson)
                temp.append(json)
                print(json)

                # writer.writerow(temp)
            except IndexError:
                pass
        print(temp)
        insert_new(temp)
if __name__=='__main__':
#假设爬取前十页所有的IP和端口
    IPspider(10)

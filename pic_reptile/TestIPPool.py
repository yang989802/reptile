#!/user/bin/env python
# _*_ coding:utf-8 _*_
import mysql.connector
import telnetlib
import demjson
def getPool():
    connect = mysql.connector.connect(user='root', password='root', database='spider', host='127.0.0.1')
    cursor = connect.cursor(dictionary=True)
    cursor.execute('select ip,port from ip_pool')
    value = cursor.fetchall()
    ip_pool =[]
    for v in value:
        pool ={}
        pool['ip']=v['ip']
        pool['port']=v['port']
        pool = demjson.encode(pool)
        ip_pool.append(pool)
    connect.close()
    return ip_pool

def test(ip,port):
    connect = mysql.connector.connect(user='root', password='root', database='spider', host='127.0.0.1')
    cursor = connect.cursor(dictionary=True)
    try:
        telnetlib.Telnet(ip,port=port,timeout=2)
        print("ok")
        cursor.execute('update ip_pool set statue = 1 where ip ="%s"'%ip)
        connect.commit()
        connect.close()
    except:
        print("false")
        connect.close()
if __name__ =='__main__':
    jsonPool = getPool()
    for row in jsonPool:
        testData = demjson.decode(row)
        ip =testData['ip']
        port = testData['port']
        print('ip:%s port:%s'%(ip,port))
        test(ip,port)

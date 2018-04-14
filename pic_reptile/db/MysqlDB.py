import mysql.connector
class MysqlDB(object):
    '连接数据库'
    def __init__(self):
        self.connect = mysql.connector.connect(user='root',password='root',database='spider',host='127.0.0.1')
        self.cursor = self.connect.cursor(dictionary=True)

    def getUrl(self):
        #获取需要下载的url
        self.cursor.execute('SELECT ID,MAIN_URL,TIME FROM MAIN_URL')
        value = self.cursor.fetchone()
        time = value['TIME']
        id = value['ID']
        print('id = %s, time = %d'%(id ,time))
        self.cursor.execute('UPDATE MAIN_URL SET TIME= %d where ID=%s'%(time+1,id))
        self.connect.commit()
        return value['MAIN_URL']

    def findInDownload(self,url):
        self.cursor.execute("SELECT ID,DOWNLOAD_URL,TIME,STATUE,TITLE FROM DOWNLOAD WHERE DOWNLOAD_URL='%s'" % url)
        value = self.cursor.fetchone()
        if(value == None):
            return True
        else:
            print('%s already exists'%value)
            return  False


    def insertDownload(self,url,title):
        #录入下载地址等待使用 如果有过就不加入
        print('insert:'+url)
        if (self.findInDownload(url)):
            self.cursor.execute("INSERT INTO DOWNLOAD (DOWNLOAD_URL,TIME,STATUE,TITLE)VALUES('%s',%d,%d,'%s')"%(url,0,0,title))
            self.connect.commit()
            return True
        else:
            return False
    def findUrlIdByUrl(self,url):
        #寻找下载页面的ID
        self.cursor.execute("SELECT ID FROM DOWNLOAD WHERE DOWNLOAD_URL='%s'" % url)
        value = self.cursor.fetchone()
        return value
    def insertPic(self,src,onerror,url_id,pic_name):
        self.cursor.execute(
            "INSERT INTO PIC_DOWNLOAD (DOWNLOAD_URL_ID,SRC,ON_ERROR_SRC,STATUE,PIC_NAME)VALUES(%d,'%s','%s',0,'%s')" % (url_id, src, onerror,pic_name))
        self.connect.commit()
    def __del__(self):
        self.connect.close()
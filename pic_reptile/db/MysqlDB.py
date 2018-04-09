import mysql.connector
class MysqlDB(object):
    '连接数据库'
    def __init__(self):
        self.connect = mysql.connector.connect(user='python',password='python',database='spider',host='39.108.63.54')
        self.cursor = self.connect.cursor(dictionary=True)
    def getUrl(self):
        self.cursor.execute('SELECT download_url,competence,statue FROM DOWNLOAD')
        value = self.cursor.fetchall()
        return value
    def __del__(self):
        self.connect.close()
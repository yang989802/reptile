#!/user/bin/env python
# _*_ coding:utf-8 _*_
import imghdr
import os
from multiprocessing import Pool

root = 'D:\\picReptile\\'
def checkFilePath(path):
    file =os.listdir(path)#获取图片个数
    length = len(file)

    for i in range(0, length):
        filename = path+file[i]
        portion = os.path.splitext(filename)  # 分离文件名字和后缀
        size = imghdr.what(filename)
        print(filename)
        newname = portion[0] + "."+size
        os.rename(filename, newname)

def checkFilelist(filepath):
    filelist = os.listdir(filepath)#获取root下所有的文件
    length = len(filelist)
    poollist =Pool(5)
    for fileName in filelist:
        path = root+str(fileName)+'\\'
        poollist.apply_async(checkFilePath,args=(path,))
    poollist.close()
    poollist.join()


if __name__ == '__main__':
    checkFilelist(root)



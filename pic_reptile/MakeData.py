#!/user/bin/env python
# _*_ coding:utf-8 _*_
import os
import os.path
from multiprocessing import Pool
import random
import shutil
root = 'D:\\picReptile\\'

def checkFile(path):
    file =os.listdir(path)#获取图片个数
    length = len(file)
    if (length<50):
        for i in range(0,51-length):
            fileName = file[int(random.random()*length)]
            fileNewName = str(i)+'copy'+fileName
            print(path+fileName)
            shutil.copyfile(path+fileName,path+fileNewName)



def getFilelist(filepath):
    filelist = os.listdir(filepath)#获取root下所有的文件
    length = len(filelist)
    poollist =Pool(5)
    for fileName in filelist:
        path = root+str(fileName)+'\\'
        print(path)
        poollist.apply_async(checkFile,args=(path,))
    poollist.close()
    poollist.join()

if __name__ == '__main__':
    getFilelist(root)

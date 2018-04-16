#!/user/bin/env python
# _*_ coding:utf-8 _*_

import os
import demjson

from db.MysqlDB import MysqlDB


def getPercent(path):

    cmd = 'python D:/pythonWork/reptile/pic_reptile/learning/label_image.py --graph=/tf_files/retrained_graph.pb --labels=/tf_files/retrained_labels.txt --input_layer=Mul --output_layer=final_result --input_mean=128 --input_std=128 --image=%s'%(path)

    x=os.popen(cmd)

    data =[]
    returnDate=[]
    print(x.read())
    request = str(x.read())
    strL = request.split('\n')
    for value in strL:
        dataList = value.split(' ')
        length = len(dataList)
        if(length<=1):
            break
        v = {'id':dataList[0],'percent':dataList[1]}
        json = demjson.encode(v)
        data.append(json)


    for value in data:
        v = demjson.decode(value)
        id = v['id']
        percent =v['percent']

        if float(percent)>=0.8 :
            print('id: '+id+' percent:'+percent+' will return')
            returnDate.append(v)
    return returnDate

def start(path):
    picPool = []
    data = getPercent(path)
    m = MysqlDB()
    if not data:
        print('no')
    else:
        for v in data:
            print(v['id'])
            picPool.append(m.findPicByUrlId(v['id']))
    return picPool

if __name__ =='__main__':
    picPool=[]
    path='D:/20180416195843.png'
    data = getPercent(path)
    m = MysqlDB()
    if not data:
        print('no')
    else:
        for v in data:
            print(v['id'])
            picPool.append(m.findPicByUrlId(v['id']))
    print(picPool)

# python
# D:/pythonWork/reptile/pic_reptile/learning/retrain.py
# --bottleneck_dir=/tf_files/bottlenecks
# --how_many_training_steps 500
# --model_dir=/tf_files/inception
# --output_graph=/tf_files/retrained_graph.pb
# --output_labels=/tf_files/retrained_labels.txt
# --image_dir e:/flower_photos
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from os import  path
import re,time
import csv
from Conf import xmlConf
import struct
confs=xmlConf('../conf/conf.xml')
import mimetypes
from Storage import Storage
class Muma():
    def __init__(self):
        while True:
            for pa in confs.list1[2]: #confs.list1[2]是一个列表，元素为路径
                # print(pa)
                self.scan(pa)
            time.sleep(5)
    def scan(self,pa):
        file=os.listdir(pa) #file为列表，元素为对应子目录
        # print(file)
        for i in file:
            res=path.join(pa,i) #组合成绝对路径
            if path.isfile(res):
                with open(res,'r')as f1:
                    content=f1.read() #二进制的有些问题
                    self.judgeMuma(content,res)
                    # if b'\0' in decontent:
                    #     content=decontent.decode()
                    #     # content=struct.unpack(format,decontent) #将二进制转化为文本
                    #     print(content)
                    # else:
                        # print(decontent)
            elif path.isdir(res):
                self.scan(res) #递归调用
    def judgeMuma(self,content,file):
        with open('../conf/security/muma.csv','r')as f:
            list=f.readlines()
            for i in list:
                j=i.strip()
                # print(j) #j为规则
                if re.findall(rf"{j}",content, re.DOTALL):
                    matching=re.findall(rf"{j}",content, re.DOTALL)
                    print(f"=======检测木马=======")
                    print(f'文件路径：{file}')
                    print(f'匹配到：{matching}')
                    storage=Storage()
                    storage.storageLog('检测木马',file,matching)
                    storage.storageJson('检测木马',file,matching)
                    break


        
# with open('../conf/security/muma.csv','r')as f:
#     list=f.readlines()
#     print(list)
#     con='<script language="php">eval($_POST[hihack]);</script>'
#     for i in list:
#         j=i.strip()
#         print(j)
#         if re.findall(rf"{j}",con, re.DOTALL):
#             print(re.findall(rf"{j}",con, re.DOTALL))

# with open('../conf/security/muma.csv','rb')as f:
#     content=f.read()
#     print(content.decode())
# muma=Muma()

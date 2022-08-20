# !/usr/bin/python
# -*- coding: UTF-8 -*-
#分析日志
from os import replace
import time
import xml.dom.minidom
from xml.dom.minidom import parse
import re
from re import template
import csv
from Conf import xmlConf #从Conf.py文件中导入xmlConf类
import threading
from threading import Thread
import json
from LogMysql import LogMysql #从LogMysql.py文件中导入LogMysql类
import pymysql
from pymysql.cursors import DictCursor
import os
from Command import Command #从Command.py文件中导入Command类
#读取设置项
confs=xmlConf('../conf/conf.xml')
#执行规则库中定义的命令，并存到/var/log/commad.log中
# command=Command()    

#日志类
class Log():
    def __init__(self):
        for file in confs.list1[0]:
            # if 'access.log' in file:  
            #     rulesPath='../conf/rules/access.log.txt'
            #     self.logAnalysis(rulesPath,file)
            # elif 'error.log' in file: 
            #     rulesPath ='../conf/rules/error.log.txt'
            #     self.logAnalysis(rulesPath,file)
            # self.logAnalysis(file)
            threading.Thread(target=self.logAnalysis,args=(file,)).start() #多线程同时监控所有规则库中定义的日志
            

    def logAnalysis(self,file):
        # self.times=0 #记录次数
        self.starttime=0
        self.endtime=61
        self.decoderConfs =xmlConf('../ruleset/decoder.xml')
        self.rulesConfs =xmlConf('../ruleset/rules.xml')
        # template=self.replace()
        with open(file, 'r',encoding='utf-8') as f2:
            f2.seek(0,2)
            while True:
                i = f2.read() #这样对于防火墙命令的多行匹配也可以了
                # print(i)
                for decoder in self.decoderConfs.list: #list是元素为字典的列
                    # print(f"======={file.split('/')[-1]}日志文件=======")
                    # for i in contentList: #一条一条日志来分析，可以记录攻击次数
                    # print(i)
                    if  re.findall(rf"{decoder['match']}", i, re.DOTALL):
                        # print(decoder['description'])
                        # print(re.findall(rf"{decoder['match']}", i, re.DOTALL)) #打印匹配到的
                        for rule in self.rulesConfs.list:
                            # print(rule)
                            if decoder['did']==rule['did']: #规则对应解码器
                                if  re.findall(rf"{rule['match']}", i, re.DOTALL):
                                    if not self.starttime or self.endtime-self.starttime>60: #最多记录60s内爆破次数，这个60只能小于等于rules.xml中的time的值，否则会不对
                                            self.times=0 #记录次数,循环清零
                                            self.starttime=time.time() 
                                    for key in rule.keys():
                                        if key=='if_times' and rule['if_times']=="yes":  #如果有if_times且其值为yes
                                            self.times+=1
                                            # print(self.times)
                                            if self.times>int(rule['frequency']) :
                                                self.endtime=time.time() #结束时间
                                                if self.endtime-self.starttime<int(rule['time']):
                                                    rule['actualTimes']=self.times
                                                    rule['interval']=round(self.endtime-self.starttime,2)
                                                    self.storageJson(decoder['option'].split(','),re.findall(rf"{decoder['match']}", i, re.DOTALL),rule)
                                                    self.storageLog(decoder['option'].split(','),re.findall(rf"{decoder['match']}", i, re.DOTALL),rule,file)
                                                    self.storageLogMysql(decoder['option'].split(','),re.findall(rf"{decoder['match']}", i, re.DOTALL),rule)
                                                    self.prohibitIp(decoder['option'].split(','),re.findall(rf"{decoder['match']}", i, re.DOTALL),rule)
                                            break #if_times为yes的话直接跳出循环,下面的else也不会执行了
                                    else:
                                        self.storageJson(decoder['option'].split(','),re.findall(rf"{decoder['match']}", i, re.DOTALL),rule)
                                        self.storageLog(decoder['option'].split(','),re.findall(rf"{decoder['match']}", i, re.DOTALL),rule,file)
                                        self.storageLogMysql(decoder['option'].split(','),re.findall(rf"{decoder['match']}", i, re.DOTALL),rule)
                                        self.prohibitIp(decoder['option'].split(','),re.findall(rf"{decoder['match']}", i, re.DOTALL),rule)
                                        #传入一个列表1，一个列表2，元素为元组，一个字典
                                        #列表1如['时间','提供服务主机','状态','用户名','远程主机'] 列表2#如[('Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1')]
                                        #字典如{'did': '1', 'rid': '100', 'match': 'select|and|or|order%20by|updatexml|union|information\\.schema', 'description': '疑似SQL注入', 'level': '10'}
                                        # print(rule) #打印规则字典
                                        # print(re.findall(rf"{rule['match']}", i, re.DOTALL))
                                        # print(rule['description'])

                time.sleep(1)


                            # new_content=template.replace("${content}",content)
                            # with open('../html/index2.html','a',encoding='utf-8')as f3: #可视化操作
                            #     f3.write(new_content)


    def prohibitIp(self,list1,list2,dict2): #封IP
        li=list(list2[0]) #将如[('Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1')]转化为['Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1']
        dict1={list1[i]:li[i] for i in range(len(list1))} #将列表self.list1和列表self.list2合并为字典
        try:
            if dict2['response']=='yes':
                cmd=f"iptables -t filter -I INPUT -s {dict1['SRC']} -j DROP"
                os.popen(cmd).read()
        except:
            pass


    def storageJson(self,list1,list2,dict2):
        # print(f"{list1},{list2},{dict2}")
        li=list(list2[0]) #将如[('Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1')]转化为['Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1']
        dict1={list1[i]:li[i] for i in range(len(list1))} #将列表self.list1和列表self.list2合并为字典
        alllist=[]
        alllist.append(dict1)   
        alllist.append(dict2)   
        jsonData=json.dumps(alllist,ensure_ascii=False) #中文不被转码
        # print(jsonData)
        with open('../log/response.json','a')as fwr:
            fwr.write(f"{jsonData}\n")

    def storageLog(self,list1,list2,dict2,file):
        li=list(list2[0]) #将如[('Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1')]转化为['Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1']
        dict1={list1[i]:li[i] for i in range(len(list1))} #将列表self.list1和列表self.list2合并为字典
        with open('../log/response.log','a')as fw:
            print(f"======={file.split('/')[-1]}日志文件=======")
            fw.write(f"======={file.split('/')[-1]}日志文件=======\n")
            for  key, value in dict1.items():
                print(f'{key}:{value}')
                fw.write(f'{key}:{value}\n')
            for  key, value in dict2.items():
                print(f'{key}:{value}')
                fw.write(f'{key}:{value}\n')
        
    def storageLogMysql(self,list1,list2,dict2):
        logMysql=LogMysql()
        # li=list(list2[0]) #将如[('Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1')]转化为['Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1']
        # dict1={list1[i]:li[i] for i in range(len(list1))} #将列表self.list1和列表self.list2合并为字典
        logMysql.insert1(dict2['did'],dict2['rid'],dict2['match'],dict2['description'],dict2['level'])
            
        
    # def replace(self):
    #     with open('../html/index.html','r',encoding='utf-8')as f:
    #         template=f.read()
    #     return template

# log=Log()

#安全配置类
# class Security():
#     def __init__(self):
#         for file in confs.list1[1]:  # 遍历安全配置项文件路径
#             if 'nginx.conf' in file:  # nginx.conf安全配置项
#                 rulesPath='../conf/security/nginx.conf.txt'
#                 self.judgeSecurity(rulesPath,file)
#             elif 'my.cnf' in file:  # php.ini安全配置项
#                 rulesPath ='../conf/security/my.cnf.txt'
#                 self.judgeSecurity(rulesPath, file)
#             elif 'php.ini' in file:  # php.ini安全配置项
#                 rulesPath ='../conf/security/php.ini.txt'
#                 self.judgeSecurity(rulesPath, file)

#     def judgeSecurity(self,rulesPath,file): #判断安全项
#         print(f"======={file.split('/')[-1]}配置文件=======")
#         with open(rulesPath, 'r') as f: #打开规则文件
#             rules = csv.reader(f) #rules是个对象
#             for rule in rules: #rule是个列表，每一行的数据都是一个列表
#                 with open(file, 'r') as f:
#                     content = f.read() #直接读取全部内容
#                     if  not re.findall(rf'{rule[0]}\s*=\s*{rule[1]}', content, re.DOTALL):
#                         print(f'{rule[0]}配置项不安全')

# security=Security()








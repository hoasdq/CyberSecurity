# !/usr/bin/python
# -*- coding: UTF-8 -*-

#检测安全配置项，如php.ini、my.cnf
from os import replace
import time
import re
from re import template
import csv
from Conf import xmlConf #从Conf.py文件中导入xmlConf类
import threading
from threading import Thread
import json
#读取设置项
confs=xmlConf('../conf/conf.xml')


#安全配置类
class SecurityConf():
    def __init__(self):
        for file in confs.list1[1]:  # 遍历安全配置项文件路径 #['/etc/php.ini', '/etc/my.cnf', '/usr/local/nginx/conf/nginx.conf']
            if 'nginx.conf' in file:  # nginx.conf安全配置项
                rulesPath='../conf/security/nginx.conf.txt'
                self.judgeSecurity(rulesPath,file)
            elif 'my.cnf' in file:  # php.ini安全配置项
                rulesPath ='../conf/security/my.cnf.txt'
                self.judgeSecurity(rulesPath, file)
            elif 'php.ini' in file:  # php.ini安全配置项
                rulesPath ='../conf/security/php.ini.txt'
                self.judgeSecurity(rulesPath, file)

    def judgeSecurity(self,rulesPath,file): #判断安全项
        print(f"======={file.split('/')[-1]}配置文件=======")
        with open(rulesPath, 'r',encoding='utf-8') as f1: #打开规则文件
            rules = csv.reader(f1) #rules是个对象
            for rule in rules: #rule是个列表，每一行的数据都是一个列表
                with open(file, 'r') as f2:
                    contentlist = f2.readlines() #直接读取内容存为列表，每行为列表元素
                    for line in contentlist:
                        if  re.findall(rule[0], line): #先匹配配置项
                            if '-' in rule[1]: #第二个是多项如system-exec-phpinfo
                                list=rule[1].split('-') #list是列表如['system','exec','phpinfo']
                                for li in list:
                                    if  not re.findall(rf'{li}', line):
                                        print(f'{rule[0]}配置项缺少{li}')
                            else: #第二个不是多项
                                if  not re.findall(rf'{rule[1]}', line): #匹配配置项值
                                    print(f'{rule[0]}配置项不安全')
                                break #已经找到配置项所在的行了，不用再往下找了
                    else:
                        print(f'没有{rule[0]}配置项') #循环正常执行结束后执行的代码，break中断的不会执行
# 这个有点问题，只能检测<securityFile>/<path>下的第一个
# security=SecurityConf()



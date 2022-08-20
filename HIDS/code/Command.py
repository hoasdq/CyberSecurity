# !/usr/bin/python
# -*- coding: UTF-8 -*-
#输出命令监测，将命令输出内容保存在/var/log/command.log中供日志类进行调用分析
import threading
from threading import Thread
from  Conf import xmlConf 
import os
import time

confs=xmlConf('../conf/conf.xml')

class Command():
    def __init__(self):
        for dict in confs.commandList:
            threading.Thread(target=self.exec,args=(dict,)).start() #多线程同时监控所有规则库中定义的日志
    def exec(self,dict):
        while True:
            res1=os.popen(dict['command']).read()
            self.storageRes(res1)
            time.sleep(int(dict['interval']))
            # elif 'status' in dict['command']:
            #     print(dict['command'])
            #     res2=os.popen(dict['command']).read()
            #     time.sleep(int(dict['interval']))
            # else:
            #     res3=os.popen(dict['command']).read()
            #     time.sleep(int(dict['interval']))

    def storageRes(self,res):
        with open('/var/log/command.log','a',encoding='utf-8')as f:
            f.write(res) #命令结果都写进command.log日志,通过日志来进行分析


# command=Command()

# res1=os.popen('ip addr').read()
# print(res1)
# !/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.dom.minidom
from xml.dom.minidom import parse
import copy

#读取设置项
class xmlConf():
    def __init__(self,file):
        tree=xml.dom.minidom.parse(file) ## 使用minidom解析器打开 XML 文档
        self.conf=tree.documentElement
        if 'conf.xml' in file:
            self.list1=['logFile','securityFile','mumaFile','OS'] #对应xml文档中的子标签，写在列表里，方便下面的代码复用   #这个列表的子项后面也会定义为列表
            self.list2=['path','command']
            self.option1()
        elif 'decoder.xml' in file:
            self.list1=['decoder']
            self.list2=['did','match','option','description','level']
            self.option2()
        elif 'rules.xml' in file:
            self.list1=['rule']
            self.list2=['did','rid','match','description','level']
            self.option2()

        # for self.li in self.list:
        #     file = conf.getElementsByTagName(self.li)[0]  # 在集合中获取所有路径
        #     paths = file.getElementsByTagName('path')  # 路径列表
        #     self.li = []  # list里面的元素也定义为列表，方便后面处理
        #     for path in paths:
        #         self.li.append(path.childNodes[0].data)
        #     print(self.li)

    def option1(self):
        for i in range(len(self.list1)): #遍历列表1,里面的每一个元素作为标签
            file=self.conf.getElementsByTagName(self.list1[i])[0] # 在集合中获取所有路径
            self.commandList=[] #列表元素如{'command':'systemctl status firewalld','interval':'60'}
            self.commandDict={}
            if self.list1[i]=='OS':
                # print(self.list1[i])
                commands=file.getElementsByTagName(self.list2[1]) #路径列表self.list2[1]='commond'
                for command in commands: #列表2中的每一个元素作为标签可能存在多个
                    self.commandDict['command']=command.childNodes[0].data
                    self.commandDict['interval']=command.getAttribute("interval")
                    # print(self.commandDict)
                    # self.commandList.append(self.commandDict) #不能这样写,字典变了列表中存的字典也跟着变self.commandDict如{'command': 'systemctl status firewalld', 'interval': '60'}
                    self.commandList.append(copy.deepcopy(self.commandDict)) #如果循环超过999次使用，则会报 溢出 错误！
                    
                # print(self.commandList)
            else:
                self.list1[i]=[] #list1里面的元素也定义为列表，方便后面处理
                paths=file.getElementsByTagName(self.list2[0]) #路径列表self.list2[0]='path'
                for path in paths: #列表2中的每一个元素作为标签可能存在多个
                    # print(path.childNodes[0].data)
                    self.list1[i].append(path.childNodes[0].data)
                # print(self.list1[i]) #打印logFile和securityFile文件路径
            



    def option2(self):
        sets=self.conf.getElementsByTagName(self.list1[0]) #获取所有的self.list1[0]作为标签
        self.list=[] #self.list1中的元素也定义为列表
        for set in sets: #列表1中的每一个元素作为标签可能存在多个,比如有多个decoder
            list1=[] #存储标签和属性
            list2=[] #存储标签的值
            for j in self.list2: #遍历列表2
                list1.append(j) 
                opt=set.getElementsByTagName(j)[0] #标签只出现一次加个[0]
                list2.append(opt.childNodes[0].data)  #标签值
                if j=='rid': #rid标签有属性
                    if opt.hasAttribute("if_times"): #判断有没有
                        list1.append('if_times') 
                        list2.append(opt.getAttribute("if_times"))
                        # print(opt.getAttribute("if_sid")) #打印rid标签属性
                    if opt.hasAttribute("frequency"): #判断有没有
                        list1.append('frequency')
                        list2.append(opt.getAttribute("frequency"))
                        # print(opt.getAttribute("frequency")) #打印rid标签属性
                    if opt.hasAttribute("time"): #判断有没有
                        list1.append('time')
                        list2.append(opt.getAttribute("time"))
                        # print(opt.getAttribute("time")) #打印rid标签属性
                    if opt.hasAttribute("response"): #判断是否需要响应
                        list1.append('response')
                        list2.append(opt.getAttribute("response"))
                        # print(opt.getAttribute("time")) #打印rid标签属性

            dict = {list1[i]:list2[i] for i in range(len(list1))} #将列表self.list2和列表list合并为字典
            #{'did': '1', 'rid': '101', 'if_sid': '1', 'frequency': '3', 'time': '60', 'match': '404', 'description': '客户端错误', 'level': '5'}
            self.list.append(dict) #self.list是元素为字典的列表

        # print(self.list)
            
    
        
# confs1 =xmlConf('../conf/conf.xml')
# confs2 =xmlConf('../ruleset/decoder.xml')
# confs3 =xmlConf('../ruleset/rules.xml')
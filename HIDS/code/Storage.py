# !/usr/bin/python
# -*- coding: UTF-8 -*-

#保存检测木马的结果
import json
from LogMysql import LogMysql #从Mysql.py文件中导入LogMysql类
class Storage():
    # print(1)
    # def storageJson(self,list1,list2,dict2):
    #     # print(f"{list1},{list2},{dict2}")
    #     li=list(list2[0]) #将如[('Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1')]转化为['Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1']
    #     dict1={list1[i]:li[i] for i in range(len(list1))} #将列表self.list1和列表self.list2合并为字典
    #     alllist=[]
    #     alllist.append(dict1)   
    #     alllist.append(dict2)   
    #     jsonData=json.dumps(alllist,ensure_ascii=False) #中文不被转码
    #     # print(jsonData)
    #     with open('../log/response.json','a')as fwr:
    #         fwr.write(f"{jsonData}\n")

    def storageLog(self,title,file,matching):
        with open('../log/response.log','a')as fw:
            fw.write(f"======={title}=======\n")
            fw.write(f'文件路径：{file}\n')
            fw.write(f'匹配到：{matching}\n')

    def storageJson(self,title,file,matching):
        dict={}
        dict['title']=title
        dict['file']=file
        dict['matching']=matching
        jsonData=json.dumps(dict,ensure_ascii=False) #中文不被转码
        with open('../log/response.json','a')as fw:
            fw.write(f"{jsonData}\n")
  
    # def storageLogMysql(self,list1,list2,dict2):
    #     logMysql=LogMysql()
    #     # li=list(list2[0]) #将如[('Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1')]转化为['Jul 24 22:41:27', 'localhost', 'Failed', 'root', '192.168.50.1']
    #     # dict1={list1[i]:li[i] for i in range(len(list1))} #将列表self.list1和列表self.list2合并为字典
    #     logMysql.insert1(dict2['did'],dict2['rid'],dict2['match'],dict2['description'],dict2['level'])


# storage=Storage()
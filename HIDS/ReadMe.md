

#### HIDS说明

##### 一、介绍

这是自己模仿Wazuh开发的一款日志监测工具，功能如下：

1.实时分析和检测Web访问日志

2.监测目录中文件是否有木马

3.该HIDS可以直接执行命令，并对输出结果进行检测

4.对php.ini和my.cnf进行配置项审计

5.检测的预警结果直接打印出来，存储为response.log、response.json，也保存到数据库中

##### 二、使用方法

1.先创建数据库

```
create database  if not exists log charset utf8 ;
use log;
create table logs(id int primary key auto_increment , did int , rid int ,logmatch varchar(255) ,description varchar(255),loglevel varchar(100) );
```

2.在code/LogMysql中修改代码中关于连接数据库的部分（用户名、密码等）

```
self.con=pymysql.connect(host='localhost',user='root',password='123456',port=3306,database='log',charset='utf8',autocommit=True) 
```

3.进入code目录，使用`python3 index.py`命令

```
[root@localhost code]# python3 index.py 
```

##### 三、功能介绍

##### 1.监控日志

conf/conf.xml是配置项文件，里面可以添加和修改要监控的日志路径

```
    <logFile>
       <path>/usr/local/nginx/logs/access.log</path>
       <path>/usr/local/nginx/logs/error.log</path>
        <path>/var/log/secure</path>
        <path>/var/log/mysqld.log</path>
        <path>/var/log/command.log</path>
        <path>/var/log/cron</path>
    </logFile>
    
注意:其中<path>/var/log/command.log</path>是命令输出的内容被写到command.log该文件中去了,自己要创建一下该文件并给写权限
```

##### 2.监控木马

conf/conf.xml是配置项文件，里面可以添加和修改要监控的木马路径

该项功能对二进制文件不能检测

```
    <mumaFile>
        <!-- <path>/etc</path> -->
        <!-- <path>/usr/bin</path> -->
        <!-- <path>/usr/sbin</path> -->
        <!-- <path>/bin</path> -->
        <!-- <path>/sbin</path> -->
        <!-- <path>/boot</path> -->
        <path>/opt/tomcat1/webapps/upload</path>
        <path>/opt/tomcat2/webapps/upload</path>
        <path>/opt/tomcat3/webapps/upload</path>
        <!-- <path>/tmp</path> -->
    </mumaFile>
```

##### 3.输出命令

conf/conf.xml是配置项文件，里面可以添加和修改要循环输出的命令内容，和间隔时间

```
    <OS>
        <command interval="6" >systemctl status firewalld</command>
        <command interval="6">netstat -antp | grep -E -v ":22|:25|:80|:443|:81|:3306|:1514|:1515|:8080|:8443" | grep -v 127.0.0.1 |grep ESTABLISHED</command>
        <command interval="6">uptime</command>
        <command interval="6">find / -perm -u=s -type f 2>/dev/null</command>
        <command interval="6"> crontab -l </command>
    </OS>
```

##### 4.审计安全配置项

conf/conf.xml是配置项文件，里面可以修改php.ini、my.cnf的路径，检测内容在/conf/security中设置

```
 <securityFile>
        <path>/etc/php.ini</path>
        <!-- <path>/etc/my.cnf</path> -->
    </securityFile>
```

##### 5.预警信息样式示例

（1）response.log

```
=======secure日志文件=======
时间:Aug 20 21:25:15
提供服务主机:localhost
状态:Failed
用户名:root
SRC:192.168.50.1
did:3
rid:201
if_times:yes
frequency:3
time:60
response:no
match:(\S+ \d+ \S+) (\S+) sshd\S+ Failed password for (\S+) from (\S+)
description:疑似ssh爆破
level:10
actualTimes:7
interval:28.1
```

（2）response.json

```
[{"时间": "Aug 20 21:25:15", "提供服务主机": "localhost", "状态": "Failed", "用户名": "root", "SRC": "192.168.50.1"}, {"did": "3", "rid": "201", "if_times": "yes", "frequency": "3", "time": "60", "response": "no", "match": "(\\S+ \\d+ \\S+) (\\S+) sshd\\S+ Failed password for (\\S+) from (\\S+)", "description": "疑似ssh爆破", "level": "10", "actualTimes": 7, "interval": 28.1}]
```

（3）数据库

```
id did  rid                                 logmatch                              description   loglevel
1   1	102	 select|and|or|order%20by|updatexml|union|information\.schema|\|\|	  疑似SQL注入	     10
```



##### 四、规则设置

##### 1.主体规则

主体规则包括解码器和预警规则，分析日志中的内容，解码器先匹配日志，规则与解码器通过did相联系，规则再去匹配对应的解码器匹配过的内容，这样就不用一个规则把所有的日志都去匹配了，毕竟规则多而解码器相对应少，可以提高效率。

###### (1)解码器

在ruleset/decoder.xml中添加和修改解码器以正则匹配日志内容

```
<decoder>
    <did>1</did> 
    <match>(\d+\.\d+\.\d+\.\d+) - - (\[\S+ \S+\]) "(\S+) (\/\S+) (HTTP\S+) (\d+) \d+ \S+ \S+ \((\S+ \S+ \S+ \S+ \S+)\)</match>
    <option>SRC,攻击时间,请求方法,URL,HTTP协议版本,状态码,主机操作系统</option>
    <description>这是web_access日志</description>
    <level>1</level>
</decoder>
```

```
<did>:解码器id,不重复
<match>:正则匹配日志内容
<option>:要提取的内容，可以自己定义名称，对应<match>中括号的内容，要封IP的话代码中的命名是SRC
<description>:说明内容,介绍匹配到的内容
<level>:预警日志等级，参考Wazuh,1-15级
```

###### (2)规则

在ruleset/decoder.xml中添加和修改解码器以正则匹配日志内容

```
<rule>
    <did >1</did>
    <rid>100</rid>
    <match>404</match>
    <description>客户端错误</description>
    <level>5</level>
</rule>

<rule>
    <did>1</did>
    <rid if_times="yes" frequency="3" time="60" response="no">101</rid>
    <match>404</match>
    <description>疑似爆破</description>
    <level>10</level>
</rule>
```

```
<did>:规则对应的解码器id
<rid>:规则的id,不重复
<match>:匹配特征、攻击行为
<description>:特征、攻击行为的说明
<level>:预警日志等级，参考Wazuh,1-15级

<did>中属性：
if_times:值为yes表示记录次数，一个标志，表示该条规则要在一段时间满足一定次数才生效
frequency:表示攻击频率 
time:表示间隔时间，因为代码中设置了最多记录60秒内的连续攻击次数，所以该time最好大于等于60，或则两个数一起变化 
response:是否响应，yes就是封ip
```

```
代码中关于time的处理：

 if not self.starttime or self.endtime-self.starttime>60: 
 #最多记录60s内爆破次数，这个60只能小于等于rules.xml中的time的值，否则会不对
     self.times=0 #记录次数,循环清零
     self.starttime=time.time() 
```



##### 2.其他规则

###### (1)木马规则

在conf\security\muma.csv中，匹配木马关键字,可以添加修改

```
eval
eval\s*\(\$_POST
eval\s*\(\$_GET
eval\s*\(\$_REQUEST
substr\(md5\(\$_REQUEST
\(\$_=\S*\$_GET
assert\s*\(\$_REQUEST
<%execute
execute request
<%eval
```

###### (2)安全配置项规则

在conf\security\中的后缀为.txt的文件，匹配安全配置项关键字，逗号代表第一次分割，“-”代表第二次分隔

比如php.ini.txt中要匹配的

```
disable_functions,system-passthru-exec-shell_exec-popen-phpinfo-chdir-chroot-dir-getcwd-opendir-readdir-scandir-fopen-unlink-delete-copy-mkdir-rmdir-rename-file-file_get_contents-fputs-fwrite-chgrp-chmod-chown,限制函数
allow_url_fopen,Off,关闭本地包含
allow_url_include,Off,关闭远程包含
expose_php,Off,关闭PHP版本信息在http头中的泄漏
register_globals,Off,关闭注册全局变量
magic_quotes_gpc,On,打开magic_quotes_gpc来防止SQL注入
display_errors,Off,错误信息控制
log_errors,On,建议打开错误日志
```

#### 五、总结

这是自己模仿Wazuh开发的小工具，本意也是为了锻炼自己的代码能力，有些功能设置的可能不合理，离真正的HIDS还差的很远，只能提供些参考，如果使用中有出错或出现bug,还望见谅。
<?php
// error_reporting(0);

include "../php/Web.php";
$a=new GetMethod($conf_get_array,$_SERVER);
$b=new POSTHeadMethod($conf_post_array,file_get_contents('php://input'),getallheaders());

#SQL注入：
    #GET:
    // echo "GET型SQL注入请输入:http://192.168.50.11/WAF/vul/vul.php/?SQL=-1 or 1=1--+"."<br>";
    $sql_get=isset($_GET['SQL'])?$_GET['SQL']:-1;
    $sql1="SELECT * FROM waf where id =$sql_get";
    $con=new MySQLCon(array('port'=>'3316'));
    $result=$con->link->query($sql1);
    $res=$result->fetch_assoc();
    // var_dump($res);
    echo $res['attribute'];
    #$POST:
    // echo "POST型SQL注入请输入:SQL=-1 or 1=1-- q<br>";
    $sql_post=isset($_POST['SQL'])?$_GET['SQL']:-1;
    $sql2="SELECT * FROM waf where id =$sql_post";
    $result2=$con->link->query($sql2);
    $res2=$result2->fetch_assoc();
    echo $res2['attribute'];
    // var_dump($res2);
    #头注:
    // echo "头注型SQL注入请输入:Referer:-1 or 1=1-- q<br>";
    $uagent = isset($_SERVER['HTTP_REFERER'])?$_SERVER['HTTP_REFERER']:-1;
    $sql3="SELECT * FROM waf where id =$uagent";
    $result3=$con->link->query($sql3);
    $res3=$result3->fetch_assoc();
    echo $res3['attribute'];
    // var_dump($res3);
    #json:
    // echo "json请求SQL注入请输入:";
    // $json_string=isset(file_get_contents('php://input'))?file_get_contents('php://input'):-1;
    // $data = json_decode($json_string, true);  

#XSS注入：
    #GET:
    // echo "GET型XSS注入请输入:http://192.168.50.11/WAF/vul/XSS/level1?name=xxx"."<br>";
    #POST:
    // echo "POST型XSS注入请输入:http://192.168.50.11/WAF/vul/XSS/level1---name=xxx"."<br>";
    #HEAD:
    // echo '头注XSS请输入:http://192.168.50.11/WAF/vul/XSS/level13.php---User-Agent:1" onmouseover="javascript:alert(1)" type="submit"<br>';

#命令注入：
    #GET:
    #$POST:
    #头注
    // echo "命令注入漏洞http://192.168.50.11/WAF/vul/vul.php?command=xxxxxxxxxxxx<br>";
    $command=isset($_REQUEST['command'])?$_REQUEST['command']:'1';
    system($command);

#木马上传： 
    // echo "文件上传访问http://192.168.50.11/WAF/vul/upload/index.php<br>";

#爆破：
    #登录
#CC攻击
    #随便快速访问有WAF的页面10次

#XXE:
    // #GET: 实验不行，xml文件内容一般在通过POST请求体
    // $xxe1=$_POST['XXE'];
	// $obj = simplexml_load_string($xxe1, 'simpleXMLElement', LIBXML_NOENT);
	// print_r($obj);

    #post:
    // echo 'XXE攻击访问http://192.168.50.11/WAF/vul/vul.php/，post请求体为<!DOCTYPE xxx1 [<!ENTITY xxx2 SYSTEM "file:///etc/passwd">]>
    // <xxx3>&xxx2;</xxx3><br>';
    // $xxe = '<!DOCTYPE xxx1 [<!ENTITY xxx2 SYSTEM "file:///etc/passwd">]>
    // <xxx3>&xxx2;</xxx3>';  //后面的标签名，&实体声明一定得有
    $xxe2=file_get_contents('php://input');
	$obj = simplexml_load_string($xxe2, 'simpleXMLElement', LIBXML_NOENT);
	print_r($obj);


#SSRF:
    #GET:
    #$POST:
    #头注
    // echo "SSRF漏洞访问";
    

#反序列化：
    #GET:
    #$POST:
    #头注
//    echo '反序列化访问http://192.168.50.11/WAF/vul/serialize/work3.php?string=O:8:"start_gg":1:{s:4:"mod1";O:4:"Call":1:{s:4:"mod1";O:5:"funct":1:{s:4:"mod1";O:4:"func":1:{s:4:"mod1";O:7:"string1":1:{s:4:"str1";O:7:"GetFlag":0:{}}}}}}<br>';


#文件包含：
    #GET:
    #$POST:
    #头注
    // echo "文件包含访问http://192.168.50.11/WAF/vul/vul.php/?include=vul.php|https://www.woniuxy.com";
    include $_REQUEST['include'];




?>

<?php 
include "../php/Web.php";

$a=new GetMethod($conf_get_array,$_SERVER);
$b=new POSTHeadMethod($conf_post_array,file_get_contents('php://input'),getallheaders());
echo "我是登录页面";


?>
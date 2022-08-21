<?php 

include "../php/Web.php";

$a=new GetMethod($conf_get_array,$_SERVER);
$b=new POSTHeadMethod($conf_post_array,file_get_contents('php://input'),getallheaders());

$array_data = json_decode(file_get_contents('php://input'), true);
$id=$array_data['id'];
// echo $id;

$sql1="SELECT * FROM waf where id =$id";
$con=new MySQLCon(array('port'=>'3316'));
$result=$con->link->query($sql1);
$res=$result->fetch_assoc();
// var_dump($res);
echo $res['attribute'];

// $array1=array("user"=>"zhangsan","id"=>"-1 or 1=1--+","time"=>"2022");
// $json_data=json_encode($array1);
// echo $json_data;

?>
<?php
class MySQLCon{
    private $host='192.168.50.11';
    private $user='root';
    private $passwd='123456';
    private $db='WAF';
    private $port='3306';
    private $charset='utf8';
    public $link;
   
    
    public function __construct($array){
        // echo $this->host;
        $this->host=isset($array['host'])?$array['host']:$this->host;
        $this->user=isset($array['user'])?$array['user']:$this->user;
        $this->passwd=isset($array['passwd'])?$array['passwd']:$this->passwd;
        $this->db=isset($array['db'])?$array['db']:$this->db;
        $this->port=isset($array['port'])?$array['port']:$this->port;
        $this->charset=isset($array['charset'])?$array['charset']:$this->charset;

        // echo $this->host.$this->user.$this->passwd.$this->db.$this->port.$this->charset;
        $this->conSql();
        


    }

    private function conSql(){
        $this->link=@new mysqli($this->host,$this->user,$this->passwd,$this->db,$this->port) ;
        if ($this->link->connect_error){
             die("连接数据库失败");
        }
        $sql1="set names $this->charset"; 
        @$this->link->query($sql1) ;

    }


    public function insertTable($rid,$priority,$attribute,$description,$times,$second_times,$src,$rule){
        $sql="insert into waf(rid,priority,attribute,description,times,secondtimes,src,time,rule) values($rid,$priority,'$attribute','$description',$times,$second_times,'$src',now(),'$rule');";
        // echo $sql;
        @$this->link->query($sql);
    }

    public function modifyData($ip,$rid){

        $sql1="update waf set times=times+1 where src='$ip' and rid=$rid ";
        // echo $sql1;
        @$this->link->query($sql1);

    }

    public function modifyTime($ip,$rid){

        $sql1="update waf set time=now() where src='$ip' and rid=$rid ";
        // echo $sql1;
        @$this->link->query($sql1);

    }

    public function modifySecondTime($ip,$rid,$second_times){

        $sql1="update waf set secondtimes=$second_times where src='$ip' and rid=$rid ";
        // echo $sql1;
        @$this->link->query($sql1);

    }


    public function selectData($ip,$rid){
        $sql="select id from waf where src='$ip' and rid=$rid";
        // echo $sql;
        $result=$this->link->query($sql);
        // var_dump($result);
   
        $res=$result->fetch_assoc();
        // var_dump($res);
        return $res;  # NULL 判断是否有该id的

    }

    public function selectAllData(){
        $sql="select * from waf ";
        // echo $sql;
        $result=$this->link->query($sql);
        // var_dump($result);
        $res=$result->fetch_all(MYSQLI_ASSOC);
        // var_dump($res);
        return $res;  

    }

    public function selectTime($ip,$rid){
        $sql="select time from waf where src='$ip' and rid=$rid";
        $result=$this->link->query($sql);
        $res=$result->fetch_assoc();
        return $res['time'];  

    }

    

    public function selectSecondTimes($ip,$rid){
        $sql="select secondtimes from waf where src='$ip' and rid=$rid";
        $result=$this->link->query($sql);
        $res=$result->fetch_assoc();
        return $res['secondtimes'];  

    }

    public function selectTimesData($ip,$rid){
        $sql="select * from times where src='$ip' and rid=$rid";
        $result=$this->link->query($sql);
        $res=$result->fetch_all(MYSQLI_ASSOC);
        // var_dump($res);
        return $res;  
    }



    // public function __destruct(){
    //     echo __FUNCTION__;

    // }

}

// $db_array=array('port'=>'3316');
// $con=new MySQLCon($db_array);

// // $con->insertTable($rid,$priority,$attribute,$description,$times,$src,$rule);
// // $con->modifyData($times,$ip,$rid);
// // $con->selectData('1',1);
// $res= $con->selectTime('192.168.50.1',100001);
// var_dump($res);
// echo $res['time'];

// date_default_timezone_set('PRC');     //将date函数默认时间设置中国区时间
// $currenttime=date("Y-m-d H:i:s");   //给变量赋值，调用date函数，格式为 年-月-日 时:分:秒
// echo $currenttime;

// echo strtotime($currenttime)-strtotime($res['time']);


?>
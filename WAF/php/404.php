<?php
echo "404notfound";
include "./MySQLCon.php";
$conf_404=file_get_contents('/opt/lampp/htdocs/WAF/yaml/404.yaml'); 
$conf_404_array=yaml_parse($conf_404);

$a=new Method404($conf_404_array);

class Method404{
    private $times=1;
    private $second_times=1;
    private $con;
    public function __construct($array){
        // var_dump($array);
        $this->con=new MySQLCon(array('port'=>'3316'));
        $this->checktimes($array);

    }

    public function checkTimes($array){
        for($i=0;$i<count($array);$i++){
            $ip=$_SERVER['REMOTE_ADDR'];
            $rid=$array[$i]['rid'];
            // echo $ip;
            // echo $rid;
            $res=$this->con->selectData($ip,$rid); #查看是否有src为$ip,rid为$rid的数据
            if($res){
                $this->con->modifyData($ip,$rid); #攻击次数加1
                $this->updateTime($ip,$rid);
               
                if(isset($array[$i]['times']) and $this->second_times>$array[$i]['times']){
                    $this->con->modifyData($ip,$rid); #攻击次数加1
                    die($this->readHtml($array[$i]['description'])); 
                }


            }
            else{
               

                if(!isset($array[$i]['times'])){
                    $this->con->insertTable($array[$i]['rid'],$array[$i]['priority'],$array[$i]['attribute'],$array[$i]['description'],$this->times,$this->second_times,$_SERVER['REMOTE_ADDR'],$array[$i]['rule']); #保存带次数的
                    
                }
                
                else if(isset($array[$i]['times']) and $this->second_times>$array[$i]['times']){
                    $this->con->insertTable($array[$i]['rid'],$array[$i]['priority'],$array[$i]['attribute'],$array[$i]['description'],$this->times,$this->second_times,$_SERVER['REMOTE_ADDR'],$array[$i]['rule']); #保存带次数的
                    die($this->readHtml($array[$i]['description'])); 
                }


            
            }

        }

        

    }

    public function readHtml($description){
        $content=file_get_contents("/opt/lampp/htdocs/WAF/html/warning2.html");
        // var_dump($match);
        $content2=str_replace("{description}",$description,$content);
        echo $content2;
    }


    public function updateTime($ip,$rid){   #不停更新数据库时间戳
        $second_times=$this->con->selectSecondTimes($ip,$rid); #读取3秒连续攻击次数
        $second_times+=1;
        $save_time=$this->con->selecTtime($ip,$rid);
        $current_time=date("Y-m-d H:i:s");   //给变量赋值，调用date函数，格式为 年-月-日 时:分:秒
        $interval=strtotime($current_time)-strtotime($save_time);
        // echo $interval.'<br>';
        // echo $second_times;
        if ($interval>3){ #间隔时间大于3秒就将连续攻击的阈值清0
            $this->con->modifyTime($ip,$rid);
            $this->con->modifySecondTime($ip,$rid,0); #阈值清零
        }

        else if( $interval<=3 ){ #3秒内连续访问
            $this->con->modifySecondTime($ip,$rid,$second_times); #更新阈值
            $this->con->modifyTime($ip,$rid); #更新时间 
            $this->second_times=$second_times;

        }
    }




}


?>
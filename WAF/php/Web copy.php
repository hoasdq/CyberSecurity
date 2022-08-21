<?php
require "/opt/lampp/htdocs/WAF/php/MySQLCon.php"; #用绝对路径，省的多次加载出错
date_default_timezone_set('PRC');     //将date函数默认时间设置中国区时间

$conf_get=file_get_contents('/opt/lampp/htdocs/WAF/yaml/GET.yaml');
$conf_post=file_get_contents('/opt/lampp/htdocs/WAF/yaml/POST.yaml');

$conf_get_array=yaml_parse($conf_get);
$conf_post_array=yaml_parse($conf_post);

// var_dump($conf_get_array);
// var_dump($conf_post_array);

// $a=new GetMethod($conf_get_array,$_SERVER);
class GetMethod{
    private $times=1;
    private $second_times;
    private $con;
    public function __construct($array,$server){
        $this->con=new MySQLCon(array('port'=>'3316'));
        $this->checkWeb($array,$server);

        
    }



    public function checkWeb($array,$server){
        for($i=0;$i<count($array);$i++){
            $rule=$array[$i]['rule'];
            // echo $rule.'<br>';
            if (preg_match("/$rule/i", $server['REQUEST_URI'])){
                preg_match("/($rule)/i", $server['REQUEST_URI'],$match);
                $ip=$server['REMOTE_ADDR'];
                $rid=$array[$i]['rid'];
                // echo $ip.$rid.'<br>';
                $res=$this->con->selectData($ip,$rid); #查看是否有src为$ip,rid为$rid的数据
                if ($res){
                    // var_dump($res);
                    $this->con->modifyData($ip,$rid); #攻击次数加1

                    $this->updateTime($ip,$rid);

                    $attribute=$array[$i]['attribute']; #同属性检查是否设置阈值次数
                    $this->checkDepth($array,$i,$attribute,$server['REQUEST_URI']); #只要匹配继续匹配所有attribute相同的规则，#检查是否设置阈值次数

                    #CC单列出来，因为要满足一定次数才阻拦
                    if ($array[$i]['description']=='访问页面' or $array[$i]['description']=='疑似CC攻击'){
                        if (isset($array[$i]['times']) and $this->second_times>$array[$i]['times']){
                            die($this->readHtml($match,$array[$i]['description'])); #计算完次数才die
                            }
                    }
                    else{
                        die($this->readHtml($match,$array[$i]['description'])); 
                    }
                    
                }
                else{
                    // var_dump($res);
                    $this->con->insertTable($array[$i]['rid'],$array[$i]['priority'],$array[$i]['attribute'],$array[$i]['description'],$this->times,0,$ip,$array[$i]['rule']);

                    
                    $attribute=$array[$i]['attribute'];
                    $this->checkDepth($array,$i,$attribute,$server['REQUEST_URI']); #只要匹配继续匹配所有attribute相同的规则，#检查是否设置阈值次数

                    #CC单列出来，因为要满足一定次数才阻拦
                    if ($array[$i]['description']=='访问页面' or $array[$i]['description']=='疑似CC攻击'){
                        if (isset($array[$i]['times']) and $this->second_times>$array[$i]['times']){
                            die($this->readHtml($match,$array[$i]['description'])); #计算完次数才die
                            }
                    }
                    else{
                        die($this->readHtml($match,$array[$i]['description'])); 
                    }
                    
                }
            }
        }
       
    }
    

    public function readHtml($match,$description){
        $content=file_get_contents("/opt/lampp/htdocs/WAF/html/warning2.html");
        // var_dump($match);
        $content1=str_replace("{parameter}",$match[0],$content);
        $content2=str_replace("{description}",$description,$content1);
        echo $content2;
    }


    public function updateTime($ip,$rid){   #不停更新数据库时间戳每五秒
        $second_times=$this->con->selectSecondTimes($ip,$rid);
        $second_times+=1;
        $save_time=$this->con->selecTtime($ip,$rid);
        $current_time=date("Y-m-d H:i:s");   //给变量赋值，调用date函数，格式为 年-月-日 时:分:秒
        $interval=strtotime($current_time)-strtotime($save_time);
        // echo $interval.'<br>';
        // echo $second_times;
        if ($interval>=5){ #间隔时间大于5秒就更新一次
            $this->con->modifyTime($ip,$rid);
            $this->con->modifySecondTime($ip,$rid,0); #阈值清零
        }

        if( $interval<=3 ){ #2-3秒内次数大于3次就更新次数和时间，只要这边一直在访问阈值就会清0
            $this->con->modifySecondTime($ip,$rid,$second_times); #更新阈值
            $this->con->modifyTime($ip,$rid); #跟新时间 
            $this->second_times=$second_times;

        }
    }


    public function checkDepth($array,$i,$attribute,$url){
        for($i;$i<count($array);$i++){
            $rule=$array[$i]['rule'];
            // echo $rule.'<br>';
            // echo $url.'<br>';
            if ($array[$i]['attribute']==$attribute){
                if (preg_match("/$rule/i", $url) and isset($array[$i]['times'])){
                    if ($this->second_times>$array[$i]['times']){
                        $res=$this->con->selectData($_SERVER['REMOTE_ADDR'],$array[$i]['rid']);
                        if($res){
                            $this->con->modifyData($_SERVER['REMOTE_ADDR'],$array[$i]['rid']); #攻击次数加1
                            $this->con->modifySecondTime($_SERVER['REMOTE_ADDR'],$array[$i]['rid'],$this->second_times); #更新阈值
                        }
                        else{
                            $this->con->insertTable($array[$i]['rid'],$array[$i]['priority'],$array[$i]['attribute'],$array[$i]['description'],$this->times,$this->second_times,$_SERVER['REMOTE_ADDR'],$array[$i]['rule']); #保存带次数的
                            // echo $array[$i]['description'].'<br>';

                        }
                    
                    }
                    
                }

            }
            
        }
    }

}


// $b=new POSTHeadMethod($conf_post_array,file_get_contents('php://input'),getallheaders());
class POSTHeadMethod{
    private $times=1;
    private $second_times=1;
    private $con;

    public function __construct($array,$postData,$AllArrayData){
        $this->con=new MySQLCon(array('port'=>'3316'));
        $AllArrayData['postData']=$postData;
        if(isset($_FILES['upload_file']['name'])){
            $upload=file_get_contents("/opt/lampp/htdocs/upload/upload/".$_FILES['upload_file']['name']);
            $AllArrayData['upload']=$upload;
        }
        $values="";
        foreach($AllArrayData as $key=>$value){ #post请求和头字段
            $values.=$value;
            // echo $key.':'.$value.'<br>';
        }
        // echo $values.'<br>';
        // echo $GLOBALS["HTTP_RAW_POST_DATA"];
        $this->checkWeb($array,$values);
    
    }

    public function checkWeb($array,$values){
        for($i=0;$i<count($array);$i++){
            $rule=$array[$i]['rule'];
            // echo $rule.'<br>';
            // echo $url.'<br>';
            if (preg_match("/$rule/i", $values)){
                preg_match("/($rule)/i", $values,$match);
                $ip=$_SERVER['REMOTE_ADDR'];
                $rid=$array[$i]['rid'];
                // echo $ip.$rid.'<br>';
                $res=$this->con->selectData($ip,$rid); #查看是否有src为$ip,rid为$rid的数据
                if ($res){
                    // var_dump($res);
                    $this->con->modifyData($ip,$rid); #攻击次数加1
                    $this->updateTime($ip,$rid);

                    $attribute=$array[$i]['attribute']; #已有的规则去检测同属性检查是否设置阈值次数,就是是否有times
                    $this->checkDepth($array,$i,$attribute,$values); #只要匹配继续匹配所有attribute相同的规则，#检查是否设置阈值次数

                    #CC单列出来，因为要满足一定次数才阻拦
                    if ($array[$i]['description']=='访问页面' or $array[$i]['description']=='疑似CC攻击'){
                        if (isset($array[$i]['times']) and $this->second_times>$array[$i]['times']){
                            die($this->readHtml($match,$array[$i]['description'])); #计算完次数才die
                            }
                    }
                    else{
                        die($this->readHtml($match,$array[$i]['description'])); 
                    }
                }

                else{
                    // var_dump($res);
                    $this->con->insertTable($array[$i]['rid'],$array[$i]['priority'],$array[$i]['attribute'],$array[$i]['description'],$this->times,0,$ip,$array[$i]['rule']);

                    $attribute=$array[$i]['attribute']; #新的规则的 去检测同属性检查是否设置阈值次数,就是是否有times
                    $this->checkDepth($array,$i,$attribute,$values); #只要匹配继续匹配所有attribute相同的规则，#检查是否设置阈值次数

                    #CC单列出来，因为要满足一定次数才阻拦
                    if ($array[$i]['description']=='访问页面' or $array[$i]['description']=='疑似CC攻击'){
                        if (isset($array[$i]['times']) and $this->second_times>$array[$i]['times']){
                        die($this->readHtml($match,$array[$i]['description'])); #计算完次数才die
                        }
                    }
                    else{
                        die($this->readHtml($match,$array[$i]['description']));
                    }

                }
            } 
        }
}

    public function readHtml($match,$description){
        $content=file_get_contents("/opt/lampp/htdocs/WAF/html/warning2.html");
        // var_dump($match);
        $content1=str_replace("{parameter}",$match[0],$content); #替换$content中的{parameter}
        $content2=str_replace("{description}",$description,$content1); #$content中的{description}
        echo $content2;
    }


    public function updateTime($ip,$rid){   #不停更新数据库时间戳每五秒
        $second_times=$this->con->selectSecondTimes($ip,$rid);
        $second_times+=1;
        $save_time=$this->con->selecTtime($ip,$rid);
        $current_time=date("Y-m-d H:i:s");   //给变量赋值，调用date函数，格式为 年-月-日 时:分:秒
        $interval=strtotime($current_time)-strtotime($save_time);
        // echo $interval.'<br>';
        // echo $second_times;
        if ($interval>=5){ #间隔时间大于5秒就更新一次
            $this->con->modifyTime($ip,$rid);
            $this->con->modifySecondTime($ip,$rid,0); #阈值清零
        }

        if( $interval<=3 ){ #2-3秒内次数大于3次就更新次数和时间，只要这边一直在访问阈值就会清0
            $this->con->modifySecondTime($ip,$rid,$second_times); #更新阈值
            $this->con->modifyTime($ip,$rid); #跟新时间 
            $this->second_times=$second_times;
        }
    }


    public function checkDepth($array,$i,$attribute,$values){
        for($i;$i<count($array);$i++){
            $rule=$array[$i]['rule'];
            // echo $rule.'<br>';
            // echo $url.'<br>';
            if ($array[$i]['attribute']==$attribute){
                if (preg_match("/$rule/i", $values) and isset($array[$i]['times'])){
                    if ($this->second_times>$array[$i]['times']){
                        $res=$this->con->selectData($_SERVER['REMOTE_ADDR'],$array[$i]['rid']);
                        if($res){
                            $this->con->modifyData($_SERVER['REMOTE_ADDR'],$array[$i]['rid']); #攻击次数加1
                            $this->con->modifySecondTime($_SERVER['REMOTE_ADDR'],$array[$i]['rid'],$this->second_times); #更新阈值
                        }
                        else{
                            $this->con->insertTable($array[$i]['rid'],$array[$i]['priority'],$array[$i]['attribute'],$array[$i]['description'],$this->times,$this->second_times,$_SERVER['REMOTE_ADDR'],$array[$i]['rule']); #保存带次数的
                            // echo $array[$i]['description'].'<br>';

                        }
                    
                    }
                    
                }

            }
            
        }
    }



   
}





?>
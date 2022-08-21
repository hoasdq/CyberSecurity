<?php
include "../../php/Web.php";
$a=new GetMethod($conf_get_array,$_SERVER);
$b=new POSTHeadMethod($conf_post_array,file_get_contents('php://input'),getallheaders());


class start_gg {
    public $mod1;
    public $mod2;
    public function __destruct() {
        $this->mod1->test1();  //起点,unserialize会调用,$this->mod1=new Call();
    }
}
class Call {
    public $mod1;
    public $mod2;
    public function test1() {
        $this->mod1->test2(); //$this->mod1=new funct(); funct无test（）方法，会触发__call();
    }
}
class funct {
    public $mod1;
    public $mod2;
    public function __call($test2,$arr) {
        $s1 = $this->mod1;  
        $s1();              //函数调用,会触发__invoke(),$this->mod1=new func();
    }
}
class func {
    public $mod1;
    public $mod2;
    public function __invoke() {
        $this->mod2 = "hello".$this->mod1; //转化为字符串，可以触发__toString(),$this->mod1=new string1();
    } 
}
class string1 {
    public $str1;
    public $str2;
    public function __toString() {
        $this->str1->get_flag(); //$this->str1=new GetFlag();
        return "1";
    }
}
class GetFlag {
    public function get_flag() {
        echo "flag:"."59DB9139E685F7D6A4A8784F9221066F";
    }
}
$a = $_REQUEST['string'];
unserialize($a);

?>
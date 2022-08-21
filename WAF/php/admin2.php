<?php
$ip=$_GET['src'];
$rid=$_GET['rid'];
// $ip='192.168.50.1';
// $rid=9700001;
include './MySQLCon.php';
$con=new MySQLCon(array('port'=>'3316'));
$res=$con->selectTimesData($ip,$rid);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"  >
    <!-- <meta http-equiv="refresh" content="1"> -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" type="text/css" href="../css/table.css"/>
</head>
<body>
<table border="1">
    <tr>
        <th >编号</th>
        <th >预警id</th>
        <th >阈值次数</th>
        <th >时间</th>
        <th >源ip</th>
    </tr>
    <?php for($i=0;$i<count($res);$i++){?>
    <tr>
        <td ><?php echo  $res[$i]['id'] ?></td>
        <td ><?php echo $res[$i]['rid'] ?></td>
        <td ><?php echo $res[$i]['attack_times'] ?></td>
        <td ><?php echo $res[$i]['time'] ?></td>
        <td ><?php echo $res[$i]['src'] ?></td>
    </tr>

    <hr>

<?php }?>


</table>


</body>
</html> 
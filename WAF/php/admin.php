<?php

include './MySQLCon.php';
$con=new MySQLCon(array('port'=>'3316'));
$res=$con->selectAllData();
// var_dump($res);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"  >
    <meta http-equiv="refresh" content="1">
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
        <th >优先级</th>
        <th >属性</th>
        <th >预警描述</th>
        <th >攻击次数</th>
        <th >3秒内连续攻击次数</th>
        <th >攻击ip</th>
        <th >最近攻击时间</th>
        <!-- <th align="center" colspan="2" height="25">匹配规则</th> -->
        <!-- <th>详情</th> -->
    </tr>
    <?php for($i=0;$i<count($res);$i++){?>
    <tr>
        <td ><?php echo  $res[$i]['id'] ?></td>
        <td ><?php echo $res[$i]['rid'] ?></td>
        <td ><?php echo $res[$i]['priority'] ?></td>
        <td ><?php echo $res[$i]['attribute'] ?></td>
        <td ><?php echo $res[$i]['description'] ?></td>
        <td ><?php echo $res[$i]['times'] ?></td>
        <td ><?php echo $res[$i]['secondtimes'] ?></td>
        <td ><?php echo $res[$i]['src'] ?></td>
        <td ><?php echo $res[$i]['time'] ?></td>
        <!-- <td align="center" colspan="2" height="25"><?php echo $res[$i]['rule'] ?></td> -->
        <!-- <td><a href="<?php // echo "admin2.php?rid=".$res[$i]['rid']."&src=".$res[$i]['src'];?>"  >查看</a></td>  -->
    
       
       
    </tr>

<?php }?>


</table>


</body>
</html>
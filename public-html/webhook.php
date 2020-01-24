<?php
$body = file_get_contents("php://input");
$webhook = json_decode($body, true);

echo "test <br>";
print_r($webhook);
error_log(serialize($webhook), 0);
?>


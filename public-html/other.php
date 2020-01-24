<?php
$command = escapeshellcmd('python /var/www/checkTrusted.py');
$output = shell_exec($command);
echo $output;
echo "Dog";
?>


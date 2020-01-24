<?php
// Author: Andrew Afonso
// GitHub: https://github.com/andrewbluepiano/SmarterMVMotionWebhookAlerts
$body = file_get_contents("php://input");
$webhook = json_decode($body, true);

$command = escapeshellcmd('python /home/ara1494/www/checkTrusted.py');
$output = shell_exec($command);

if($output == 1){
    $email_subject = "Priority Motion Alert";
    $email_body = serialize($webhook);
    $to = "ara1494@rit.edu";
    $headers = "From: '$visitor_email' \r\n";
    $headers .= "Reply-To: $visitor_email \r\n";
    mail($to,$email_subject,$email_body,$headers);
    error_log(serialize($webhook), 0);
}
?>


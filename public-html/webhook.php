<?php
// Author: Andrew Afonso
// GitHub: https://github.com/andrewbluepiano/SmarterMVMotionWebhookAlerts

// Set this address to the email you would like to receive alerts to
$myEmail = "YOUR EMAIL HERE";

// Receives and decodes the message from dashboard
$body = file_get_contents("php://input");
$webhook = json_decode($body, true);

// Runs checkTrusted.py to see if any trusted devices are on the network
$cmd = "python " . $_SERVER["CONTEXT_DOCUMENT_ROOT"] . "/checkTrusted.py";
$command = escapeshellcmd($cmd);
$output = shell_exec($command);

// Constructs and sends the alert email
if($output == 1){
    $email_subject = "Priority Motion Alert";
    $email_body = serialize($webhook);
    $headers = "From: YOURSERVER@noreply.com \r\n";
    $headers .= "Reply-To: YOURSERVER@noreply.com \r\n";
    mail($myEmail,$email_subject,$email_body,$headers);
    error_log(serialize($webhook), 0);
}
?>


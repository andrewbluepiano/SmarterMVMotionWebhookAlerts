<?php
// Author: Andrew Afonso
// GitHub: https://github.com/andrewbluepiano/SmarterMVMotionWebhookAlerts

// Set $myEmail to the email you would like alerts delivered to, and $sharedSecret to a random password to use for verifying data is coming from the Meraki Dashboard
$myEmail = "yourname@website.com";
$sharedSecret = "somePassword";

// Receives and decodes the message from dashboard
$body = file_get_contents("php://input");
$webhook = json_decode($body, true);

// Check shared secret
if($webhook['sharedSecret'] != $sharedSecret){
    die("Error");
}

// Runs checkTrusted.py to see if any trusted devices are on the network
$cmd = "python " . $_SERVER["CONTEXT_DOCUMENT_ROOT"] . "/checkTrusted.py";
$command = escapeshellcmd($cmd);
$output = shell_exec($command);


// Constructs and sends the alert email
if($output == 1){
    // Sets Email headers
    $email_subject = "Priority Motion Alert";
    $headers = "From: MVAlert@noreply.com \r\n";
    $headers .= "Reply-To: MVAlert@noreply.com \r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=utf-8\r\n";
    
    // Checks if just someone loading the page.
    if($webhook != "N;"){
        $email_body = "<html><body>";
        
        $email_body .= "<h1>Motion Alert</h1>";
        
        $email_body .= "<h3>Org Info</h3>";
        $email_body .=  $webhook['organizationName'] . "<br>";
        $email_body .=  $webhook['organizationUrl'] . "<br><br>";
        
        $email_body .= "<h3>Camera Info</h3>";
        
        if($webhook['deviceName'] != ""){    // If device has a custom name set in dashboard
            $email_body .=  $webhook['deviceName'] . " : ";
        }
        $email_body .= $webhook['deviceModel'] . " : " . $webhook['deviceMac'] . "<br>";
        $email_body .=  $webhook['deviceUrl'] . "<br><br>";
        
        $email_body .= "<h3>Alert Data</h3>";
        $email_body .=  "Timestamp: " . date( "Y-m-d T H:i:s", $webhook['alertData']['timestamp']) . "<br>";
        $email_body .=  "Review footage: <a href=\"" . $webhook['deviceUrl'] . "?timestamp=" . str_replace( ".", "", $webhook['alertData']['timestamp']) . ".0\">Here</a><br>";
        
        // Only embed image if the device is using Motion Detection 2.0
        if($webhook['deviceModel'] != "MV71" && $webhook['deviceModel'] != "MV21" && $webhook['alertData']['imageEnabled']){
            $email_body .= '<img src="'. $webhook['alertData']['imageUrl'] .'" alt="Snapshot" width="500" height="281" /><br>';
        }
       
        $email_body .= "</body></html>";
        
        // Send the email.
        mail($myEmail,$email_subject,$email_body,$headers);
    }
	
	// For debugging
    // error_log(serialize($webhook), 0);
}
?>

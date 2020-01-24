# SmarterMVMotionAlerts (Webhook version)
A filtering system for Meraki MV camera motion alerts that uses the idea that you don't need alerts for motion if a trusted individual is in the same location where the motion was detected. By remembering a few network / bluetooth devices that you usually take with you when you leave the house, the program can check if you are likely home or not when motion is detected, and alert you accordingly.  


### Setup
1. Enable Meraki API access, store your api key somewhere safe.  https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API
2. Configure information in config.json. There is an example config as well.
3. Configure the email you want to recieve alerts in webhook.php
4. Publish webhook receiver to your website
5. Put config.json and checkTrusted.py somewhere on your server that PHP can access, but browsers cannot. 
6. Update path to checkTrusted.py in the webhook file
7. Set up things in dashboard. (Network-Wide -> Alerts -> Webhooks)

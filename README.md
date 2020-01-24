# SmarterMVMotionAlerts (Webhook version)
A filtering system for Meraki MV camera motion alerts that uses the idea that you don't need alerts for motion if a trusted individual is in the same location where the motion was detected. 


This is being built. Just posting so I can version control at this point. 


This is a seperate program from an earlier proof of this concept I built as a simple python script. 


### Setup
1. Enable Meraki API access, store your api key somewhere safe.  https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API
2. Configure information in config.json. There is an example config as well.
3. Configure the email you want to recieve alerts in webhook.php
4. Publish webhook receiver to your website
5. Put config.json and checkTrusted.py somewhere on your server that PHP can access, but browsers cannot. 
6. Update path to checkTrusted.py in the webhook file
7. Set up things in dashboard. (Network-Wide -> Alerts -> Webhooks)

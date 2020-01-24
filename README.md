# SmarterMVMotionAlerts (Webhook version)
A filtering system for Meraki MV camera motion alerts that uses the idea that you don't need alerts for motion if a trusted individual is in the same location where the motion was detected. 


This is being built. Just posting so I can version control at this point. 


This is a seperate program from an earlier proof of this concept I built as a simple python script. 


### Setup
1. Configure information in config.json
2. Publish webhook receiver to your website
3. Put config.json and checkTrusted.py somewhere on your server that PHP can access, but browsers cannot. 
4. Update path to checkTrusted.py in the webhook file
5. Configure email settings in MVConfig.php

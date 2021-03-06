# SmarterMVMotionAlerts (Webhook version) [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/andrewbluepiano/SmarterMVMotionWebhookAlerts)
### Overview
A log filtering / smart alert program that can use both WiFi and Bluetooth (for MR's with BT) clients as trusted devices, and when the webhook receiver webhook.php receives a motion alert, it uses checkTrusted.py to determine if you are home or not, and if not, it sends an alert email.

#### Info / ToDo:
- This implementation of the concept is built for a home / small office implementation. I highly doubt it would be able to process alerts from more then a few MV's. Making a more complex version of the idea is down the line. 
- I will be testing this application to get a statistic on what the reduction in unneeded alerts is.
- Needs to be changed so that python program has a timeout before it checks again (maybe a half a minute / minute)

#### Background Concept
I use my Meraki MV cameras to monitor the entrance of my apartment. The Meraki Dashboard offers the ability to schedule times during which detected motion will generate alerts, but with 3 roommates and being in college, there’s no real schedule that would provide more meaningful filter motion alerts. 

One day while thinking about my cameras & their alerts, networking, and IoT, I had a thought. If your smart home can perform actions when it detects you are arriving at or leaving the house, similarly I should be able to only get motion alerts when neither my roommates or myself are home, which is the only time I really care about motion detected.

Having a Meraki stack running my home network, I can get details about clients on my network with the Dashboard API. This provides the way to determine if someone is at a location (home), by checking to see if the MAC addresses of the devices they carry on their person are connected to / detected by devices on the network. 

This program operates on that concept of detecting if you are "home" or not to determine if you need to be notified of camera motion. By setting your phone, and any other devices that leave the house daily when you do to be "trusted devices", we can use the Meraki Dashboard API to check if those devices are online, before sending a motion alert.


### Setup
https://github.com/andrewbluepiano/SmarterMVMotionWebhookAlerts/wiki/Setup

### Sample Alert
<img src="https://i.imgur.com/bAsBMHe.png" width="700" height="855" />

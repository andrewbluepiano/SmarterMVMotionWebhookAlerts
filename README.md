# SmarterMVMotionAlerts (Webhook version)
One day I had a realization while thinking about smart cameras, motion detection, and IoT. Your smart home can detect if you are home based on whether or not your phone is connected to the network, and perform actions when you arrive. Thinking along those lines, your camera should be able to know when you are home, and if so, it really doesn't need to alert you of motion. 

This program operates on that concept of detecting if you are "home" or not to determine if you need to be notified of camera motion. By setting your phone, and any other devices that leave the house daily when you do to be "trusted devices", we can use the Meraki Dashboard API to check if those devices are online, before sending a motion alert.

The program can use both WiFi and Bluetooth (for AP's with BT) clients as trusted devices, and when it receives a motion alert, it uses checkTrusted.py to determine if you are home or not, and if not, it sends an alert email.


### Setup
1. Enable Meraki API access, store your api key somewhere safe.  https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API
2. Configure information in config.json. There is an example config as well.
3. Configure the email you want to recieve alerts in webhook.php, as well as your desired secret. 
4. Publish webhook.php receiver to your website
5. Put config.json and checkTrusted.py somewhere on your server that PHP can access, but browsers cannot. 
6. Update path to checkTrusted.py in the webhook file
7. Set up things in dashboard. (Network-Wide -> Alerts -> Webhooks)

### Planned improvements
The main thing I will be trying to implement is including a snapshot of the motion in the alert email. I have figured out a method that will work across all MV versions, but its going to be annoying to implement. Going to see if I can get an official way first.  

### Sample Alert
<img src="https://i.imgur.com/PJEXawP.png"  />

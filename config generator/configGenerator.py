# Author: Andrew Afonso
# Github: https://github.com/andrewbluepiano/SmarterMVMotionWebhookAlerts
# Description: Generates a config.json file for use with the Smarter MV Motion Alerts.
import requests
import os
import time
import json
import sys

def main():
    # Fields.
    apikey = ""
    networkID = ""
    trusted = []
    
    print("First time?\n Lets get things set up. \n")

    apikey = input('Enter your API Key: ')

    # Select target network by querying dashboard for organizations using that API key.
    print("Lets find your network ID\n~~~\nListing your organizations:")
    orgs = requests.get( 'https://api-mp.meraki.com/api/v0/organizations',
       headers={'x-cisco-meraki-api-key': apikey, 'Accept': 'application/json'}
    )
    if orgs.text == " ":
        # Query will return empty if the API key is incorrect.
        print("Uoho, something is wrong with the API key you entered.")
        sys.exit(0)
    else:
        organizations = json.loads(orgs.text)
        count=1
        for org in organizations:
            print(str(count) + "- Name: " + org["name"] + "  ID: " + org["id"])
            count+=1
    targetorg = organizations[int(input("\n\nEnter number for target organization: "))-1]["id"]

    # Queries dashboard for list of networks in the selected organization. Asks user to pick the correct one.
    networksget = requests.get( 'https://api-mp.meraki.com/api/v0/organizations/' + targetorg + '/networks',
       headers={'x-cisco-meraki-api-key': apikey, 'Accept': 'application/json'}
    )
    if networksget.text == " ":
       print("Hmm, something is wrong with that organization.")
       sys.exit(0)
    else:
       print("~~~~\nHere are the networks in that organization: ")
       networks = json.loads(networksget.text)
       count=1
       for network in networks:
           print(str(count) + "- Name: " + network["name"])
           count+=1
    networkID = networks[int(input('\n\nEnter the target network\'s ID: '))-1]["id"]
    
    # Checks if network is valid
    netidtest = requests.get(
       'https://api-mp.meraki.com/api/v0/networks/' + networkID,
       headers={'x-cisco-meraki-api-key': apikey, 'Accept': 'application/json'},
    )
    if netidtest.text == " ":
       print("Uoho, something is wrong with that network.")
       sys.exit(0)
       
    # Asks the user to enter the MAC addresses of the trusted devices.
    print("~~~~\nEnter on-person device's MAC addresses, one per line. Press enter or enter \"done\" when done.\n")
    while True:
       newtrust = input('MAC: ').lower()
       if newtrust == "" or newtrust == "done":
           break
       else:
           trusted.append(newtrust)
    with open('config.json', 'w') as newConfig:
        # Writes to file.
        json.dump( {"trusted" : trusted, "apikey" : apikey, "networkID" : networkID, "shard" : "api-mp.meraki.com"}, newConfig)
    newConfig.close()

if __name__ == "__main__":
    main()

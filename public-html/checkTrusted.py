# Author: Andrew Afonso
# Github: https://github.com/andrewbluepiano/SmarterMVMotionWebhookAlerts
import socket
import os
import json
import ssl
import sys
#pprint used for debugging
#import pprint

class config:
    # Defines config information
    def __init__(self):
        self.trusted = []
        self.apikey = ""
        self.networkID = ""
        self.shard = ""
    
    # Loads information from an existing config.json file.
    def loadConfig(self):
        configFile = open('config.json', 'r')
        tempConfig = json.load(configFile)
        self.trusted = tempConfig["trusted"]
        self.apikey = tempConfig["apikey"]
        self.networkID = tempConfig["networkID"]
        self.shard = tempConfig["shard"]
        configFile.close()
        
    # Converts the config data into a single list.
    def getList(self):
        return {"trusted" : self.trusted, "apikey" : self.apikey, "networkID" : self.networkID, "shard" : self.shard}
        

# Sockets used because importing requests didnt work in tests
class mySocket:
    # Initialize socket object
    def __init__(self, host):
        # It uses SSL
        self.port = 443
        self.host = host
        self.theSocket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    
    # Sends a message out of the socket, and returns the response.
    def query(self, request):
        # Creates the connection to the host
        try:
            self.theSocket.connect((self.host, self.port))
        except socket.error as socketerror:
            print("Socket Connect Error: ", socketerror)
        # Sends the request
        try:
            output = ""
            self.theSocket.send(request.encode())
            # Continues receiving 4096 response bits(?) at a time until the response has been completely read
            while 1==1:
                response = self.theSocket.recv(4096)
                #print(response)
                if not response:
                    break
                output+=str(response)
            self.theSocket.close()
        except socket.error as socketerror:
                print("Socket Error: ", socketerror)
        return output
        
# Takes a few options, builds an GET request for the API call
def makerequest(config, target, params):
    request = "GET "
    request += target
    request += " HTTP/1.1"
    request += "\r\n"
    request += "Host: "
    request += config.shard
    request += "\r\n"
    request += "x-cisco-meraki-api-key: "
    request += config.apikey
    request += "\r\n"
    request += "Accept: application/json"
    request += "\r\n\r\n"
    request += params
    return request
    

# Gets Wifi clients, returns an array of the clients.
def getWifiClients(config, socket):
    WifiTarget = '/api/v0/networks/' + config.networkID + '/clients'
    WifiRequest = makerequest( config, WifiTarget, "timespan=1800")
    WifiClientsGet = socket.query( WifiRequest )
    WifiClients =  ("[{" + (WifiClientsGet.split("}]")[0] + "}]").split("[{")[1]).replace("\\", "")
    WifiClientsArray = json.loads(WifiClients)
    return WifiClientsArray
    
# Gets Bluetooth clients, returns an array of the clients.
def getBTClients(config, socket):
    BTtarget = '/api/v0/networks/' + config.networkID + '/bluetoothClients'
    BTrequest = makerequest( config, BTtarget, "timespan=60")
    BTClientsGet = socket.query( BTrequest)
    BTClients =  ("[{" + (BTClientsGet.split("}]")[0] + "}]").split("[{")[1]).replace("\\", "")
    BTClientsArray = json.loads(BTClients)
    return BTClientsArray
    
def main():
    appConfig = config()
    appConfig.loadConfig()
    WifiSocket = mySocket(appConfig.shard)
    BTSocket = mySocket(appConfig.shard)
    wifiClients = getWifiClients(appConfig, WifiSocket)
    bluetoothClients = getBTClients(appConfig, BTSocket)
    notify = 1
    
    # Runs through the list of current Wifi and Bluetooth clients, and checks if they are trusted devices
    for client in wifiClients:
        if notify == 1 and client["status"] != "Offline" and client["mac"] in appConfig.trusted:
            notify = 0
    
    if notify == 1:
        for client in bluetoothClients:
            if client["mac"] in appConfig.trusted:
                notify = 0
    
    if notify == 1:
        print("1") # Notifiable person
    else:
        print("0") # Trusted devices detected, all safe (Probabaly)

if __name__ == "__main__":
    main()

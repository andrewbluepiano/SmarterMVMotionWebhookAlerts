# Author: Andrew Afonso
# Github:
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
    
    # Loads information from an existing config.json file.
    def loadConfig(self):
        configFile = open('config.json', 'r')
        tempConfig = json.load(configFile)
        self.trusted = tempConfig["trusted"]
        self.apikey = tempConfig["apikey"]
        self.networkID = tempConfig["networkID"]
        configFile.close()
        
    # Converts the config data into a single list.
    def getList(self):
        return {"trusted" : self.trusted, "apikey" : self.apikey, "networkID" : self.networkID}
        
        
class mySocket:
    def __init__(self):
        self.port = 443
        self.theSocket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    
    def query(self, host, request):
        try:
            self.theSocket.connect((host, self.port))
        except socket.error as socketerror:
            print("Socket Connect Error: ", socketerror)
        try:
            output = ""
            self.theSocket.send(request.encode())
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
        
def makerequest(target, host, api_key, params):
    request = "GET "
    request += target
    request += " HTTP/1.1"
    request += "\r\n"
    request += "Host: "
    request += host
    request += "\r\n"
    request += "x-cisco-meraki-api-key: "
    request += api_key
    request += "\r\n"
    request += "Accept: application/json"
    request += "\r\n\r\n"
    request += params
    return request

def main():
    appConfig = config()
    senderSocket = mySocket()
    
    host = "n151.meraki.com"
    wifitar = '/api/v0/networks/' + appConfig.networkID + '/clients';
    wifireq = makerequest( wifitar, host, appConfig.apikey, "timespan=1800")
#    print(wifireq)
    wificlientsget = senderSocket.query( host, wifireq)
    wificlients =  ("[{" + (wificlientsget.split("}]")[0] + "}]").split("[{")[1]).replace("\\", "")
#    print(wificlients)
#    print(soup)
#    print(wificlients)
    
    
    # The main loop. Checks if the camera detects a person, if so, check if any trusted devices are on the network. If not, alert.
#    wificlientsget = requests.get(
#        'https://api.meraki.com/api/v0/networks/' + appConfig.networkID + '/clients',
#        headers={'x-cisco-meraki-api-key': appConfig.apikey, 'Accept': 'application/json'},
#        params={'timespan' : '1800'}
#    )
#    bluetoothclientsget = requests.get(
#        'https://api.meraki.com/api/v0/networks/' + appConfig.networkID + '/bluetoothClients',
#        headers={'x-cisco-meraki-api-key': appConfig.apikey, 'Accept': 'application/json'},
#        params={'timespan' : '60'}
#    )
    
    wifiClients = json.loads(wificlients)
#    bluetoothClients = json.loads(bluetoothclientsget.text)
    
#                    print(wificlientsget.url)
#                    print(wificlientsget.text)
#                    pp.pprint(wifiClients)
#                    pp.pprint(bluetoothClients)
    
    notify = 1
    
    for client in wifiClients:
        if client["status"] != "Offline" and client["mac"] in appConfig.trusted:
            notify = 0
#
#    for client in bluetoothClients:
#        if client["mac"] in appConfig.trusted:
#            notify = 0
    
    # What happens if a warnable person is detected. Ideal place to start customizations.
    if notify == 1:
        print("1")
    else:
        print("0")

if __name__ == "__main__":
    main()

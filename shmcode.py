import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "35bc98"
deviceType = "NodeMcu"
deviceId = "shm123"
authMethod = "token"
authToken = "smarthealthmonitor123"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()


deviceCli.connect()

while True:
        
        #Generating random temperature values and pulse rates to imiatate a real sensor
        temp =round(random.uniform(96,102),1)
        pul=random.randint(30, 160)
        if temp<=97 or temp>=100:
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=tpf3OnrXzVe1HAlswdakiRbP6g70GEmoZyJNScUDQIuCL92TW85WXU7IuiSJwf3r2mCpcLGzK1MZbnAx&sender_id=FSTSMS&message=ABNORMAL TEMPERATURE DETECTION&language=english&route=p&numbers=YOUR NUMBER')
        if pul<60 or pul>100:
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=tpf3OnrXzVe1HAlswdakiRbP6g70GEmoZyJNScUDQIuCL92TW85WXU7IuiSJwf3r2mCpcLGzK1MZbnAx&sender_id=FSTSMS&message=ABNORMAL PULSE DETECTION&language=english&route=p&numbers=YOUR NUMBER')
                print(r.status_code)
        #Send Temperature & Pulse to IBM Watson
        data = { 'Temperature' : temp, 'Pulse': pul }
        #print(data)
        def myOnPublishCallback():
            print ("Published Temperature = %s F" % temp, "Pulse = %s bpm" % pul, "to IBM Watson")

        success = deviceCli.publishEvent("Health_status", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(10)
       
                
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()

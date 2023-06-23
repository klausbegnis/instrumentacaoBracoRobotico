#Define Libraries
import RPi.GPIO as gpio
import time
from paho.mqtt import client as mqtt_client
import json

class GPIOmanager():
    def __init__(self,x_max=0,y_max=0):
        
        #Configuring don’t show warnings 
        gpio.setwarnings(False)

        # definitions
        self.x_pin = 27
        self.y_pin = 22

        self.xi = 50 # value readed
        self.yi = 25 # value readed

        self.x_max = x_max #mm
        self.y_max = y_max #mm
        self.x_min = 0
        self.y_min = 0

        self.period = 0.1 #s
        self.frequency = 1/self.period # Hz

        #Configuring GPIO
        gpio.setmode(gpio.BCM)
        gpio.setup(self.x_pin,gpio.OUT)
        gpio.setup(self.y_pin,gpio.OUT)

        self.pwmX = gpio.PWM(self.x_pin,self.frequency)
        self.pwmX.start(50)

        self.pwmY = gpio.PWM(self.y_pin,self.frequency)
        self.pwmY.start(50)

        ## creates mqtt connection

        #config_path = r"./json/brokerInfo.json"
        #mqtt_Config = self.readMQTTconfig(config_path)
        #client = self.connectMqtt(mqtt_Config)

 
    def update_dc(self,xi,yi):


        if xi >= self.x_max:
            dcX = 99.99 #maximum value allowed from the library
        elif xi <= self.x_min:
            dcX = 0
        else:
            dcX = (xi/self.x_max)*100

        if yi >= self.y_max:
            dcY = 99.99 #maximum value allowed from the library
        elif yi <= self.y_min:
            dcY = 0
        else:
            dcY  = (yi/self.y_max)*100

        self.pwmX.ChangeDutyCycle(dcX)
        self.pwmX.ChangeDutyCycle(dcY)

    def setMAXvalues(self,x,y):
        self.x_max = x
        self.y_max = y

    #Create the dutycycle variables


    #def readMQTTconfig(self,path):
    #    # opens json file and returns dictionaty
    #    with open(path,'r') as file:
    #        info = json.load(file)
    #    return info

    #def connectMqtt(self,client_json):
    #    def on_connect(client, userdata, flags, rc):
    #        if client._client_id != None: ###to debug only the write
    #            if rc == 0:
    #                print("MQTT connection successful")
    #            else:
    #                print(f"MQTT connection failed: rc{rc}")
    #        else:
    #            pass
    #    def on_disconnect(client, userdata, rc):
    #        print(f"Client disconnected code= {rc}")
    #    
    #    client = mqtt_client.Client(client_json["client"])
    #    client.username_pw_set(client_json["user"], client_json["pwd"])
    #    client.on_connect = on_connect
    #    client.on_disconnect = on_disconnect
    #    client.connect(client_json["broker"], client_json["port"])
    #    return client
                
    #def readCoordinates(self,client_json,client,pwmx,pwmy):
    #        def on_message(client, userdata, msg):
    #            global xi
    #            global yi
    #            info = json.loads(msg.payload.decode())
    #            xi = info["x_coord"]
    #            yi = info["y_coord"]
    #            self.update_dc(xi,yi,pwmx,pwmy)
    #            print(xi,yi)
#Define Libraries
import RPi.GPIO as gpio
import time
from paho.mqtt import client as mqtt_client
import json

#Configuring don’t show warnings 
gpio.setwarnings(False)

# definitions
x_pin = 27
y_pin = 22

xi = 50 # value readed
yi = 25 # value readed

x_max = 100 #mm
y_max = 100 #mm
x_min = 0
y_min = 0

period = 0.1 #s
frequency = 1/period # Hz

#Configuring GPIO
gpio.setmode(gpio.BCM)
gpio.setup(x_pin,gpio.OUT)
gpio.setup(y_pin,gpio.OUT)

pwmX = gpio.PWM(x_pin,frequency)
pwmX.start(0)

pwmY = gpio.PWM(y_pin,frequency)
pwmY.start(0)

 
def update_dc(xi,yi,pwnx,pwmy):

    x_max = 100
    y_max = 100
    x_min = 0
    y_min = 0
    if xi >= x_max:
        print(xi,x_max)
        dcX = 99.99 #maximum value allowed from the library
    elif xi <= x_min:
        print(xi,x_min)
        dcX = 0
    else:
        dcX = (xi/x_max)*100

    if yi >= y_max:
        dcY = 99.99 #maximum value allowed from the library
    elif yi <= y_min:
        dcY = 0
    else:
        dcY  = (yi/y_max)*100

    pwnx.ChangeDutyCycle(dcX)
    pwmy.ChangeDutyCycle(dcY)


#Create the dutycycle variables


def readMQTTconfig(path):
    # opens json file and returns dictionaty
    with open(path,'r') as file:
        info = json.load(file)
    return info

def connectMqtt(client_json):
    def on_connect(client, userdata, flags, rc):
        if client._client_id != None: ###to debug only the write
            if rc == 0:
                print("MQTT connection successful")
            else:
                print(f"MQTT connection failed: rc{rc}")
        else:
            pass
    def on_disconnect(client, userdata, rc):
        print(f"Client disconnected code= {rc}")
    
    client = mqtt_client.Client(client_json["client"])
    client.username_pw_set(client_json["user"], client_json["pwd"])
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(client_json["broker"], client_json["port"])
    return client
            
def readCoordinates(client_json,client,pwmx,pwmy):
    def on_message(client, userdata, msg):
        global xi
        global yi
        info = json.loads(msg.payload.decode())
        xi = info["x_coord"]
        yi = info["y_coord"]
        update_dc(xi,yi,pwmx,pwmy)
        print(xi,yi)

    client.subscribe(client_json["topic"])
    client.on_message = on_message
    client.loop_forever()

## creates mqtt connection

config_path = r"./json/brokerInfo.json"
mqtt_Config = readMQTTconfig(config_path)
client = connectMqtt(mqtt_Config)
readCoordinates(mqtt_Config,client,pwmX,pwmY)



#Configure the pwm objects and initialize its value

update_dc(xi,yi)



#Loop infinite
while True:
    try:
        #increment gradually the luminosity
        time.sleep(0.5)

            
    except Exception as e:
        print(e)
        #End code
        gpio.cleanup()
        exit()
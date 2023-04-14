from paho.mqtt import client as mqtt_client
import json
import time

class MQTT():
    def __init__(self) -> None:
        self.configs = r"./json/brokerinfo.json"
        with open(self.configs,'r') as file:
            info = json.load(file)

        self.broker     = info["broker"]
        self.port       = info["port"]
        self.topic     = info["topic"] # topic for inputs reading
        self.user       = info["user"]
        self.pwd        = info["pwd"]
        self.client_id    = info["client"]

        self.client = mqtt_client.Client(self.client_id)
        self.client.username_pw_set(self.user,self.pwd)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(self.broker,self.port)
        self.client.loop_start()
    
    
        
    def on_connect(self,client, userdata, flags, rc):
        if client._client_id != None and self.client_id in str(client._client_id): ###to debug only the write
            if rc == 0:
                print("Connected")
            else:
                pass
        else:
            pass

    def on_disconnect(client, userdata, rc):
            print("Client disconnected")
    
    def sendCoordinates(self,cords):
        self.client.publish(self.topic,json.dumps({"cords":cords}))

mqtt = MQTT()

if __name__ == "__main__":
    while True:
        mqtt.sendCoordinates((100,50))
        time.sleep(1)
        
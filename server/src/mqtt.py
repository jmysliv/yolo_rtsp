import json
from paho.mqtt import client as mqtt_client
from dataclasses import dataclass
import threading

@dataclass
class MqttInfo:
    client_id: str
    username: str
    password: str
    broker: str
    port: int
    topic: str


class MqttManager:
    objects = []
    def __init__(self, mqtt_info: MqttInfo):
        self._mqtt_info = mqtt_info
        self._mqtt_client = self.connect_mqtt() if mqtt_info else None
        def on_message(client, userdata, msg):
            data = json.loads(msg.payload)
            if len(data['detected_objects']) > 0:
                self.objects.append(data)

        self._mqtt_client.subscribe(self._mqtt_info.topic)
        self._mqtt_client.on_message = on_message
        self.mqtt_thread = threading.Thread(target=self._mqtt_client.loop_forever, args=())
        self.mqtt_thread.start()

    def connect_mqtt(self):
        def on_connect(client_instance, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker")
            else:
                print("Failed to connect to MQTT broker, return code %d\n", rc)
        
        try:
            client = mqtt_client.Client(self._mqtt_info.client_id)
            client.username_pw_set(self._mqtt_info.username, self._mqtt_info.password)
            client.on_connect = on_connect
           
            client.connect(self._mqtt_info.broker, self._mqtt_info.port)
            return client
        except Exception as e:
            print(e)
            return None

    def stop(self):
        if self._mqtt_client:
            self._mqtt_client.disconnect()
            self.mqtt_thread.join()

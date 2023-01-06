import json
from paho.mqtt import client as mqtt_client
from ..utils.types import  MqttInfo
from ..utils.logger import logger
import threading

def generate_detected_objects_info(result):
    info = []
    classes, confidences, boxes = result
    for class_name, confidence, box in zip(classes, confidences, boxes):
        info.append({
            'class': class_name,
            'confidence': confidence,
            'box': {
                'upperLeft': (box[0], box[1]),
                'lowerRight': (box[0] + box[2], box[1] + box[3])
            }
        })
    return info


class MqttManager:
    def __init__(self, mqtt_info: MqttInfo):
        self._mqtt_info = mqtt_info
        self._mqtt_client = self.connect_mqtt() if mqtt_info else None
        self.loop_thread = threading.Thread(target=self._mqtt_client.loop_forever, args=())
        self.loop_thread.start()

    def connect_mqtt(self):
        def on_connect(client_instance, userdata, flags, rc):
            if rc == 0:
                logger.info("Connected to MQTT broker")
            else:
                logger.warning("Failed to connect to MQTT broker, return code %d\n", rc)
        
        # def on_message(client, userdata, msg):
        #     print(msg.topic+" "+str(msg.payload))
        try:
            client = mqtt_client.Client(self._mqtt_info.client_id)
            client.username_pw_set(self._mqtt_info.username, self._mqtt_info.password)
            client.on_connect = on_connect
            # client.on_message = on_message
            client.connect(self._mqtt_info.broker, self._mqtt_info.port)
            return client
        except Exception as e:
            print(e)
            return None

    def publish_message(self, obj):
        msg = json.dumps(obj, default=str)
        if self._mqtt_client:
            result = self._mqtt_client.publish(self._mqtt_info.topic, msg)
            status = result[0]
            if status == 0:
                logger.info(f"Send message to MQTT topic")
            else:
                logger.warning(f"Failed to send message to MQTT topic")
                logger.info(msg)
        else:
            logger.info(msg)

    def stop(self):
        if self._mqtt_client:
            self._mqtt_client.disconnect()
            self.loop_thread.join()

from .src.server import app
from .src.mqtt import MqttManager, MqttInfo
import yaml 

if __name__ == "__main__":
    file_path = './server/res/config/conf.yaml'
    with open(file_path, 'r') as stream:
        conf = yaml.safe_load(stream)
    info = conf['mqtt_info']
    mqtt_info = MqttInfo(
        client_id=info['client_id'], username=info['username'], password=info['password'],
        broker=info['broker'], port=info['port'], topic=info['topic']
    )
    manager = MqttManager(mqtt_info)
    app.run()

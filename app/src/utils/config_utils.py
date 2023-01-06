import yaml
from .types import Config, FrameStrategy, MqttInfo

  

def load_and_parse_config() -> Config:
    file_path = './app/res/config/conf.yaml'
    with open(file_path, 'r') as stream:
        conf = yaml.safe_load(stream)
    info = conf['mqtt_info']
    mqtt_info = MqttInfo(
        client_id=info['client_id'], username=info['username'], password=info['password'],
        broker=info['broker'], port=info['port'], topic=info['topic']
    )
    return Config(
        frame_rate_timeout=conf['frame_rate_timeout'], rtsp_url=conf['rtsp_url'],
        mqtt_info=mqtt_info, frame_strategy=FrameStrategy[conf['frame_strategy']]
    )
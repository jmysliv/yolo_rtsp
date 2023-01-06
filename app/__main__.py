from .src.utils.config_utils import load_and_parse_config
from .src.frames.frames_manager import FramesManager
from .src.frames.rtsp_reader import RtspReader
from .src.utils.logger import logger
from .src.utils.metric_collector import MetricCollector
from .src.utils.mqtt import MqttManager



if __name__ == "__main__":
    config = load_and_parse_config()
    mqtt_manager = MqttManager(config.mqtt_info)
    frames_manager = FramesManager(config.frame_strategy, mqtt_manager)
    rtsp_reader = RtspReader(config.frame_rate_timeout, config.rtsp_url, frames_manager)
    metric_collector = MetricCollector(rtsp_reader, mqtt_manager)
    metric_collector.start_collecting_metrics()

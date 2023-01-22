import psutil
from datetime import datetime
import time
from ..frames.rtsp_reader import RtspReader
from .mqtt import MqttManager
class MetricCollector:
    def __init__(self, rtsp_reader: RtspReader, mqtt_manager: MqttManager):
        self.rtsp_reader = rtsp_reader
        self.mqtt_manager = mqtt_manager
        self.timestamp = datetime.now()
        self.cpu_usage = None
        self.memory_usage = None
        self.number_of_frames = 0
        self.frames_per_second = None

    def start_collecting_metrics(self):
        while True:
            self.cpu_usage = psutil.cpu_percent(4)
            self.ram_usage =  psutil.virtual_memory()[2]
            current_time = datetime.now()
            frames_diff = self.rtsp_reader.number_of_frames - self.number_of_frames
            times_diff = (current_time - self.timestamp).total_seconds()
            self.frames_per_second = frames_diff / times_diff
            self.number_of_frames = self.rtsp_reader.number_of_frames
            self.timestamp =  current_time

            stats = {
                "cpu": self.cpu_usage,
                "ram": self.ram_usage,
                "frames": self.frames_per_second
            }

            self.mqtt_manager.publish_message(stats, "metric")

            time.sleep(5)

import psutil
from datetime import datetime
import time
from ..frames.rtsp_reader import RtspReader
from .mqtt import MqttManager
from ..frames.frames_manager import FramesManager            
import pycurl

class MetricCollector:
    def __init__(self, rtsp_reader: RtspReader, mqtt_manager: MqttManager, frames_manager: FramesManager):
        self.rtsp_reader = rtsp_reader
        self.mqtt_manager = mqtt_manager
        self.frames_manager = frames_manager
        self.timestamp = datetime.now()
        self.cpu_usage = None
        self.memory_usage = None
        self.number_of_frames = 0
        self.frames_per_second = None

    def start_collecting_metrics(self):
        while True:
            self.cpu_usage = psutil.cpu_percent(4)
            data = {
                "value": self.cpu_usage,
                "timestamp": datetime.now(),
                "sensor_id": 1,
            }
            self.mqtt_manager.publish_message(data, "S_1")
            self.ram_usage =  psutil.virtual_memory()[2]
            data = {
                "value": self.ram_usage,
                "timestamp": datetime.now(),
                "sensor_id": 2,
            }
            self.mqtt_manager.publish_message(self.ram_usage, "S_2")
            current_time = datetime.now()
            frames_diff = self.rtsp_reader.number_of_frames - self.number_of_frames
            times_diff = (current_time - self.timestamp).total_seconds()
            self.frames_per_second = frames_diff / times_diff
            self.number_of_frames = self.rtsp_reader.number_of_frames
            self.timestamp =  current_time
            data = {
                "value": self.frames_per_second,
                "timestamp": datetime.now(),
                "sensor_id": 3,
            }
            self.mqtt_manager.publish_message(data, "S_3")

            c = pycurl.Curl()

            c.setopt(c.URL, 'rtsp://admin:L279ED32@172.20.10.9:554/cam/realmonitor?channel=1&subtype=0')
            c.setopt(c.NOBODY, 1)
            c.setopt(c.CUSTOMREQUEST, 'HEAD')
            c.perform()

            print('Content-Length:', c.getinfo(c.CONTENT_LENGTH_DOWNLOAD))
            print('Average download speed:', c.getinfo(c.SPEED_DOWNLOAD), 'bytes/sec')

            data = {
                "value": self.frames_manager.objects_detected,
                "timestamp": datetime.now(),
                "sensor_id": 6,
            }
            self.mqtt_manager.publish_message(data, "S_6")
            self.frames_manager.objects_detected = 0

            temp = psutil.sensors_temperatures().get('coretemp')[0].current
            data = {
                "value": temp,
                "timestamp": datetime.now(),
                "sensor_id": 7,
            }
            self.mqtt_manager.publish_message(data, "S_7")

            time.sleep(5)

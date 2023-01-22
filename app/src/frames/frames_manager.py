import threading
from datetime import datetime
from ..utils.types import FrameStrategy
from .frame import FrameInfo
from .yolo import Yolo
from ..utils.logger import logger
from ..utils.mqtt import MqttManager

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


class FramesManager:
    def __init__(self, frame_strategy: FrameStrategy, mqtt_manager: MqttManager):
        self._stored_frames = []
        self._yolo = Yolo(self._stored_frames, self.result_callback)
        self._frame_strategy = frame_strategy
        self.mqtt_manager = mqtt_manager
        self._yolo_thread = threading.Thread(target=self._yolo.run_analyzing, args=())
        self._yolo_thread.start()

    def handle_frame(self, frame):
        time = datetime.now()
        frame_info = FrameInfo(frame=frame, timestamp=time)
        if self._frame_strategy == FrameStrategy.DROP:
            if not self._yolo.is_running():
                self._stored_frames.append(frame_info)
        elif self._frame_strategy == FrameStrategy.STORE:
            self._stored_frames.append(frame_info)


    def result_callback(self, frame_info: FrameInfo, result):
        msg = {
            'timestamp': frame_info.timestamp,
            'detected_objects': generate_detected_objects_info(result)
        }
        self.mqtt_manager.publish_message(msg, "yolo")

    def stop(self):
        if self._yolo_thread:
            self._yolo.stop()
            self._yolo_thread.join()

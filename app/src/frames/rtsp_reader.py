import threading
from datetime import datetime

import cv2

from .frames_manager import FramesManager
from ..utils.logger import logger


class RtspReader:
    def __init__(self, frame_rate_timeout: float, rtsp_url: str, frames_manager: FramesManager) -> None:
        self._capture = None
        self._frame_rate_timeout = frame_rate_timeout
        self._rtsp_url = rtsp_url
        self._frames_manager = frames_manager
        self._capture_thread = None
        self._running = True
        self.number_of_frames = 0
        self.initialize_capture()

    def initialize_capture(self):
        self._capture = cv2.VideoCapture(self._rtsp_url)
        # self.run_capture()
        self._capture_thread = threading.Thread(target=self.run_capture, args=())
        self._capture_thread.start()

    def stop_capture(self):
        if self._capture_thread:
            self._running = False
            self._capture_thread.join()

    def run_capture(self):
        while self._capture.isOpened() and self._running:
            ret, frame = self._capture.read()
            self._frames_manager.handle_frame(frame)

            if ret:
                self.number_of_frames += 1
                t = datetime.now()
                cv2.imwrite(f'./outputs/frame_${t}.jpg', frame)
                # cv2.imshow('frame', frame)
                # time.sleep(self._frame_rate_timeout)
            else:
                self._capture.release()
                logger.warning("Failed to read frames")
                break

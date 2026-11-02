
import base64
import cv2
import numpy as np
from mss import mss
from PIL import Image
import io

class ScreenCapturer:
    def __init__(self):
        self.sct = mss()

    def capture_frame_base64(self) -> str:
        """Captures primary monitor and converts to base64 JPEG string."""
        monitor = self.sct.monitors[1]  # Primary monitor
        sct_img = self.sct.grab(monitor)
        
        # Convert raw MSS image to OpenCV BGR format
        frame = np.array(sct_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        # Resize to maintain high speed without choking local VLM
        height, width, _ = frame.shape
        new_dim = (1024, int(1024 * (height / width)))
        resized = cv2.resize(frame, new_dim, interpolation=cv2.INTER_AREA)

        # Encode frame to JPEG buffer
        _, buffer = cv2.imencode('.jpg', resized, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        return base64.b64encode(buffer).decode('utf-8')
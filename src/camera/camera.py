import cv2
import numpy as np


class Camera:
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480

    def __init__(self) -> None:
        self.device = cv2.VideoCapture(0)

        # set the resolution
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_WIDTH)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_HEIGHT)

    def __del__(self) -> None:
        # release the camera
        self.stop()
        cv2.destroyAllWindows()

    def start(self) -> None:
        self.device.open(0)

    def stop(self) -> None:
        self.device.release()

    def capture(self) -> np.ndarray:
        # read a frame from the camera
        captured, frame = self.device.read()
        if not captured:
            raise Exception("Could not capture a frame from the camera")
        
        return frame
    
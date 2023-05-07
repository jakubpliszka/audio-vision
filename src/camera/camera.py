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
        self.device.release()
        cv2.destroyAllWindows()

    def capture(self) -> np.ndarray:
        # read a frame from the camera
        _, frame = self.device.read()
        return frame

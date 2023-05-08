import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from src.camera import Camera

@pytest.fixture(scope="module")
def camera_instance():
    with patch("cv2.VideoCapture") as mock_video_capture:
        mock_video_capture.return_value.set.return_value = True
        mock_video_capture.return_value.open.return_value = True
        mock_video_capture.return_value.release.return_value = None
        mock_video_capture.return_value.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

        camera = Camera()
        yield camera

def test_start(camera_instance: Camera):
    with patch("cv2.VideoCapture.open") as mock_open:
        mock_open.return_value = True
        camera_instance.start()
        mock_open.assert_called_once_with(0)

def test_stop(camera_instance: Camera):
    with patch("cv2.VideoCapture.release") as mock_release:
        mock_release.return_value = None
        camera_instance.stop()
        mock_release.assert_called_once()

def test_capture(camera_instance: Camera):
    with patch("cv2.VideoCapture.read") as mock_read:
        mock_read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        frame = camera_instance.capture()
        mock_read.assert_called_once()
        assert frame.shape == (480, 640, 3)
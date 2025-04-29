# cam.py

import cv2
import numpy as np
from roboflow import Roboflow
from PIL import Image, ImageTk
import tkinter as tk
import datetime
import threading
import time

class CameraDetection:
    def __init__(self):
        # Initialize Roboflow
        rf = Roboflow(api_key="f4UBb9Y1BqAaVoiasTC1")
        project = rf.workspace("cacaotrain").project("trained-q5iwo")
        self.model = project.version(2).model

        # HSV color thresholds
        self.criollo_lower = np.array([0, 70, 50])
        self.criollo_upper = np.array([10, 255, 255])
        self.forastero_lower = np.array([130, 50, 50])
        self.forastero_upper = np.array([170, 255, 255])
        self.trinitario_lower = np.array([10, 100, 20])
        self.trinitario_upper = np.array([25, 255, 200])
        self.min_match_threshold = 10.0

        # Start camera
        self.cap = cv2.VideoCapture(1)
        time.sleep(0.2)

        # For UI
        self.last_detected_type = "Unknown"

    def detect_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        frame = cv2.resize(frame, (640, 480))

        # Save frame
        cv2.imwrite("frame.jpg", frame)

        # Roboflow prediction
        predictions = self.model.predict("frame.jpg", confidence=40, overlap=30).json()

        best_pred = None
        best_conf = 0

        for pred in predictions['predictions']:
            if pred['confidence'] > best_conf:
                best_pred = pred
                best_conf = pred['confidence']

        if best_pred:
            x, y, w, h = int(best_pred['x']), int(best_pred['y']), int(best_pred['width']), int(best_pred['height'])
            label = best_pred['class']
            confidence = best_pred['confidence']

            x1, y1 = max(x - w // 2, 0), max(y - h // 2, 0)
            x2, y2 = min(x + w // 2, frame.shape[1]), min(y + h // 2, frame.shape[0])

            crop = frame[y1:y2, x1:x2]
            hsv_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

            criollo_mask = cv2.inRange(hsv_crop, self.criollo_lower, self.criollo_upper)
            forastero_mask = cv2.inRange(hsv_crop, self.forastero_lower, self.forastero_upper)
            trinitario_mask = cv2.inRange(hsv_crop, self.trinitario_lower, self.trinitario_upper)

            criollo_ratio = (cv2.countNonZero(criollo_mask) / (crop.size / 3))

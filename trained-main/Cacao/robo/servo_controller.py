# servo_controller.py

import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class ServoController:
    def __init__(self, servo_pin=18):
        self.servo_pin = servo_pin
        GPIO.setup(self.servo_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.servo_pin, 50)  # 50Hz PWM for SG90
        self.pwm.start(7.5)  # Neutral position

        self.lock = threading.Lock()

    def angle_to_duty_cycle(self, angle):
        return 7.5 + (angle / 18.0)

    def set_angle(self, angle):
        duty = self.angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)  # Allow servo to move
        self.pwm.ChangeDutyCycle(0)  # Stop to avoid jitter

    def move_to_variety(self, variety):
        with self.lock:
            if variety == "Criollo":
                print("[Servo] Moving to 0° (Criollo)")
                self.set_angle(0)
                time.sleep(5)
            elif variety == "Forastero":
                print("[Servo] Moving to +90° (Forastero)")
                self.set_angle(90)
                time.sleep(5)
                self.set_angle(0)
            elif variety == "Trinitario":
                print("[Servo] Moving to -90° (Trinitario)")
                self.set_angle(-90)
                time.sleep(5)
                self.set_angle(0)
            else:
                print("[Servo] Unknown variety - no movement.")

    def cleanup(self):

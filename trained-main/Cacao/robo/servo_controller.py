# servo_controller.py

import RPi.GPIO as GPIO
import time
import threading

# Set up GPIO mode and warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class ServoController:
    def __init__(self, servo_pin=18):
        """
        Initializes the servo controller with the specified GPIO pin.
        """
        self.servo_pin = servo_pin
        GPIO.setup(self.servo_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.servo_pin, 50)  # 50Hz PWM for SG90
        self.pwm.start(7.5)  # Neutral position (typically 90 degrees)

        self.lock = threading.Lock()

    def angle_to_duty_cycle(self, angle):
        """
        Converts an angle in degrees to a duty cycle for the servo.
        """
        return 7.5 + (angle / 18.0)

    def set_angle(self, angle):
        """
        Moves the servo to the specified angle.
        """
        duty = self.angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)  # Allow servo time to reach position
        self.pwm.ChangeDutyCycle(0)  # Stop sending signal to reduce jitter

    def move_to_variety(self, variety):
        """
        Moves the servo based on the cacao variety.
        """
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
        """
        Stops the PWM and cleans up GPIO settings.
        """
        print("[Servo] Cleaning up GPIO and stopping PWM.")
        self.pwm.stop()
        GPIO.cleanup()

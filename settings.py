from gpiozero import Servo
from josneslib.devices import (
    MotorL298N, Picamera2Wrapper, 
    PicoI2CMotor, PicoI2CServo,
    Esp32SerialMotor, Esp32SerialServo
)


device_mapping = {
    "Picamera2Wrapper": Picamera2Wrapper,
    
    "Servo": Servo,
    "MotorL298N": MotorL298N,
    "PicoI2CMotor": PicoI2CMotor,
    "PicoI2CServo": PicoI2CServo,
    "Esp32SerialMotor": Esp32SerialMotor,
    "Esp32SerialServo": Esp32SerialServo
}
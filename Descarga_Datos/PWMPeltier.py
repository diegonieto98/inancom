
import RPi.GPIO as GPIO
from time import sleep

PWMpin = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWMpin,GPIO.OUT)
pi_pwm = GPIO.PWM(PWMpin,500)
pi_pwm.start(0)

while True:
    duty=90
    pi_pwm.ChangeDutyCycle(duty)
    sleep(0.01)
    
    

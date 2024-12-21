import RPi.GPIO as GPIO
import time

PIN_REALY_1 = 12
PIN_REALY_2 = 16
PIN_REALY_3 = 20
PIN_REALY_4 = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN_REALY_1, GPIO.OUT)
GPIO.setup(PIN_REALY_2,GPIO.OUT)
GPIO.setup(PIN_REALY_3, GPIO.OUT)
GPIO.setup(PIN_REALY_4, GPIO.OUT)

try:
	while True:
		print("turn on")
		GPIO.output(PIN_REALY_1, GPIO.HIGH)
		GPIO.output(PIN_REALY_2, GPIO.HIGH)
		GPIO.output(PIN_REALY_3, GPIO.HIGH)
		GPIO.output(PIN_REALY_4, GPIO.HIGH)
		
		time.sleep(3)
		
		print("turn off")
		
		GPIO.output(PIN_REALY_1, GPIO.LOW)
		GPIO.output(PIN_REALY_2, GPIO.LOW)
		GPIO.output(PIN_REALY_3, GPIO.LOW)
		GPIO.output(PIN_REALY_4, GPIO.LOW)
		
		time.sleep(3)

except KeyboardInterrupt:
	GPIO.cleanup()

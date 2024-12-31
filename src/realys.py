
import RPi.GPIO as GPIO

# GPIO pin configuration for relays
PIN_RELAY_1 = 12
PIN_RELAY_2 = 16
PIN_RELAY_3 = 20
PIN_RELAY_4 = 21

def init_relays():
    """Initialize GPIO pins for relay control."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_RELAY_1, GPIO.OUT)
    GPIO.setup(PIN_RELAY_2, GPIO.OUT)
    GPIO.setup(PIN_RELAY_3, GPIO.OUT)
    GPIO.setup(PIN_RELAY_4, GPIO.OUT)
    GPIO.output(PIN_RELAY_1, GPIO.LOW)
    GPIO.output(PIN_RELAY_2, GPIO.LOW)
    GPIO.output(PIN_RELAY_3, GPIO.LOW)
    GPIO.output(PIN_RELAY_4, GPIO.LOW)
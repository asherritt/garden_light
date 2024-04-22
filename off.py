from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 190        # Number of LED pixels.
LED_PIN        = 18         # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000     # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10         # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255        # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0          # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def turn_off_leds():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

turn_off_leds()

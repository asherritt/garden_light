from rpi_ws281x import *
from dataclasses import dataclass
import globals

# LED strip configuration
LED_COUNT = 144
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 40
LED_INVERT = False
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_BRGW

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

def set_light(color_list):
    """
    Set the LED strip to the colors in the provided list, cycling through the list
    until all pixels are filled.

    :param color_list: A list of tuples representing RGB or RGBW values.
    """
    num_colors = len(color_list)
    num_pixels = strip.numPixels()

    for i in range(num_pixels):
        # Calculate the index in the color list, cycling through it
        color = color_list[i % num_colors]

        # Unpack the color tuple (supports both RGB and RGBW)
        if len(color) == 3:  # RGB
            r, g, b = color
            w = 0  # Default white channel to 0
        elif len(color) == 4:  # RGBW
            r, g, b, w = color
        else:
            raise ValueError(f"Invalid color tuple: {color}. Must be RGB or RGBW.")

        # Set the color for the current pixel
        strip.setPixelColorRGB(i, r, g, b, w)

    # Update the strip to show the changes
    strip.show()

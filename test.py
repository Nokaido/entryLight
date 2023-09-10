
import time
import neopixel
import board
num_leds = 16*6
data_pin = board.D18 
pixels = neopixel.NeoPixel(data_pin, num_leds, auto_write=False, brightness=1)
pixels.fill((255, 255, 255))
pixels.show()

time.sleep(10)

# Turn off all LEDs
pixels.fill((0, 0, 0))
pixels.show()

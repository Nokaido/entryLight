
import neopixel
import board

from PIL import Image
import serial
from time import sleep
import numpy as np
#from matplotlib.pyplot import imshow

matrixSize_x = 16
matrixSize_y = 48
pixelCount = matrixSize_x * matrixSize_y

# Define the number of LEDs and the pin they are connected to
num_leds = 768
data_pin = board.D18  # Change this to the actual pin you're using

def scale_down_image(image_path, x, y):
    # Open the image
    image = Image.open(image_path)

    # Resize the image to 16x16 pixels
    image = image.resize((x, y))
    #imshow(np.asarray(image))
    # Convert the image to RGB mode
    image = image.convert('RGB')

    # Get the pixel data
    pixels = list(image.getdata())

    # Separate the pixel data into three color matrices
    #for pixel in pixels:
     #   r, g, b = pixel

    return pixels

def wrap_matrix_forward_reverse(matrix, x_dim, y_dim):
    wrapped_array = []

    for row_count in range(y_dim):
        row = matrix[row_count * x_dim:(1+row_count)*x_dim]
        #print(row)
        if row_count % 2 == 1:
            #print(row_count)
            wrapped_array.extend(row)
        else:
            temp = []
            for i in range(len(row)):
               temp.append(row[-(i+1)])
            wrapped_array.extend(temp)
    return wrapped_array

def set_neopixel_array(rgb_values, leds, pin):

    # Initialize the neopixel array
    #pixels = neopixel.NeoPixel(pin, leds)
    pixels = neopixel.NeoPixel(pin, leds, auto_write=False, brightness=0.01)
    pixels.fill((0, 0, 0))
    pixels.show()
    # Set the RGB values for each pixel in the array
    for i in range(leds):
        pixels[i] = rgb_values[i]

    pixels.show()
    sleep(2)

path=[]

path.append("/home/nokaido/workspace/entry_light/res/empty.png")
path.append("/home/nokaido/workspace/entry_light/res/H.png")
path.append("/home/nokaido/workspace/entry_light/res/Ha.png")
path.append("/home/nokaido/workspace/entry_light/res/Hal.png")
path.append("/home/nokaido/workspace/entry_light/res/Hall.png")
path.append("/home/nokaido/workspace/entry_light/res/Hallo.png")

for i in path:

    matrix = scale_down_image(i,matrixSize_x,matrixSize_y)
    matrix = wrap_matrix_forward_reverse(matrix, matrixSize_x, matrixSize_y)
    set_neopixel_array(matrix, num_leds, data_pin)



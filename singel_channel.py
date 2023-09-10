
import os
import time
import neopixel
import board
import cv2
from PIL import Image
import numpy as np
import multiprocessing

panel_count = 9
matrixSize_x = 16
leds_per_panel = 256
matrixSize_y = panel_count*matrixSize_x
pixelCount = matrixSize_x * matrixSize_y


# Define the number of LEDs and the pin they are connected to
num_leds = panel_count*leds_per_panel
data_pin = board.D18  # Change this to the actual pin you're using
video_path = []
video_folder_path = "/home/nokaido/workspace/entry_light/image_show"

def find_mp4_files(folder_path):
    mp4_files = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.mp4'):
            mp4_path = os.path.join(folder_path, filename)
            mp4_files.append(mp4_path)
    #mp4_files = mp4_files.sort()
    return mp4_files

def wrap_matrix_forward_reverse(matrix, x_dim, y_dim):
    wrapped_array = []

    for row_count in range(y_dim):
        row = matrix[row_count * x_dim:(1+row_count)*x_dim]
        if row_count % 2 == 1:
            wrapped_array.extend(row)
        else:
            temp = []
            for i in range(len(row)):
               temp.append(row[-(i+1)])
            wrapped_array.extend(temp)
    return wrapped_array

def set_neopixel_array(rgb_values, leds):

    # Initialize the neopixel array
    pixels = neopixel.NeoPixel(data_pin, leds, auto_write=False, brightness=0.1)
    
    # Set the RGB values for each pixel in the array
    for i in range(leds):
        pixels[i] = rgb_values[i]

    pixels.show()

def crop_middle_slice(frame, x, y):
    frame_height, frame_width, _ = frame.shape

    pixel_size = int(frame_height / y)
    whidth = x * pixel_size

    middle = int(frame_width / 2)
    
    x_start = middle - int(whidth / 2)
    x_end = middle + int(whidth / 2)
    
    y_start = 0
    y_end = frame_height
    
    cropped_slice = frame[y_start:y_end, x_start:x_end]
    return cropped_slice

def process_frames_worker(processed_frame_queue, resize_x, resize_y, video_folder_path):
    video_path = find_mp4_files(video_folder_path)
    for path in video_path:
        cap = cv2.VideoCapture(path)
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                processed_frame = process_frame(frame, resize_x, resize_y)
                processed_frame_queue.put(processed_frame)
        finally:
            print("video {} done!".format(path))
            cap.release()

    processed_frame_queue.put(None)

def process_frame(frame, resize_x, resize_y):
    frame = crop_middle_slice(frame, resize_x, resize_y)

    # Resize the frame
    resized_frame = cv2.resize(frame, (resize_x, resize_y))
    
    # Convert the resized frame to RGB
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Convert the RGB frame to a flat list of RGB values
    rgb_list = rgb_frame.reshape(-1, 3).tolist()
    
    return wrap_matrix_forward_reverse(rgb_list, matrixSize_x, matrixSize_y)

def main():
    processed_frame_queue = multiprocessing.Queue()
    process_process = multiprocessing.Process(target=process_frames_worker, args=(processed_frame_queue, matrixSize_x, matrixSize_y, video_folder_path))


    process_process.start()
    time.sleep(5)
    try:
        while True:
            processed_frame = processed_frame_queue.get()
            if processed_frame is None:
                print("processing done")
                break
            #time.sleep(0.02)
            set_neopixel_array(processed_frame, num_leds)

    finally:
        print("try join after finaly")
        process_process.join()
        print("process_process.join()")
        print("joined after finaly")
        pixels = neopixel.NeoPixel(data_pin, num_leds, auto_write=False, brightness=0.05)
        pixels.fill((0, 0, 0))
        pixels.show()
        

if __name__ == "__main__":
    main()

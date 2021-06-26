import os, imageio, pyvirtualcam
import numpy as np
from pyvirtualcam import PixelFormat

this_dir = os.path.dirname(__file__)
gif_path = os.path.join(this_dir, "kanye.gif")

gif = imageio.get_reader(sample_gif_path)
gif_length = gif.get_length()
gif_height, gif_width = gif.get_data(0).shape[:2]
gif_fps = 1000 / gif.get_meta_data()['duration']

cam_width = 220
cam_height = 122
cam_fmt = PixelFormat.RGBA

gif_x = (cam_width - gif_width) // 2
gif_y = (cam_height - gif_height) // 2

with pyvirtualcam.Camera(cam_width, cam_height, gif_fps, fmt=cam_fmt) as cam:
    print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')

    count = 0
    frame = np.zeros((cam.height, cam.width, 4), np.uint8)
    while True:
        if count == gif_length:
            count = 0
        gif_frame = gif.get_data(count)
        frame[:] = 0
        frame[gif_y:gif_y+gif_height, gif_x:gif_x+gif_width] = gif_frame
        cam.send(frame)
        cam.sleep_until_next_frame()
        
        count += 1
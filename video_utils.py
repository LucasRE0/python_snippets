import os
from glob import glob
from tqdm import tqdm
import numpy as np
import cv2
from PIL import Image


def convert_video_to_mp4(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if not cap.isOpened():
        return

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = input_fps #30
    frame_size = (input_width, input_height)
    video = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    n_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(n_frame):
        ret, frame = cap.read()
        video.write(frame)

    video.release()

    
def convert_video_to_gif(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    resize_width = 800 ### default
    resize_height = int(float(resize_width) * float(input_height) / float(input_width))
    gif_fps = 3 ### default
    duration = 1000 / gif_fps

    img_list = []
    n_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(n_frame):
        ret, frame = cap.read()
        if ret and i % (input_fps / gif_fps) < 1:
            img_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_array = cv2.resize(img_array, (resize_width, resize_height))
            img = Image.fromarray(img_array).quantize(method=0)
            img_list += [img]

    img_list[0].save(output_path, save_all=True, append_images=img_list[1:], loop=0, duration=duration)


def make_mp4(..., output_path):
    frame_width = 640 ### default
    frame_height = 480 ### default
    input_fps = 30 ### default

    frames = [] ### list of frames


    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = input_fps #30
    frame_size = (frame_width, frame_height)
    video = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    for frame in frames:
        video.write(frame)

    video.release()




import os
import cv2
import glob
import imagehash
import time
import numpy as np
from subprocess import call
from PIL import Image

def get_hash_images(im_dir):
    if not os.path.isdir(im_dir):
        raise Exception('{} is not directory!'.format(im_dir))
    im_paths = glob.glob(im_dir + '/*.*', recursive=False)
    hash_im = []
    for path in im_paths:
        im = Image.open(path)
        hash_im.append((path, imagehash.average_hash(im)))
    return hash_im


def get_hash_video(video_dir, num_skip_frame):
    video = cv2.VideoCapture(video_dir)
    
    if not video.isOpened():
        raise Exception('Cant open video {}!'.format(video_dir))
    
    video_len = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) - 1 #last frame usually broken
    
    
    if num_skip_frame > video_len:
        raise Exception('num_skip_frame({}) must less than total frame of video({})!'.format(num_skip_frame, 
                                                                                             video_len))
    
    hash_frame = []
    counter = 0
    
    for i in range(video_len):
        rval, cur_frame = video.read()
        if rval:
            if counter % num_skip_frame == 0:
                hash_frame.append((i, imagehash.average_hash(Image.fromarray(cur_frame))))
            counter += 1

    video.release()
    return hash_frame
    
def save_frame_video(video_dir, frame_id, dest_dir):
    video = cv2.VideoCapture(video_dir)
    
    if not video.isOpened():
        raise Exception('Cant open video {}!'.format(video_dir))
    
    video_len = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) - 1 #last frame usually broken
    
    
    video_name = video_dir.split('/')[-1].split('.')[0]
    for i in range(video_len):
        _, cur_frame = video.read()
        if i in frame_id:
            image = Image.fromarray(cur_frame[:,:,::-1])
            image_name = '{}_{}.png'.format(video_name, i)
            image.save(os.path.join(dest_dir, image_name))
    
def extract_distinct_hashes(hashes, ration_remain):
    if ration_remain > 1 or ration_remain < 0:
        raise Exception('ration_remain must in range [0;1]')
    
    num_remain = ration_remain * len(hashes)
    result = None
    
    max_distant = 64
    for threshold in reversed(range(max_distant + 1)):
        temp_res = [hashes[0]]
        for _hash in hashes:
            distant = max_distant
            for res_item in temp_res:
                distant = min(distant, _hash[1] - res_item[1])
            if distant > threshold:
                temp_res.append(_hash)
        if len(temp_res) >= num_remain:
            result = temp_res
            break
    return [_id for _id, _ in result]
        
    
def extract_distinct_video(video_dir, dest_dir, num_skip_frame = 20, ration_remain = 0.1):
    hashes = get_hash_video(video_dir, num_skip_frame)
    image_id = extract_distinct_hashes(hashes, ration_remain)
    save_frame_video(video_dir, image_id, dest_dir)
    

def extract_distinct_image(image_dir, dest_dir, ration_remain = 0.1):
    hashes = get_hash_images(image_dir)
    image_id = extract_distinct_hashes(hashes, ration_remain)
    for path in image_id:
        image_name = path.split('/')[-1]
        new_path = os.path.join(dest_dir, image_name)
        call(['scp', path, new_path])
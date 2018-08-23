import os
import cv2
import glob
import imagehash
import time
import numpy as np
from subprocess import call
from PIL import Image

'''
compute average hash for images in directory
input: 
    im_dir: images directory
output: list of pairs (im_path, im_average_hash)
'''
def get_hash_images(im_dir):
    if not os.path.isdir(im_dir):
        raise Exception('{} is not directory!'.format(im_dir))
    im_paths = glob.glob(im_dir + '/*.*', recursive=False)
    hash_im = []
    for path in im_paths:
        im = Image.open(path)
        hash_im.append((path, imagehash.average_hash(im)))
    return hash_im

'''
comput average hash for specific frames of video
input: 
    video_dir: video directory
    num_skip_frame: number of skiped frame
output:
    average hash of skiped frame
'''
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
    
    
'''
save specific frame of video
input: 
    video_dir: video directory
    frame_id: id of frame which want to save
    dest_dir: directory to save frame
output:
    None
'''
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
  
'''
extract biggest subset of hash set which minimum distant between 2 hash greater than some threshold
input: 
    hashes: list of hash
    ratio_remain: ratio of remain item after skip frame
output:
    biggest subset of hash set which minimum distant between 2 hash greater than some threshold determine by ratio_remain
'''
def extract_distinct_hashes(hashes, ratio_remain):
    if ratio_remain > 1 or ratio_remain < 0:
        raise Exception('ratio_remain must in range [0;1]')
    
    num_remain = ratio_remain * len(hashes)
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
        
'''
extract distinct frame in video
input:
    video_dir: video directory
    dest_dir: directory to save result
    num_skip_frame: number of skip frame
    ratio_remain: ratio of remain item after skip fame
output:
    distinct frame of video save to dest_dir with name has form {video_name}_{frame_index}.png
'''
def extract_distinct_video(video_dir, dest_dir, num_skip_frame = 20, ratio_remain = 0.1):
    hashes = get_hash_video(video_dir, num_skip_frame)
    image_id = extract_distinct_hashes(hashes, ratio_remain)
    save_frame_video(video_dir, image_id, dest_dir)
    
'''
extract distinct frame in image dir
input:
    image_dir: images directory
    dest_dir: directory to save result
    ratio_remain: ratio of remain item after skip fame
output:
    distinct images copy to dest_dir 
'''
def extract_distinct_image(image_dir, dest_dir, ratio_remain = 0.1):
    hashes = get_hash_images(image_dir)
    image_id = extract_distinct_hashes(hashes, ratio_remain)
    for path in image_id:
        image_name = path.split('/')[-1]
        new_path = os.path.join(dest_dir, image_name)
        call(['scp', path, new_path])
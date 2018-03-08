import os
import sys
import glob
import hashlib
from PIL import Image
from send2trash import send2trash

def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def remove_duplicate_image(dirs, extends = ['jpg', 'png', 'jpeg']):
    #get path of all image
    image_paths = []
    for extend in extends:
        image_paths += glob.glob(dirs + '/**/*.' + extend, recursive=True)
    
    print('Total images:', len(image_paths))
    num_PIL_cant_open = 0
    num_duplicate = 0
    #dictionary to save origin images by hash
    origins = {}
    
    for image_path in image_paths:
        try:
            Image.open(image_path)
        except:
            num_PIL_cant_open += 1
            send2trash(image_path)
            print('PIL cant open: ', image_path)
            print()
            continue
        
        file_hash = hashfile(image_path)
        if file_hash in origins:
            num_duplicate += 1
            print('Move to trash:', image_path)
            print('Duplicate with:', origins[file_hash])
            print()
            send2trash(image_path)
        else:
            origins[file_hash] = image_path
            
    #report
    print()
    print('Total images:', len(image_paths))
    print('Number of images PIL cant open:', num_PIL_cant_open)
    print('Number of images duplicate:', num_duplicate)
    print('Moved to trash:', num_PIL_cant_open + num_duplicate)
    print('Number of images remain:', len(image_paths) - num_PIL_cant_open - num_duplicate)

remove_duplicate_image(sys.argv[1])

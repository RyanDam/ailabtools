import os
import sys
import glob
import magic
import hashlib
from subprocess import call
from PIL import Image
from send2trash import send2trash

def __hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def __change_namge(cur_name, new_name):
    call(['mv', cur_name, new_name])
    print('from', cur_name)
    print('to', new_name)
    print()

#Adjust file's extension
def adj_extension(_dir):
    if not os.path.isdir(_dir):
        raise Exception('{} is not a directory!'.format(_dir))

    #get path of all image
    image_paths = glob.glob(_dir + '/**/*', recursive=True)
    
    num_img = 0
    num_file_is_not_image = 0
    num_img_add_extension = 0
    num_img_change_extension = 0

    for image_path in image_paths:
        if os.path.isdir(image_path):
            continue
        num_img += 1
        file_type = magic.from_file(path, mime=True).split('/')[0]
        if file_type != 'image':
            num_file_is_not_image += 1
            send2trash(image_path)
            print('Sent to trash:', image_path)
            continue

        real_ex = magic.from_file(path, mime=True).split('/')[-1]
        im_name_splited = image_path.split('.')
        
        
        #case: non-extensions
        if len(im_name_splited) == 1:
            num_img_add_extension += 1
            im_name_splited.append(real_ex)
            __change_namge(image_path, '.'.join(im_name_splited))
            
        #case: wrong-extensions
        elif im_name_splited[-1] != real_ex:
            num_img_change_extension += 1
            im_name_splited[-1] = real_ex
            __change_namge(image_path, '.'.join(im_name_splited))

    print('Number of image:', num_img)
    print('Number of file is not image (sent to trash):', num_img_not_in_list_extensions)
    print('Number of file added extension:', num_img_add_extension)
    print('Number of file changed extension:', num_img_change_extension)
    print('Number of images remain:', num_img - num_img_not_in_list_extensions)


#remove duplicate file (bit level)
def rm_duplicate(_dir):
    if not os.path.isdir(_dir):
        raise Exception('{} is not a directory!'.format(_dir))

    #get path of all image
    image_paths = glob.glob(_dir + '/**/*.*', recursive=True)
    
    num_duplicate = 0
    #dictionary to save origin images by hash
    origins = {}
    
    for image_path in image_paths:        
        file_hash = __hashfile(image_path)
        if file_hash in origins:
            num_duplicate += 1
            print('Move to trash:', image_path)
            print('Duplicate with:', origins[file_hash])
            print()
            send2trash(image_path)
        else:
            origins[file_hash] = image_path
            
    #report
    print('Total images:', len(image_paths))
    print('Number of images duplicate:', num_duplicate)
    print('Number of images remain:', len(image_paths) - num_duplicate)

#remove file which PIL can't read
def rm_unreadable(_dir):

    if not os.path.isdir(_dir):
        raise Exception('{} is not a directory!'.format(_dir))

    #get path of all image
    image_paths = glob.glob(_dir + '/**/*.*', recursive=True)
    
    num_PIL_cant_open = 0
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
            
    #report
    print('Total file:', len(image_paths))
    print('Number of file PIL cant open:', num_PIL_cant_open)
    print('Number of images remain:', len(image_paths) - num_PIL_cant_open)
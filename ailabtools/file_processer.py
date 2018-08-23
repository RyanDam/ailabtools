import magic
import hashlib
from subprocess import call
from PIL import Image
from send2trash import send2trash
from multiprocessing import Pool

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
    print('change name file {} to {}'.format(cur_name, new_name))
    
def __adj_extension(path):
    real_ex = magic.from_file(path, mime=True).split('/')[1]
    cur_ex = path.split('.')[-1]
    if cur_ex != real_ex:
        __change_namge(path, '{}.{}'.format(path, real_ex))
        
def adj_extension(paths, num_worker=4):
    """Adjust extension of files
    wrong_name => wrong_name.true_extension

    Parameters
    ----------
    paths : list
        list of path
    num_worker: int
        number of worker

    Returns
    -------
    None
    """
    with Pool(num_worker) as p:
        p.map(__adj_extension, paths)
        
        
def __rm_unreadable(path):
    try:
        Image.open(path)
    except:
        send2trash(path)
        print('remove file: {}'.format(path))
        
def rm_unreadable(paths, num_worker=4):
    """Remove file witch PIL.Image faile to read

    Parameters
    ----------
    paths : list
        list of path
    num_worker: int
        number of worker

    Returns
    -------
    None
    """
    with Pool(num_worker) as p:
        p.map(__rm_unreadable, paths)
        
def rm_duplicate(paths, num_worker=4):
    """Remove duplicate file

    Parameters
    ----------
    paths : list
        list of path
    num_worker: int
        number of worker

    Returns
    -------
    None
    """
    
    with Pool(num_worker) as p:
        hashes = p.map(__hashfile, paths)
        
    filted = {}
    remove_list = []
    for i in range(len(hashes)):
        if hashes[i] not in filted:
            filted[hashes[i]] = paths[i]
        else:
            send2trash(paths[i])
            print('remove file: {}'.format(paths[i]))
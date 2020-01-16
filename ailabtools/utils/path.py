import os

def dir_path(p):
    return os.path.abspath(os.path.join(p, os.pardir))

def makedirs(p):
    os.makedirs(p, exist_ok=True)

def ensure_dir(p):
    makedirs(dir_path(p))
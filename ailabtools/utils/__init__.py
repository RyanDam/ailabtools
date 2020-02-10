from tqdm import tqdm
def tqdm_ailab(*args, **kwargs):
    if hasattr(tqdm, '__instances'): 
        tqdm._instances.clear()
    return tqdm(*args, **kwargs)

def set_gpu_device(device_str):
    import os, sys
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = device_str
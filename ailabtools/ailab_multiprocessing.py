from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
from tqdm import tqdm

def pool_worker(target, inputs, pool_type = 'process', num_worker=None, verbose=True):
    """Run target function in multi-process

    Parameters
    ----------
    target : func
        function to excute multi process
    inputs: list
        list of argument of target function
    num_worker: int
    pool_type: str
        valid value: ['process', 'thread']
        type of pool worker
    number of worker
    verbose: bool
        True: progress bar
        False: silent

    Returns
    -------
    list of output of func
    """
    if pool_type == "process":
        pool_use = Pool
    elif pool_type == "thread":
        pool_use = ThreadPool
    else:
        raise("pool_type varibile only accept value 'process' or 'thread'")
    
    if num_worker is None:
        num_worker = cpu_count()

    if verbose:
        with pool_use(num_worker) as p:
            res = list(tqdm(p.imap(target, inputs), total=len(inputs)))
    else:
        with pool_use(num_worker) as p:
            res = p.map(target, inputs)
    return res
import os
import time
import requests
import multiprocessing
from multiprocessing import Process, Queue, Lock, Value
from glob import glob
import numpy as np
import pandas as pd
from multiprocessing import Process, Queue, Value
import traceback
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class mass_detector:
    def __init__(self, 
                 input_data, 
                 gpu_schedule, 
                 batch_size=1, 
                 num_producer=5, 
                 max_queue_batch_len=10, 
                 num_verbose=1000, 
                 is_tensorflow=False, 
                 show_warning=True):
        self.input_data = input_data
        self.num_input = len(self.input_data)
        self.batch_size = batch_size
        self.gpu_schedule = gpu_schedule
        
        self.num_producer = num_producer
        self.num_consumer = len(self.gpu_schedule)
        
        self.max_queue_batch_len = max_queue_batch_len

        self.data_queue = Queue(self.max_queue_batch_len)
        self.producer_lock = Lock()
        self.counter = Value('i', 0)
        self.producer_done = Value('i', 0)
        self.consumer_done = Value('i', 0)
        
        self.save_queue = Queue(self.max_queue_batch_len)
        
        self.num_verbose = num_verbose
        self.is_tensorflow = is_tensorflow
        self.show_warning = show_warning
        self.last_show_time = time.time()
    #====================================================
    def produce(self):
        while True:
            counter_batch = 0
            items = []
            indexes = []
            current_producer_done = False
            while True:
                #get item index
                with self.producer_lock:
                    index = self.counter.value
                    if index == self.num_input:
                        print('Producer {} done!'.format(self.producer_done.value))
                        self.producer_done.value += 1
                        current_producer_done = True
                        break
                    else:
                        self.counter.value += 1

                if index != 0 and index % self.num_verbose == 0:
                    cur_queue_size = self.data_queue.qsize()
                    print('current index: {} \t current queue size: {}'.format(index, cur_queue_size))
                    
                    if self.show_warning and cur_queue_size < int(0.1 * self.max_queue_batch_len):
                        print("WARNING: current queue size is too low, consumers is faster producers!")
                
                #try get item by index
                try:
                    item = self.get_item(index)
                    indexes.append(index)
                    items.append(item)
                    counter_batch += 1
                except Exception as e:
                    print('producer error:', e)
                    traceback.print_exc()
                    
                #stop when enough batch size
                if counter_batch == self.batch_size:
                    break

            if len(items) > 0:
            
                #items to batch
                batch = self.batch_from_items(items)

                #put batch to queue include indexs to know input
                self.data_queue.put((indexes, batch))
            
            #print('current queue size:', self.data_queue.qsize())
            
            if current_producer_done:
                break
            
    def get_item(self, index):
        raise NotImplementedError
    
    def batch_from_items(self, items):
        raise NotImplementedError
    
    
    #====================================================
    def consum(self, gpu_info):
        gpu_index, capacity = gpu_info
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_index
        
        if self.is_tensorflow:
            import tensorflow as tf
            from keras.backend.tensorflow_backend import set_session
            config = tf.ConfigProto()
            if capacity == 'growth':
                config.gpu_options.allow_growth = True
            else:
                config.gpu_options.per_process_gpu_memory_fraction = capacity
            set_session(tf.Session(config=config))
        print('start load model on GPU: {}'.format(gpu_index))
        model = self.load_model()
        print('load done')
        while True:
            get_batch_success = False
            try:
                indexes, batch = self.data_queue.get(timeout=1)
                get_batch_success = True
            except multiprocessing.queues.Empty:
                if self.producer_done.value == self.num_producer:
                    if gpu_index == "":
                        print('''Consumer use cpu done!''')
                    else:
                        print('''Consumer use gpu {} done!'''.format(gpu_index))
                    self.consumer_done.value += 1
                    break
                else:
                    continue
            except Exception as e:
                print('Unexpected dequeue problem:', e)
                traceback.print_exc()
            
            if get_batch_success:
                try:
                    predictions = self.predict(model, batch)
                    self.save_queue.put((indexes, predictions))
                except Exception as e:
                    print('Consumer error:', e)
                    traceback.print_exc()

    
    def load_model(self):
        raise NotImplementedError
    
    def save_prediction(self, indexs, predictions):
        s ='''Not implement function save_prediction(self, indexs, predictions) error
        function use to save result
        input:
            indexs: index of items in batch
            predictions: result predicted of item corresponding to indexs
        output:
            return prediction
        '''
        print(s)
        raise NotImplementedError
        
    def predict(self, model, batch):
        s ='''Not implement function predict(self, model, batch) error
        function describe how to use model predict batch of input
        input:
            model: model use to predict
            batch: batch of input 
        output:
            return prediction
        '''
        print(s)
        raise NotImplementedError
    
    #=====================================================
    def saver(self):
        while True:
            try:
                indexes, predictions = self.save_queue.get(timeout=1)
                self.save_prediction(indexes, predictions)
            except multiprocessing.queues.Empty:
                if self.consumer_done.value == self.num_consumer:
                    print('Saver done!')
                    break
                else:
                    continue
            except Exception as e:
                print('Saver error:', e)
                traceback.print_exc()
            
    
    #=====================================================
    def run(self):
        ps = []
        #init producer
        for _ in range(self.num_producer):
            p = Process(target=self.produce)
            ps.append(p)
            
        #init consumer
        for gpu_index in self.gpu_schedule:
            p = Process(target=self.consum, args=(gpu_index,))
            ps.append(p)
            
        p = Process(target=self.saver)
        ps.append(p)
        
        # start
        for p in ps:
            p.start()
            
        for p in ps:
            p.join()
            
        self.counter.value = 0
        self.producer_done.value = 0

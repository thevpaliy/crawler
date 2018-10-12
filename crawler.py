import threading
import queue
import time

from _base import Storage
from fetcher import Fetcher
from processor import Processor

fetchers, processors = [], []
storage = Storage(queue.Queue(), queue.Queue())

for index in range(5):
  fetcher = Fetcher(storage)
  processor = Processor(storage)
  fetchers.append(threading.Thread(target=fetcher.run))
  processors.append(threading.Thread(target=processor.run))
  fetchers[-1].start(); processors[-1].start();

storage.put('https://github.com')
time.sleep(10) # TODO: remove

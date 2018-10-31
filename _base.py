import abc
import sys
import threading

class Output(object):
  __slots__ = ('_file', '_lock', '_worker')

  def __init__(self, file=None, lock=None, async=True):
    self._file = file or sys.stdout
    self._lock = lock or threading.Lock() # XXX: RLock maybe?

  def write(self, writer):
    with self._lock:
      if self._file is not sys.stdout:
        with open(self._file, 'a+') as fp:
          writer(fp)
      else:
        writer(self._file)
        self._file.write('\n')


class BaseProcessor(abc.ABC):
  def __init__(self, output, allow_duplicates=True):
    self._output = output
    self._allow_duplicates = allow_duplicates

  def _filter_duplicates(data):
    return data

  @abc.abstractmethod
  def process(self, data):
    pass


class BaseExtractor(abc.ABC):
  def __init__(self, processor):
    self.processor = processor

  @abc.abstractmethod
  def extract(self, data):
    """Extract whatever you need."""

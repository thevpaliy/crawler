import abc

class CrawlingResult(object):
  __slots__ = ('target', 'urls')

  def __init__(self, target, urls):
    self.target = target
    self.urls = urls


class Storage(object):
  __slots__ = ('_ready', '_arrived')

  def __init__(self, ready, arrived):
    self._ready = ready
    self._arrived = arrived

  def fetch(self, timeout=None):
    return self._ready.get(timeout=timeout)

  def get(self, timeout=None):
    return self._arrived.get(timeout=timeout)

  def put(self, data):
    self._ready.put(data)

  def push(self, data):
    if isinstance(data, tuple):
      data = CrawlingResult(*data)
    elif not isinstance(data, CrawlingResult):
      raise TypeError('should be either tuple or CrawlingResult')
    self._arrived.put(data)


class Worker(abc.ABC):
  def __init__(self, storage):
    self._storage = storage
    self._running = False

  @property
  def running(self):
    return self._running

  @running.setter
  def running(self, is_running):
    self._running = is_running

  @abc.abstractmethod
  def run(self, timeout=None):
    """ Perform necessary operations."""

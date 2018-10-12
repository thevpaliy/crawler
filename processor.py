import _base

class Processor(_base.Worker):
  def _save(self, url):
    self._crawled.add(url)

  def run(self, timeout=None):
    storage = self._storage
    self._crawled = set()
    self._running = True
    while self._running:
      result = storage.get(timeout)
      self._save(result.target)
      for url in list(result.urls - self._crawled):
        storage.put(url)

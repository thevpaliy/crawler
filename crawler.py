import requests
import functools
import _base
import threading
import queue
import time

from  extractor import LinkExtractor

class Looper(object):
  def __init__(self, queue, extractors):
    self._queue = queue
    self._extractors = extractors
    self._running = False

  @property
  def running(self):
    if hasattr(self, '_endtime'):
      return self._endtime - time.time() > 0 and self._running
    return self._running

  @running.setter
  def running(self, is_running):
    self._running = is_running

  def run(self, timeout=None):
    self._running = True
    _prepare_url = self._prepare_url
    if timeout is not None:
      if timeout < 0.0:
        raise ValueError('timeout should be > 0')
      self._endtime = time.time() + timeout
    while self.running:
      target_url = _prepare_url(self._queue.get())
      response = requests.get(target_url)
      for extractor in self._extractors:
        extractor.extract((target_url, response.text))
      self._queue.task_done()
    print('-----Finished-------')

  def _prepare_url(self, target_url):
    return target_url # XXX: update this


class Provider(_base.BaseProcessor):
  def __init__(self, queue, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._queue = queue
    self._used_links = set()

  def process(self, data):
    url, links = data
    fresh = set(links) - self._used_links
    self._used_links.update(fresh)
    for link in fresh:
      queue.put(link)
    data = (url, fresh)
    self._output.write(functools.partial(self._save, data))

  @staticmethod
  def _save(data, fp):
    url, links = data
    fp.write('--URL crawled---:' + url + '\n')
    print('URL crawled---:' + url)
    for link in links:
      fp.write('\t' + link + '\n')
      print(link)


queue = queue.Queue()
queue.put('https://github.com')

provider = Provider(queue, _base.Output('links.txt'))
looper = Looper(queue, [LinkExtractor(provider)])
looper.run(timeout=1)

queue.join()

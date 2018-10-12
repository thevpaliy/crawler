import requests
import threading
import queue
import time
import abc
import os
import re

from urllib import parse
from html.parser import HTMLParser


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


class LinkFinder(HTMLParser):
  def __init__(self, url):
    super().__init__()
    self.url = url
    self.links = set()

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      for attr, val in attrs:
        if attr == 'href':
          if not re.compile('https|http').search(val):
            val = parse.urljoin(self.url, val)
          self.links.add(val)


class Fetcher(Worker):
  def _crawl_url(self, url):
    response = self._session.get(url)
    finder = LinkFinder(url)
    finder.feed(response.text)
    return finder.links

  def run(self, timeout=None):
    self._running = True
    while self._running:
      target_url = self._storage.fetch(timeout)
      urls = self._crawl_url(target_url)
      self._storage.push((target_url, urls))


class Processer(Worker):
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


fetchers, processers = [], []

storage = Storage(queue.Queue(), queue.Queue())

for index in range(5):
  fetcher = Fetcher(storage)
  processer = Processer(storage)
  fetchers.append(threading.Thread(target=fetcher.run))
  processers.append(threading.Thread(target=processer.run))
  fetchers[-1].start(); processers[-1].start();

time.sleep(10) # TODO: remove 

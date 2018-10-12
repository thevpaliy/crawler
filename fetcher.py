import requests
import _base

from urllib import parse
from html.parser import HTMLParser

class LinkFinder(HTMLParser):
  def __init__(self, url):
    super().__init__()
    self.url = url
    self.links = set()

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      for attr, val in attrs:
        if attr == 'href':
          if not any((sc in val for sc in ['https','http'])):
            val = parse.urljoin(self.url, val)
          self.links.add(val)


class Fetcher(_base.Worker):
  def _crawl_url(self, url):
    response = requests.get(url)
    finder = LinkFinder(url)
    finder.feed(response.text)
    return finder.links

  def run(self, timeout=None):
    self._running = True
    while self._running:
      target_url = self._storage.fetch(timeout)
      urls = self._crawl_url(target_url)
      self._storage.push((target_url, urls))

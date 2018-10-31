import _base
import re
from urllib import parse

class JSExtractor(_base.BaseExtractor):
  def extract(self, data):
    url, response = data
    matches = re.findall(r'src=[\'"](.*?\.js)["\']', response)
    self.processor.process((url, matches))


class FileExtractor(_base.BaseExtractor):
  def extract(self):
    url, response = data
    matches = re.findall(r'src=[\'"](.*?\.js)["\']', response)
    self.processor.process((url, matches))


class LinkExtractor(_base.BaseExtractor):
  def extract(self, data):
    url, response = data
    matches, res = re.findall(r'<[aA].*href=["\']{0,1}(.*?)["\']', response), []
    for match in matches:
      if not match.startswith('http'):
        if not match.startswith('/'):
          continue
        if not match.startswith('//'):
          match = parse.urljoin(url, match)
      res.append(match)
    self.processor.process((url, res))


class ContactExtractor(_base.BaseExtractor):
    def extract(self, data):
      url, response = data
      matches, res = re.findall(r'<[aA].*?href=[\']{0,1}(.*?)[\'"]', response), []
      for match in matches:
        if not match.startswith('http'):
          if not match.startswith('/'):
            continue
          if not match.startswith('//'):
            match = parse.urljoin(self.url, match)
        res.append(match)
      self.processor.process((url, res))


class RegexExtractor(_base.BaseExtractor):
  def extract(self, data):
    url, response = data
    matches = re.findall(self.regex)
    self.processor.process((url, matches))

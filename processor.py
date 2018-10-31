import _base

class JSProcessor(_base.BaseProcessor):
  def process(self, data):
    data = self._filter_duplicates(data)

class FileProcessor(_base.BaseProcessor):
  def process(self, data):
    data = self._filter_duplicates(data)

class ContextProcessor(_base.BaseProcessor):
  def process(self, data):
    data = self._filter_duplicates(data)

class RegexProcessor(_base.BaseProcessor):
  def process(self, data):
    data = self._filter_duplicates(data)

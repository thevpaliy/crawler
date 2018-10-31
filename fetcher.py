
class ExtractorFactory(object):
  @staticmethod
  def create_js_extractor(**kwargs):
    processor = JSProcessor(**kwargs)
    return JSExtractor(processor)

  @staticmethod
  def create_file_extractor(**kwargs):
    processor = FileProcessor(**kwargs)
    return FileExtractor(processor)

  @staticmethod
  def create_link_extractor(**kwargs):
    pass

  @staticmethod
  def create_contact_extractor(**kwargs):
    processor = ContactProcessor(**kwargs)
    return ContactExtractor(processor)

  @staticmethod
  def create_regex_extractor(**kwargs):
    processor = RegexProcessor(**kwargs)
    return RegexExtractor(processor)

extractors = [ExtractorFactory.create_link_extractor()]
extractors.append(ExtractorFactory.create_link_extractor())
extractors.append(ExtractorFactory.create_link_extractor())
extractors.append(ExtractorFactory.create_link_extractor())
extractors.append(ExtractorFactory.create_link_extractor())

looper = Looper(queue, extractors)
looper.run()

'''
1. Get the args from the user. Otherwise use the default info.
 Seed URL should be provided (could be a bunch of URLs from a file)

2. Provider sends the first URL to the Looper

3. Looper reads the page, sends data to the extractors.

4. Extractors extract information, send everything to the processors

'''

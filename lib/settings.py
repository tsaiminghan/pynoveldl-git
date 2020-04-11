import yaml
import os

class _base(object):
    data = {}

    def __init__(self, filename):
        self.filename = filename
    
    def load(self, filename=None):
      if filename:
        self.filename = filename

      try:
        with open(self.filename, 'r', encoding='utf-8') as f:
          self.data = yaml.safe_load(f)          
      except FileNotFoundError:
        pass
      return self.data

    def dump(self, data, filename=None):
      if filename:
        self.filename = filename
      with open(self.filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


class novelsettings(_base):

  def __init__(self, filename):
    self.load(filename)
    
  def get_by_key(self, key):
    return self.data.get(key)

  @property
  def Downloader(self):
    return self.get_by_key('Downloader')

  @property
  def NovelDownloader(self):
    return self.get_by_key('NovelDownloader')

  @property
  def Website(self):
    return self.get_by_key('Website')

if __name__ == '__main__':
  settings = novelsettings('..\\config\\novelwebsite\\www_b5200_net.yml')

  print (settings.downloader)
  print (settings.noveldownloader)
  print (settings.website)

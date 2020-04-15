import yaml
import os
from .constant import *

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

    def dump(self, data=None, filename=None):
      if filename:
        self.filename = filename
      if not data:
        data = self.data
        
      with open(self.filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


class _settings(object):
  
  def __init__(self, base):
    self.base = base

  def list(self, *argv):
    data = self.base.data
    
    for key in argv:
      data = data[key]
    if isinstance(data, dict):
      for k in sorted(data.keys()):
        print('{}: {}'.format(k, data[k]))
    else:
      print (data)
    
  def put(self, *argv):
    k, v = argv[-2:]
    data = self.base.data
    
    for key in argv[0:-2]:
      data = data[key]
    data[k] = v
    self.base.dump()

  def remove(self, *argv):
    target = argv[-1]
    data = self.base.data
    for key in argv[0:-1]:
      data = data[key]
    del data[target]
    self.base.dump()
   
  def get(self, *argv):
    data = self.base.data
    for key in argv:
      data = data[keys]
    return data   

class _global(_base):
  yamlfile = os.path.join(GLOBALS_YAML)
  def __init__(self):
    super().__init__(self.yamlfile)
    self.load()

  def __getattr__(self, key):
    return self.data.get(key)

  def __setattr__(self, key, value):
    if key == 'data' or key not in self.data:
      super().__setattr__(key, value)
    else:
      self.data[key] = value


class _aozora(_global):
  linesep = '\n'
  yamlfile = os.path.join(AOZORA_YAML)
  def __init__(self):
    super().__init__()
          
  def title(self, text):
    return '{0}{1}{2}{3}{3}'.format(
        self.TITLE_START,
        text,
        self.TITLE_END,
        self.linesep)

  def section(self, text):
    return '{}{}'.format(text, self.linesep)

  def bookinfo(self, **kwargs):
    intro = '{0}{3}website:{3}<a href="{1}">{1}</a>{3}{0}{3}{2}{3}'.format(
        self.SEPARATOR_LINE,
        kwargs['url'],
        self.CHANGE_PAGE,
        self.linesep)
      
    return '{0}{3}{1}{3}{2}{3}'.format(
        kwargs[K_BOOKNAME],
        kwargs[K_AUTHOR],
        intro,
        self.linesep)
     
AOZORA = _aozora()
GLOBAL = _global()

class novelsettings(_base):

  def __init__(self, filename):
    self.load(filename)
    
  def get_by_key(self, key):
    return self.data.get(key)

  @property
  def Downloader(self):
    return self.get_by_key(K_DOWNLOADER)

  @property
  def NovelDownloader(self):
    return self.get_by_key(K_NOVELDOWNLOADER)

  @property
  def Website(self):
    return self.get_by_key(K_WEBSITE)

if __name__ == '__main__':
  settings = novelsettings('..\\config\\novelwebsite\\www_b5200_net.yml')

  print (settings.downloader)
  print (settings.noveldownloader)
  print (settings.website)

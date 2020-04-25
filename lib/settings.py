from .yamlbase import yamlbase
import os
from .constant import *

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

class _global(yamlbase):
  yamlfile = GLOBALS_YAML
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

GLOBAL = _global()

class novelsettings(yamlbase):

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

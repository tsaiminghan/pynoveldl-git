from .yamlbase import yamlbase
from .color_console import MAGENTA
import os, sys
from collections import OrderedDict
from datetime import datetime, timedelta
from .constant import *
from .common import exitfalse
from contextlib import contextmanager

_tfmt = '%Y-%m-%d %H:%M'

class Database(yamlbase):

  @classmethod
  def getDB(cls):
    if not hasattr(cls, 'db'):
      db = cls()
      db.load()
      cls.db = db    
    return cls.db

  @classmethod
  def getItemById(cls, id_):
    return cls.getDB().find_item_by_id(id_)    

  def __init__(self):
    super().__init__(DATABASES_YAML)  

  @staticmethod
  def item(mydl):
    '''
    0:
      id:
      author:
      bookname:
      url:
      last_check:     last check time
      last_update:    last check time that book is updated.
      update_time:    book update time
      chaps:
      dir:
    '''
    return {
      K_AUTHOR: mydl.get_author(),
      K_BOOKNAME: mydl.get_bookname(),
      K_URL: mydl.booklink,
      K_CHAPS: len(mydl.all_chaps),
      K_DIR: mydl.get_book_dir(),
      K_UPTIME: mydl.update_time,
      K_LTCHK: datetime.strftime(datetime.now(), _tfmt),
      K_COVER: getattr(mydl, K_COVER, None)
    }    

  @staticmethod
  def isNew(now, past, hours=6):
    last_update = datetime.strptime(past, _tfmt)
    return (now - last_update) <= timedelta(hours=hours)

  def load(self, filename=DATABASES_YAML):
    data = super().load(filename)
    od = OrderedDict()   
    keys = sorted(data.keys(), key=int)
    for k in keys:
      od[k] = data[k]
    self.data = od

  def dump(self):
    super().dump(dict(self.data))

  def list(self):
    color = MAGENTA()
    print ('{0:^4} | {1:^10} | {2:>5} | {3}'.format('ID', 'DATE', 'CHAPS', 'TITLE'))
    now = datetime.now()
    for v in self.data.values():

      isNew = self.isNew(now, v[K_LTUPTIME])
                      
      print ('{0:>4} | {1:^10} | {2:>5} | {3}'.format(
        v[K_ID],
        v[K_UPTIME].split()[0],
        v[K_CHAPS],
        v[K_BOOKNAME]), end='')
      
      color.start(isNew)      
      if isNew:
        new_chaps = v[K_CHAPS] - v[K_CHAPS_OLD]
        print ('*new({})'.format(new_chaps) if new_chaps>0 else '*new')
      else:
        print ('')
      color.end()

  def show_by_id(self, id_):
      d = self.find_item_by_id(id_)
      if d:
        for k in sorted(d.keys()):
          print(' {0:11} | {1}'.format(k, d[k]))   
      else:
        print ('book not find(id={})'.format(id_))

  def find_key_by_id(self, id):
    for k, v in self.data.items():      
      if v[K_ID] == id:
        return k
      
  def find_item_by_id(self, id_):
    k = self.find_key_by_id(id_)
    return self.data.get(k)

  def find_key_by_url(self, url):
    for k, v in self.data.items():
      if v[K_URL] == url:
        return k
  
  def find_item_by_url(self, url):
    k = self.find_key_by_url(url)
    return self.data.get(k)

  def add(self, d):
    item = self.find_item_by_url(d[K_URL])
    if item:      
      if item[K_CHAPS] != d[K_CHAPS]:
        # new chapters
        d[K_LTUPTIME] = d[K_LTCHK]
        
        now = datetime.now()
        if not self.isNew(now, item[K_LTUPTIME]):
          item[K_CHAPS_OLD] = item[K_CHAPS]
      item.update(d)
    else:
      d[K_ID] = str(len(self.data))
      d[K_LTUPTIME] = d[K_LTCHK]
      d[K_CHAPS_OLD] = d[K_CHAPS]
      self.data[d[K_ID]] = d

  def update(self):
    od = OrderedDict()
    for idx, (k, v) in enumerate(self.data.items()):
      v[K_ID] = str(idx)
      od[v[K_ID]] = v
    self.data = od
    
  def remove_by_id(self, id):
    return self.data.pop(id, None)
    
  def remove(self, d):
    k = self.find_key_by_url(d[K_URL])
    if k:
      self.remove_by_id(k)

@contextmanager
def wrapper(id_):
  d = Database.getItemById(id_)
  exitfalse(d, 'not find book id: {}'.format(id_))
  yield d

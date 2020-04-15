from .settings import _base
from .color_console import MAGENTA
import os
from collections import OrderedDict
from datetime import datetime, timedelta
from .constant import *

_tfmt = '%Y-%m-%d %H:%M'


class Database(_base):

  def getDB():
    if not hasattr(Database, 'db'):
      db = Database()
      db.load()
      Database.db = db    
    return Database.db

  def getItemById(id_):
    return Database.getDB().find_item_by_id(id_)    

  def __init__(self):
    super().__init__(DATABASES_YAML)  

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
  def item(self, mydl):
    return {
    K_AUTHOR: mydl.author,
    K_BOOKNAME: mydl.bookname,
    K_URL: mydl.booklink,
    K_CHAPS: len(mydl.all_chaps),
    K_DIR: mydl.get_book_dir(),
    K_UPTIME: mydl.update_time,
    K_LTCHK: datetime.strftime(datetime.now(), _tfmt)
   }

  def load(self, filename=DATABASES_YAML):
    data = super().load(filename)
    od = OrderedDict()   
    keys = sorted(data.keys(), key=int)
    for k in keys:
      od[k] = data[k]
    self.data = od

  def dump(self):
    d = {}
    d.update(self.data)
    super().dump(d)

  def list(self):
    color = MAGENTA()
    print ('{0:^4} | {1:^10} | {2:>5} | {3}'.format('ID', 'DATE', 'CHAPS', 'TITLE'))
    now = datetime.now()
    for v in self.data.values():

      last_update = datetime.strptime(v[K_LTUPTIME], _tfmt)
      flag_new = (now - last_update) <= timedelta(hours=8)
                      
      print ('{0:>4} | {1:^10} | {2:>5} | {3}'.format(
        v[K_ID],
        v[K_UPTIME].split()[0],
        v[K_CHAPS],
        v[K_BOOKNAME]), end='')
      
      color.start(flag_new)
      print ('*new' if flag_new else '')      
      color.end()

  def show_by_id(self, id_):
      d = self.find_item_by_id(id_)
      if d:
        fmt = ' {0:11} | {1}'
        order_keys = sorted(d.keys())
        for k in order_keys:
          print(fmt.format(k, d[k]))   
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

  def add(self, d):
    k = self.find_key_by_url(d[K_URL])
    if k:
      if self.data[k][K_CHAPS] != d[K_CHAPS]:
        # new chapters
        d[K_LTUPTIME] = d[K_LTCHK]      
      self.data[k].update(d)
    else:
      id_ = str(len(self.data))
      d[K_ID] = id_
      d[K_LTUPTIME] = d[K_LTCHK]
      self.data[id_] = d

  def update(self):
    od = OrderedDict()
    for idx, (k, v) in enumerate(self.data.items()):
      id = str(idx)
      v[K_ID] = id
      od[id] = v
    self.data = od
    
  def remove_by_id(self, id):
    d = self.data.get(id)
    del self.data[id]
    return d

  def remove(self, d):
    k = self.find_key_by_url(d[K_URL])
    if k:
      self.remove_by_id(k)

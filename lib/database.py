from .settings import _base
from .color_console import MAGENTA
import os
from collections import OrderedDict
from datetime import datetime, timedelta

_listdb = os.path.join('config', 'database.yaml')
_tfmt = '%Y-%m-%d %H:%M'


class Database(_base):

  def __init__(self):
    super().__init__(_listdb)

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
    'author': mydl.author,
    'bookname': mydl.bookname,
    'url': mydl.booklink,
    'chaps': len(mydl.all_chaps),
    'dir': mydl.get_book_dir(),
    'update_time': mydl.update_time,
    'last_check': datetime.strftime(datetime.now(), _tfmt)
   }

  def load(self, filename=_listdb):
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
    for v in self.data.values():

      last_check = datetime.strptime(v['last_check'], _tfmt)
      last_update = datetime.strptime(v['last_update'], _tfmt)
      flag_new = (last_check - last_update) <= timedelta(days=1)
                      
      print ('{0:>4} | {1:^10} | {2:>5} | {3}'.format(
        v['id'],
        v['update_time'].split()[0],
        v['chaps'],
        v['bookname']), end='')
      
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
      if v['id'] == id:
        return k
      
  def find_item_by_id(self, id_):
    k = self.find_key_by_id(id_)
    return self.data.get(k)

  def find_key_by_url(self, url):
    for k, v in self.data.items():
      if v['url'] == url:
        return k

  def add(self, d):
    k = self.find_key_by_url(d['url'])
    if k:
      if self.data[k]['chaps'] != d['chaps']:
        # new chapters
        d['last_update'] = d['last_check']      
      self.data[k].update(d)
    else:
      id_ = str(len(self.data))
      d['id'] = id_
      d['last_update'] = d['last_check']
      self.data[id_] = d

  def update(self):
    od = OrderedDict()
    for idx, (k, v) in enumerate(self.data.items()):
      id = str(idx)
      v['id'] = id
      od[id] = v
    self.data = od
    
  def remove_by_id(self, id):
    d = self.data.get(id)
    del self.data[id]
    return d

  def remove(self, d):
    k = self.find_key_by_url(d['url'])
    if k:
      self.remove_by_id(k)

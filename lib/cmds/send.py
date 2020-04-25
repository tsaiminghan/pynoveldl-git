from lib.device import Kindle
from lib.database import Database
from lib.constant import K_DIR
import os

def send(id_):
  '''Usage n send <id>
  copy the mobi to Kindle device.
  e.g.
    n send 0
    n sen 0
'''
  d = Database.getItemById(id_)
  if d:
    path = d[K_DIR]
    name = os.path.basename(path)
    mobi = os.path.join(path, name + '.mobi')
    r = Kindle().push(mobi)
    if r:
      print (r)
  else:
    print ('not find book id', id_)

from lib.device import Kindle
from lib.database import wrapper
from lib.constant import K_DIR
from lib.common import exitfalse
import os

def send(*argv, **kwarg):
  '''Usage n send <id1> [<id2>]...
  copy the mobi to Kindle device.
  e.g.
    n send 0
    n sen 0 1 2'''
  k = Kindle()
  exitfalse(k.exist(), 'not find Kindle device')
  for id_ in argv:    
    with wrapper(id_) as d:
      path = d[K_DIR]
      name = os.path.basename(path)
      mobi = os.path.join(path, name + '.mobi')
      r = k.push(mobi)
      if r:
        print (r)

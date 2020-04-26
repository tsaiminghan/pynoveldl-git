from lib.database import Database
from lib.constant import K_DIR
from shutil import rmtree

def remove(*ids, **kwarg):
  '''Usage: n remove <id1> [<id2>...]
  use the list command to get id of novel.
  and then remove it by id.
  e.g.
    n remove 0
    n r 0 1 2'''
  db = Database.getDB()
  for i in ids:
    d = db.remove_by_id(i)
    if d:
      print ('rmtree {}'.format(d[K_DIR]))
      rmtree(d[K_DIR], ignore_errors=True)
    else:
      print ('unknow id {}'.format(i))
  db.update()
  db.dump()

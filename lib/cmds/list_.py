from lib.database import Database

def list_(id_=None, *argv, **kwarg):
  '''Usage: n list [<id>]
  show the list id of all novels.
    DATE: the last time to check (update_time)
 
  e.g.
    n list
    n l
    
  show information for a special id of novels.
    last_update:  the last time to check
    update_time:  the time of newest chapter
    chaps:        number of chapters
    dir:          download folder
  
  e.g.
    n l 0
  '''
  db = Database.getDB()
  if id_:
    db.show_by_id(id_)
  else:
    db.list()

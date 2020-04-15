import importlib
from .common import url_check
from .database import Database
from .novel_convert import *
from .constant import *

def _select(booklink, **kwargs):

  if booklink.isdigit():
    # this is book id
    db = Database.getDB()
    d = db.find_item_by_id(booklink)    
    booklink = d[K_URL]
    
  url = booklink.split('/')[2]
  mod_name = url.replace('.', '_')
  
  mod = importlib.import_module(NOVELWEBSITE + '.' + mod_name)
  cls_mydl = getattr(mod, 'mydl')
  
  mydl = cls_mydl(url_check(booklink))
  
  # this is for debug, append debug argv to class
  for k, v in kwargs.items():
    setattr(mydl, k , v)
  return mydl

def _download(booklink, **kwargs):
  try:
    mydl = _select(booklink, **kwargs)
  except ImportError as e:
    print (e)
    print ("Please run command 'n support' to check upport website")
    return
  
  mydl.get_chapter_list()
  mydl.dl_all_chapters()
     
  db = Database.getDB()
  d = db.item(mydl)

  raw2text(d)
  raw2aozora(d)
  aozora2epub(d)
  epub2mobi(d)
  
  db.add(d)
  db.dump()

def download(*argv, **kwargs):
  '''Usage: n download <url>|[<id>...]
  use 'n list' to check id of book

  download book by url
  e.g.
    n download http://www.b5200.net/101_101696/
    n d http://www.b5200.net/101_101696/

  <id>
    update the id of books.
    e.g.
      n d 0 1 2
'''
  if len(argv) == 0:
    db = Database.getDB()
    for v in db.data.values():
      _download(v[K_ID], **kwargs)
  else:
    for id_ in argv:
      _download(id_, **kwargs)

def update(*argv, **kwargs):
  '''Usage: n update [<id>...]

    update ids of books
    e.g.
      n update 0
      n u 0 1

    update all of books
    e.g.
      n update
      n u
'''
  download(*argv, **kwargs)

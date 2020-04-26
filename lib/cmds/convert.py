from lib.database import wrapper
from lib.novel_convert import *

def convert(id_, *argv, **kwarg):
  '''Usage: n convert <id> txt|aozora|epub|mobi  
  txt      raw -> txt
  aozora   raw -> aozora txt
  epub     aozora txt -> epub
  mobi     epub -> mobi
  e.g.
    n c 0 t e'''
  with wrapper(id_) as d:  
    if not argv:
      argv ='taem'
  
    for ext in argv:
      if 'txt'.startswith(ext):
        raw2text(d)
      elif 'aozora'.startswith(ext):
        raw2aozora(d)
      elif 'epub'.startswith(ext):
        aozora2epub(d)
      elif 'mobi'.startswith(ext):
        epub2mobi(d)

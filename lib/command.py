import importlib
import sys, os
from bs4 import BeautifulSoup
from shutil import rmtree
from .database import Database
from .common import url_check

class Command(object):
  _options = [ 'download', 'remove', 'list_', 'support', 'test', 'info']
  cmd = 'help_'
  
  def __init__(self, *argv, **kwargs):
    self.argv = argv
    self.kwargs = kwargs
    if len(argv) > 0:
     cmd = argv[0]
     cmds = [ opt for opt in self._options if opt.startswith(cmd)]
  
     if len(cmds) == 1:
       self.cmd = cmds[0]    
    
  def __call__(self):
    return eval(self.cmd)(*self.argv[1:], **self.kwargs)  

def _select(booklink, **kwargs):

  if booklink.isdigit():
    # this is book id
    db = Database()
    db.load()
    d = db.find_item_by_id(booklink)    
    booklink = d['url']
    
  url = booklink.split('/')[2]
  mod_name = url.replace('.', '_')
  
  mod = importlib.import_module('novelwebsite.' + mod_name)
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
  mydl.raw2text()
  
  db = Database()
  db.load()  
  d = db.item(mydl)
  db.add(d)
  db.dump()

def download(*argv, **kwargs):
  '''Usage: n <url>|[<id>...]|all
  use 'n l' to check id of book

  download book by url
  e.g.
    n download http://www.b5200.net/101_101696/
    n d http://www.b5200.net/101_101696/

  <id>
    update the id of books.
    e.g.
      n u 0 1 2

  all
    update all of books
    e.g.
      n u all
      n u a  
'''
  if len(argv) == 1 and argv in ('all', 'a'):
    db = Database()
    db.load()
    for v in db.data.values():
      _download(v['id'], **kwargs)
  else:
    for id_ in argv:
      _download(id_, **kwargs)    
  
def test(*argv):

  if len(argv) == 0:
    download('http://www.b5200.net/101_101696/')
    return
  cmd = argv[0]
  if cmd.startswith('http'):
    from .downloader import Downloader
    #from bs4 import BeautifulSoup
    url = cmd
    dl = Downloader(encoding='gbk', verify=False)
    r = dl.get(url)
    print (r)
    with open('test.txt', 'w', encoding='utf-8') as f:
      f.write(BeautifulSoup(r.text, 'lxml').prettify())
  else:
    Command(*argv, debug_chaps_limit=10)()
    

def info():
  '''setup information.
'''
  print ('''enviroment setup step:
1. install python3, and then setup python and pip enviroemnt path.
2. install below python module.
  pip install PyYAML
  pip install lxml
  pip install BeautifulSoup
  pip install requests
  pip install html2text

my enviroment is:
  Window8
  Python 3.8.2
''')

def support():
  '''Usage: n support
  list support website
'''
  import glob
  _dir = os.path.join('config', 'novelwebsite')
  print ('support website list:')
  for site in glob.glob1(_dir, '*.yaml'):
    print ('  {}'.format(site[0:-5]))

def list_(id_=None):
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
  db = Database()
  db.load()
  if id_:
    db.show_by_id(id_)
  else:
    db.list()

def remove(*ids):
  '''Usage: n remove <id1> [<id2>...]
  use the list command to get id of novel.
  and then remove it by id.
  e.g.
    n remove 0
    n r 0 1 2
  '''
  db = Database()
  db.load()
  for i in ids:
    d = db.remove_by_id(i)
    if d:
      print ('rmtree {}'.format(d['dir']))
      rmtree(d['dir'], ignore_errors=True)
    else:
      print ('unknow id {}'.format(i))
  db.update()
  db.dump()

def help_(cmd='h'):
  cmd = Command(cmd).cmd
  if cmd != help_.__name__:
    print (eval(cmd).__doc__)
  else:
    print('''Usage: n <command> [arguments...]

command:
  download  download books.
  remove    remove download files by id
  list      list information of download books (e.g. id)
  support   list support websites
  info      setup information.
  help      use 'n help <command>' to get command details.
  
  each command could use head of command string to instead of full command
  e.g. n download <url> -> n d <url>
       n list -> l
  ''')

if __name__ == '__main__':
  
  Command(*sys.argv[1:])()


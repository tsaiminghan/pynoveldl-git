import sys, os
from bs4 import BeautifulSoup
from shutil import rmtree
from .database import Database
from .novel_convert import *
from .download import download, update
from .constant import *
from .browser import *

class Command(object):
  _options = [ 'convert', 'download', 'update', 'remove',
               'list_', 'support', 'test', 'init', 'settings',
               'browser', 'folder', 'help_']
  cmd = 'help_'
  def match(cmd, default=None):
    cmds = [ opt for opt in Command._options if opt.startswith(cmd)]
    if len(cmds) == 1:      
      return cmds[0]
    print ('WARN: "{}" need to matche 1 command: {}'.format(cmd, cmds))
    return default
  
  def __init__(self, *argv, **kwargs):
    self.argv = argv
    self.kwargs = kwargs
    if len(argv) > 0:
      cmd = argv[0]
      self.cmd = Command.match(cmd)
    
  def __call__(self):
    if self.cmd:
      return eval(self.cmd)(*self.argv[1:], **self.kwargs)  
  
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
    

def init():
  '''setup information.
'''
  from .settings import GLOBAL
  import subprocess as sp
  from subprocess import DEVNULL
  AozoraEpub3_path = input('The path of AozoraEpub3: ')

  GLOBAL.AozoraEpub3_path = None
  GLOBAL.kindlegen_path = None

  if os.path.exists(os.path.join(AozoraEpub3_path, 'AozoraEpub3.jar')):
    print ('find AozoraEpub3, set it')
    GLOBAL.AozoraEpub3_path = AozoraEpub3_path
    try:
      sp.check_call('java -version', stderr=DEVNULL, stdout=DEVNULL)
    except:
      print ('WARN: AozoraEpub3 need java enviroment')
  
  if os.path.exists(os.path.join(AozoraEpub3_path, 'kindlegen.exe')):
    print ('find kindlegen, set it')
    GLOBAL.kindlegen_path = AozoraEpub3_path    
    
  GLOBAL.dump()
    

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
  db = Database.getDB()
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
  db = Database.getDB()
  for i in ids:
    d = db.remove_by_id(i)
    if d:
      print ('rmtree {}'.format(d[K_DIR]))
      rmtree(d['dir'], ignore_errors=True)
    else:
      print ('unknow id {}'.format(i))
  db.update()
  db.dump()

def convert(id_, *argv):
  '''n convert <id> txt|aozora|epub|mobi
''' 
  d = Database.geItemById(id_)
  if not d:
    print ('not find book id:', id_)
    return
  
  for ext in argv:
    if 'txt'.startswith(ext):
      raw2text(d)
    elif 'aozora'.startswith(ext):
      raw2aozora(d)
    elif 'epub'.startswith(ext):
      aozora2epub(d)
    elif 'mobi'.startswith(ext):
      epub2mobi(d)

def settings(*argv, **kwargs):
  '''Usage: n settings <module> list|put|get|remove [key...] [value]
  chagne the yaml settings. you alos can edit yaml files by notepad..etc.

  <module>
    1. global
    2. database

  list [keys..]
    print the target dict
    e.g.
    n settings database list 0 bookname
    n se d list 0 bookname
    n se g list

  get [keys..]
    return the target dict

  remove [keys..]
    remove the target from dict

  put [key..] value
    add or chagne the dict

    e.g.
    n se database put 0 bookname "this is a book"
'''
  # 1. GLOBAL
  # 2. config\database.yaml
  from .settings import _settings, novelsettings
  import glob
  mod, func = argv[0:2]

  if 'global'.startswith(mod):
    from .settings import GLOBAL as base
    base.load()
  elif 'database'.startswith(mod):
    base = Database.getDB()
  else:
    _dir = CONF_NOVELWEBSITE
    sites = []
    for site in glob.glob1(_dir, '*.yaml'):
      if mod in site:     
         sites.append(site)
    if len(sites) == 1:
      base = novelsettings(os.path.join(_dir, sites[0]))
    else:
      print ('can not find only one yaml:')
      print (*sites, sep='\n')
      return
        
  s = _settings(base)
  getattr(s, func)(*argv[2:])

 
def help_(cmd='h'):
  cmd = Command.match(cmd)
  if cmd != help_.__name__:
    print (eval(cmd).__doc__)
  else:
    print('''Usage: n <command> [arguments...]

command:
  bowser    open the book url.
  download  download books.
  update    currently this is same with download
  remove    remove download files by id
  list      list information of download books (e.g. id)
  support   list support websites
  info      setup information.
  help      use 'n help <command>' to get command details.
  
  each command could use head of command string to instead of full command
  e.g. n download <url> -> n d <url>
       n list -> n l
  ''')

if __name__ == '__main__':
  
  Command(*sys.argv[1:])()


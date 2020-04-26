import sys, os
from .database import Database
from .constant import *
import glob
from .cmds import *
from .common import exitrue

class Command(object):
  _options = [ 'browser',
               'convert',
               'download',
               'folder',
               'help_',
               'init',
               'list_',
               'remove',
               'send', 'setting', 'support',
               'test',
               'update',               
               ]
  cmd = 'help_'
  def match(cmd):
    cmds = [ opt for opt in Command._options if opt.startswith(cmd)]
    exitrue(len(cmds) != 1,
            'WARN: "{}" matches {} command(s): {}'.format(cmd, len(cmds), cmds))
    return cmds[0]
  
  def __init__(self, *argv, **kwargs):
    self.argv = argv
    self.kwargs = kwargs
    if len(argv) > 0:
      cmd = argv[0]
      self.cmd = Command.match(cmd)
    
  def __call__(self):
    if self.cmd:
      return eval(self.cmd)(*self.argv[1:], **self.kwargs)

def test(*argv, **kwargs):  

  if len(argv) == 0:
    download('http://www.b5200.net/101_101696/')
    return
  cmd = argv[0]
  if cmd.startswith('http'):
    from bs4 import BeautifulSoup
    from .downloader import Downloader
    url = cmd
    dl = Downloader(verify=False, **kwargs)
    r = dl.get(url)
    print (r)
    with open('test.txt', 'w', encoding='utf-8') as f:
      f.write(BeautifulSoup(r.text, 'lxml').prettify())
  else:
    Command(*argv, debug_chaps_limit=10, **kwargs)()

def help_(cmd='h'):
  cmd = Command.match(cmd)
  if cmd != help_.__name__:
    print (eval(cmd).__doc__)
  else:
    print('''Usage: n <command> [arguments...]

command:
  browser   open the book url.
  folder    open the book folders
  download  download books.
  update    currently this is same with download
  remove    remove download files by id
  list      list information of books
  support   list support websites
  send      copy books to Kindle device by id
  init      setup enviroment.
  help      use 'n help <command>' to get command details.
  
  each command could use head words of a command to instead of full one.
  e.g. n download <url> -> n d <url>
       n list           -> n l
       n support        -> n su
  ''')

if __name__ == '__main__':
  
  Command(*sys.argv[1:])()


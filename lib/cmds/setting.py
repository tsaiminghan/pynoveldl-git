from lib.database import Database
from lib.settings import _settings, novelsettings
from lib.constant import CONF_NOVELWEBSITE
import os

def setting(*argv, **kwargs):
  '''Usage: n settings <module> list|put|get|remove [key...] [value]
  chagne the yaml settings, or you can edit yaml files by notepad.

  <module>
    1. global
    2. database

  list [keys..]
    print the target dict
    e.g.
    n settings database list 0 bookname
    n se d list 0 bookname

  get [keys..]
    return the target dict

  remove [keys..]
    remove the target from dict

  put [key..] value
    add or chagne the dict
    e.g.
    n se database put 0 bookname "this is a book"'''
  # 1. GLOBAL
  # 2. config\database.yaml  
  
  mod, func = argv[0:2]

  if 'global'.startswith(mod):
    from lib.settings import GLOBAL as base
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

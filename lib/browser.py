import subprocess
import webbrowser
import sys, os
from .database import Database
from .constant import K_URL, K_DIR

def _open_url(url):
  if sys.platform == 'darwin':
    subprocess.Popen(['open', url])
  else:
    webbrowser.open_new_tab(url)

def _open_folder(path):
  abspath = os.path.abspath(path)
  webbrowser.open('file:///' + abspath)

def browser(id_):
  '''n browser <id>
  open the book url.
'''
  d = Database.getItemById(id_)
  if d:
    _open_url(d[K_URL])    
    return
  print ('not find book id:', id_)  

def folder(id_):
  '''n browser <id>
  open the book folder.
'''
  d = Database.getItemById(id_)
  if d:
    _open_folder(d[K_DIR])    
    return
  print ('not find book id:', id_)
  
  

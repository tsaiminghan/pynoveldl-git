import subprocess
import webbrowser
import sys, os
from lib.database import wrapper
from lib.constant import K_URL, K_DIR

def _open_url(url):
  if sys.platform == 'darwin':
    subprocess.Popen(['open', url])
  else:
    webbrowser.open_new_tab(url)

def _open_folder(path):
  abspath = os.path.abspath(path)
  webbrowser.open('file:///' + abspath)

def browser(id_=None, *argv, **kwarg):
  '''n browser <id>
  open the book url.'''
  with wrapper(id_) as d:
    _open_url(d[K_URL])

def folder(id_=None, *argv, **kwarg):
  '''n browser <id>
  open the book folder.'''
  with wrapper(id_) as d:
    _open_folder(d[K_DIR])
  

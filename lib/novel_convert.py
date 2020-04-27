import os
import sys
import re
from .common import timelog
from .constant import *
from .settings import GLOBAL
from types import SimpleNamespace
from subprocess import Popen, PIPE, STDOUT
from shutil import copyfile, move
import tempfile
import glob
from .yamlbase import yamlbase
from .aozora import aozora

def _run_cmd(cmd, stdout=PIPE, stderr=STDOUT, **kwargs):
  #print ('cmd: {}'.format(cmd))
  p = Popen(cmd, stdout=stdout, stderr=stderr, **kwargs)

  while p.poll() is None:
    line = p.stdout.readline().strip()
    if line:
      print(line.decode('utf-8'))
  return p.returncode  

@timelog
def raw2text(novel_dict):
  
  book_dir = novel_dict[K_DIR]
  name = os.path.basename(book_dir) + '.txt'
  textfile = os.path.join(book_dir, name)
  cont_dir = os.path.join(book_dir, CONT)

  with open(textfile, 'w', encoding='utf-8') as fout:
    all_yamls = glob.glob1(cont_dir, '*.yaml')
    
    total = len(all_yamls)
    for idx, yaml in enumerate(all_yamls, start=1):
      print('{}/{}'.format(idx, total), end='\r')

      yaml = os.path.join(cont_dir, yaml)

      d = yamlbase(yaml).load()
      fout.write(d[K_TITLE] + '\n'*2)
      fout.write(d[K_BODY] + '\n'*2)

    print ('')

@timelog
def raw2aozora(novel_dict):           
  
  book_dir = novel_dict[K_DIR]
  name = os.path.basename(book_dir) + '-aozora.txt'
  textfile = os.path.join(book_dir, name)
  cont_dir = os.path.join(book_dir, CONT)  

  with aozora(textfile) as aoz:
    aoz.bookinfo(**novel_dict)
  
    all_yamls = os.listdir(cont_dir)
    total = len(all_yamls)  
    for idx, yaml in enumerate(all_yamls, start=1):
      print('{}/{}'.format(idx, total), end='\r')

      yaml = os.path.join(cont_dir, yaml)
      d = yamlbase(yaml).load()

      if d.get(K_CHAPTER):
        aoz.chapter(d[K_CHAPTER])
      aoz.title(d[K_TITLE])
      lines = d[K_BODY]
      for line in lines.splitlines():
        aoz.paragraph(line.strip())
      aoz.chapter_end()

    print ('')

class _tmp(object):
  def __init__(self, name, suffix):
    _, tmp = tempfile.mkstemp(suffix=suffix)
    os.close(_)
    copyfile(name, tmp)
    self.tmp = tmp
    
  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    os.remove(self.tmp)

  def __str__(self):
    return self.tmp
  
  def __getitem__(self, key):      
    return self.tmp[key]

@timelog
def epub2mobi(novel_dict):
  
  book_dir = novel_dict[K_DIR]
  name = os.path.basename(book_dir) + '.epub'
  epub = os.path.join(book_dir, name)
  
  kindlegen = os.path.join(GLOBAL.kindlegen_path, 'kindlegen.exe')
  cmd = [kindlegen, epub, '-' + GLOBAL.kindlegen_compresslevel]

  _run_cmd(cmd, shell=False)

@timelog
def aozora2epub(novel_dict):
  '''AozoraEpub3 can only use the argument with japenese code page
     so we use _tmp
  '''
  book_dir = novel_dict[K_DIR]
  name = os.path.basename(book_dir) + '-aozora.txt'
  aozoratext = os.path.join(book_dir, name)
  with _tmp(aozoratext, suffix='.txt') as tmp:
    ini = os.path.abspath(os.path.join(CONF, 'AozoraEpub3.ini'))
    
    jar_path = GLOBAL.AozoraEpub3_path
    cmd = 'java -Dfile.encoding=UTF-8 -cp AozoraEpub3.jar AozoraEpub3 -enc UTF-8 -of -i ' + ini
    if GLOBAL.AozoraEpub3_device:
      cmd += ' -device {}'.format(GLOBAL.AozoraEpub3_device)
    if GLOBAL.AozoraEpub3_hor:
      cmd += ' -hor'
    if novel_dict.get(K_COVER):
      cover = _tmp(novel_dict[K_COVER], suffix='.jpg')
      #cover = os.path.abspath(novel_dict.get(K_COVER))
      cmd += ' -c {}'.format(cover)
    cmd += ' "{}"'.format(tmp)
  
    _run_cmd(cmd, cwd=jar_path, shell=True)
    
    move(tmp[0:-4] + '.epub', aozoratext[0:-11] + '.epub')

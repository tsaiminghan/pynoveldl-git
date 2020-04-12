import html2text
import os
import sys
from .common import timelog
from .novel_downloader import _RAW
from .settings import AOZORA, GLOBAL
from types import SimpleNamespace
from subprocess import Popen, PIPE, run
from shutil import copyfile, move
import tempfile

@timelog
def raw2text(novel_dict):
  h = html2text.HTML2Text()
  h.ignore_links = True
  book_dir = novel_dict['dir']
  name = os.path.basename(book_dir) + '.txt'
  textfile = os.path.join(book_dir, name)
  raw_dir = os.path.join(book_dir, _RAW)

  with open(textfile, 'w', encoding='utf-8') as fout:
    all_htmls = [os.path.join(raw_dir, h) for h in os.listdir(raw_dir)]
    total = len(all_htmls)
    for idx, html in enumerate(all_htmls, start=1):
      print('{}/{}'.format(idx, total), end='\r')
      with open(html, 'r', encoding ='utf-8') as fin:
        lines = h.handle(fin.read())
        fout.write(lines)
    print ('')

@timelog
def raw2aozora(novel_dict):           
  h = html2text.HTML2Text()
  h.ignore_links = True

  author = novel_dict['author']
  bookname = novel_dict['bookname']
  book_dir = novel_dict['dir']
  name = os.path.basename(book_dir) + '-aozora.txt'
  textfile = os.path.join(book_dir, name)
  raw_dir = os.path.join(book_dir, _RAW)  

  with open(textfile, 'w', encoding='utf-8') as fout:

    
    fout.write(AOZORA.bookinfo(**novel_dict))
    
    all_htmls = os.listdir(raw_dir)
    total = len(all_htmls)
    for idx, html in enumerate(all_htmls, start=1):
      print('{}/{}'.format(idx, total), end='\r')
      
      title = html[5:-5]
      html = os.path.join(raw_dir, html)
      
      with open(html, 'r', encoding ='utf-8') as fin:
        lines = h.handle(fin.read())
        fout.write(AOZORA.title(title))
        for line in lines.splitlines():
          if len(line) != 0:
            line = AOZORA.section(line)
          fout.write(line)
    print ('')

class _tmp(object):
  ''' Popen could not working on unicode path,
copy them to non-unicode path.
  '''
  def __init__(self, name, suffix):
    _, tmp = tempfile.mkstemp(suffix=suffix)
    os.close(_)
    copyfile(name, tmp)
    self.tmp = tmp

  def __del__(self):
    os.remove(self.tmp)

  def __str__(self):
    return self.tmp
  
  def __getitem__(self, key):      
    return self.tmp[key]

@timelog
def epub2mobi(novel_dict):
  book_dir = novel_dict['dir']
  name = os.path.basename(book_dir) + '.epub'
  epub = os.path.join(book_dir, name)
  tmp = _tmp(epub, suffix='.epub')
    
  kindlegen = os.path.join(GLOBAL.AozoraEpub3_path, 'kindlegen.exe')
  cmd = '{} {} -{}'.format(kindlegen, tmp, GLOBAL.kindlegen_compresslevel)

  print (cmd)
  p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)  
  stdout, stderr = p.communicate('')  
  print((stdout + stderr).decode('utf-8'), end='')
    
  move(tmp[0:-5] + '.mobi', epub[0:-5] + '.mobi')

@timelog
def aozora2epub(novel_dict):
  
  book_dir = novel_dict['dir']
  name = os.path.basename(book_dir) + '-aozora.txt'
  aozoratext = os.path.join(book_dir, name)
  tmp = _tmp(aozoratext, suffix='.txt')
  
  oridir = os.getcwd()
  
  jar_path = GLOBAL.AozoraEpub3_path
  cmd = 'java -Dfile.encoding=UTF-8 -cp AozoraEpub3.jar AozoraEpub3 -of'
  cmd += ' -enc {}'.format(GLOBAL.AozoraEpub3_enc)
  if GLOBAL.AozoraEpub3_device:
    cmd += ' -device {}'.format(GLOBAL.AozoraEpub3_device)
  if GLOBAL.AozoraEpub3_hor:
    cmd += ' -hor'  
  cmd += ' "{}"'.format(tmp)

  print (cmd)
  os.chdir(jar_path)  
  p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)  
  stdout, stderr = p.communicate('')  
  print((stdout + stderr).decode('utf-8'), end='')
  os.chdir(oridir)
  
  move(tmp[0:-4] + '.epub', aozoratext[0:-11] + '.epub')

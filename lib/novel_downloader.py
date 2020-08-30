# -*- coding: utf-8 -*-
from .downloader import Downloader
from .common import timelog
from .yamlbase import yamlbase
from .settings import novelsettings
from bs4 import BeautifulSoup
import os
import time
import re
import multiprocessing
from .opencc.wrapper import OpenCC
from .constant import *
from .settings import GLOBAL
import html2text

if GLOBAL.opencc:
  _convert = OpenCC(GLOBAL.opencc).convert
  
_h = html2text.HTML2Text()
_h.ignore_links = True  

def _pattern(title):
  pattern = '^.*\s*{}\s*\n'
  chars ='()[]'
  for c in chars:
    title = title.replace(c, '\\' + c)
  return pattern.format(title)

def _makedirs(path):
  if not os.path.exists(path):
    os.makedirs(path)  

def _win_save_path(name):
  ''' not allow symbol \/:*?"<>|
  '''
  symbols = {'\\':'＼',
            '/' :'／',
            ':' :'：',
            '*' :'＊',
            '?' :'？',
            '"' :'”',
            '<' :'＜',
            '>' :'＞',
            '|' :'｜',}
  ret = ''
  for c in name:
    ret += symbols.get(c, c)
  return ret
  
def remove_rubi(s):
  return s.replace('》', '※［＃終わり二重山括弧］').replace('《', '※［＃始め二重山括弧］')

class NovelDownloader(object):
  ctl_dl_delay = 0  
  debug_chaps_limit = -1
  pool_num = 1

  def load_settings(self, yamlfile=None):

    if not yamlfile:
      url = self.booklink.split('/')[2]
      yamlfile = os.path.join(CONF_NOVELWEBSITE,
                              url + '.yaml')
    
    s = novelsettings(yamlfile)
    self.downloader = Downloader(**s.Downloader)
    
    for k, v in s.NovelDownloader.items():
      setattr(self, k, v)

    self.dl_path = os.path.join(DATA, s.Website[K_URL])
  
  def __init__(self, **kwargs):
    self.downloader = Downloader(**kwargs) 

  def chapter_list_filter(self, soup):
    ''' need implement
        [ ('title', 'link') , .... ]
    '''
    return []

  def chapter_content_filter(self, soup):
    ''' need implement '''
    return 'na'

  def find_author(self, soup):
    ''' need implement '''
    return 'na'

  def find_update_time(self, soup):
    ''' need implement '''
    return 'na'

  def find_bookname(self, soup):
    ''' need implement '''
    return 'na'

  def dl_cover(self, soup):
    ''' need implement '''
    return ''

  def get_book_folder(self):
    if not hasattr(self, '_book_folder'):
      self._book_folder = '[{}] {}'.format(self.author, self.bookname)
    return self._book_folder

  def get_book_dir(self, extra=[]):
    if not hasattr(self, '_book_dir'):
      folder = self.get_book_folder()
      self._book_dir = os.path.join(self.dl_path, folder)
    return os.path.join(self._book_dir, *extra)

  def set_booklink(self, link):
    self.booklink = link

  def get_booklink(self):
    return self.booklink

  def get_author(self):
    if GLOBAL.opencc:
      return _convert(self.author)
    return self.author

  def get_bookname(self):
    if GLOBAL.opencc:
      return _convert(self.bookname)
    return self.bookname
  
  def get_update_time(self):
    return self.update_time

  @timelog
  def get_chapter_list(self):
    r = self.downloader.get(self.booklink)
    soup = BeautifulSoup(r.text,'lxml')
    self.author = self.find_author(soup)
    self.bookname = self.find_bookname(soup)
    self.all_chaps = self.chapter_list_filter(soup)[0:int(self.debug_chaps_limit)]
    self.update_time = self.find_update_time(soup)
    print (' {0:11} | {1}'.format(K_AUTHOR, self.author))
    print (' {0:11} | {1}'.format(K_BOOKNAME, self.bookname))
    print (' {0:11} | {1}'.format(K_URL, self.booklink))
    print (' {0:11} | {1}'.format(K_UPTIME, self.update_time))
    print (' {0:11} | {1}'.format(K_CHAPS, len(self.all_chaps)))    

  def dl_raw_chapter(self, idx, chap_dict):
    #print ('{} {} {}'.format(idx, title, link))
    title = chap_dict[K_TITLE]
    link = chap_dict[K_URL]
    
    filename = '{0:04} {1}'.format(idx, _win_save_path(title))
    html = self.get_book_dir([RAW, filename + '.html'])
     
    if os.path.exists(html):
      return (True, idx, chap_dict)
    
    time.sleep(self.ctl_dl_delay)
    
    r = self.downloader.get(link)
    if not r:
      #print ('dl fail: {} {} {}'.format(idx, title, link))
      return (False, idx, chap_dict)
    
    soup = BeautifulSoup(r.text,'lxml')
    content = self.chapter_content_filter(soup)
    
    with open(html, 'w', encoding='utf-8') as f:
      f.write(content)
      return (True, idx, chap_dict)
        
    return (False, idx, chap_dict)

  def gen_content(self, idx, chap_dict):
    title = chap_dict[K_TITLE]
    filename = '{0:04} {1}'.format(idx, _win_save_path(title))
    html = self.get_book_dir([RAW, filename + '.html'])
    yaml = self.get_book_dir([CONT, filename + '.yaml'])

    if os.path.exists(yaml):
      return

    with open(html, 'r', encoding='utf-8') as f:
      content = f.read()
      c = _h.handle(content)
      c = re.sub(_pattern(title), '', c, re.S).strip()
      c = remove_rubi(c)
      if GLOBAL.opencc:
        c = _convert(c)
        chap_dict[K_TITLE] = _convert(title)
      d = dict(chap_dict)
      d[K_BODY] = c
      yamlbase(yaml).dump(data=d)
      return True

  @timelog
  def dl_all_chapters(self):
    multiprocessing.freeze_support()  # for windows, RuntimeError
    pool = multiprocessing.Pool(self.pool_num)

    _makedirs(self.get_book_dir([RAW]))
    _makedirs(self.get_book_dir([CONT]))

    result = []
    for idx, chap_dict in enumerate(self.all_chaps, start=1):
      #print ('{} {} {}'.format(idx, title, link))
      res = pool.apply_async(self.dl_raw_chapter, args=(idx, chap_dict))
      result.append(res)
    pool.close()
    #pool.join()
    
    self.h = html2text.HTML2Text()
    self.h.ignore_links = True
    success = 0
    total = len(self.all_chaps)    
    gen_ret = []    
    for idx, r in enumerate(result, start=1):
      ret, idx, chap_dict = r.get()
      success += ret
      gen_ret.append(self.gen_content(idx, chap_dict))      
      print('{}/{}'.format(idx, total), end='\r')
      
    print('{}/{} ok'.format(idx, total))  
    fmt = '{{0:{}}}/{{1}} fail.'.format(len(str(total)))
    print(fmt.format(total-success, total))
    return gen_ret

from .downloader import Downloader
from .common import timelog
from .settings import novelsettings
from bs4 import BeautifulSoup
import os
import time
import multiprocessing
from .constant import *

def _makedirs(path):
  if not os.path.exists(path):
    os.makedirs(path)  

class NovelDownloader(object):
  ctl_append_title_when_dl_chapter = False
  ctl_dl_delay = 0
  debug_chaps_limit = -1
  pool_num = 1
  
  author = 'na'
  bookname = 'na'
  dl_path = '.'

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
    return self.author

  def get_bookname(self):
    return self.bookname
  
  def get_update_time(self):
    return self.update_time

  @timelog
  def get_chapter_list(self):
    r = self.downloader.get(self.booklink)
    soup = BeautifulSoup(r.text,'lxml')
    self.author = self.find_author(soup)
    self.bookname = self.find_bookname(soup)
    self.update_time = self.find_update_time(soup)
    self.all_chaps = self.chapter_list_filter(soup)[0:self.debug_chaps_limit]
    print (' {0:11} | {1}'.format(K_AUTHOR, self.author))
    print (' {0:11} | {1}'.format(K_BOOKNAME, self.bookname))
    print (' {0:11} | {1}'.format(K_URL, self.booklink))
    print (' {0:11} | {1}'.format(K_UPTIME, self.update_time))
    print (' {0:11} | {1}'.format(K_CHAPS, len(self.all_chaps)))    

  def dl_chapter(self, idx, title, link):
    #print ('{} {} {}'.format(idx, title, link))
    
    filename = os.path.join(self.get_book_dir(),
                            RAW, '{0:04} {1}.html'.format(idx, title))
    if os.path.exists(filename):
      return True
    
    time.sleep(self.ctl_dl_delay)
    
    r = self.downloader.get(link)
    if not r:
      #print ('dl fail: {} {} {}'.format(idx, title, link))
      return False
    
    soup = BeautifulSoup(r.text,'lxml')
    content = self.chapter_content_filter(soup)
    
    with open(filename, 'w', encoding='utf-8') as f:
      if self.ctl_append_title_when_dl_chapter:
        f.write(title)        
      f.write(content)
      return True
    
    return False

  @timelog
  def dl_all_chapters(self):
    multiprocessing.freeze_support()  # for windows, RuntimeError
    pool = multiprocessing.Pool(self.pool_num)

    _makedirs(self.get_book_dir([RAW]))

    result = []
    for idx, (title, link) in enumerate(self.all_chaps, start=1):
      #print ('{} {} {}'.format(idx, title, link))
      res = pool.apply_async(self.dl_chapter, args=(idx, title, link))
      result.append(res)      
    pool.close()
    #pool.join()

    success = 0
    total = len(self.all_chaps)
    self.dl_ret = []
    for idx, r in enumerate(result, start=1):
      ret = r.get()
      success += ret
      self.dl_ret.append(ret)
        
      print('{}/{}'.format(idx, total), end='\r')
      
    print('{}/{} ok'.format(idx, total))  
    fmt = '{{0:{}}}/{{1}} fail.'.format(len(str(total)))
    print(fmt.format(total-success, total))


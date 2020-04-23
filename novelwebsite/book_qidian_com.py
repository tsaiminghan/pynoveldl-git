from lib.novel_downloader import NovelDownloader, _makedirs
from bs4 import BeautifulSoup
from lib.common import timelog
from lib.constant import *

class mydl(NovelDownloader):
  chap_url = 'https://read.qidian.com/chapter/'
  cate_url = 'https://book.qidian.com/ajax/book/category'
  ctl_dl_cover = True
    
  def __init__(self, booklink=None):
    self.set_booklink(booklink)
    self.load_settings()

  def chapter_link(self, link):
    return self.chap_url + link
  
  def chapter_list_filter(self, d):
    self.all_chaps = []
    data = d['data']
    vs = data['vs'] #list
    for d in vs:
      chapter = d['vN']
      vip = d['vS']
      if vip:
        # skip vip chapter
        break
      
      for d2 in d['cs']:
        item = {}
        item[K_DATE] = d2['uT']
        item[K_URL] = self.chapter_link(d2['cU'])
        item[K_TITLE] = d2['cN']
        if chapter:
          item[K_CHAPTER] = chapter
          chapter = None
        self.all_chaps.append(item)

    # the time of the last free chapter 
    self.update_time = item[K_DATE]
    return self.all_chaps 

  @timelog
  def get_chapter_list(self):
    r = self.downloader.get(self.booklink)
    cookie = r.cookies.get_dict()
    soup = BeautifulSoup(r.text,'lxml')
    self.author = self.find_author(soup)
    self.bookname = self.find_bookname(soup)
    if self.ctl_dl_cover:
      self.dl_cover(soup)
    
    bookId = self.booklink.split('/')[-2]
    params = dict(cookie)
    params['bookId'] = bookId

    r = self.downloader.get(self.cate_url, params=params)

    self.all_chaps = self.chapter_list_filter(r.json())[0:self.debug_chaps_limit]
    #self.update_time = self.find_update_time(soup)
    print (' {0:11} | {1}'.format(K_AUTHOR, self.author))
    print (' {0:11} | {1}'.format(K_BOOKNAME, self.bookname))
    print (' {0:11} | {1}'.format(K_URL, self.booklink))
    print (' {0:11} | {1}'.format(K_UPTIME, self.update_time))
    print (' {0:11} | {1}'.format(K_CHAPS, len(self.all_chaps)))
    if self.ctl_dl_cover:
      print (' {0:11} | {1}'.format(K_COVER, self.cover))

  def dl_cover(self, soup):
    img_url = 'https:' + soup.find(id='bookImg').find('img').get('src').strip()
    r = self.downloader.get(img_url, stream=True)
    _makedirs(self.get_book_dir([RAW]))
    img = self.get_book_dir([RAW, 'cover.jpg'])
    with open(img, 'wb') as f:
      f.write(r.content)
      self.cover = img

  def chapter_content_filter(self, soup):
    return str(soup.find('div', class_='read-content j_readContent'))

  def find_author(self, soup):        
    return soup.find('h1').find('a').text

  def find_bookname(self, soup):
    return soup.find('h1').find('em').text

  def find_update_time(self, soup):
    # set it during get_chapter_list
    return self.update_time

if __name__ == '__main__':
  a = mydl('https://book.qidian.com/info/1010868264')
  a.get_chapter_list()
  a.dl_all_chapters()

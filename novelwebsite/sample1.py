from lib.novel_downloader import NovelDownloader
from collections import OrderedDict
import os


class mydl(NovelDownloader):
    
  def __init__(self, booklink=None):
    self.set_booklink(booklink)
    self.load_settings()

  def chapter_link(self, link):
    if not link.startswith('http'):
      link = self.booklink + link
    return link
  
  def filter_hrefs(self, href_list):
    all_chaps = href_list.find_all('a')
    odict = OrderedDict()
    for chap in all_chaps:
      link = self.chapter_link(chap['href'])
      
      title = str(chap.string)
      if link in odict:
        del odict[link]
      odict[link] = title

    result = []
    for link, title in odict.items():
      result.append((title, link))

    return result

  def chapter_list_filter(self, soup):
    div_list = soup.find('div', id='list')    
    return self.filter_hrefs(div_list)

  def chapter_content_filter(self, soup):
    return str(soup.find(id='content'))

  def find_author(self, soup):
    return soup.find('meta', property='og:novel:author')['content']    

  def find_bookname(self, soup):
    return soup.find('meta', property='og:novel:book_name')['content']

  def find_update_time(self, soup):
    return soup.find('meta', property='og:novel:update_time')['content']

if __name__ == '__main__':
  a = mydl('http://www.b5200.net/101_101696/')
  a.get_chapter_list()
  a.dl_all_chapters()

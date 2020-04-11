from .sample1 import mydl as base
from collections import OrderedDict
from bs4 import BeautifulSoup
import os

class mydl(base):
  def __init__(self, booklink=None):
    self.set_booklink(booklink)
    self.load_settings()

  def chapter_list_filter(self, soup):
    div_list = soup.find(id='container_bookinfo')
    return self.filter_hrefs(div_list)    

  def find_update_time(self, soup):
    url = soup.find('meta', property='og:url')['content']
    r = self.downloader.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('td', width='27%').text    

if __name__ == '__main__':
  a = mydl('https://www.qiuwu.net/html/449/449302/')
  a.get_chapter_list()
  a.dl_all_chapters()

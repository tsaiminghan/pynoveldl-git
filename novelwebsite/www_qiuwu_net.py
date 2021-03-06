from .sample1 import mydl as base
from collections import OrderedDict
from bs4 import BeautifulSoup
import os
import re

class mydl(base):

  def chapter_list_filter(self, soup):
    div_list = soup.find(id='container_bookinfo')
    return self.filter_hrefs(div_list)    

  def find_update_time(self, soup):
    url = soup.find('meta', property='og:url')['content']
    r = self.downloader.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    s = soup.find('td', width='27%').text
    return re.search('\d{4}-\d{1,2}-\d{1,2}', s).group()

if __name__ == '__main__':
  a = mydl('https://www.qiuwu.net/html/449/449302/')
  a.get_chapter_list()
  a.dl_all_chapters()

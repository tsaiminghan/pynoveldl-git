from lib.novel_downloader import NovelDownloader
from collections import OrderedDict
from bs4 import BeautifulSoup
import os

class mydl(NovelDownloader):
  def __init__(self, booklink):
    '''super().__init__(encoding='gbk', timeout=10)
    self.dl_path = os.path.join('data', 'www.qiuwu.net')'''
    self.set_booklink(booklink)
    self.load_settings()

  def chapter_list_filter(self, soup):
    div_list = soup.find(id='container_bookinfo')
    all_chaps = div_list.find_all('a')

    result = []
    for chap in all_chaps:
      link = chap['href']
      if not link.startswith('http'):
        link = self.booklink + link
      title = str(chap.string)
      result.append((title, link))       
    return result

  def chapter_content_filter(self, soup):
    return str(soup.find(id='content'))

  def find_author(self, soup):
    return soup.find('meta', property='og:novel:author')['content']    

  def find_bookname(self, soup):
    return soup.find('meta', property='og:novel:book_name')['content']

  def find_update_time(self, soup):
    url = soup.find('meta', property='og:url')['content']
    r = self.downloader.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('td', width='27%').text    

if __name__ == '__main__':
  a = mydl('https://www.qiuwu.net/html/449/449302/')
  a.get_chapter_list()
  a.dl_all_chapters()

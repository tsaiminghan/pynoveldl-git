from .sample1 import mydl as base
import re

class mydl(base):

  def find_bookname(self, soup):
    return soup.find('meta', property='og:title')['content']

  def find_update_time(self, soup):
    s = soup.find('div', id='info').text
    return re.search('\d{4}-\d{1,2}-\d{1,2}', s).group()

if __name__ == '__main__':
  a = mydl('http://www.b5200.net/101_101696/')
  a.get_chapter_list()
  a.dl_all_chapters()

from .sample1 import mydl as base
from bs4 import BeautifulSoup
import re

class mydl(base):

  def chapter_list_filter(self, soup):
    dl_list = soup.find('div', class_='centent')
    return self.filter_hrefs(dl_list)

  def find_author(self, soup):    
    return soup.find('meta', attrs={'name':'author'})['content']

  def find_bookname(self, soup):
    url = soup.find('div', id='tl').find_all('a')[1]['href']
    r = self.downloader.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    self.update_time = re.search('\d{4}-\d{1,2}-\d{1,2}', soup.text).group()
    
    return soup.find('h1').text
  
  def find_update_time(self, soup):
    return self.update_time    
  
if __name__ == '__main__':
  a = mydl('https://www.ptwxz.com/html/10/10231/')
  a.get_chapter_list()
  a.dl_all_chapters()

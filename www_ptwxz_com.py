from .sample1 import mydl as base
from bs4 import BeautifulSoup

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

    self.update_time = soup.find_all('td')[8].text[-10:]
    
    return soup.find('h1').text
  
  def find_update_time(self, soup):
    return self.update_time    
  
if __name__ == '__main__':
  a = mydl('https://www.ptwxz.com/html/10/10231/')
  a.get_chapter_list()
  a.dl_all_chapters()

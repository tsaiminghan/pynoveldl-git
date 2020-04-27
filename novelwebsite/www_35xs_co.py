from .sample1 import mydl as base
import re

class mydl(base):
  top_url = 'https://www.35xs.co'

  def chapter_link(self, link):
    return self.top_url + link

  def chapter_list_filter(self, soup):
    dl_list = soup.find('ul', class_='mulu_list')
    return self.filter_hrefs(dl_list)

  def chapter_content_filter(self, soup):
    return str(soup.find(id='chaptercontent'))
  
  def find_update_time(self, soup):
    s = soup.find(class_='bookinfoLastChapter').text
    return re.search('\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}', s).group()
  
if __name__ == '__main__':
  a = mydl('https://www.35xs.co/book/336181/')
  a.get_chapter_list()
  a.dl_all_chapters()

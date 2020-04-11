from .sample1 import mydl as base

class mydl(base):

  def chapter_list_filter(self, soup):
    dl_list = soup.find('dl', class_='book_article_listtext')
    return self.filter_hrefs(dl_list)
  
  def find_update_time(self, soup):
    return soup.find('span', id='updatetime').text
  
if __name__ == '__main__':
  a = mydl('https://www.67shu.net/112/112092/')
  a.get_chapter_list()
  a.dl_all_chapters()

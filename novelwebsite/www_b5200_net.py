from .sample1 import mydl as base

class mydl(base):

  def find_bookname(self, soup):
    return soup.find('meta', property='og:title')['content']

  def find_update_time(self, soup):
    tag = soup.find('div', id='info')
    resultset = tag.find_all('p')    
    return (resultset[-1].text[-10:])

if __name__ == '__main__':
  a = mydl('http://www.b5200.net/101_101696/')
  a.get_chapter_list()
  a.dl_all_chapters()

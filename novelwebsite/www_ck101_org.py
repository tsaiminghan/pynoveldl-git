from .sample1 import mydl as base

class mydl(base):
  top_url = 'https://www.ck101.org/'
  
  def chapter_link(self, link):
    return  self.top_url + link
  
  def chapter_list_filter(self, soup):
    div_list = soup.find('div', class_='novel_list')    
    return self.filter_hrefs(div_list)

  def find_author(self, soup):
    return soup.find('meta', attrs={'name':'og:novel:author'})['content']    

  def find_bookname(self, soup):
    return soup.find('meta', attrs={'name':'og:novel:book_name'})['content']

  def find_update_time(self, soup):
    id_ = self.booklink.split('/')[-2]
    url = self.top_url + '/modules/article/52mb.php?id={}&uptime='.format(id_)
    r = self.downloader.get(url)
    return (r.text.split('"')[1])
    
if __name__ == '__main__':
  a = mydl('https://www.ck101.org/0/367312/')
  a.get_chapter_list()
  a.dl_all_chapters()

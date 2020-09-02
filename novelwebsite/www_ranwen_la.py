from .sample1 import mydl as base

# work at 2020/09/02
class mydl(base):
  def chapter_link(self, link):
    if not link.startswith('http'):
      link = 'https://www.ranwen.la' + link
    return link

if __name__ == '__main__':
  a = mydl('https://www.ranwen.la/files/article/89/89698/')
  a.get_chapter_list()
  a.dl_all_chapters()

from .sample1 import mydl

if __name__ == '__main__':
  a = mydl('https://www.ranwen.la/files/article/89/89698/')
  a.get_chapter_list()
  a.dl_all_chapters()

from .settings import _global
from .constant import *
import os

class aozora(_global):
  linesep = '\n'
  yamlfile = AOZORA_YAML
  def __init__(self, textfile):
    super().__init__()
    self.fout = open(textfile, 'w', encoding='utf-8')

  def __enter__(self):
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.fout:
      self.fout.close()

  def write(self, fmt, *arg, **kwarg):
    self.fout.write(fmt.format(*arg, **kwarg))
    
  def title(self, text):
    self.fout.write('{0}{1}{2}{3}{3}'.format(
        self.H2_START,
        text,
        self.H2_END,
        self.linesep))

  def chapter_end(self):
    self.fout.write(self.CHANGE_PAGE + self.linesep)

  def chapter(self, text):
    self.fout.write('{0}{6}{1}{2}{3}{4}{6}{5}{6}'.format(
        self.HCENTRAL,
        self.SHIFT_3,
        self.H1_START,
        text,
        self.H1_END,
        self.CHANGE_PAGE,
        self.linesep,
        ))

  def paragraph(self, text):
    if text:
      text = '{}{}{}'.format(
        self.INDENT,
        text,
        self.linesep)
    else:
      text = self.linesep
    self.fout.write(text)

  def bookinfo(self, **kwargs):
    intro = '{0}{3}website:{3}<a href="{1}">{1}</a>{3}{0}{3}{2}{3}'.format(
        self.SEPARATOR_LINE,
        kwargs[K_URL],
        self.CHANGE_PAGE,
        self.linesep)
      
    self.fout.write('{0}{3}{1}{3}{2}{3}'.format(
        kwargs[K_BOOKNAME],
        kwargs[K_AUTHOR],
        intro,
        self.linesep))

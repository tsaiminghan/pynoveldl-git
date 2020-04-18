#from hanziconv import HanziConv
import time
import os
  
'''def s2t(string):
  return HanziConv.toTraditional(string)'''

def url_check(url):
  url = url.strip('\'"')  

  if url[-1] != '/':
    url += '/'
    
  return url

def timelog(func):
 def wrapper(*arg):
   try:
     print('[Phase: {}] ----------> Start'.format(func.__name__))
     starttime = time.time()
     return func(*arg)
   finally:
     print('[Phase: {}] ----------> End in {}'.format(
               func.__name__, time.time() - starttime))
 wrapper.__name__ = func.__name__
 return wrapper

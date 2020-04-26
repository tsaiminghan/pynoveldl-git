import time
import sys
  
def exitrue(cond, msg, returncode=-1):
  if cond:
    if msg:
      print (msg)
    sys.exit(returncode)

def exitfalse(cond, msg, returncode=-1):
  exitrue(not cond, msg, returncode)

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

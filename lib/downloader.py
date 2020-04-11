import requests
import time

class Downloader(object):
  retry_time = 3
  retry_delay = 1
  headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
  
  def __init__(self, encoding='gbk', **kwargs):
    
    if not kwargs.get('headers'):
      kwargs['headers'] = self.headers
    
    self.kwargs = kwargs
    self.encoding = encoding

  def get(self, link):
    r = None
    for _ in range(self.retry_time):
      try:
        r = requests.get(link, **self.kwargs)
        r.raise_for_status()
        if r.status_code == 200:
          break
      except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
      except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
      except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
      except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        if r.status_code == 404:
          break
        elif r.status_code == 503:
          time.sleep(self.retry_delay)
          continue
          
      break
      
    if r:  
      r.encoding = self.encoding
    
    return r

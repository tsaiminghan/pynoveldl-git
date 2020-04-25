import glob
from lib.constant import CONF_NOVELWEBSITE

def support(*argv, **kwarg):
  '''Usage: n support
  list support website
'''
  print ('support website list:')
  for site in glob.glob1(CONF_NOVELWEBSITE, '*.yaml'):
    print ('  {}'.format(site[0:-5]))

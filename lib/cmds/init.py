import subprocess as sp
from subprocess import DEVNULL
from lib.settings import GLOBAL  
  
def init(*argv, **kwarg):
  '''Usage: n init <options>
  setup information.
  e.g.
    n init
    n i
    
  options:
    opencc setup opencc
      e.g.
        n init opencc
        n i opencc
'''
  if 'opencc' in argv:
    opencc_conf = {'1':'s2t',
                 '2':'t2s',
                 '3':'s2tw',
                 '4':'tw2s',
                 '5':'s2hk',
                 '6':'hk2s',
                 '7':'s2twp',
                 }
    while True:
      ret = input('''1. s2t,  Simplified Chinese to Traditional Chinese
2. t2s,  Traditional Chinese to Simplified Chinese
3. s2tw, Simplified Chinese to Traditional Chinese (Taiwan Standard)
4. tw2s, Traditional Chinese (Taiwan Standard) to Simplified Chinese
5. s2hk, Simplified Chinese to Traditional Chinese (Hong Kong Standard) 
6. hk2s, Traditional Chinese (Hong Kong Standard) to Simplified Chinese
7. s2twp, s2tw with Taiwanese idiom
8. None, don't use opencc
opencc config, select a number [{}]: '''.format(GLOBAL.opencc))
      if ret in '1234567':
        GLOBAL.opencc = opencc_conf.get(opencc)
        break
    print ('set opencc to {}'.format(GLOBAL.opencc))
    GLOBAL.dump()
    return
  
  AozoraEpub3_path = input('The path of AozoraEpub3: ')

  GLOBAL.AozoraEpub3_path = None
  GLOBAL.kindlegen_path = None

  if os.path.exists(os.path.join(AozoraEpub3_path, 'AozoraEpub3.jar')):
    print ('find AozoraEpub3, set it')
    GLOBAL.AozoraEpub3_path = AozoraEpub3_path
    try:
      sp.check_call('java -version', stderr=DEVNULL, stdout=DEVNULL)
    except:
      print ('WARN: AozoraEpub3 need java enviroment')
  
  if os.path.exists(os.path.join(AozoraEpub3_path, 'kindlegen.exe')):
    print ('find kindlegen, set it')
    GLOBAL.kindlegen_path = AozoraEpub3_path
    ret = input('''''')
    
  GLOBAL.dump()

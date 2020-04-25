import subprocess as sp
from subprocess import DEVNULL
from lib.settings import GLOBAL  
  
def init():
  '''setup information.
'''
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
    
  GLOBAL.dump()

from lib.database import wrapper
from lib.constant import K_DIR
import pathlib
from subprocess import run
from lib.settings import GLOBAL

def push(*argv, **kwarg):
  '''Usage n send <id>
  copy the epub to MTP device.
  e.g.
    n push 0
    
  required: 
    need global settings, mtp_device and mtp_copyto
    mtp_device: 
      the name of MTP device. ex. Pixel 3 XL
    mtp_copyto: 
      the path we copy books to, use the internal storage.
      ex Download\aa\bb'''

  sample = pathlib.Path('lib\cmds\shell\mtptransferSample.ps1')  
  content = sample.read_text()
  ps1 = pathlib.Path('tmp.ps1')
  heads = '''param([string]$deviceName = '{}',
        [System.IO.FileInfo]$copyFrom = '{}',
        [string]$copyTo = '{}')
        '''
  for id_ in argv:    
    with wrapper(id_) as d:
      epub = pathlib.Path(d[K_DIR])      
      epub = epub / epub.name 
      epub = epub.with_suffix('.epub')
      with ps1.open('w', encoding='utf-8') as f:
        f.write(u'\ufeff') # Write window BOM
        f.write(heads.format(
            GLOBAL.mtp_device,
            epub,
            GLOBAL.mtp_copyto,
        ))
        f.write(content)
      cmd = f'powershell -ExecutionPolicy Bypass -file {ps1}'
      r = run(cmd)
      ps1.unlink()

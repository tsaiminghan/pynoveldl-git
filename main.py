from lib.command import Command
import sys

if __name__ == '__main__':
  argv = []
  kwarg = {}
  for a in sys.argv[1:]:
    if '=' in a:
      k, v = a.split('=')
      kwarg[k] = v
    else:
      argv.append(a)
  
  Command(*argv, **kwarg)()

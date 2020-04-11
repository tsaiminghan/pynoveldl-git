from lib.command import Command
import sys

if __name__ == '__main__':  
  Command(*sys.argv[1:])()

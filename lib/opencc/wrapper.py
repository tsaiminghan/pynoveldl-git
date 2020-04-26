from opencc import OpenCC as base
import opencc

class OpenCC(base):
  def __init__(self, conversion=None):
    # make opencc to load local config files
    opencc.opencc.__file__ = __file__
    super().__init__(conversion)

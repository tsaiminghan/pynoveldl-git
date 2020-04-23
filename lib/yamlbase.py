import yaml

class yamlbase(object):
  data = {}
    
  def __init__(self, filename):
    self.filename = filename

  def load(self, filename=None):
    if filename:
      self.filename = filename
    try:
      with open(self.filename, 'r', encoding='utf-8') as f:
        self.data = yaml.safe_load(f)
    except FileNotFoundError:
      pass      
    return self.data

  def dump(self, data=None, filename=None):
    if filename:
      self.filename = filename
    if not data:
      data = self.data
        
    with open(self.filename, 'w', encoding='utf-8') as f:
      yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

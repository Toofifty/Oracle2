"""
Oracle 2.0 Plugin Loader
Created by Alex Matheson

http://toofifty.me/
"""

class Loader(object):
  """
  Plugin Loader class
  
  Finds and imports all allowed modules
  from path/modules. Modules are only allowed
  if they are in config.included or not in
  config.excluded.
  
  <self>.__init__()
    loads modules and stores them in
    self.modules
    
    returns: None
  
  <self>.process_command(input{list})
    finds the command in the aforementioned
    loaded modules and returns it (will
    return True if all is good)
    will return False if the command
    given is not in the loaded modules
    
    returns: Boolean
    
  <self>.get_modules()
    returns a list of loaded modules
    
    returns: modules list
    
  <self>.reload_all()
    iterates through all modules and
    reloads them self.reload(module)
    
    returns: True if all successful
    
  <self>.reload_module(module{module})
    reloads the module with Python's reload()
    method
    
    returns: True if successful
  
  """
  def __init__(self):
    """
    for file in listdir(path/modules):
      if not file in config.excluded 
            or file in config.included:
        self.__import__ file # maybz?
        
        # this should work?
    """
    pass
    
  def process_command(self, input):
    
    # input = {nick, channel, command, *args}
    
    try:
      """
      if self.has_attr('command'):
        return globals.command(self, input)
      """
      pass
    except AttributeException, e:
      return False # Attrib not found
    except Exception:
      raise
    
  def get_modules(self):
    list = []
    
    for mod in self.modules?:
      list.append(mod)
    
    return list
    
  def reload_all(self):
    """
    try:
      for module in self.modules:
        self.reload_module(module)
    except Exception, e:
      raise
    """
    return True
    
  def reload_module(self, module):
    try:
      reload(module)
    except Exception, e:
      return False
    return True
    
if __name__ == "__main__":
  print __doc__

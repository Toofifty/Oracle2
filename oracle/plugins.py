#!/user/bin/evn python
"""
Oracle 2.0 Plugin Loader
Created by Alex Matheson

http://toofifty.me/
"""

import os
import traceback

class Loader(object):
    """
    Plugin Loader class
    
    Finds and imports all allowed modules
    from path/modules. Modules are only allowed
    if they are in config.included or not in
    config.excluded.    
    """
    
    def __init__(self, config):
        """
        Iterates through possible modules to
        load and sends them to load_module()
        
        returns None
        """
        self.modules = []
        print 'Loading modules...'
        for file in os.listdir('../Oracle/modules'):
            if not file in config.excluded or file in config.included:
                if not '.pyc' in file and not '__init__' in file:
                    self.load_module(file.replace('.py', ''))
                    
    def load_module(self, module_name):
        """
        Loads module with string module_name
        
        returns None        
        """
        name = 'modules.%s' % module_name
        module = getattr(__import__(name), module_name)
        
        self.modules.append(module)
        try: module.init()
        except AttributeError: pass
        
    def process_command(self, bot, input):
        """
        Finds the command in the aforementioned
        loaded modules and returns it (will
        return True if all is good).
        Will return False if the command
        given is not in the loaded modules.
        
        returns Boolean
        """
        print 'Command received!'
        
        if input.command == 'init':
            return False
        
        for m in self.modules:
            try:
                if hasattr(m, input.command):
                    exec 'm.' + input.command + '(self, bot, input)'
            except Exception: raise
        return False
            
    def get_modules(self):
        """
        Iterates over loaded modules and 
        adds them to a list
        
        returns List (strings)
        """
        list = []
        for mod in self.modules:
            list.append(mod.__name__)
        return list
        
    def reload_all(self):
        """
        Iterates over all modules and
        sends them to the reload_module()
        function
        
        returns True
        """
        try:
            self.reload_module(mod for mod in self.modules)
        except Exception, e: raise
        return True
        
    def reload_module(self, module):
        """
        Reloads the module given to it
        If there is any exception, returns
        False.
        
        returns Boolean
        """
        try: reload(module)
        except Exception, e:
            return False
        return True
    
if __name__ == "__main__":
    print __doc__

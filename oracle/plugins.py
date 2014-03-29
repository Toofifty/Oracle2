#!/user/bin/evn python
"""
Oracle 2.0 Plugin Loader
Created by Alex Matheson

http://toofifty.me/
"""

import os, sys
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
        return True
        
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
        
        if input.command == 'doc':
            for m in self.modules:
                if input.args[0] == m.__name__:
                    if m.__doc__ is not None:
                        for line in m.__doc__.split('\n'):
                            bot.l_say(line, input, 0)
                    else:
                        bot.msg('No doc found for that module.', input, 0)
                    return True
            else:
                bot.l_say('No doc found for that module. Maybe try modules.%s?'\
                         % input.args[0], input, 0)
                return True
        
        for m in self.modules:
            if hasattr(m, input.command):
                return getattr(m, input.command)(self, bot, input)
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
        
    def reload_all(self, bot, input):
        """
        Iterates over all modules and
        sends them to the reload_module()
        function
        
        returns True
        """
        try:
            for mod in self.modules:
                self.reload_module(mod, bot, input)
        except Exception, e: 
            return False
        return True
    
    def get_module_from_string(self, module_name):
        try:
            return sys.modules[module_name]
        except KeyError:
            raise
        
    def reload_module(self, module, bot, input):
        """
        Reloads the module given to it
        If there is any exception, returns
        False.
        
        returns Boolean
        """
        
        try: 
            reload(module)
            print '\tReloaded', module.__name__
            bot.l_say('Reloaded %s' % module.__name__, input, 0)
        except Exception, e:
            print '\tFailed reloading of', module.__name__
            print '\tError', e
            bot.l_say('Failed to reload %s. Error: %s'\
                       % (module.__name__, e), input, 0)
            return False
        return True
    
if __name__ == "__main__":
    print __doc__

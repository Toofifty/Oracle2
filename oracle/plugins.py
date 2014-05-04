#!/user/bin/evn python
"""
Oracle 2.0 Plugin Loader
Created by Alex Matheson

http://toofifty.me/
"""

import os, sys
import traceback

class Loader:
    """Plugin Loader class
    
    Finds and imports all allowed modules
    from path/modules. Modules are only allowed
    if they are in config.included or not in
    config.excluded.    
    """
    
    def __init__(self, config, bot):
        """Iterates through possible modules to
        load and sends them to load_module()
        
        returns None
        """
        self.modules = []
        print 'Loading modules...'
        path = os.path.join('..', 'oracle', 'modules')
        for file in os.listdir(path):
            if not file in config.excluded or file in config.included:
                if not '.pyc' in file and not '__init__' in file:
                    self.load_module(file.replace('.py', ''), bot)
                    
    def load_module(self, module_name, bot):
        """Loads module with string module_name
        
        returns None        
        """
        name = 'modules.%s' % module_name
        module = getattr(__import__(name), module_name)
        
        self.modules.append(module)
        try: module._init(bot)
        except AttributeError: pass
        return True
        
    def process_command(self, bot, input):
        """Finds the command in the aforementioned
        loaded modules and returns it (will
        return True if all is good).
        Will return False if the command
        given is not in the loaded modules.
        
        returns Boolean
        """
        
        if input.command.startswith('_'):
            return False
        
        input.user.increment_commands()
        
        for m in self.modules:
            if hasattr(m, input.command):
                self.try_command(bot, input, m)
                return
                
        bot.l_say('%s is not recognised as an internal or external command.' \
                  % input.command, input, 0)
        return True
    
    def try_command(self, bot, input, m):
        def fail():
            bot.l_say('Sorry, you do not have the required permissions for'
                      ' this command.', input, 0)
            print 'command failed'
            return
    
        try:
            doc = getattr(m, input.command).__doc__
            
            # Get ranks for sub-commands
            if '!parent-command' in doc:
                try:
                    c_rank = doc.split('!c ' + input.args[0], 1)[1]\
                             .split('!r ', 1)[1].split(' ', 1)[0].lower()
                except:
                    c_rank = 'user'
            # Get ranks for regular commands
            else:
                if '!r' in doc:
                    c_rank = doc.split('!r ', 1)[1].split(' ', 1)[0].lower()
                else: c_rank = 'user'
                        
            c_rank = c_rank.replace('\n','')
                
            # Get user rank (int)
            u_rank = input.user.get_rank()
            
            # Get command rank as int
            c_rank = self.get_rank_from_string(c_rank)

            if not u_rank >= c_rank:
                return fail()
            
            # If return False
            if not getattr(m, input.command)(self, bot, input):
                bot.l_say('Command returned false.', input, 0)
                return
                
        except Exception, e:
            traceback.print_exc()
            bot.l_say('Something went wrong with that command.', input, 0)
            bot.l_say('Please alert an admin about the problem.', input, 0)
            bot.l_say('Error: %s' % e, input, 0)
            return
            
    def get_modules_list(self):
        """Iterates over loaded modules and 
        adds them to a list
        
        returns List (strings)
        """
        list = []
        for mod in self.modules:
            list.append(mod.__name__)
        return list
        
    def get_modules(self):
        """Gets the module list
        
        returns List (modules)
        """
        return self.modules
        
    def reload_all(self, bot, input):
        """Iterates over all modules and
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
            if module_name == 'bot':
                module_name = '__main__'
            return sys.modules[module_name]
        except KeyError:
            raise
        
    def reload_module(self, module, bot, input):
        """Reloads the module given to it
        If there is any exception, returns
        False.
        
        returns Boolean
        """
        
        try: 
            # Easy method for closing threads etc.
            try: module._del(bot)
            except AttributeError: pass
            reload(module)
            print '\tReloaded', module.__name__
            bot.l_say('Reloaded module: %s' % module.__name__, input, 0)
            try: module._init(bot)
            except AttributeError: pass
        except Exception, e:
            print '\tFailed reloading of module:', module.__name__
            print '\tError', e
            bot.l_say('Failed to reload %s. Error: %s'\
                       % (module.__name__, e), input, 0)
            return False
        return True
        
    
    def get_rank_from_string(self, string):
        string = string.lower()
        if string == 'hidden':
            return -1
        if string == 'developer':
            return 4
        if string == 'administrator':
            return 3
        if string == 'moderator':
            return 2
        if string == 'user':
            return 1
        return 0
        
        
    def get_string_from_rank(self, rank):
        if rank == 1:
            return 'user'
        if rank == 2:
            return 'moderator'
        if rank == 3:
            return 'administrator'
        if rank == 4:
            return 'developer'
        if rank == -1:
            return 'hidden'
        return 'none'
        
        
    def event(self, bot, type, args):
        """Executes any methods that match the
        type of event within the modules - allowing
        modules to 'subscribe' to them.
        
        Functions triggered by events:
            _chat (nick, channel, message)
            _command (input)
            _message (nick, message)
            _user_join (nick, channel)
            _user_part (nick, channel)
            _user_nick (nick, new_nick)
            _bot_join (channel)
            _bot_invite (nick, channel)
            _whois_311 (nick, realname, domain)
            _whois_319 (nick, channels)
            _whois_317 (nick, idle_seconds, signon_time)
            _whois_330 (nick, user)
            
        Example:
        
        def _message(b, a):
            nick, channel, message = a
            print '%s from %s said: %s' % (nick, channel, message)
        """
        
        function = '_' + type
        
        for m in self.modules:
            if hasattr(m, function):
                try:
                    getattr(m, function)(bot, args)
                except:
                    traceback.print_exc()
                    print 'Error encountered executing event', type,
                    print 'for module:', m.__name__
    
    
if __name__ == "__main__":
    print __doc__

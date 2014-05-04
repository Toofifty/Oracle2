"""
Oracle 2.0 IRC Bot
help.py plugin module

http://toofifty.me/oracle
"""

import types, inspect
import traceback

from format import WHITE, CYAN, GREY, PURPLE

def _init(bot):
    print '\t%s loaded' % __name__
    
# All commands are called with the arguments
# <module>.<command>(plugins.Loader(), bot.Oracle(), bot.Input())
# In all other plugins, these are abbreviated to l, b, i
def help(loader, bot, input):
    """Welcome to the Oracle guide! Commands are categorised for neatness.
    Use .help [category] to list those commands. Categories:"""
    
    BASE = CYAN
    BRKT = PURPLE
    FILL = GREY
    
    def format_children(func, doc):
        user_rank = input.user.get_rank()
        doc = doc.split('\n')[1:]
        commands = {}
        list = []
        cmd = None
        
        for line in doc:
            line = line.strip(' ')
            
            if line.startswith('!c '):
                cmd = line.replace('!c ', '').upper()
                list.append(cmd)
                commands[cmd] = {}
                
            elif line.startswith('!d '):
                commands[cmd]['desc'] = line.replace('!d ', '').capitalize()
                
            elif line.startswith('!a '):
                commands[cmd]['args'] = line.replace('!a ', '').upper()
                
            elif line.startswith('!r '):
                commands[cmd]['rank'] = line.replace('!r ', '').upper()
                command_rank = commands[cmd]['rank']
                try:
                        
                    if command_rank == 'HIDDEN':
                        list.remove(cmd)
                        continue
                    if user_rank == 'developer':
                        continue
                    if command_rank == 'DEVELOPER':
                        list.remove(cmd)
                    if user_rank == 'administrator':
                        continue
                    if command_rank == 'ADMINISTRATOR':
                        list.remove(cmd)
                    if user_rank == 'moderator':
                        continue
                    if command_rank == 'MODERATOR':
                        list.remove(cmd)
                    if user_rank == 'user':
                        continue
                    if command_rank == 'USER':
                        list.remove(cmd)
                except Exception, e:
                    traceback.print_exc()
                
        for c in sorted(list):
            if commands[c].has_key('args'):
                cmd = '%s %s %s' % (func.__name__.upper(), c, commands[c]['args'])
            else:
                cmd = '%s %s' % (func.__name__.upper(), c)
                
            return_command(cmd, commands[c]['desc'], commands[c]['rank'])
    
    def formatdoc(func):
        user_rank = input.user.get_rank()
        doc = inspect.getdoc(func)
        command_rank = ''
        args = rank = None
        desc = doc
        
        if doc is not None:
            if '!parent-command' in doc.split('\n')[0]:
                print 'Formatting children...'
                format_children(func, doc)
                return
                
            for line in doc.split('\n'):
                if line.startswith('!d '):
                    desc = line.replace('!d ', '').capitalize()
                    
                elif line.startswith('!a '):
                    args = line.replace('!a ', '').upper()
                    
                elif line.startswith('!r '):
                    command_rank = line.replace('!r ', '').upper()
                    try:
                        if command_rank == 'HIDDEN':
                            return
                        if user_rank == 'developer':
                            continue
                        if command_rank == 'DEVELOPER':
                            return
                        if user_rank == 'administrator':
                            continue
                        if command_rank == 'ADMINISTRATOR':
                            return
                        if user_rank == 'moderator':
                            continue
                        if command_rank == 'MODERATOR':
                            return
                        if user_rank == 'user':
                            continue
                        if command_rank == 'USER':
                            return
                    except Exception, e:
                        traceback.print_exc()                 
                    
        if args is None:
            cmd = func.__name__.upper()
        else:
            cmd = '%s %s' % (func.__name__.upper(), args)
        
        return_command(cmd, desc, command_rank)
    
    def return_command(cmd, desc, rank):
        if cmd is None: return
        if desc is None: desc = ''
    
        if input.game == '':
            cmd = cmd.ljust(25)
            cmd = cmd.replace('<',BRKT+'<'+FILL).replace('>',BRKT+'>'+BASE)
            cmd = cmd.replace('[',BRKT+'['+FILL).replace(']',BRKT+']'+BASE)
            cmd = cmd.replace('...',BRKT+'...'+BASE)
            
            str = '%s - %s' % (BASE + cmd, FILL + desc)
        else:
            cmd = cmd.replace('<',BRKT+'<'+FILL).replace('>',BRKT+'>'+BASE)
            cmd = cmd.replace('[',BRKT+'['+FILL).replace(']',BRKT+']'+BASE)
            cmd = cmd.replace('...',BRKT+'...'+BASE)
            str = '%s - %s' % (BASE + cmd, FILL + desc)
    
        return bot.l_say(str, input, 0)
    
    def get_categories(input):
        rank = input.user.get_rank()
        if rank == 'developer':
            return 'Emotes - Server - Personal - Other - Moderator - Admin - Dev'
        elif rank == 'administrator':
            return 'Emotes - Server - Personal - Other - Moderator - Admin'
        elif rank == 'moderator':
            return 'Emotes - Server - Personal - Other - Moderator'
        elif rank == 'user':
            return 'Emotes - Server - Personal - Other'
        else:
            return 'Sorry! No categories found!'
    
    try:
        # Grab the module from the laoded modules
        # This will throw a KeyError if no module is found,
        # and so it will print the default help message
        mod = loader.get_module_from_string('modules.%s' % input.args[0])
        func_list = [getattr(mod, a, None) for a in dir(mod)
                     if isinstance(getattr(mod, a, None), 
                                   types.FunctionType)]
        for func in func_list:
            if not func.__name__.startswith('_'):
                formatdoc(func)
        return True
    
    except (KeyError, TypeError):
        # Try to see if the query is a function of its
        # own, and not a module
        if input.args is not None:
            for m in loader.get_modules_list():
                m = loader.get_module_from_string(m)
                if hasattr(m, input.args[0]):
                    func = getattr(m, input.args[0])
                    formatdoc(func)
                    return True
        
        # Can't find the query anywhere, so we'll
        # print the default help message
        for line in inspect.getdoc(help).split('\n'):
            bot.l_say(line, input, 0)
        # Categories. Need an algorithm to get these
        bot.l_say(get_categories(input), input, 0)
        return True
        
    except:
        traceback.print_exc()
    
def version(l, b, i):
    """
    !d Get the version of Oracle
    !r user
    """
    return b.l_say('Oracle Version %s' % b.get_version(), i, 0)
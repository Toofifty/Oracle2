"""
Oracle 2.0 IRC Bot
help.py plugin module

http://toofifty.me/oracle
"""

import types, inspect
import traceback

def init():
    print '\t%s loaded' % __name__
    
# All commands are called with the arguments
# <module>.<command>(plugins.Loader(), bot.Oracle(), bot.Input())
# In all other plugins, these are abbreviated to l, b, i
def help(loader, bot, input):
    """Welcome to the Oracle guide! Commands are categorised for neatness.
    Use .help [category] to list those commands. Categories:"""
    
    def format_children(func, doc):
        print 'Formatting children functions'
        doc = doc.split('\n')[1:]
        print doc
        commands = {}
        list = []
        cmd = None
        for line in doc:
            line = line.strip(' ')
            print line
            print 'CMD', cmd
            if line.startswith('!c '):
                print 'Starts with !c'
                cmd = line.replace('!c ', '').upper()
                print cmd
                list.append(cmd)
                commands[cmd] = {}
                print 'Name =', cmd
            elif line.startswith('!d '):
                print 'Starts with !d'
                print 'Desc of', cmd, '=', line.replace('!d ', '').capitalize()
                commands[cmd]['desc'] = line.replace('!d ', '').capitalize()
            elif line.startswith('!a '):
                commands[cmd]['args'] = line.replace('!a ', '').upper()
            elif line.startswith('!r '):
                commands[cmd]['rank'] = line.replace('!r ', '').upper()
        print commands
        for c in sorted(list):
            print c
            if commands[c].has_key('args'):
                cmd = '%s %s %s' % (func.__name__.upper(), c, commands[c]['args'])
            else:
                cmd = '%s %s' % (func.__name__.upper(), c)
                
            return_command(cmd, commands[c]['desc'], commands[c]['rank'])
    
    def formatdoc(func):
        doc = inspect.getdoc(func)
        args = rank = None
        desc = doc
        
        if doc is not None:
            if '!parent-command' in doc.split('\n')[0]:
                format_children(func, doc)
                return
            for line in doc.split('\n'):
                if line.startswith('!d '):
                    desc = line.replace('!d ', '').capitalize()
                elif line.startswith('!a '):
                    args = line.replace('!a ', '').upper()
                elif line.startswith('!r '):
                    rank = line.replace('!r ', '').upper()                    
                    
        if args is None:
            cmd = func.__name__.upper()
        else:
            cmd = '%s %s' % (func.__name__.upper(), args)
        
        return_command(cmd, desc, rank)
    
    def return_command(cmd, desc, rank):
        return bot.l_say('%s - %s' % (cmd.ljust(25), desc), input, 0)
    
    def get_categories(input):
        return 'none'
    
    try:
        # Grab the module from the laoded modules
        # This will throw a KeyError if no module is found,
        # and so it will print the default help message
        mod = loader.get_module_from_string('modules.%s' % input.args[0])
        func_list = [getattr(mod, a, None) for a in dir(mod)
                     if isinstance(getattr(mod, a, None), 
                                   types.FunctionType)]
        for func in func_list:
            if func.__name__ != 'init':
                formatdoc(func)
        return True
    
    except (KeyError, TypeError):
        # Try to see if the query is a function of its
        # own, and not a module
        if input.args is not None:
            for m in loader.get_modules():
                m = loader.get_module_from_string(m)
                if hasattr(m, input.args[0]):
                    func = getattr(m, input.args[0])
                    formatdoc(func)
                    return True
        
        # Can't find the query anywhere, so we'll
        # print the default help message
        print 'Printing help list...'
        for line in inspect.getdoc(help).split('\n'):
            bot.l_say(line, input, 0)
        # Categories. Need an algorithm to get these
        bot.l_say(get_categories(input), input, 0)
        return True
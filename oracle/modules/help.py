"""
Oracle 2.0 IRC Bot
help.py plugin module

http://toofifty.me/oracle
"""

import types, inspect

def init():
    print '\t%s loaded' % __name__
    
def help(l, bot, input):
    """Welcome to the Oracle guide! Commands are categorised for neatness.
    Use .help [category] to list those commands. Categories:"""
    
    def formatdoc(func):
        doc = inspect.getdoc(func)
        args = rank = None
        desc = doc
        
        if doc is not None:
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
        
        return '%s - %s' % (cmd.ljust(20), desc)
    
    def get_categories(input):
        return 'none'
    
    try:
        # Grab the module from the laoded modules
        # This will throw a KeyError if no module is found,
        # and so it will print the default help message
        mod = l.get_module_from_string('modules.%s' % input.args[0])
        func_list = [getattr(mod, a, None) for a in dir(mod)
                     if isinstance(getattr(mod, a, None), 
                                   types.FunctionType)]
        for func in func_list:
            if func.__name__ != 'init':
                bot.l_say(formatdoc(func), input, 0)
        return True
    
    except (KeyError, TypeError):
        # Try to see if the query is a function of its
        # own, and not a module
        if input.args is not None:
            for m in l.get_modules():
                m = l.get_module_from_string(m)
                if hasattr(m, input.args[0]):
                    func = getattr(m, input.args[0])
                    bot.l_say(formatdoc(func), input, 0)
                    return True
        
        # Can't find the query anywhere, so we'll
        # print the default help message
        print 'Printing help list...'
        for line in inspect.getdoc(help).split('\n'):
            bot.l_say(line, input, 0)
        # Categories. Need an algorithm to get these
        bot.l_say(get_categories(input), input, 0)
        return True
    
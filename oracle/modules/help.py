"""
Oracle 2.0 IRC Bot
help.py plugin module

http://toofifty.me/oracle
"""

import types, inspect
import traceback
import math

from format import WHITE, CYAN, GREY, PURPLE

def _init(bot):
    print '\t%s loaded' % __name__
    
# All commands are called with the arguments
# <module>.<command>(plugins.Loader(), bot.Oracle(), bot.Input())
# In all other plugins, these are abbreviated to l, b, i
def help(loader, bot, input):
    """Print the command usage and other
    help to the user
    """
    
    BASE = CYAN
    BRKT = PURPLE
    FILL = GREY
    
    help_dict = {}

    def s(str):
        return bot.l_say(str, input, 0)
    
    def append_cmd(cmd, desc):
        help_dict[cmd] = desc
        
    def parse_child(function, doc):
        u_rank = input.user.get_rank()
        # First line is '!parent-command'
        doc = doc.split('\n')[1:]
        
        c = d = a = r = ''
        
        for line in doc:
            line = line.strip(' ')
            
            # Command
            if line.startswith('!c '):
                c = line.replace('!c ', '').upper()
                
            # Description
            elif line.startswith('!d '):
                d = line.replace('!d ', '').capitalize()
                
            # Arguments
            elif line.startswith('!a '):
                a = line.replace('!a ', '').upper()
                
            # Rank
            # ALL child commands NEED a rank to
            # be processed.
            elif line.startswith('!r '):
                str = line.replace('!r ', '')
                r = loader.get_rank_from_string(str)
                
                # Don't add to help dict
                if not u_rank >= r:
                    continue
                
                # Add them all together and append
                cmd = func.__name__.upper()
                cmd += ' ' + c + ' ' + a
                
                append_cmd(cmd.upper(), d)
                
                # Reset values
                c = d = a = r = ''
                continue

    def parse_doc(function):
        u_rank = input.user.get_rank()
        doc = inspect.getdoc(function)
        c_rank = 0
        a = r = d = ''
        
        if doc is not None:
            if '!parent-command' in doc:
                parse_child(function, doc)
                return
                
            for line in doc.split('\n'):
                
                # Description
                if line.startswith('!d '):
                    d = line.replace('!d ', '').capitalize()
                    
                # Command
                elif line.startswith('!a '):
                    a = line.replace('!a ', '').upper()
                    
                # Rank
                elif line.startswith('!r '):
                    str = line.replace('!r ', '')
                    r = loader.get_rank_from_string(str)
                    if not u_rank >= r:
                        return
                    
            cmd = function.__name__.upper()
            if a != '':
                cmd += ' ' + a
                
            # Append
            append_cmd(cmd, d)
            
    def print_line(cmd, desc):
        # Ensure the command exists
        # Description doesn't matter as much.
        if cmd is None: return
        if desc is None: desc = ''

        # Game has different kerning, so aligning
        # the message wouldn't look right.
        
        # Not game
        if input.game == '':
            cmd = cmd.ljust(25)
            cmd = cmd.replace('<',BRKT+'<'+FILL).replace('>',BRKT+'>'+BASE)
            cmd = cmd.replace('[',BRKT+'['+FILL).replace(']',BRKT+']'+BASE)
            cmd = cmd.replace('...',BRKT+'...'+BASE)
            
            str = '%s - %s' % (BASE + cmd, FILL + desc)
        # In game
        else:
            cmd = cmd.replace('<',BRKT+'<'+FILL).replace('>',BRKT+'>'+BASE)
            cmd = cmd.replace('[',BRKT+'['+FILL).replace(']',BRKT+']'+BASE)
            cmd = cmd.replace('...',BRKT+'...'+BASE)
            
            str = '%s - %s' % (BASE + cmd, FILL + desc)

        # Say the line to the user.
        return s(str)
            
    def get_page_count():
        return math.ceil(len(help_dict) / 10.0)
            
    def print_help(page):
        max_page = get_page_count()
    
        if page > max_page:
            page = max_page
        elif page < 1:
            page = 1
        
        if input.game != '':
            s('%s================ Page: %d/%d ================' % (PURPLE, page, max_page))
            s('\t')
        else:
            s('%sPage %d/%d:' % (PURPLE, page, max_page))
            
        # 10 per page
        start = 10 * page - 10
        end = start + 10
        count = 0
        
        # Iter through commands
        for k, v in sorted(help_dict.iteritems()):
            if count >= start and count < end:
                print_line(k, v)
            count += 1
            
        if input.game != '':
            s('\t')
            s('%s=========================================' % PURPLE)
            
        return True
    
    try:
    
        # User might ask for categories
        if input.args is not None and input.args[0] == 'categories':
            return categories(loader, bot, input)
        
        # Grab the module from the laoded modules
        # This will throw a KeyError if no module is found,
        # and so it will print the default help message
        mod = loader.get_module_from_string('modules.%s' % input.args[0])
        func_list = [getattr(mod, a, None) for a in dir(mod)
                     if isinstance(getattr(mod, a, None), 
                                   types.FunctionType)]
        for func in func_list:
            if not func.__name__.startswith('_'):
                parse_doc(func)
                
        page = 1
        try:
            page = int(input.args[1])
        except IndexError:
            pass
            
        print_help(page)
            
        return True
    
    except (KeyError, TypeError):
    
        # Try to see if the query is a function of its
        # own, and not a module
        if input.args is not None:
        
            # Let's assume the arg is bad
            bad_arg = True
        
            for m in loader.get_modules():
                
                if hasattr(m, input.args[0]):
                    bad_arg = False
                    func = getattr(m, input.args[0])
                    parse_doc(func)
                    
            if not bad_arg:
                print_help(1)
                return True
            
            else:
                s('%sUnknown argument: %s%s%s.\n\t' 
                  % (WHITE, PURPLE, input.args[0], WHITE))
        
        # Can't find the query anywhere, so we'll
        # print the default help message
        if input.game != '':
            s('%s=========================================' % PURPLE)
            s('\t')
        s('Welcome to the Oracle help guide!')
        s('\t')
        s('%sHELP %susage:' % (PURPLE, WHITE))
        s('\t%s.help' % CYAN)
        s('\t%s.help oracle' % CYAN)
        s('\t%s.help %s[%scategory%s] <%spage%s>' 
          % (CYAN, WHITE, GREY, WHITE, GREY, WHITE))
        s('\t%s.help %s[%scommand%s]' % (CYAN, WHITE, GREY, WHITE))
        s('\t%s.help search %s[%sphrase...%s] <%spage%s>' 
          % (CYAN, WHITE, GREY, WHITE, GREY, WHITE))
        s('\t%s.help all %s<%spage%s>' % (CYAN, WHITE, GREY, WHITE))
        s('\t')
        s('Categories can be listed with')
        s('the %s.categories%s command.' % (CYAN, WHITE))
        if input.game != '':
            s('\t')
            s('%s=========================================' % PURPLE)
        return True
        
    except:
        traceback.print_exc()
        
def categories(l, b, i):
    """
    !d List loaded modules
    !r user
    """
    restricted = [
            'modules.admin',
            'modules.format',
            'modules.log',
        ]
    
    message = []
    for m in l.get_modules_list():
        if not m in restricted: 
            message.append(m.replace('modules.','').capitalize())
    b.l_say('%sCategories: %s%s' % (CYAN, PURPLE, 
                (WHITE+', '+PURPLE).join(message)), i, 0)
    return True
    

def cats(l, b, i):
    """
    !d Alias for .categories
    !r user
    """
    return categories(l, b, i)
    
def version(l, b, i):
    """
    !d Get the version of Oracle
    !r user
    """
    return b.l_say('Oracle Version %s' % b.get_version(), i, 0)
import random
import re
import socket
from format import CYAN, GREY, PURPLE, WHITE

def _init(bot):
    print '\t%s loaded' % __name__
    
def pick(l, b, i):
    """
    !d Pick an option from a list (separated by a space)
    !a [options...]
    !r user
    """
    if len(i.args) < 2:
        b.l_say('Usage: %s.pick [option1] [option2] ...' % CYAN, i, 0)
        return True
    choice = random.randint(1, len(i.args)) - 1
    b.l_say('%s: %s' % (i.nick, i.args[choice]), i, 1)
    return True
    
def nether(l, b, i):
    """
    !d Overworld coordinates - Nether conversion
    !a [x] <y> [z]
    !r user
    """
    def usage():
        b.l_say('Usage: %s.nether [x] [y] [z]' % CYAN, i, 0)

    if len(i.args) < 2:
        usage()
    elif len(i.args) == 2:
        try:
            x = math.floor(float(i.args[0]) / 8)
            z = math.floor(float(i.args[1]) / 8)
            b.l_say('Nether co-ords: %dx, %dz' % (x, z), i, 0)
        except:
            usage()
    else:
        try:
            x = math.floor(float(i.args[0]) / 8)
            y = i.args[1]
            z = math.floor(float(i.args[2]) / 8)
            b.l_say('Nether co-ords: %dx, %dy, %dz' % (x, y, z), i, 0)
        except:
            usage()
    return True         

def overworld(l, b, i):
    """
    !d Nether coordinates - Overworld conversion
    !a [x] <y> [z]
    !r user
    """
    def usage():
        b.l_say('Usage: %s.overworld [x] [y] [z]' % CYAN, i, 0)

    if len(i.args) < 2:
        usage()
    elif len(i.args) == 2:
        try:
            x = math.floor(float(i.args[0]) * 8)
            z = math.floor(float(i.args[1]) * 8)
            b.l_say('Overworld co-ords: %dx, %dz' % (x, z), i, 0)
        except:
            usage()
    else:
        try:
            x = math.floor(float(i.args[0]) * 8)
            y = i.args[1]
            z = math.floor(float(i.args[2]) * 8)
            b.l_say('Overworld co-ords: %dx, %dy, %dz' % (x, y, z), i, 0)
        except:
            usage()
    return True   
    
def alias(l, b, i):
    """
    !d Define a custom command to any word/phrase
    !a [new|remove] "[alias]" "[command+args]"
    !r user
    """
    charset = (b.config.char, b.config.prchar, b.config.puchar)
    
    if i.user.get_alias_list() is []:
        i.user.add_attribute('aliases', [])
    try:
        if i.args[0].lower() == 'new':
            splitter = re.compile(r'"(.*?)" "(.*?)"')
            message = ' '.join(i.args[1:])
            spl_match = splitter.match(message)
            if spl_match is not None:
                accept = False
                for c in charset:
                    if spl_match.group(2).startswith(c):
                        accept = True
                        
                if accept:
                    i.user.add_alias(spl_match.group(1), spl_match.group(2))
                    b.l_say('Alias %s added.' % (PURPLE+spl_match.group(1)+WHITE), i, 0)
                    return True
                else:
                    b.l_say('Alias rejected, command must start with %s or %s' \
                            % (PURPLE+b.config.char+WHITE, PURPLE+b.config.prchar+WHITE), i, 0)
                    return True
            b.l_say('Usage %s.alias new "[alias]" "[command]"' % GREY, i, 0)
            return True
            
        elif i.args[0].lower() == 'rem' or i.args[0].lower() == 'remove':
            alias = ' '.join(i.args[1:])
            if i.user.rem_alias(alias):
                b.l_say('Alias successfully removed', i, 0)
            else:
                b.l_say('Alias not found', i, 0)
            return True
    except:
        pass
    b.l_say('Usage %s.alias [new|remove]' % GREY, i, 0)
    return True
    
def resolve(l, b, i):
    """
    !d Resolve a domain name/adress to an IP
    !a [domain|address]
    !r user
    """
    if i.args is None or len(i.args) < 1:
        b.l_say('Usage %s.resolve [domain]' % GREY, i, 0)
        return True
    data = socket.gethostbyname_ex(i.args[0])
    b.l_say('%s resolved to %s' % (i.args[0], str(data[2])), i, 0)
    return True
    
    
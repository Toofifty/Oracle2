"""
Oracle 2.0 IRC Bot
admin.py plugin module

http://toofifty.me/oracle
"""

import sys, os, subprocess
import traceback, time
from format import GREY, WHITE, PURPLE

def _init(b):
    print '\t%s loaded' % __name__
    
def reload(l, b, i):
    """
    !d Reload all or specific modules (separated by a space)
    !a <modules...>
    !r developer
    """
    if b.reload_modules(i):
        b.l_say('Module(s) reloaded', i, 0)
        return True
    return False
    
def modules(l, b, i):
    """
    !d Get all loaded modules
    !r developer
    """
    for m in l.get_modules_list():
        b.l_say(m.capitalize(), i, 0)
    return True

def load(l, b, i):
    """
    !d Load a module into Oracle
    !a [module]
    !r developer
    """
    fl = l.load_module(i.args[0], b)
    
    if fl:
        b.l_say('Module loaded.', i, 0)
    return fl

def close(l, b, i):
    """
    !d Close Oracle
    !a <message...>
    !r administrator
    """
    if i.args is None:
        b.l_say('Goodbye!', i, 3)
    else:
        b.say(' '.join(i.args).capitalize(), channel='all')
    b.exit()
    sys.exit()
    
def fpart(l, b, i):
    """
    !d Fake a user part event
    !a <user>
    !r developer
    """
    if i.args is None:
        name = i.nick
    else:
        name = i.args[0]
    b.user_part_event(name, i.channel)
    b.l_say('Faked user part for %s' % (PURPLE+name), i, 0)
    return True

def fjoin(l, b, i):
    """
    !d Fake a user join event
    !a <user>
    !r developer
    """
    if i.args is None:
        name = i.nick
    else:
        name = i.args[0]
    b.user_join_event(name, i.channel)
    b.l_say('Faked user join for %s' % (PURPLE+name), i, 0)
    return True

def restart(l, b, i):
    """
    !d Restart Oracle
    !a <message...>
    !r administrator
    """
    if i.args is None:
        b.l_say('I\'ll be back in a jiffy!', i, 3)
    else:
        boy.say(' '.join(i.args).capitalize(), channel='all')
    b.exit()
    print '\n' * 5
    
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)
    
def say(l, b, i):
    """
    !d Instruct Oracle to repeat a word or phrase
    !a [message...]
    !r administrator
    """
    try:
        print 'Saying the phrase:', ' '.join(i.args)
        b.l_say(' '.join(i.args), i, 1)
        return True
    except TypeError:
        return False

def exe(l, b, i):
    """
    !d Execute some (Python) code and print to IRC
    !a [code...]
    !r developer
    """
    try:
        exec ' '.join(i.args)
    except Exception, e:
        b.l_say(e, i, 0)
        return False
    return True
    
def raw(l, b, i):
    """
    !d Send a raw message to the IRC server
    !a [message...]
    !r developer
    """
    if i.args is not None:
        return b.send_('%s\r\n' % ' '.join(i.args))
    return False

def whois(l, b, i):
    """
    !d Send a WHOIS message to the IRC server
    !a <nick>
    !r administrator
    """
    if i.args is None:
        return b.whois(i.nick)
    return b.whois(' '.join(i.args))
    
def doc(l, b, i):
    """
    !d Return the main docstring of a module
    !a [module]
    !r developer
    """
    for m in l.get_modules():
        if i.args[0] == m.__name__:
            if m.__doc__ is not None:
                for line in m.__doc__.split('\n'):
                    b.l_say(line, i, 0)
            else:
                b.l_say('No doc found for that module.', i, 0)
            return True
        else:
            if 'modules.' in i.args[0]:
                return b.l_say('No doc found for that module.', i, 0)
            return b.l_say('No doc found for that module. '
                             'Maybe try modules.%s?' % i.args[0], 
                             i, 0)
            
def getrank(l, b, i):
    """
    !d Return a user's (or own) rank
    !a <user>
    !r administrator
    """
    if i.args is None:
        b.l_say('You are rank %s.' % i.user.get_rank().upper(), i, 0)
    else:
        try:
            rank = b.get_user(i.args[0]).get_rank()
            b.l_say('%s\'s rank is %s.' % (i.args[0], rank.upper()), i, 0)
        except Exception, e:
            b.l_say('No rank found for %s: %s' % (i.args[0], e), i, 0)
    return True

def setrank(l, b, i):
    """
    !d Set a user's rank
    !a [user] [rank]
    !r administrator
    """
    ranks = ['developer',
             'administrator',
             'moderator',
             'user']
    if i.args is None or len(i.args) < 2:
        b.l_say('Usage: %s.setrank [user] [developer|administrator|moderator|user]' % GREY, i, 0)
        return True
    if i.args[1] in ranks:
        try:
            user = b.get_user(i.args[0])
            b.l_say('%s\'s rank set to %s.' % (i.args[0], user.set_rank(i.args[1]).upper()), i, 0)
        except Exception, e:
            b.l_say('No user found for %s: %s' % (i.args[0], e), i, 0)
    return True

def makeadmin(l, b, i):
    """
    !d Fallback command to make a yourself admin
    !r hidden
    """
    i.user.set_rank('administrator')
    b.l_say('You are now administrator', i, 0)
    return True
    
def open(l, b, i):
    """
    !d Open a specific directory, the the path of the b
    !a [path]
    !r developer
    """
    if i.args is None: path = os.getcwd()
    else: path = '\\'.join(i.args)
    try:
        b.l_say('Opening %s' % path, i, 0)
        subprocess.Popen(r'explorer /open, "%s"' % path)
    except Exception, e:
        tracepack.print_exc()
    return True
    
if __name__ == '__main__':
    print __doc__
"""
Oracle 2.0 IRC Bot
admin.py plugin module

http://toofifty.me/oracle
"""

import sys, os, subprocess
import traceback, time

def _init(bot):
    print '\t%s loaded' % __name__
    
def reload(l, bot, input):
    """
    !d Reload all or specific modules (separated by a space)
    !a <modules...>
    !r developer
    """
    if bot.reload_modules(input):
        bot.l_say('Module(s) reloaded', input, 0)
        return True
    return False
    
def modules(l, bot, input):
    """
    !d Get all loaded modules
    !r developer
    """
    for m in l.get_modules_list():
        bot.l_say(m.capitalize(), input, 0)
    return True

def load(l, bot, input):
    """
    !d Load a module into Oracle
    !a [module]
    !r developer
    """
    fl = l.load_module(input.args[0], bot)
    
    if fl:
        b.l_say('Module loaded.', i, 0)
    return fl

def close(l, bot, input):
    """
    !d Close Oracle
    !a <message...>
    !r administrator
    """
    if input.args is None:
        bot.l_say('Goodbye!', input, 3)
    else:
        bot.say(' '.join(input.args).capitalize(), channel='all')
    bot.exit()
    sys.exit()
    
def fpart(l, bot, input):
    """
    !d Fake a user part event
    !a <user>
    !r developer
    """
    if input.args is None:
        name = input.nick
    else:
        name = input.args[0]
    bot.user_part_event(name, input.channel)
    bot.l_say('Faked user part for %s' % name, input, 0)
    return True

def fjoin(l, bot, input):
    """
    !d Fake a user join event
    !a <user>
    !r developer
    """
    if input.args is None:
        name = input.nick
    else:
        name = input.args[0]
    bot.user_join_event(name, input.channel)
    bot.l_say('Faked user join for %s' % name, input, 0)
    return True

def restart(l, bot, input):
    """
    !d Restart Oracle
    !a <message...>
    !r administrator
    """
    if input.args is None:
        bot.l_say('I\'ll be back in a jiffy!', input, 3)
    else:
        boy.say(' '.join(input.args).capitalize(), channel='all')
    bot.exit()
    print '\n' * 5
    
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)
    
def say(l, bot, input):
    """
    !d Instruct Oracle to repeat a word or phrase
    !a [message...]
    !r administrator
    """
    try:
        bot.l_say(' '.join(input.args), input)
        return True
    except TypeError:
        return False

def exe(l, bot, input):
    """
    !d Execute some (Python) code and print to IRC
    !a [code...]
    !r developer
    """
    try:
        exec ' '.join(input.args)
    except Exception, e:
        bot.l_say(e, input, 0)
        return False
    return True
    
def raw(l, bot, input):
    """
    !d Send a raw message to the IRC server
    !a [message...]
    !r developer
    """
    if input.args is not None:
        return bot.send_('%s\r\n' % ' '.join(input.args))
    return False

def whois(l, bot, input):
    """
    !d Send a WHOIS message to the IRC server
    !a <nick>
    !r administrator
    """
    if input.args is None:
        return bot.whois(input.nick)
    return bot.whois(' '.join(input.args))
    
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
        b.l_say('Usage: .setrank [user] [developer|administrator|moderator|user]', i, 0)
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
    
def open(l, bot, input):
    """
    !d Open a specific directory, the the path of the bot
    !a [path]
    !r developer
    """
    if input.args is None: path = os.getcwd()
    else: path = '\\'.join(input.args)
    try:
        bot.l_say('Opening %s' % path, input, 0)
        subprocess.Popen(r'explorer /open, "%s"' % path)
    except Exception, e:
        tracepack.print_exc()
    return True
    
if __name__ == '__main__':
    print __doc__
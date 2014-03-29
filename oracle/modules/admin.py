"""
Oracle 2.0 IRC Bot
admin.py plugin module

http://toofifty.me/oracle
"""

import sys, os, subprocess
import traceback, time

def init():
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
    for m in l.get_modules():
        bot.l_say(m.capitalize(), input, 0)
    return True

def load(l, bot, input):
    """
    !d Load a module into Oracle
    !a [module]
    !r developer
    """
    return l.load_module(input.args[0])

def close(l, bot, input):
    """
    !d Close Oracle
    !a <message...>
    !r developer
    """
    if input.args is None:
        bot.l_say('Goodbye!', input, 3)
    else:
        bot.say(' '.join(input.args).capitalize(), channel='all')
    bot.quit()
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
    !r developer
    """
    if input.args is None:
        bot.l_say('I\'ll be back in a jiffy!', input, 3)
    else:
        boy.say(' '.join(input.args).capitalize(), channel='all')
    bot.quit()
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
    !r developer
    """
    bot.l_say(' '.join(input.args), input)
    return True

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
    !r developer
    """
    if input.args is None:
        return bot.whois(input.nick)
    return bot.whois(' '.join(input.args))
    
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
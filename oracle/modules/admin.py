"""
Oracle 2.0 IRC Bot
admin.py plugin module

http://toofifty.me/oracle
"""

import sys, os, subprocess
import traceback, time
import format as f
import random
from format import GREY, WHITE, PURPLE, YELLOW

def _init(b):
    print '\t%s loaded' % __name__

def reload(l, b, i):
    """
    !d Reload all or specific modules (separated by a space)
    !a [modules...]
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
    !d Load modules into $nick$
    !a <modules...>
    !r developer
    """
    for mod in i.args:
        if not l.load_module(mod, b):
            b.l_say('Module failed to load: %s' % mod, i, 0)
        else:
            b.l_say('Loaded module: %s' % mod, i, 0)
    return True

def close(l, b, i):
    """
    !d Close $nick$
    !a [message...]
    !r administrator
    """
    if i.args is None:
        b.l_say(YELLOW+'Goodbye!', i, 3)
    else:
        b.say(' '.join(i.args).capitalize(), channel='all')
    b.exit()
    sys.exit()

def fpart(l, b, i):
    """
    !d Fake a user part event (or self)
    !a [user]
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
    !d Fake a user join event (or self)
    !a [user]
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
    !d Restart $nick$
    !a [message...]
    !r administrator
    """
    if i.args is None:
        quotes = [
            '(Terminator voice) I\'ll be back!',
            'I\'ll be back in a jiffy!',
            'brb',
            'I\'ll be right back, homies',
            ]
        choice = random.randint(1, len(quotes)) - 1
        b.l_say(YELLOW+quotes[choice], i, 3)
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
    !d Repeat a word or phrase
    !a <message...>
    !r moderator
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
    !a <code...>
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
    !a <message...>
    !r developer
    """
    if i.args is not None:
        return b.send_('%s\r\n' % ' '.join(i.args))
    return False

def whois(l, b, i):
    """
    !d Send a WHOIS "nick" message to the IRC server (defaults to self)
    !a [nick]
    !r administrator
    """
    if i.args is None:
        return b.whois(i.nick)
    return b.whois(' '.join(i.args))

def doc(l, b, i):
    """
    !d Return the main docstring of a module
    !a <module>
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
    !a [user]
    !r administrator
    """
    if i.args is None:
        rank = l.get_string_from_rank(i.user.get_rank()).upper()
        b.l_say('You are rank %s.' % rank, i, 0)
    else:
        try:
            rank = b.get_user(i.args[0]).get_rank()
            str_rank = l.get_string_from_rank(rank).upper()
            b.l_say('%s\'s rank is %s.' % (i.args[0], str_rank), i, 0)
        except Exception, e:
            b.l_say('No rank found for %s: %s' % (i.args[0], e), i, 0)
    return True

def setrank(l, b, i):
    """
    !d Set a user's rank
    !a <user> <rank>
    !r administrator
    """
    ranks = [
             'hidden',
             'developer',
             'administrator',
             'moderator',
             'user',
             'none',
            ]
    numbers = [
             '0', '1', '2',
             '3', '4', '-1'
             ]
    if i.args is None or len(i.args) < 2:
        b.l_say('Usage: %s.setrank <user> developer|administrator|moderator|user' % GREY, i, 0)
        return True
    if i.args[1] in ranks:
        try:
            user = b.get_user(i.args[0])

            str_rank = i.args[1].upper()
            user.set_rank(l.get_rank_from_string(i.args[1]))

            b.l_say('%s\'s rank set to %s.' % (i.args[0], str_rank), i, 0)

        except Exception, e:
            b.l_say('No user found for %s: %s' % (i.args[0], e), i, 0)
    if i.args[1] in numbers:
        try:
            user = b.get_user(i.args[0])
            rank = int(i.args[1])
            user.set_rank(rank)
            str_rank = l.get_string_from_rank(rank).upper()
            b.l_say('%s\'s rank set to %s.' % (i.args[0], str_rank), i, 0)

        except:
            b.l_say('No user found for %s: %s' % (i.args[0], e), i, 0)
    return True

def makeadmin(l, b, i):
    """
    !d Fallback command to make a yourself admin
    !r hidden
    """
    if i.nick == 'Toofifty':
        i.user.set_rank(3)
        b.l_say('You are now administrator', i, 0)
        return True

def open(l, b, i):
    """
    !d Open a specific directory, default bot's path
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

def ban(l, b, i):
    """
    !d Ban a user from all channels $nick$ is in
    !a <user>
    !r moderator
    """
    if i.args is None:
        b.l_say('Usage: %s.ban <user>' % GREY, i, 0)
        return True
    user = b.get_user(i.args[0])
    if not user:
        b.l_say('No user found under that name.', i, 0)
        return True
    user.set_rank(0)
    b.l_say('%s successfully banned.' % user.get_name(), i, 0)
    return True


def kick(l, b, i):
    """
    !d Kick a user from all channels $nick$ is in
    !a <user>
    !r moderator
    """
    if i.args is None:
        b.l_say('Usage: %s.kick <user>' % GREY, i, 0)
        return True
    b.kick(i.args[0])
    b.l_say('%s kicked.' % i.args[0])
    return True


if __name__ == '__main__':
    print __doc__

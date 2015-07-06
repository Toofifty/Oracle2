"""
Oracle 2.0 IRC Bot
stats.py plugin module

http://toofifty.me/oracle
"""

import socket
import time, calendar
from datetime import datetime

DOMAIN = ''
USER = None

def _init(bot):
    print '\t%s loaded' % __name__

def utc(l, b, i):
    """
    !d Get the current UTC time (used for server events)
    !r user
    """
    d = datetime.utcnow()
    t = calendar.timegm(d.utctimetuple())
    b.l_say('Current UTC time: %s' % str(time.ctime(t)), i, 0)
    return True

def ip(l, b, i):
    """
    !d Get the current, working IP of the server
    !r user
    """
    try:
        data = socket.gethostbyname_ex('s.rapidcraftmc.com')
        b.l_say('s.rapidcraftmc.com resolved to IP: %s' % str(data[2]), i, 0)

    except:
        global DOMAIN
        if DOMAIN is '':
            b.l_say('Calculating IP, one moment...', i, 0)
            global USER
            USER = i
            b.whois('RapidSurvival')
            return True
        try:
            data = socket.gethostbyname_ex(DOMAIN)
            b.l_say('%s resolved to IP: %s' % (DOMAIN, str(data[2])), i, 0)
        except:
            b.l_say('No IP could be found, sorry!', i, 0)
    return True

def _whois_311(bot, args):
    nick, realname, domain = args
    if realname != '~PircBot':
        return

    global DOMAIN
    DOMAIN = domain
    global USER
    if USER is not None:
        data = socket.gethostbyname_ex(domain)
        bot.l_say('%s resolved to IP: %s' % (domain, str(data[2])), USER, 0)

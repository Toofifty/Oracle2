"""
Oracle 2.0 IRC Bot
log.py plugin module

http://toofifty.me/oracle
"""

from datetime import datetime

def _init(b):
    print '\t%s loaded' % __name__
    
def _log(info, title, user, message):
    
    # ===== Construct print line ===== #
    line = ''
    
    # First two characters
    if 'send' in info: line += '-> '
    elif 'receive' in info: line += '<- '
    elif 'action' in info: line += '!! '
    elif 'command' in info: line += '?? '
    else: line += '   '
    
    # Timestamp
    line += '[%s]' % str(datetime.now())
    
    # Set logging level
    if 'debug' in info: line += '[DEBUG]'.ljust(11)
    elif 'warning' in info: line += '[WARNING]'.ljust(11)
    else: line += '[INFO]'.ljust(11)
    
    # Title each message
    title = title.upper()
    line += '| %s | ' % title.ljust(12)
    
    # Add user
    if user is '': line += ': '.rjust(14)
    else: line += user.ljust(12) + ': '
    
    line += message
    
    # Print!
    print line
    
def _chat(bot, args):
    nick, channel, message = args
    if nick == 'RapidSurvival' or nick == 'RapidCreative':
        _log('receive', 'rapid chat', 
             message[0].replace('<', '').replace('>', ''),
             ' '.join(message[1:]))
    else:
        _log('receive', 'chat', nick, ' '.join(message))
"""
Oracle 2.0 IRC Bot
log.py plugin module

http://toofifty.me/oracle
"""

from format import _console_colours, Fore, Back, Style
from datetime import datetime

LAST_TITLE = ''

def _init(b):
    print '\t%s loaded' % __name__

def _log(info, title, user, message):

    # ===== Construct print line ===== #
    line = Style.NORMAL

    # First two characters
    if 'send' in info: line += Back.GREEN + '-> '
    elif 'receive' in info: line += Back.GREEN + '<- '
    elif 'action' in info: line += Back.RED + '!! '
    elif 'command' in info: line += Back.MAGENTA + '?? '
    else: line += '   '

    # Timestamp
    line += Back.CYAN
    line += '[%s]' % str(datetime.now().strftime('%d/%m %H:%M:%S'))

    # Set logging level
    if 'debug' in info: line += '[D]'
    elif 'warning' in info: line += '[W]'
    else: line += '[I]'

    # Title each message
    title = title.upper()
    global LAST_TITLE

    if LAST_TITLE == title:
        title = ' |'

    if len(title) > 12:
        title = title[:9] + '...'

    if title != ' |':
        LAST_TITLE = title

    line += Back.WHITE + Fore.BLACK + '| %s | ' % title.ljust(12)

    # Fix user length
    if len(user) > 12:
        user = user[:9] + '...'

    # Add user
    if user is '':
        line += ('|' + Style.NORMAL + Back.RESET + Fore.RESET + ' ').rjust(14)
    else:
        line += user.ljust(12) + '| ' + Style.NORMAL
        line += Back.RESET + Fore.RESET + ' '

    line += message

    # Print!
    print line

def _chat(bot, args):
    nick, channel, message = args
    message = _console_colours(message)
    if nick == 'RapidSurvival' or nick == 'RapidCreative':
        if '<' in message[0] and '>' in message[0]:
            _log('receive', 'rapid chat',
                 message[0].replace('<', '').replace('>', ''),
                 ' '.join(message[1:]))
        else:
            _log('receive', 'rapid event', nick, message)
    else:
        _log('receive', 'chat(%s)' % channel, nick, message)

def _command(bot, args):
    input = args
    if input.args is not None:
        m = '*%s* %s' % (input.command.upper(), ' '.join(input.args).upper())
    else:
        m = '*%s*' % (input.command.upper())
    _log('action', 'command', input.nick, m)

def _message(bot, args):
    nick, message = args
    _log('receive', 'message', nick, message)

def _user_join(bot, args):
    nick, channel = args
    m = '%s joined %s.' % (nick, channel)
    _log('receive', 'join' + channel, nick, m)

def _user_part(bot, args):
    nick, channel = args
    m = '%s left %s.' % (nick, channel)
    _log('receive', 'part' + channel, nick, m)

def _user_nick(bot, args):
    nick, new_nick = args
    m = '%s has changed nick to %s.' % (nick, new_nick)
    _log('receive', 'nick change', nick, m)

def _bot_join(bot, args):
    channel = args
    m = '%s has joined %s.' % (bot.config.nick, channel)
    _log('action', 'bot join', bot.config.nick, m)

def _bot_invite(bot, args):
    nick, channel = args
    m = '%s has invited me to %s, joining...' % (nick, channel)
    _log('action', 'bot invite', nick, m)

"""
Oracle 2.0 IRC Bot
stats.py plugin module

http://toofifty.me/oracle
"""

import os

def init():
    print '\t%s loaded' % __name__
    
def seen(l, bot, input):
    if input.args is None:
        bot.l_say('Usage: .seen [user]', input, 0)
        return True
    else:
        seen = None
        try:
            seen = bot.users[input.args[0]].get_seen()
        except KeyError:
            for f in os.listdir(os.path.join('..', 'files', 'users')):
                try:
                    print f
                    f = f.replace('.json', '')
                    # Hehe, flower
                    print f
                    if f.lower() == input.args[0].lower():
                        seen = bot.open_user(f).get_seen()
                except KeyError:
                    continue
                
        if seen is not None:
            bot.l_say('Last seen: %s' % seen, input, 0)
        else:
            bot.l_say('User %s not found in the database.' % input.args[0],
                       input, 0)
        return True
        
def listusers(l, bot, input):
    pass
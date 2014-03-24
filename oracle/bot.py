#!/user/bin/env python
"""
Oracle 2.0 IRC Bot
bot.py

http://toofifty.me/oracle
"""

import irc

class Oracle(irc.Bot):
    def __init__(self, config):
        irc.Bot.__init__(self, config.nick, config.ident, 
                         config.channel, config.password)
        self.config = config
        self.doc = {}
        self.setup()
        
    def setup(self):
        pass
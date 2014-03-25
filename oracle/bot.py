#!/user/bin/env python
"""
Oracle 2.0 IRC Bot
bot.py

http://toofifty.me/oracle
"""

import string
import irc

class Oracle(irc.IRC):
    def __init__(self, config):
        irc.IRC.__init__(self, config.nick, config.ident, 
                         config.channel, config.password)
        self.config = config
        self.doc = {}
        self.setup()
        
    def setup(self):
        pass
        
class Configuration:
    def __init__(self):
        self.nick       = 'Perry'
        self.ident      = 'PerryBot'
        self.channel    = '#toofifty'
        self.password   = 'none'
        
def main():

    config = Configuration()

    bot = Oracle(config)
    
    bot.init_connect('irc.esper.net', 6667)

    readbuffer = ''
    
    while True:
        readbuffer += bot.recv(1024)
        
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()
        
        for line in temp:
            print line
            
            line = string.split(string.rstrip(line))
            message = " ".join(line)
            
            if 'PING' in line[0]:
                bot.ping_event(line[1:])
                
if __name__ == "__main__":
    main()
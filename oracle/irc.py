# -- coding: utf-8 --
"""
Oracle 2.0 IRC Bot
irc.py

http://toofifty.me/oracle
"""

import socket, sys
            
class IRC(socket.socket):
    def __init__(self, config):
        socket.socket.__init__(self)
        
        self.nick = config.nick
        self.ident = config.ident
        self.channels = config.channels or []
        if hasattr(config, 'password'):
            self.password = config.password
        else: self.password = None
        self.host = config.host
        self.port = config.port
        self.char = config.char
    
    def send_(self, s):
        self.send(s)
        if self.config.verbose:
            print s.rstrip()
        return True
        
    def init_connect(self):
        
        try:
            self.connect((self.host, self.port))
            self.send_('NICK %s\r\n' % self.nick)
            self.send_('USER %s %s bla :BOT\r\n' % (self.ident, self.host))
        except Exception, e:
            print e
        
    def join_channels(self):
        for c in self.channels:
            self.send_('JOIN %s\r\n' % c)
            
    def msg(self, nick, m):
        # NOTICE sends a message without a new window
        self.send_('NOTICE %s :%s\r\n' % (nick, m))
        return True
        
    def say(self, m, channel=None):
        # PRIVMSG usually opens a new window
        if channel == 'all':
            for c in self.channels:
                self.send_('PRIVMSG %s :%s\r\n' % (c, m))
        else:
            channel = channel or self.channels[0]
            try:
                self.send_('PRIVMSG %s :%s\r\n' % (channel, m))
            except Exception, e:
                self.send_('PRIVMSG %s :%s\r\n' % (channel, e))
                
    def l_say(self, m, input, f_level=1):
        if input.level == 0:
            self.msg(input.nick, m)
        elif input.level == 1:
            if f_level == 0:
                self.msg(input.nick, m)
            elif f_level == 1:
                self.say(m, input.channel)
            else:
                self.say(m, 'all')
        else:
            self.say(m, 'all')
        
    def ping_event(self, id):
        self.send_('PONG %s\r\n' % str(id))
        
    def mode(self, args):
        self.send_('MODE %s : %s\r\n' % (self.channel, args))
        
    def kick(self, nick):
        self.send_('KICK %s %s\r\n' % (self.channel, nick))
        
    def stop(self):
        self.quit()
        sys.exit()
        
    def quit(self):
        self.send_('QUIT\r\n')
            
if __name__ == '__main__':
    print __doc__

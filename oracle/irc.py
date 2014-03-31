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
        if self.config.verbose:
            print '--> %s --> sent %d bytes'% (s.rstrip(), self.send('%s\r\n' % s))
            return True
        else:
            return self.send('%s\r\n' % s)
        
    def init_connect(self):
        
        try:
            self.connect((self.host, self.port))
            self.set_nick(self.nick)
            self.send_('USER %s %s bla :BOT' % (self.ident, self.host))
        except Exception, e:
            print e
            
    def set_nick(self, nick):
        self.nick = nick
        return self.send_('NICK %s' % nick)
        
    def join_channels(self):
        for c in self.channels:
            self.join_channel(c)
            
    def join_channel(self, channel):
        self.send_('JOIN %s' % channel)
        if not channel in self.channels:
            self.channels.append(channel)
            
    def msg(self, nick, m):
        # NOTICE sends a message without a new window
        return self.send_('NOTICE %s :%s' % (nick, m))
        
    def say(self, m, channel=None):
        # PRIVMSG usually opens a new window
        if channel == 'all':
            for c in self.channels:
                self.send_('PRIVMSG %s :%s' % (c, m))
            return True
        else:
            channel = channel or self.channels[0]
            try:
                return self.send_('PRIVMSG %s :%s' % (channel, m))
            except Exception, e:
                return self.send_('PRIVMSG %s :%s' % (channel, e))
                
    def l_say(self, m, input, f_level=1):
        if input.level == 0:
            return self.msg(input.nick, m)
        elif input.level == 1:
            if f_level == 0:
                return self.msg(input.nick, m)
            elif f_level == 1:
                return self.say(m, input.channel)
            else:
                return self.say(m, 'all')
        else:
            return self.say(m, 'all')
        
    def ping_event(self, id):
        self.send_('PONG %s' % str(id))
        
    def mode(self, args):
        self.send_('MODE %s : %s' % (self.channel, args))
        
    def kick(self, nick):
        self.send_('KICK %s %s' % (self.channel, nick))
        
    def stop(self):
        self.quit()
        sys.exit()
        
    def whois(self, nick):
        return self.send_('WHOIS %s' % nick)
        
    def quit(self):
        self.send_('QUIT')
            
if __name__ == '__main__':
    print __doc__

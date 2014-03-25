#!/user/bin/env python
"""
Oracle 2.0 IRC Bot
irc.py

http://toofifty.me/oracle
"""

import socket, sys
import asynchat

# class Bot(asynchat.async_chat):
    # def __init__(self, nick, ident, channel, password=None):
        # asynchat.async_chat.__init__(self)
        # self.buffer = ''
        
        # self.nick = nick
        # self.ident = ident
        # self.channel = channel or []
        # self.password = password
        
    # def run(self, host, port=6667):
        # self.connect(host, port)
        
    # def start_connect(self, host, port):
        # self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.connect((host, port))
        # try: asyncore.loop()
        # except KeyboardInterrupt:
            # sys.exit()
            
class IRC(socket.socket):
    def __init__(self, nick, ident, channel, password=None):
        socket.socket.__init__(self)
        
        self.nick = nick
        self.ident = ident
        self.channel = channel or []
        self.password = password
        
    def init_connect(self, host, port):
        # we may need these for later
        self.host = host
        self.port = port
        
        try:
            self.connect((host, port))
            self.send("NICK %s\r\n" % self.nick)
            print("NICK %s\r\n" % self.nick)
            self.send("USER %s %s bla :BOT\r\n" % (self.ident, self.host))
            print("USER %s %s bla :BOT\r\n" % (self.ident, self.host))
        except Exception, e:
            print e
            
    def write(self, args, text=None):
        if text is not None:
            self.push((' '.join(args) + ' :' + text)[:500] + '\r\n')
        else:
            self.push(' '.join(args)[:500] + '\r\n')
        
    def join_channel(self, channel):
        self.send("JOIN %s" % channel)
            
    def msg(self, nick, m):
        self.send("PRIVMSG %s : %s\r\n" % (nick, m))
        return True
        
    def say(self, m):
        return self.msg(self.channel, m)
        
    def ping_event(self, id):
        self.send("PONG %s\r\n" % str(id))
        self.send("PONG " + str(id) + "\r\n")
        print('PONGED! %s' % str(id))
        
    def mode(self, args):
        self.send("MODE %s : %s\r\n" % (self.channel, args))
        
    def kick(self, nick):
        self.send("KICK %s %s\r\n" % (self.channel, nick))
        
    def stop(self):
        sys.exit()
        
            
if __name__ == "__main__":
    print __doc__

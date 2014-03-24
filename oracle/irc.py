#!/user/bin/env python
"""
Oracle 2.0 IRC Bot
irc.py

http://toofifty.me/oracle
"""

import socket
import asynchat

class Bot(asynchat.async_chat):
    def __init__(self, nick, ident, channel, password=None):
        asynchat.async_chat.__init__(self)
        self.buffer = ''
        
        self.nick = nick
        self.ident = ident
        self.channel = channel or []
        self.password = password
        
    def run(self, host, port=6667):
        self.connect(host, port)
        
    def start_connect(self, host, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        try: asyncore.loop()
        except KeyboardInterrupt:
            sys.exit()
            
    
            
if __name__ == "__main__":
    print __doc__
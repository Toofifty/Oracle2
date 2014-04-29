# -- coding: utf-8 --
"""
Oracle 2.0 IRC Bot
irc.py

http://toofifty.me/oracle
"""

import socket, sys
            
class IRC(socket.socket):
    """Main Socket Class
    
    Allows interaction with the IRC
    server through various means
    """
    def __init__(self, config):
        """Initialized the IRC socket as a
        socket, as well as assigning the
        config value to attributes.    
        """
        
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
        """Sends the text required.
        Use instead of 'send()' in order
        to print the message to console (if
        verbose) and apply necessary \r\n
        characters.
        
        @returns Boolean -> if sent        
        """
        
        if self.config.verbose:
            print '--> %s'% s.rstrip()
            return self.send('%s\r\n' % s) > 0
        else:
            return self.send('%s\r\n' % s) > 0
        
    def init_connect(self):
        """The initial connection process
        with the IRC server.
        Connects the socket to the host and port,
        and identifies a nick and user information.       
        """
        
        try:
            self.connect((self.host, self.port))
            self.set_nick(self.nick)
            self.send_('USER %s %s bla :BOT' % (self.ident, self.host))
        except Exception, e:
            print e
            
    def set_nick(self, nick):
        """Set nick.
        
        @returns Boolean -> if command sent
        """
        
        self.nick = nick
        return self.send_('NICK %s' % nick)
        
    def join_channels(self):
        """Join channels defined within
        config.channels        
        """
        
        for c in self.channels:
            self.join_channel(c)
            
    def join_channel(self, channel):
        """Join a specific channel.        
        """
        
        self.send_('JOIN %s' % channel)
        if not channel in self.channels:
            self.channels.append(channel)
            
    def msg(self, nick, m):
        """Send a private message to a user
        WITHOUT asking their client to open
        a new window. (Many do this, it's annoying)        
        """
        
        return self.send_('NOTICE %s :%s' % (nick, m))
            
    def pmsg(self, nick, m):
        """Send a private message to a user,
        which MAY cause their client to open
        a new window.
        """
        
        return self.send_('PRIVMSG %s :%s' % (nick, m))
        
    def say(self, m, channel=None):
        """Decide what channel(s) to send a message to,
        and format it to send the message (m) to the
        channel
        
        @return Boolean -> if messages were sent
        """
        
        # Loop through channels that we're in
        if channel == 'all':
            for c in self.channels:
                # Send the message to each individual channel
                self.send_('PRIVMSG %s :%s' % (c, m))
            return True
            
        else:
            # Channel is either that provided, or the default
            # channel within the config
            channel = channel or self.channels[0]
            try:
                return self.send_('PRIVMSG %s :%s' % (channel, m))
            except Exception, e:
                # Catch any error present within the message
                return self.send_('PRIVMSG %s :%s' % (channel, e))
                
    def l_say(self, m, input, f_level=1):
        """Logical 'say()'.
        Determine what level the user asked for
        ([0, quiet], [1, channel], [2, all])
        as well as what the command's default
        level is, and use this to send the 
        message accordingly.
        
        Also determines who to private message
        in the event that a MC server bot is used
        to send the message.
        
        @returns Boolean -> if message was sent
        """
        
        # Check if the message is from the game
        if input.game is not '':
        
            # Set nick to the bot that sent the message
            nick = input.game
            
            # If the input level is 0, we need to private
            # message the user a bit differently.
            if input.level == 0 or f_level == 0:
                m = input.nick + ' ' + m
        else:
            
            nick = input.nick
            
        # User is asking for a private message.
        # Private message is highest priority.
        if input.level == 0:
            if input.game is not '':
                return self.pmsg(nick, m)
            return self.msg(nick, m)
            
        # User isn't fussed on if the message is
        # private or not. Priority goes to
        # the function level.
        elif input.level == 1:
        
            # Function is supposed to be private.
            if f_level == 0:
                if input.game is not '':
                    return self.pmsg(nick, m)
                return self.msg(nick, m)
                
            # Function is supposed to go to the
            # channel.
            elif f_level == 1:
                return self.say(m, input.channel)
                
            # Function is supposed to be broadcast
            # to all channels.
            else:
                return self.say(m, 'all')
        
        # User wants their message to be broadcast
        # to all channels. This will be restricted to
        # moderator+ only in the future.
        else:
            return self.say(m, 'all')
        
    def ping_event(self, id):
        """Event called when the server pings the bot.
        Simply replies with the id given in the PING        
        
        @returns Boolean -> message sent
        """
        
        return self.send_('PONG %s' % str(id))
        
    def mode(self, args):
        """Set MODE args for the channel we're in.
        On second thought, this'll probably break.
        I'll fix it later.
        
        @returns Boolean -> message sent        
        """
        
        return self.send_('MODE %s : %s' % (self.channel, args))
        
    def kick(self, nick):
        """Kick a user from the channel we're in.
        Like above, I'll fix it later.
        
        @retuns Boolean -> message sent
        """
        
        return self.send_('KICK %s %s' % (self.channel, nick))
        
    def stop(self):
        """This kills the crab."""
        
        self.quit()
        sys.exit()
        
    def whois(self, nick):
        """Send a WHOIS message to the server.
        
        @returns Boolean -> message sent
        """
        
        return self.send_('WHOIS %s' % nick)
        
    def quit(self):
        """Very different to 'stop()', this only
        disconnects from the server.
        
        Just for whatever reason that we still need
        the bot running.
        
        @returns Boolean -> message sent
        """
        
        return self.send_('QUIT')
            
if __name__ == '__main__':
    print __doc__

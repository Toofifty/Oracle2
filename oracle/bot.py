#!/user/bin/env python
"""
Oracle 2.0 IRC Bot
bot.py

http://toofifty.me/oracle
"""

import string, sys
import irc, plugins

class Oracle(irc.IRC):
    def __init__(self, config):
        irc.IRC.__init__(self, config)
        self.config = config
        print sys.argv
        self.plugins = plugins.Loader(config)
        self.doc = {}
        self.setup()
        self.init_connect()
        
    def setup(self):
        pass
        
    def process(self, w):
        if self.config.verbose:
            print ' '.join(w)
            
        # PING event from server
        if 'PING' in w[0]:
            self.ping_event(''.join(w[1:]))
            return
            
        # End of MOTD
        if '376' in w[1] and self.config.nick in w[2]:
            if self.config.verbose:
                print 'Joining channel...'
            self.join_channels()
            return
            
        # NickServ asking for authentication
        if 'NickServ!' in w[1] and 'nickname' in w[4]:
            return
        
        # NAMES response
        if '353' in w[1]:
            return
        
        # End of NAMES list
        if '366' in w[1]:
            return
        
        # On bot join
        if 'JOIN' in w[1] and ":" + self.config.nick + "!" in w[0]:
            self.say("Never fear, %s is here!" % self.config.nick, w[2])
            return
            
        # MODE changes
        if 'MODE' in w[1]:
            return
        
        # MOTD messages
        if '372' in w[1]:
            return
            
        # End of things that can be done without a nick
        try:
            # Isolate nick from user string
            nick = w[0].split('!',1)[0].replace(':','')
        except Exception, e:
            print e
            
        if 'PART' in w[1]:
            return self.user_part_event(nick, w[2])
            
        if 'JOIN' in w[1]:
            return self.user_join_event(nick, w[2])
            
        if 'PRIVMSG' in w[1]:
            w[3] = w[3].replace(':', '', 1)
            
            if w[2] is not self.config.nick:
                return self.chat_event(nick, w[2], w[3:])
            else:
                return self.message_event(nick, ' '.join(w[3:]))
            
    def chat_event(self, nick, channel, message):
        print message
        if '.close' in message:
            sys.exit()
            
        input = Input(nick, channel, message)      
        
        if input.command.startswith(self.config.char):
            input.command = input.command.split('.', 1)[1]
            if self.plugins.process_command(self, input):
                pass
            else:
                self.msg(nick, 'Command not recognised!')
        else:
            return True
    
    def message_event(self, nick, message):
        pass
    
    def user_join_event(self, nick, channel):
        pass
    
    def user_part_event(self, nick, channel):
        pass
    
    def reload_modules(self, module=None):
        if module is None:
            return self.plugins.reload_all()
        return self.plugins.reload_module(module)
    
    def get_modules(self):
        return self.plugins.get_modules()
    
class Input:
    def __init__(self, nick, channel, message):
        self.nick = nick
        self.channel = channel
        self.command = message[0]
        if len(message[1:]) < 1:
            self.args = None
        else:
            self.args = message[1:]
    
class Configuration:
    def __init__(self):
        self.nick       = u'Oracle2'
        self.ident      = u'Oracle2'
        self.channels   = [u'#toofifty',
                           u'#toofiftyone',
                           u'#rapid']
        self.host = u'irc.esper.net'
        self.port = 6667
        
        self.verbose = True
        
        self.included = []
        self.excluded = []
        self.char = '.'
        
def main():

    config = Configuration()

    bot = Oracle(config)

    readbuffer = ''
    
    while True:
        try:
            readbuffer += bot.recv(32)
        except (KeyBoardInterrupt, SystemExit):
            print 'KeyBoardInterrupt'
            raise
        except Exception, e:
            print e
        
        temp = string.split(readbuffer, "\n")
        readbuffer = temp.pop()
        
        for line in temp:
            w = string.split(string.rstrip(line))
            
            bot.process(w)
            
                
if __name__ == "__main__":
    main()
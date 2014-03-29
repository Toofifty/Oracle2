#!/user/bin/env python
"""
Oracle 2.0 IRC Bot
bot.py

http://toofifty.me/oracle
"""

import string, sys, traceback
from optparse import OptionParser, OptionGroup
import irc, plugins

VERSION = '2.0.0a'

class Oracle(irc.IRC):
    """"""
    def __init__(self, config):
        """"""
        irc.IRC.__init__(self, config)
        self.config = config
        self.plugins = plugins.Loader(config)
        self.doc = {}
        self.setup()
        self.init_connect()
        
    def setup(self):
        """"""
        
    def process(self, w):
        """"""
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
        if 'NickServ!' in w[0] and 'nickname' in w[4]:
            self.send_('NICKSERV IDENTIFY %s %s\r\n'\
                       % (self.config.nick, self.config.password))
            return True
        
        # NAMES response
        if '353' in w[1]:
            return
        
        # End of NAMES list
        if '366' in w[1]:
            return
        
        # On bot join
        if 'JOIN' in w[1] and ":" + self.config.nick + "!" in w[0]:
            return self.bot_join_event(w[2])
            
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
        """"""
        
        def get_level(char):
            if char == self.config.char:
                return 1
            if char == self.config.prchar:
                return 0
            if char == self.config.puchar:
                return 2
        
        print '<%s(%s)>' % (nick, channel), ' '.join(message)            
        if nick != 'Toofifty':
            return False
                
        input = Input(nick, channel, message)
        
        charset = (self.config.char, self.config.prchar, self.config.puchar)
        
        for c in charset:
            if message[0].startswith(c):
                input.set_command(message[0].split(c, 1)[1])
                input.set_level(get_level(c))
                if not self.plugins.process_command(self, input):
                    self.l_say('Command failed to execute!', input, 0)
                    return True
        else:
            return True
    
    def message_event(self, nick, message):
        """"""
    
    def user_join_event(self, nick, channel):
        """"""
    
    def user_part_event(self, nick, channel):
        """"""
        
    def bot_join_event(self, chan):
        self.say(("Never fear, %s is here!" % self.config.nick), chan)
        return
    
    def reload_modules(self, input):
        """"""
        print 'Reloading modules...'
        if input.args is None:
            return self.plugins.reload_all(self, input)
        
        for m_s in input.args:
            m = self.plugins.get_module_from_string(m_s)
            if not m:
                self.l_say('%s is not a valid module, try modules.%s'\
                            % (m_s, m_s), input, 0)
                return False
            
            return self.plugins.reload_module(m, self, input)
        return True
    
    def get_char(self):
        return self.char
    
class Input:
    """"""
    def __init__(self, nick, channel, message):
        """"""
        self.nick = nick
        self.channel = channel
        self.command = None
        if len(message[1:]) < 1:
            self.args = None
        else:
            self.args = message[1:]
        self.level = 1
        
    def set_level(self, level):
        self.level = level
        
    def set_command(self, cmd):
        self.command = cmd
        
def parse_options():
    p = OptionParser(version='Version: %s' % VERSION)
    d = OptionGroup(p, 'Debug Options')
    i = OptionGroup(p, 'IRC Options')
    b = OptionGroup(p, 'Bot Options')
    
    d.add_option('-v', '--verbose', action='store_true', dest='verbose',
                 default=False, 
                 help='output absolutely everything                     '
                      'default: %default')
    
    d.add_option('-q', '--quiet', action='store_false', dest='verbose',
                 help='output only the important things')
    
    i.add_option('-c', '--channel', action='append', type='string', 
                 dest='channels', default=['#toofifty'],
                 help='add a channel for the bot to connect to on join\n'
                      'default: %default')
    
    i.add_option('--port', action='store', type='int', dest='port', 
                 default=6667, 
                 help='change the port to connect to the server on      '
                      'default: %default')
    
    i.add_option('-s', '--server', '--host', action='store', type='string', 
                 dest='host', default='irc.esper.net', 
                 help='change the host/server to connect to             '
                      'default: %default')
    
    b.add_option('-a', '--incl-module', action='append', type='string', 
                 dest='included', default=[],
                 help='add a module to the inclusions list, overrides config')
    
    b.add_option('-r', '--excl-module', action='append', type='string', 
                 dest='excluded', default=[],
                 help='add a module to the exclusions list, overrides config')
    
    b.add_option('--char', action='store', type='string', dest='char', 
                 default='.',
                 help='change the character used to access bot commands\n'
                      'default: %default')
    b.add_option('--private-char', action='store', type='string',
                 dest='prchar',  default='!',
                 help='change the character used to access bot commands '
                      'and receive private responses                    '
                      'default: %default')
    b.add_option('--public-char', action='store', type='string', dest='puchar', 
                 default='?',
                 help='change the character used to access bot commands '
                      'and receive public responses (admin only)        '
                      'default: %default')
    i.add_option('-n', '--nick', action='store', type='string', 
                 dest='nick', default='Oracle',
                 help='change the nick the bot uses                     '
                      'default: %default')
    i.add_option('-p', '--password', action='store', type='string', 
                 dest='password',
                 help='change the password the bot uses to identify to '
                      'chanserv with')
    i.add_option('-i', '--ident', action='store', type='string', dest='ident',
                 default='Oracle',
                 help='change the ident the bot uses to connect         '
                      'default: %default')
    
    p.add_option_group(d)
    p.add_option_group(i)
    p.add_option_group(b)
    return p.parse_args()
        
def main():
    """"""

    config, args = parse_options()

    bot = Oracle(config)

    readbuffer = ''
    
    while True:
        try:
            readbuffer += bot.recv(32)
        except (SystemExit):
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
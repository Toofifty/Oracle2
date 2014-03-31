#!/user/bin/env python
"""
Oracle 2.0 IRC Bot
bot.py

http://toofifty.me/oracle
"""

import string, sys, traceback, os
from optparse import OptionParser, OptionGroup
import irc, plugins, user

VERSION = '2.0.1a'

class Oracle(irc.IRC):
    """Main Bot Class
    
    Decodes messages and performs certain events
    depending on their nature.
    """
    def __init__(self, config):
        """Initializes the bot with the IRC
        socket class. Also assigns it a plugin
        loader, and tries to connect to the
        server.
        
        returns None
        """
        irc.IRC.__init__(self, config)
        self.config = config
        self.plugins = plugins.Loader(config)
        self.users = {}
        self.init_connect()
        
    def process(self, w):
        """Processes a raw message from the server.
        Used to discern:
            - PRIVMSGs
            - PINGs
            - JOINs
            - MODEs
            - PARTs
            - NICKs
            - End of MOTD
            - NickServ asking for auth
            - NAMES response
            - WHOIS response
            - JOIN of bot
            
        And sends the messages to the respective
        functions.
        
        returns Boolean        
        """
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
        
        # WHOIS - 'User' :is logged in as
        if '330' in w[1]:
            try:
                if not self.users.has_key(w[3]):
                    self.users[w[3]] = user.User(w[4])
                    self.users[w[3]].set_nick(w[3])
            except:
                traceback.print_exc()
            return True
        
        #################################################
        # End of things that can be done without a nick #
        #################################################
        try:
            # Isolate nick from user string
            nick = w[0].split('!',1)[0].replace(':','')
        except Exception, e:
            return
        
        if 'INVITE' in w[1]:
            return self.bot_invite_event(nick, w[3])
            
        if 'PART' in w[1]:
            return self.user_part_event(nick, w[2])
            
        if 'JOIN' in w[1]:
            return self.user_join_event(nick, w[2])
        
        if 'NICK' in w[1]:
            return self.user_nick_event(nick, w[2])
            
        if 'PRIVMSG' in w[1]:
            w[3] = w[3].replace(':', '', 1)
            
            if w[2] is not self.config.nick:
                return self.chat_event(nick, w[2], w[3:])
            else:
                return self.message_event(nick, ' '.join(w[3:]))
            
    def chat_event(self, nick, channel, message):
        """Chat event called by 'PRIVMSG channel'.
        Checks if the message is a command and
        sends it to the command processor at
        self.plugins
        
        returns Boolean
        """
        
        def get_level(char):
            """Gets the privacy level of char
            
            returns int -> 0-2, 0 being most private
            """
            if char == self.config.char:
                return 1
            if char == self.config.prchar:
                return 0
            if char == self.config.puchar:
                return 2
                
        input = Input(nick, channel, message)
        
        input.set_user(self.get_user(nick))
        
        print '<%s(%s)>' % (nick, channel), ' '.join(message)            
        
        if 'https://www.youtube.com/watch?v' in ' '.join(message):
            input.set_command('parselink')
            input.set_level(1)
            input.args = []
            # Handle multiple links
            for word in message:
                if 'https://www.youtube.com/' in word:
                    input.args.append(word)                    
            self.plugins.process_command(self, input)
        
        if nick != 'Toofifty' and nick != 'Oracle' and nick != 'Manyman':
            return False
        
        charset = (self.config.char, self.config.prchar, self.config.puchar)
        
        for c in charset:
            if message[0].startswith(c):
                input.set_command(message[0].split(c, 1)[1])
                input.set_level(get_level(c))
                self.plugins.process_command(self, input)
        else:
            return True
    
    def message_event(self, nick, message):
        """Message event called by 'PRIVMSG self'."""
        print '<%s(NOTICE)>' % (nick), ' '.join(message)
    
    def user_join_event(self, nick, channel):
        """User join event called by 'JOIN user'."""
        self.whois(nick)
    
    def user_part_event(self, nick, channel):
        """User part event called by 'PART user'."""
        if self.users.has_key(nick):
            self.users[nick].part()
            
    def user_nick_event(self, nick, new_nick):
        """User nick change event called by 'NICK user'."""
        
    def bot_join_event(self, chan):
        """Bot join event called by 'JOIN self'."""
        self.say(("Never fear, %s is here!" % self.config.nick), chan)
        return
    
    def bot_invite_event(self, nick, chan):
        """Invite event called by 'INVITE self'."""
        print nick, 'has invited me to', chan
        self.join_channel(chan)
        return
    
    def exit(self):
        """Bot exit event called by .restart and .close
        Ensures saving of user files among other things
        (to be added later)
        """
        for u in self.users:
            self.users[u].part()
        self.quit()
    
    def reload_modules(self, input):
        """Reload modules within self.plugins.
        Used when called by the command '.reload'
        
        returns Boolean
        """
        print 'Reloading modules...'
        if input.args is None:
            return self.plugins.reload_all(self, input)
        
        for m_s in input.args:
            try:
                m = self.plugins.get_module_from_string(m_s)
            except KeyError:
                self.l_say('%s is not a valid module, try modules.%s'\
                            % (m_s, m_s), input, 0)
                return False
            
            return self.plugins.reload_module(m, self, input)
        return True
    
    def get_char(self):
        """returns string -> self.char
        """
        return self.char
    
    def open_user(self, name):
        """Opens a new user class - in order
        to not need upper-level imports in the
        modules.
        
        returns user.User()
        """
        return user.User(name)
    
    def get_user(self, nick):
        """Tries to grab a user from self.users
        if none are found, creates a new one
        
        returns user.User()
        """
        PATH = os.path.join('..', 'files', 'users')
        
        try:
            return self.users[nick]
        except KeyError:
            if nick + '.json' in os.listdir(PATH):
                self.users[nick] = self.open_user(nick)
                return self.users[nick]
            else:
                return False
        
    def try_create_user(self, nick):
        """Tries to grab a user from self.users
        if none are found, creates a new one
        
        returns user.User()
        """
        try:
            return self.users[nick]
        except KeyError:
            self.users[nick] = self.open_user(nick)
            return self.users[nick]
        
    
    def get_version(self):
        """Version getter
        
        returns String -> VERSION
        """
        return VERSION
    
class Input(object):
    """Input class
    Bundles input information into an object to
    be sent around through functions and commands.
    """
    def __init__(self, nick, channel, message):
        """Initialize a new set of input"""
        self.nick = nick
        self.channel = channel
        self.command = None
        if len(message[1:]) < 1:
            self.args = None
        else:
            self.args = message[1:]
        self.level = 1
        self.user = None
        
    def set_level(self, level):
        """Set the privacy level of the input"""
        self.level = level
        return self.level
        
    def set_command(self, cmd):
        """Set the command of the input"""
        self.command = cmd
        return self.command
    
    def set_user(self, user):
        """Set the user class of the input"""
        self.user = user
        return self.user
        
def parse_options():
    """Parse options from the console using
    optparse's OptionParser
    """
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
    """Main Bot Loop
    Initializes first classes, and loops over
    reading a buffer to generate lines to be
    processed in bot.process
    """

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
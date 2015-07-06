"""
Oracle 2.0 IRC Bot
help.py plugin module

http://toofifty.me/oracle
"""

import types, inspect
import traceback
import math
import time

from format import WHITE, CYAN, GREY, PURPLE

def _init(bot):
    print '\t%s loaded' % __name__

# All commands are called with the arguments
# <module>.<command>(plugins.Loader(), bot.Oracle(), bot.Input())
# In all other plugins, these are abbreviated to l, b, i
def help(loader, bot, input):
    """Print the command usage and other
    help to the user
    """

    BASE = CYAN
    BRKT = PURPLE
    FILL = GREY

    help_dict = {}

    def s(str):
        return bot.l_say(str, input, 0)

    def append_cmd(cmd, desc):
        if cmd is '': return
        if desc is '': return #desc = ''

        help_dict[cmd] = desc

    def parse_child(function, doc):
        u_rank = input.user.get_rank()
        # First line is '!parent-command'
        doc = doc.split('\n')[1:]

        c = d = a = r = ''

        for line in doc:
            line = line.strip(' ')

            # Command
            if line.startswith('!c '):
                c = line.replace('!c ', '').upper()

            # Description
            elif line.startswith('!d '):
                d = line.replace('!d ', '').capitalize()

            # Arguments
            elif line.startswith('!a '):
                a = line.replace('!a ', '').upper()

            # Rank
            # ALL child commands NEED a rank to
            # be processed.
            elif line.startswith('!r '):
                str = line.replace('!r ', '')
                r = loader.get_rank_from_string(str)

                # Don't add to help dict
                if not u_rank >= r:
                    continue

                # Add them all together and append
                cmd = function.__name__.upper()
                cmd += ' ' + c + ' ' + a

                append_cmd(cmd.upper(), d)

                # Reset values
                c = d = a = r = ''
                continue

    def parse_doc(function):
        u_rank = input.user.get_rank()
        doc = inspect.getdoc(function)
        c_rank = 0
        a = r = d = ''

        if doc is not None:
            if '!parent-command' in doc:
                parse_child(function, doc)
                return

            for line in doc.split('\n'):

                # Description
                if line.startswith('!d '):
                    d = line.replace('!d ', '').capitalize()

                # Command
                elif line.startswith('!a '):
                    a = line.replace('!a ', '').upper()

                # Rank
                elif line.startswith('!r '):
                    str = line.replace('!r ', '')
                    r = loader.get_rank_from_string(str)
                    if not u_rank >= r:
                        return

            cmd = function.__name__.upper()
            if a != '':
                cmd += ' ' + a

            # Append
            append_cmd(cmd, d)

    def print_line(cmd, desc):
        margin = 25

        # Ensure the command exists
        # Description doesn't matter as much.
        if cmd is None: return
        if desc is None: desc = ''

        cmdlen = len(cmd)

        # Game has different kerning, so aligning
        # the message wouldn't look right.
        if input.game == '':
            cmd = cmd.ljust(margin)
        cmd = cmd.replace('<',BRKT+'<'+FILL).replace('>',BRKT+'>'+BASE)
        cmd = cmd.replace('[',BRKT+'['+FILL).replace(']',BRKT+']'+BASE)
        cmd = cmd.replace('...',BRKT+'...'+BASE)

        # Say the line to the user.
        if cmdlen > margin and input.game == '':
            s(BASE + cmd)
            cmd = ' '.ljust(margin)
        return s('%s - %s' % (BASE + cmd, FILL + desc))

    def get_page_count():
        return math.ceil(len(help_dict) / 10.0)

    def print_help(page):
        max_page = get_page_count()

        if page > max_page:
            page = max_page
        elif page < 1:
            page = 1

        if input.game != '':
            s('%s================ Page: %d/%d ================' % (PURPLE, page, max_page))
            s('\t')
        else:
            s('%s< Page %d/%d >' % (PURPLE, page, max_page))

        # 10 per page
        start = 10 * page - 10
        end = start + 10
        count = 0

        # Iter through commands
        for k, v in sorted(help_dict.iteritems()):
            if count >= start and count < end:
                print_line(k, v)
            count += 1


        if input.game != '':
            s('\t')
            s('%s=========================================' % PURPLE)
        else:
            s('%s< End Page >' % PURPLE)

        return True

    def print_all(page):
        for m in loader.get_modules():
            func_list = [getattr(m, a, None) for a in dir(m)
                         if isinstance(getattr(m, a, None),
                                       types.FunctionType)]
            for func in func_list:
                if not func.__name__.startswith('_'):
                    parse_doc(func)

        page = 1
        try:
            page = int(input.args[1])
        except IndexError:
            pass

        print_help(page)

        return True

    def print_oracle_help():
        # Max length is 25 lines
        help_text1 = [
            '<- $nick$ Master Guide ->',
            '\t',
            'COMMAND Usage:',
            '  <angle brackets>  |  Required arguments.',
            '  [square brackets] |  Optional arguments.',
            '  option1|option2   |  Use one of the arguments shown.',
            '  ellipses ...      |  Arguments that allow multiple ',
            '                    |  words, separated by spaces.',
            '  ',
            'Helpful Tip:',
            '  - Use /invite $nick$ <#channel> to automatically bring $nick$ into',
            '    your channel.',
            '  ',
            'Suggestions / bugs:',
            '  Please report these either directly to Toofifty or the GitHub issue',
            '  tracker located at https://github.com/Toofifty/Oracle2/issues',
            '  ',
            'CHANGELOG:',
            '  30/07/2014',
            '    > Added commands: .help all|oracle , .reddit',
            '    > Fixed some command definitions',
            '    > Began changelog',
            '  ',
            'CURRENT BUGS:',
            '  - Bot does not authenticate with NickServ',
        ]
        help_text2 = [
            '  - Trivia is not broadcasted into invitee channels',
            '  ',
            'TO DO LIST:',
            '  - Mock language converters',
            '  - .help search',
            '  - .graph',
            '  - Colour %s.help oracle' % PURPLE,
        ]

        [s(line) for line in help_text1]
        time.sleep(5)
        [s(line) for line in help_text2]

        return True

    try:

        # User might ask for categories
        if input.args is not None:
            if input.args[0] == 'categories':
                return categories(loader, bot, input)
            elif input.args[0] == bot.nick.lower():
                return print_oracle_help()
            elif input.args[0] == 'all':
                page = 1
                try:
                    page = int(input.args[1])
                except IndexError:
                    pass
                return print_all(page)

        # Grab the module from the laoded modules
        # This will throw a KeyError if no module is found,
        # and so it will print the default help message
        mod = loader.get_module_from_string('modules.%s' % input.args[0])
        func_list = [getattr(mod, a, None) for a in dir(mod)
                     if isinstance(getattr(mod, a, None),
                                   types.FunctionType)]
        for func in func_list:
            if not func.__name__.startswith('_'):
                parse_doc(func)

        page = 1
        try:
            page = int(input.args[1])
        except IndexError:
            pass

        print_help(page)

        return True

    except (KeyError, TypeError):

        # Try to see if the query is a function of its
        # own, and not a module
        if input.args is not None:

            # Let's assume the arg is bad
            bad_arg = True

            for m in loader.get_modules():

                if hasattr(m, input.args[0]):
                    bad_arg = False
                    func = getattr(m, input.args[0])
                    parse_doc(func)

            if not bad_arg:
                print_help(1)
                return True

            else:
                s('%sUnknown argument: %s%s%s.\n\t'
                  % (WHITE, PURPLE, input.args[0], WHITE))

        # Can't find the query anywhere, so we'll
        # print the default help message
        if input.game != '':
            s('%s=========================================' % PURPLE)
            s('\t')
        s('Welcome to the $nick$ help guide!')
        s('\t')
        s('%sHELP %susage:' % (PURPLE, WHITE))
        s('\t%s.help' % CYAN)
        s('\t%s.help $nick.lower()$' % CYAN)
        s('\t%s.help %s<%scategory%s> [%spage%s]'
          % (CYAN, WHITE, GREY, WHITE, GREY, WHITE))
        s('\t%s.help %s<%scommand%s>' % (CYAN, WHITE, GREY, WHITE))
        s('\t%s.help search %s<%sphrase...%s> [%spage%s]'
          % (CYAN, WHITE, GREY, WHITE, GREY, WHITE))
        s('\t%s.help all %s[%spage%s]' % (CYAN, WHITE, GREY, WHITE))
        s('\t')
        s('Categories can be listed with')
        s('the %s.categories%s command.' % (CYAN, WHITE))
        if input.game != '':
            s('\t')
            s('%s=========================================' % PURPLE)
        return True

    except:
        traceback.print_exc()

def categories(l, b, i):
    """
    !d List loaded modules
    !r user
    """
    restricted = [
            'modules.admin',
            'modules.format',
            'modules.log',
            'modules.input',
        ]

    message = []
    for m in l.get_modules_list():
        if not m in restricted:
            message.append(m.replace('modules.','').capitalize())
    b.l_say('%sCategories: %s%s' % (CYAN, PURPLE,
                (WHITE+', '+PURPLE).join(message)), i, 0)
    return True


def cats(l, b, i):
    """
    !d Alias for .categories
    !r user
    """
    return categories(l, b, i)

def version(l, b, i):
    """
    !d Get the version of Oracle bot
    !r user
    """
    return b.l_say('Oracle Version %s' % b.get_version(), i, 0)

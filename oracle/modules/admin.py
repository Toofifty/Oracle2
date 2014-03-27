import sys, os

def init():
    print '    admin module loaded'
    
def reload(l, bot, input):
    if input.args is None:
        bot.reload_modules()
    else:
        bot.reload_modules(input.args[0])
    bot.msg(input.nick, 'Modules reloaded')
    return True
    
def modules(l, bot, input):
    for m in bot.get_modules():
        bot.msg(input.nick, m.capitalize())
    return True

def close(l, bot, input):
    bot.say('Goodbye!', channel='all')
    sys.exit()
    
def restart(l, bot, input):
    bot.say('I\'ll be back in a jiffy!', channel='all')
    bot.quit()
    
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)
    
if __name__ == '__main__':
    print __doc__
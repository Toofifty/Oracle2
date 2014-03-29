import sys, os, subprocess
import traceback

def init():
    print '\t%s loaded' % __name__
    
def reload(l, bot, input):
    if input.args is None:
        bot.reload_modules()
        bot.msg(input.nick, 'Module(s) reloaded')
    else:
        if bot.reload_modules(input.nick, input.args):
            bot.msg(input.nick, 'Module(s) reloaded')
    return True
    
def modules(l, bot, input):
    for m in bot.get_modules():
        bot.msg(input.nick, m.capitalize())
    return True

def close(l, bot, input):
    bot.say('Goodbye!', channel='all')
    bot.quit()
    sys.exit()
    
def restart(l, bot, input):
    bot.say('I\'ll be back in a jiffy!', channel='all')
    bot.quit()
    print '\n' * 5
    
    args = sys.argv[:]
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)
    
def open(l, bot, input):
    bot.msg(input.nick, 'Opening %s' % '\\'.join(input.args))
    try:
        subprocess.Popen(r'explorer /select, "%s"' % '\\'.join(input.args))
    except:
        tracepack.print_exc()
    return True
    
if __name__ == '__main__':
    print __doc__
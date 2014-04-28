import random
from format import CYAN

def _init(bot):
    print '\t%s loaded' % __name__
    
def pick(l, b, i):
    """
    !d Pick an option from a list (separated by a space)
    !a [options...]
    !r user
    """
    if len(i.args) < 2:
        b.l_say('Usage: %s.pick [option1] [option2] ...' % CYAN, i, 0)
        return True
    choice = random.randint(1, len(i.args)) - 1
    b.l_say('%s: %s' % (i.nick, i.args[choice]), i, 1)
    return True
    
def nether(l, b, i):
    """
    !d Overworld coordinates - Nether conversion
    !a [x] <y> [z]
    !r user
    """
    def usage():
        b.l_say('Usage: %s.nether [x] [y] [z]' % CYAN, i, 0)

    if len(i.args) < 2:
        usage()
    elif len(i.args) == 2:
        try:
            x = math.floor(float(i.args[0]) / 8)
            z = math.floor(float(i.args[1]) / 8)
            b.l_say('Nether co-ords: %dx, %dz' % (x, z), i, 0)
        except:
            usage()
    else:
        try:
            x = math.floor(float(i.args[0]) / 8)
            y = i.args[1]
            z = math.floor(float(i.args[2]) / 8)
            b.l_say('Nether co-ords: %dx, %dy, %dz' % (x, y, z), i, 0)
        except:
            usage()
    return True         

def overworld(l, b, i):
    """
    !d Nether coordinates - Overworld conversion
    !a [x] <y> [z]
    !r user
    """
    def usage():
        b.l_say('Usage: %s.overworld [x] [y] [z]' % CYAN, i, 0)

    if len(i.args) < 2:
        usage()
    elif len(i.args) == 2:
        try:
            x = math.floor(float(i.args[0]) * 8)
            z = math.floor(float(i.args[1]) * 8)
            b.l_say('Overworld co-ords: %dx, %dz' % (x, z), i, 0)
        except:
            usage()
    else:
        try:
            x = math.floor(float(i.args[0]) * 8)
            y = i.args[1]
            z = math.floor(float(i.args[2]) * 8)
            b.l_say('Overworld co-ords: %dx, %dy, %dz' % (x, y, z), i, 0)
        except:
            usage()
    return True   
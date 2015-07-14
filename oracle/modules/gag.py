def _init(b):
    print '\t%s loaded' % __name__

def flog(l, b, i):
    """
    !d flog!
    !r user
    """
    b.l_say(':flog', i)
    return True

def flip(l, b, i):
    """
    !d flip!
    !r user
    """
    if len(i.args) == 0:
        return True
    b.l_say(':flip %s' % ' '.join(i.args).encode('ascii', 'ignore'), i)
    return True

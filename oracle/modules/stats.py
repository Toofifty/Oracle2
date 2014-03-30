"""
Oracle 2.0 IRC Bot
stats.py plugin module

http://toofifty.me/oracle
"""

import os, traceback

def init():
    print '\t%s loaded' % __name__
    
def seen(l, b, i):
    """
    !d Return the last time the user was seen by Oracle
    !a [user]
    !r user
    """
    if i.args is None:
        b.l_say('Usage: .seen [user]', i, 0)
        return True
    else:
        seen = None
        try:
            seen = b.users[i.args[0]].get_seen()
        except KeyError:
            for f in os.listdir(os.path.join('..', 'files', 'users')):
                try:
                    print f
                    f = f.replace('.json', '')
                    # Hehe, flower
                    print f
                    if f.lower() == i.args[0].lower():
                        seen = b.open_user(f).get_seen()
                except KeyError:
                    continue
                
        if seen is not None:
            b.l_say('Last seen: %s' % seen, i, 0)
        else:
            b.l_say('User %s not found in the database.' % i.args[0],
                       i, 0)
        return True
        
def listusers(l, b, i):
    """
    !d List all users who have files
    !r user
    """
    b.l_say('Users:', i, 0)
    for f in os.listdir(os.path.join('..', 'files', 'users')):
        b.l_say('    %s' % f.replace('.json', ''), i, 0)
    return True

def score(l, b, i):
    """!parent-command
    !c top
        !d Access the score boards
        !a [top] <amount>
        !r user
    !c check
        !d Check your score
        !r user
    !c peek
        !d Check a user's score
        !a [user]
        !r admin
    !c set
        !d Set a user's score
        !a [user] [points]
        !r admin
    !c add
        !d Add an amount to a user's score
        !a [user] [amount]
        !r admin
    !c rem
        !d Remove an amount from a user's score
        !a [user] [amount]
        !r admin
    """
    def top(l, b, i):
        pass
        
    def check(l, b, i):
        pass
        
    def peek(l, b, i):
        pass
        
    def set(l, b, i):
        pass
        
    def add(l, b, i):
        pass
        
    def rem(l, b, i):
        pass
    
    # CHILD COMMAND CONSTRUCTOR
    try:
        getattr(score, input.args[0])(l, b, i)
    except Exception, e:
        traceback.print_exc()
        b.l_say('Usage: .score [top|check]', i, 0)
    
    
    
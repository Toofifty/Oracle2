"""
Oracle 2.0 IRC Bot
stats.py plugin module

http://toofifty.me/oracle
"""

import os, inspect, traceback

from format import CYAN, WHITE, GREY, PURPLE, RED, GREEN, _random

def _init(bot):
    print '\t%s loaded' % __name__
    
def seen(l, b, i):
    """
    !d Return the last time the user was seen by Oracle
    !a [user]
    !r user
    """
    if i.args is None:
        b.l_say('Usage: %s.seen [user]' % CYAN, i, 0)
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
            b.l_say('Last seen: %s' % PURPLE + seen, i, 0)
        else:
            b.l_say('User %s not found in the database.' % (GREY + i.args[0] + WHITE),
                       i, 0)
        return True
        
def listusers(l, b, i):
    """
    !d List all users who have files
    !r user
    """
    b.l_say('Users:', i, 0)
    for f in os.listdir(os.path.join('..', 'files', 'users')):
        b.l_say('    %s' % (_random() + f.replace('.json', '')), i, 0)
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
        !r moderator
    !c set
        !d Set a user's score
        !a [user] [points]
        !r administrator
    !c add
        !d Add an amount to a user's score
        !a [user] [amount]
        !r administrator
    !c rem
        !d Remove an amount from a user's score
        !a [user] [amount]
        !r administrator
    """
    
    PATH = os.path.join('..', 'files', 'users')
    
    def top(l, b, i):
        all_scores = {}
        for file in os.listdir(PATH):
            name = file.replace('.json', '')
            all_scores[name] = b.get_user(name).get_points()
        sorted_scores = sorted(all_scores.iteritems(), key = op.itemgetter(1),
                               reverse = True)
        amount = int(i.args[1]) if len(i.args) > 1 else 5
        n = 1
        for line in sorted_scores:
            b.l_say('%s%s%s. %s - %s%s' % (CYAN, str(n), WHITE, line[0], 
                                           GREEN, str(int(line[1]))), 
                    i, 0)
            n += 1
            if n > amount: break
        return True
        
    def check(l, b, i):
        n = i.nick
        if not n + '.json' in os.listdir(PATH):
            return b.l_say('%sYou don\'t seem to have a user file - make one '
                           'by rejoining the IRC channel.' % RED, i, 0)
        user = b.get_user(n)
        return b.l_say('You have %s%d%s points.' % (GREEN, user.get_points(), WHITE), i, 0)
        return b.l_say('You have %s%d%s points.' % (GREEN, user.get_points(),
                                                    WHITE), i, 0)
        
    def peek(l, b, i):
        n = i.args[1]
        if not n + '.json' in os.listdir(PATH):
            return b.l_say('%s does not seem to have a user file.' % (GREY + n + WHITE), i, 0)
        user = b.get_user(n)
        b.l_say('%s has %s%d%s points.' % (GREY+user.get_name()+WHITE, GREEN, user.get_points(), WHITE), i, 0)
        
    def set(l, b, i):
        pass
        
    def add(l, b, i):
        pass
        
    def rem(l, b, i):
        pass
            return b.l_say('%s does not seem to have a user file.'\
                           % (GREY + n + WHITE), i, 0)
        user = b.get_user(n)
        b.l_say('%s has %s%d%s points.' % (GREY+user.get_name()+WHITE, GREEN,
                                           user.get_points(), WHITE), i, 0)
        
    def set(l, b, i):
        if len(i.args) > 2:
            user = b.get_user(i.args[1])
            if not user:
                b.l_say('No user found for that name.')
                return True
            p = user.set_points(int(i.args[2]))
            b.l_say('%s%s%s now has %s%d%s points' % (GREY, i.args[1], WHITE,
                                                      GREEN, p, WHITE), i, 0)
            return True
        
    def add(l, b, i):
        if len(i.args) > 2:
            user = b.get_user(i.args[1])
            if not user:
                b.l_say('No user found for that name.')
                return True
            p = user.add_points(int(i.args[2]))
            b.l_say('%s%s%s now has %s%d%s points' % (GREY, i.args[1], WHITE,
                                                      GREEN, p, WHITE), i, 0)
            return True
        
    def rem(l, b, i):
        if len(i.args) > 2:
            user = b.get_user(i.args[1])
            if not user:
                b.l_say('No user found for that name.')
                return True
            p = user.add_points(-1 * int(i.args[2]))
            b.l_say('%s%s%s now has %s%d%s points' % (GREY, i.args[1], WHITE,
                                                      GREEN, p, WHITE), i, 0)
            return True
    
    # CHILD COMMAND CONSTRUCTOR
    # Copy/paste-able :)
    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        b.l_say('Usage: %s.score [top|check]' % CYAN, i, 0)
    return True
    
def commandcount(l, b, i):
    """
    !d Get the amount of commands a user has performed
    !a <user>
    !r user
    """
    if i.args is None:
        b.l_say('Commands sent by you: %s%d' % (PURPLE, i.user.get_commands()), i, 0)
    else:
        u = b.get_user(i.args[0])
        if u:
            b.l_say('Commands sent by %s: %s%d' % (GREY+u.get_name()+WHITE, PURPLE, u.get_commands()), i, 0)
        else:
            b.l_say('No user found under the name "%s".' % (GREY+i.args[0]+WHITE), i, 0)
    return True
    
def cmdcount(l, b, i):
    """
    !d Alias for .commandcount
    !a <user>
    !r user
    """
    return commandcount(l, b, i)
    

"""
Oracle 2.0 IRC Bot
reddit.py plugin module

http://toofifty.me/oracle
"""

import praw

USER_AGENT = ('Oracle IRC link grabber script '
              'by /u/Toofifty')
REDDIT = None

def _init(bot):
    global REDDIT
    REDDIT = praw.Reddit(user_agent=USER_AGENT)
    print '\t%s loaded' % __name__
    
def parsereddit(l, b, i):
    if i.args > 0:
        if i.args[0].startswith('http://www.reddit.com/'):
            global REDDIT
            print REDDIT
            for thing in REDDIT.get_content(i.args[0]):
                if isinstance(thing, praw.objects.Submission):
                    print thing
                    b.l_say(thing.short_link, i, 0)
                else:
                    print thing
                
        else:
            b.l_say('Please provide a Reddit link.', i, 0)            
    else:
        b.l_say('Usage: .parsereddit [link] <link2> ...', i, 0)
    return True
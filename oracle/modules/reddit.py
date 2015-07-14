"""
Oracle 2.0 IRC Bot
reddit.py plugin module

http://toofifty.me/oracle
"""

import urllib, json
from format import BOLD, RESET

def _init(bot):
    print '\t%s loaded' % __name__

def parsereddit(l, b, i):
    """
    !d Parse a Reddit link into it's information
    !a <link>
    !r user
    """
    def parselink(link):
        meta_data_link = link + '.json'
        tables = urllib.urlopen(meta_data_link)
        data = json.loads(tables.read())[0]['data']['children'][0]['data']

        title = data['title']
        author = data['author']
        subreddit = data['subreddit']
        score = data['score']
        comments = data['num_comments']

        mod_status = ' [M]' if data['distinguished'] == 'moderator' else ''
        sticky_status = ' [sticky]' if data['stickied'] else ''

        b.l_say(
            'Reddit post: %s%s%s%s by %s%s%s' % (
                BOLD, title, sticky_status, RESET, BOLD, author, mod_status
            ), i
        )
        b.l_say(
            'Subreddit: %s | Score: %s | Comments: %s' \
            % (subreddit, score, comments), i
        )

    if i.args > 0:
        for link in i.args:
            if '.reddit.com/' in i.args[0].lower():
                parselink(i.args[0].lower())

    else:
        b.l_say('Usage: .parsereddit <link>', i, 0)
    return True


def reddit(l, b, i):
    """
    !d Alias for .parsereddit
    !a <link>
    !r user
    """
    return parsereddit(l, b, i)


def _chat(bot, args):
    n, c, m = args
    if '.reddit.com/' in ' '.join(m):
        input = bot.new_input(n, c, m)
        # Treat input as a command.
        input.set_command('parsereddit')
        input.set_level(1)
        input.set_user(bot.get_user(n))
        input.args = []
        # Handle multiple links
        for word in m:
            if '.reddit.com/' in word:
                input.args.append(word)
        bot.plugins.process_command(bot, input)

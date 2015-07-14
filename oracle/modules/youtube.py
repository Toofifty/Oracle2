"""
Oracle 2.0 IRC Bot
youtube.py plugin module

http://toofifty.me/oracle
"""

import urllib, json
from datetime import datetime

from format import GREEN, RED, BLUE, WHITE, BOLD, ITALICS, RESET

def _init(bot):
    print '\t%s loaded' % __name__

def fullparseyoutube(l, b, i):
    """
    !d Get the full metadata sample from a YouTube link
    !a <link>
    !r developer
    """
    if i.args is not None:
        vidid = i.args[0]
        b.l_say('Getting data for %s' % vidid, i, 0)
        if vidid.startswith('http'):
            vidid = vidid.split('&')[0]
            vidid = vidid.split('=')[1]

        api_key = 'AIzaSyABEUwRK3ZqlkMXSG7Nw9TdZxI3slGLdnM'
        meta_data_link = ('https://www.googleapis.com/youtube/v3/videos?key=%s&part=snippet&id=%s' % (api_key, vidid))
        tables = urllib.urlopen(meta_data_link)
        meta_data = json.loads(tables.read())
        print meta_data
        for m in meta_data:
            b.l_say(m, i, 0)
            print m
            for thing in meta_data[m]:
                try:
                    print thing
                    b.l_say(thing, i, 0)
                except KeyError:
                    print 'KeyError'
    else:
        b.l_say('Usage: fullparselink [vidid] [value]', i, 0)

    return True

def parseyoutube(l, b, i):
    """
    !d Parse one or more YouTube links
    !a <link> [links...]
    !r user
    """
    def parsevid(vidid):
        api_key = 'AIzaSyABEUwRK3ZqlkMXSG7Nw9TdZxI3slGLdnM'
        meta_data_link = ('https://www.googleapis.com/youtube/v3/videos?key=%s&part=snippet&id=%s' % (api_key, vidid))

        tables = urllib.urlopen(meta_data_link)
        data = json.loads(tables.read())['items'][0]['snippet']
        print data

        title = data['title']
        description = data['description'].replace('\n', ' ')
        if description == '':
            description = 'No description available.'
        author = data['channelTitle']
        published = data['publishedAt'].split('T')
        date = published[0]
        time = published[1].split('.')[0]

        b.l_say('Youtube video: %s%s%s by %s%s' % (BOLD, title, RESET, BOLD, author), i)
        b.l_say('Description: %s | Published: %s' % (description, date), i)


        '''
        title = author = duration = views = favourites = None
        likes = dislikes = description = date = None
        title = data['entry']['title']['$t']
        author = data['entry']['author'][0]['name']['$t']
        duration = data['entry']['media$group']['media$content'][1]['duration'] - 1
        views = data['entry']['yt$statistics']['viewCount']
        favourites = data['entry']['yt$statistics']['favoriteCount']
        likes = data['entry']['yt$rating']['numLikes']
        dislikes = data['entry']['yt$rating']['numDislikes']
        description = data['entry']['media$group']['media$description']['$t']
        d = data['entry']['media$group']['yt$uploaded']['$t']

        d2 = datetime(year=int(d[0:4]), month=int(d[5:7]), day=int(d[8:10]),
                        hour=int(d[11:13]), minute=int(d[14:16]), second=int(d[17:19]))
        date = d2.strftime("%d %B %Y")

        favourites = '{0:,}'.format(int(favourites))
        views = '{0:,}'.format(int(views))
        likes = '{0:,}'.format(int(likes))
        dislikes = '{0:,}'.format(int(dislikes))

        if description == '':
            description = 'No description available.'

        b.l_say('%sYoutube video%s \'%s\' [%ss]' % (RED, WHITE,
            title, duration), i)

        b.l_say('Views %s | Likes:dislikes %s:%s | Uploaded: %s' \
                % (GREEN + views + WHITE,
                GREEN + likes + WHITE, RED + dislikes + WHITE,
                date), i)

        b.l_say('Description: %s' % ITALICS + description, i)
        '''
    if i.args is not None:
        for link in i.args:
            # b.l_say('Getting data for %s' % link, i, 0)
            if 'youtu.be' in link:
                vidid = link.split('.be/')[1]
                vidid = vidid.split('?')[0]
            elif link.startswith('http'):
                vidid = link.split('&')[0]
                vidid = vidid.split('=')[1]
            parsevid(vidid)

    else:
        b.l_say('Usage: parselink <vidid...>', i, 0)

    return True

def pyt(l, b, i):
    """
    !d Alias for .parseyoutube
    !a <link> [links...]
    !r user
    """
    return parseyoutube(l, b, i)

def _chat(bot, args):
    n, c, m = args
    if 'www.youtube.com' in ' '.join(m) or 'youtu.be' in ' '.join(m):
        input = bot.new_input(n, c, m)
        # Treat input as a command.
        input.set_command('parseyoutube')
        input.set_level(1)
        input.set_user(bot.get_user(n))
        input.args = []
        # Handle multiple links
        for word in m:
            if 'www.youtube.com' in word or 'youtu.be' in word:
                input.args.append(word)
        bot.plugins.process_command(bot, input)

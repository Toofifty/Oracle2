"""
Oracle 2.0 IRC Bot
youtube.py plugin module

http://toofifty.me/oracle
"""

import urllib, json
from datetime import datetime

def init():
    print '\t%s loaded' % __name__
    
def fullparselink(l, b, i):
    if i.args is not None:
        vidid = i.args[0]
        b.l_say('Getting data for %s' % vidid, i, 0)
        if vidid.startswith('http'):
            vidid = vidid.split('&')[0]
            vidid = vidid.split('=')[1]
        
        meta_data_link = ('https://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % vidid)
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

def parselink(l, b, i):
    """
    !d Parse a YouTube link
    !a [link] <link2> ...
    !r user
    """
    def parsevid(vidid):
        meta_data_link = ('https://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % vidid)
        tables = urllib.urlopen(meta_data_link)
        data = json.loads(tables.read())
        
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
        # 2008-04-08T07:05:41.000Z
        d2 = datetime(year=int(d[0:4]), month=int(d[5:7]), day=int(d[8:10]),
                        hour=int(d[11:13]), minute=int(d[14:16]), second=int(d[17:19]))
        date = d2.strftime("%A %d. %B %Y, %X")
        
        favourites = '{0:,}'.format(int(favourites))
        views = '{0:,}'.format(int(views))
        likes = '{0:,}'.format(int(likes))
        dislikes = '{0:,}'.format(int(dislikes))
        
        if description == '':
            description = 'No description available.'
        
        b.l_say('Youtube video - %s by %s [%ss]' % (title, author, duration), i)
        b.l_say('Views: %s Favourites: %s L|D: %s|%s Uploaded: %s' \
                % (views, favourites, likes, dislikes, date), i)
        b.l_say('Description: %s' % description, i)
    
    if i.args is not None:
        for link in i.args:
            b.l_say('Getting data for %s' % link, i, 0)
            if link.startswith('http'):
                vidid = link.split('&')[0]
                vidid = vidid.split('=')[1]
            parsevid(vidid)
        
    else:
        b.l_say('Usage: parselink [vidid] [value]', i, 0)
    
    return True
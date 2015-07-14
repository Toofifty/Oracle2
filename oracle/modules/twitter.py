import db
import tweepy, sqlite3, json
from threading import Thread

access_token = '866086669-80MhHHYeNNQnQIUGhHbA4EkmKSRjLb43EKzwyETp'
access_secret = 'envPhXfbIIdiZe0mhI3BbAGu5mPUxM1KxOclbn2kobFDC'
consumer_key = 'cfPJDpFNBRFj6hvpCzSVLKDdM'
consumer_secret = '7PXnSOZ1ez6LtkOfeoQ5Ohxh5f1unzQyIj8ynisBEUXVQ2MarW'

# CON = sqlite3.connect('../../data/data.db')
# CON.row_factory = sqlite3.Row
# CUR = CON.cursor()

class TwitterStream(Thread):
    def __init__(self, bot, twitters):
        Thread.__init__(self)
        self.bot = bot
        self.twitters = twitters

    def run(self):
        out = TwitterOut(self.bot, self.twitters)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        stream = tweepy.Stream(auth, out)

        follows = []

        for twit in self.twitters:
            follows.append(twit['id'])

        stream.filter(follow=follows)

class TwitterOut(tweepy.streaming.StreamListener):

    def __init__(self, bot, twitters):
        self.bot = bot
        self.twitters = twitters

    def on_data(self, data):
        data = json.loads(data)
        name = data['user']['name']
        screen_name = data['user']['screen_name']
        text = data['text'].encode('ascii', 'ignore')
        if self.is_not_rt(screen_name):
            self.bot.say('%s (@%s) just tweeted this:' % (name, screen_name), 'all')
            self.bot.say(text, 'all')
        return True

    def is_not_rt(self, screen_name):
        for twit in self.twitters:
            if twit['account'] == screen_name:
                return True
        return False

    def on_error(self, status):
        print status

def _init(b):
    print '\t%s loaded' % __name__
    twi = TwitterStream(b, db.get_twitters())
    twi.start()

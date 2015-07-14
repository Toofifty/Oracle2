# -*- coding: utf-8 -*-

from format import PURPLE, CYAN, ORANGE, GREEN, RED, BLUE, RESET, BOLD
from threading import Thread
import math
import random
import traceback

GAME = None
PLAYERS = []

def _init(bot):
    print '\t%s loaded' % __name__

def ng(l, b, i):
    """!parent-command
    !c help
        !d Print the help for Number game
        !r user
    !c new
        !d Start a new Number game
        !a -r=[min],[max] -d=[T/F]
        !r moderator
    !c guess
        !d Guess a number
        !a <number>
        !r user
    !c play
        !d Enter PLAY mode. All chat will be treated as a guess
        !r user
    !c stop
        !d Exit PLAY mode
        !r user
    !c cancel
        !d Stop the current game
        !r moderator
    """
    def c(str):
        b.l_say(str, i)

    def p(str):
        b.l_say(str, i, 0)

    def help(l, b, i):
        p('%s=== Number Game Help Guide ===' % ORANGE)
        p('\tTo start a new game, use %s.ng new%s. You will then be ' % (CYAN, RESET))
        p('\tgiven an interval, everyone in the chat will be able to')
        p('\tguess the number. Close guesses will result in         ')
        p('\tcumulative points, until the max amounts of points have')
        p('\tbeen awarded. Use %s.ng guess <number> %sto guess, OR  ' % (CYAN, RESET))
        p('\tuse %s.ng play%s to enter a mode in which everything   ' % (CYAN, RESET))
        p('\tyou type in chat will be treated as a guess. Exit this ')
        p('\tmode with %s.ng stop%s.' % (CYAN, RESET))
        p('%s=== End help ===' % ORANGE)
        return True

    def new(l, b, i):
        global GAME
        if GAME is not None:
            b.l_say('%sThere\'s already a Number Game running!' % BOLD, i, 0)
            return True

        min = 0
        max = 1000
        dec = False
        if i.args is not None:
            for arg in i.args:
                if arg.startswith('-r='):
                    min, max = arg.replace('-r=', '').split(',')
                    min = int(min)
                    max = int(max)

                elif arg.startswith('-d='):
                    if 't' in arg.lower():
                        dec = True
            str_dec = 'OFF'
            if dec:
                str_dec = 'ON'

        p('Creating new Number Game, with')
        p('range (%s%d%s, %s%d%s) and decimals %s%s%s.' \
                % (CYAN, min, RESET, CYAN, max, RESET,
                   CYAN, str_dec, RESET))
        GAME = Game(b, min, max, dec)

    def cancel(l, b, i):
        global GAME
        GAME = None
        p('Game stopped.')

    def guess(l, b, i):
        global GAME
        if GAME == None:
            p('There is no Number Game running at the moment.')
            return True

        if len(i.args) > 1:
            if '.' in i.args[1]:
                guess = float(i.args[1])
            else:
                guess = int(i.args[1])

            if not (isinstance(guess, float) or isinstance(guess, int)):
                p('You must guess a number, silly!')
                return True

            success = GAME.guess(i.nick, guess)
            if success == 'win':
                new_points = b.get_user(i.nick).get_points()
                p('New score: %s' % format(new_points, ',d'))
                GAME = None

            elif success == 'kill':
                GAME = None

            elif success == 'reward':
                new_points = b.get_user(i.nick).get_points()
                p('New score: %s' % format(new_points, ',d'))
                GAME = None

        else:
            p('You must guess something, silly!')

    def play(l, b, i):
        global PLAYERS
        PLAYERS.append(i.nick)
        p('You are now in %sPLAY%s mode.' % (BOLD, RESET))
        return True

    def stop(l, b, i):
        global PLAYERS
        PLAYERS.remove(i.nick)
        p('You are now %snot%s in %sPLAY%s mode.' % (BOLD, RESET, BOLD, RESET))
        return True




    #====================================================================#
    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        b.l_say('Usage: %s.ng new|guess|play|stop' % CYAN, i, 0)
    return True
    #====================================================================#

class Game(Thread):

    BASE_MULT = 15
    MAX_MULT = 10
    MAX_VARIANCE = 0.4
    FORMAT = '%s[%sNumbers%s]' % (RESET, ORANGE, RESET)

    def __init__(self, bot, min=-1000, max=1000, dec=False):
        Thread.__init__(self)

        self.bot = bot

        if not dec:
            self.number = random.randint(min, max)
        else:
            # Gives a number with heaps of digits,
            # very hard to guess correctly.
            self.number = random.uniform(min, max)

        self.points_multiplier = self.calc_multiplier(min, max, dec)
        self.max_points = self.calc_max(self.points_multiplier)
        self.points = self.max_points
        self.interval = self.calc_interval(self.number, max, min)

        self.print_start(self.interval, self.max_points)

    def calc_multiplier(self, min, max, dec):
        """Lowest amount of points to award each
        reasonable guess
        """
        base = self.BASE_MULT
        if dec:
            base *= 3
        base *= math.sqrt((max - min)/250.0)
        return int(base)

    def calc_max(self, points):
        vmin = 1 - self.MAX_VARIANCE/2
        vmax = 1 + self.MAX_VARIANCE/2
        return int(self.MAX_MULT * random.uniform(vmin, vmax) * points)

    def calc_interval(self, number, max, min):
        variance = (max - min)/2
        if isinstance(number, float):
            i_max = number + random.uniform(0, variance)
            i_min = number - random.uniform(0, variance)
        else:
            i_max = number + random.randint(0, variance)
            i_min = number - random.randint(0, variance)

        if i_max > max: i_max = max
        if i_min < min: i_min = min
        return (i_min, i_max)

    def print_start(self, interval, max_points):
        self.bot.say('%s A new Number Game has begun!' \
                     ' Use %s.ng guess <n> %sto guess.' % (self.FORMAT, BOLD, RESET), 'all')

        self.bot.say('%s The number is between %s%s%s and %s%s%s.'\
                     % (self.FORMAT, CYAN, format(interval[0], ',d'), RESET,
                        CYAN, format(interval[1], ',d'), RESET), 'all')
        self.bot.say('%s Points up for grabs: %s+%d'\
                     % (self.FORMAT, GREEN, max_points), 'all')

    def guess(self, nick, guess):

        if int(guess) == self.number or float(guess) == self.number:
            self.bot.say('%s %s guessed correctly! %s+%s%s points' \
                          % (self.FORMAT, BOLD+nick+RESET, GREEN, format(int(self.points), ',d'), RESET), 'all')
            # award points here
            self.bot.get_user(nick).add_points(int(self.points))
            return 'win'
            _delete()
        else:
            # 0.5 is max mult
            reward_mult = 1.0 / ((float(self.number) - float(guess))**2 + 2.0 )
            reward = self.points * reward_mult
            remove = max(reward, 1)
            self.points -= remove * self.points_multiplier * 0.5

            give_reward = False
            if reward_mult > 0.05:
                self.bot.say('%s %s was rewarded %s%s%s points for their guess of %s%d%s.'\
                             % (self.FORMAT, BOLD+nick+RESET, GREEN, format(int(reward), ',d'), RESET,
                                CYAN, guess, RESET), 'all')
                self.bot.get_user(nick).add_points(int(reward))
                self.points = 0
            else:
                if self.number > guess:
                    self.bot.say('%s Higher! Pool dropped to %s+%s%s points.' \
                                 % (self.FORMAT, GREEN, format(int(self.points), ',d'), RESET), 'all')
                else:
                    self.bot.say('%s Lower! Pool dropped to %s+%s%s points.'
                                 % (self.FORMAT, GREEN, format(int(self.points), ',d'), RESET), 'all')

            if self.points <= 0:
                self.bot.say('%s Game over! Pool dropped to %s0%s!' % (self.FORMAT, GREEN, RESET), 'all')
                self.bot.say('%s The number was %s%s%s.' % (self.FORMAT, GREEN, self.number, RESET), 'all')
                self.number = None
                if give_reward:
                    return 'win'
                return 'kill'
            if give_reward:
                return 'reward'

def _delete():
    global GAME
    GAME = None

def _chat(bot, args):
    nick, channel, message = args

    global PLAYERS
    if nick in PLAYERS:
        try:
            global GAME
            if '.' in message[0]:
                guess = float(message[0])
            else:
                guess = int(message[0])

            if not (isinstance(guess, float) or isinstance(guess, int)):
                return True

            success = GAME.guess(nick, guess)
            if success == 'win':
                new_points = b.get_user(nick).get_points()
                p('New score: %s' % format(new_points, ',d'))
                GAME = None

            elif success == 'kill':
                GAME = None

            elif success == 'reward':
                new_points = b.get_user(nick).get_points()
                p('New score: %s' % format(new_points, ',d'))
        except:
            pass

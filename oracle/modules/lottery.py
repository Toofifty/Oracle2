from threading import Thread
import time, traceback, random
from format import BOLD, RESET, CYAN, GREEN

lotto = None

def _init(b):
    print '\t%s loaded' % __name__

def lottery(l, b, i):
    """!parent-command
    !c new
        !d Create a new lottery (cost: 10 points)
        !a [duration] [min-bet] [max-bet]
        !r user
    !c info
        !d Get info about the current lottery
        !r user
    !c bet
        !d Place a bet in the current lottery
        !a <amount>
        !r user
    """

    def new(l, b, i):
        if lotto is not None:
            b.l_say('There\'s already a lottery running.', i, 0)
            return True

        if i.user.get_points() < 10:
            b.l_say('You don\'t have enough points to begin a lottery.', i, 0)
            return True

        duration = 600
        min_bet = 10
        max_bet = 200

        if len(i.args) > 1:
            try:
                if 'm' in i.args[1]:
                    duration = 60 * int(i.args[1].replace('m', ''))
                else:
                    duration = int(i.args[1])
            except:
                traceback.print_exc()
                b.l_say('Please only use digits or \'m\' for the duration.', i, 0)
                return True

            if len(i.args) > 2:
                try:
                    min_bet = max(min_bet, int(i.args[2]))
                except:
                    b.l_say('The minimum bet must be a number.', i, 0)
                    return True

                if len(i.args) > 3:
                    try:
                        max_bet = max(min_bet, int(i.args[3]))
                    except:
                        b.l_say('The maximum bet must be a number.', i, 0)
                        return True
        global lotto
        lotto = Lotto(b, duration, min_bet, max_bet)
        lotto.start()

        i.user.add_points(-10)
        b.l_say('You have %d points left.' % i.user.get_points(), i, 0)

    def info(l, b, i):
        global lotto
        if lotto is None:
            b.l_say('There is no lottery at the moment.', i, 0)
            return True
        m, s = divmod(lotto.time_left, 60)
        b.l_say(
            '%s Time left: %02d:%02d, Prize pool: %d, Bet range: %d - %d' % (
                lotto.format, m, s, lotto.get_pool(), lotto.min_bet,
                lotto.max_bet
            ), i, 0
        )

    def bet(l, b, i):
        global lotto
        if lotto is None:
            b.l_say('There is no lottery at the moment.', i, 0)
            return True
        if len(i.args) > 1:
            try:
                global lotto
                bet = lotto.add_bet(i.nick, int(i.args[1]))
                if not bet:
                    b.l_say('You don\'t have enough points.', i, 0)
                    return True
                i.user.add_points(-1 * bet)
                b.l_say('You have %d points left.' % i.user.get_points(), i, 0)

            except:
                traceback.print_exc()
                b.l_say('The amount must be a number.', i, 0)

            return True
        b.l_say('You need to specify a bet amount.', i, 0)

    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        b.l_say('Usage: %s.lottery new|bet|info' % CYAN, i, 0)
    return True

class Lotto(Thread):
    def __init__(self, bot, duration, min_bet, max_bet):
        Thread.__init__(self)
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.time_left = duration
        self.bets = {}
        self.bot = bot
        self.dead = False
        self.format = '[%sLottery%s]' % (CYAN, RESET)
        print '\t\tNew %s started' % __name__
        m, s = divmod(duration, 60)
        self.bot.say(
            '%s New lottery started! Will run for %02d:%02d. Bet range: %d - %d'\
            % (self.format, m, s, self.min_bet, self.max_bet),
            'all'
        )

    def add_bet(self, nick, bet):
        if bet < self.min_bet:
            return False
        elif bet > self.max_bet:
            bet = self.max_bet

        if nick in self.bets:
            return False
        self.bets[nick] = bet

        pool = self.get_pool()

        self.bot.say(
            '%s %s bet %dp. Pool is now %dp.' % (self.format, nick, bet, pool),
            'all'
        )
        return bet

    def get_pool(self):
        pool = 0
        for k, v in self.bets.iteritems():
            pool += v
        return pool

    def find_winner(self, num):
        for k, v in self.bets.iteritems():
            if num < v:
                return k
            else:
                num -= v
        return None

    def kill():
        self.dead = True

    def end(self):
        pool = self.get_pool()
        winning_num = random.randint(1, pool)

        winner = self.find_winner(winning_num)

        if winner is None:
            return False
        self.bot.say(
            '%s %s%s%s is the lucky winner of this round and receives %s%d%s points!' % \
            (self.format, BOLD, winner, RESET, GREEN, pool, RESET),
            'all'
        )
        win_user = self.bot.get_user(winner)
        win_user.add_points(pool)
        self.bot.msg(
            win_user, 'You now have %s%d%s points.' % (BOLD,
                win_user.get_points(), RESET)
        )
        self.kill()


    def run(self):
        while not self.dead:
            while self.time_left > 0 and not self.dead:
                self.time_left -= 2
                time.sleep(2)
            if self.dead:
                return
            self.end()

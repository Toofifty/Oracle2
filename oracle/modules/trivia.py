# -*- coding: utf-8 -*-

import misc
import yaml, random, time, traceback
from os import path, listdir
from threading import Thread

from format import PURPLE, WHITE, GREEN, BLUE, RESET, BOLD

winning_alts = [
    'got the answer!',
    'knows their stuff!',
    'is a genius!',
    'is a trivia master!'
]

cls = None

def _init(bot):
    print '\t%s loaded' % __name__
    global cls
    cls = TriviaClass(1200, 100, bot)
    cls.start()

def _del(bot):
    print '\t%s unloaded' % __name__
    global cls
    cls.kill()

class TriviaClass(Thread):
    def __init__(self, interval, reward, bot):
        Thread.__init__(self)
        self.questions = self.load_trivia()
        self.reward = reward
        self.interval = interval
        self.current_interval = interval
        self.bot = bot
        self.current = ''
        self.format = '[%sTrivia%s]' % (PURPLE, RESET)
        self.disabled = False
        self.dead = False
        self.kickstarters = []
        print '\t\t%s thread started' % __name__

    def load_trivia(self):
        try:
            questions = {}
            for f in listdir(path.join('..', 'files', 'trivia')):
                if 'disabled' in f:
                    continue;
                else:
                    with open(path.join('..', 'files', 'trivia', f)) as f:
                        questions_list = f.read().strip().split('\n')
                    for line in questions_list:
                        qa = line.split(': ')
                        question = qa[0]
                        answers = qa[1]
                        questions[question] = answers.lower().strip().split(', ')
            return questions
        except:
            traceback.print_exc()

    def get_time_remaining(self):
        return self.current_interval

    def kickstart(self, nick):
        if nick in self.kickstarters:
            return 0
        self.kickstarters.append(nick)
        diff = random.randint(60, 720)
        self.current_interval -= diff
        return diff

    def get_question(self):
        return random.choice(self.questions.keys())

    def get_answers(self, question=None):
        if question is not '' and question is not None:
            return self.questions[question]
        else:
            for k, v in self.questions.iteritems():
                if k == self.current:
                    return v
        return 'No answer found.'

    def guess(self, guess):
        if self.check(guess):
            self.current = ''
            return True, self.reward
        else:
            return False, None

    def check(self, guess):
        g = str(' '.join(guess))
        if g.lower() in self.get_answers():
            return True
        return False

    def disable(self):
        self.disabled = True
        return self.disabled

    def enable(self):
        self.disabled = False
        return self.disabled

    def get_info(self):
        n = 0
        for k in self.questions:
            n += 1
        return n, self.interval

    def _get_disabled(self):
        return self.disabled

    def print_question(self):
        if self.current != '':
            self.bot.say('%s %s' % (self.format, self.current), 'all')
            self.bot.say('%s Use .a <answer> to answer.' % self.format, 'all')
            return
        self.bot.say('%s There is no trivia question at the moment.' % self.format, 'all')

    def end_cycle(self):
        self.current = self.get_question()
        self.print_question()

    def kill(self):
        self.dead = True

    def is_running(self):
        return self.current != ''

    def run(self):
        while not self.dead:
            while self.current_interval > 0:
                self.current_interval -= 2
                time.sleep(2)
            if not self.disabled and self.current == '':
                self.current_interval = self.interval
                self.kickstarters = []
                self.end_cycle()

    def instance(self):
        return self

def trivia(l, b, i):
    """!parent-command
    !c new
        !d Ask a new question
        !r administrator
    !c disable
        !d Disable trivia
        !r moderator
    !c enable
        !d Enable trivia
        !r moderator
    !c info
        !d Get info on trivia
        !r user
    !c repeat
        !d Ask the current trivia question again
        !r user
    !c answer
        !d Get the answer to the current trivia question
        !a [question]
        !r administrator
    !c checktime
        !d Check how long until the next trivia question
        !r user
    !c kickstart
        !d Chew away at the time remaining until the next question
        !r user
    """
    def new(l, b, i):
        global cls
        cls.end_cycle()

    def disable(l, b, i):
        global cls
        cls.disable()

    def enable(l, b, i):
        global cls
        cls.enable()

    def info(l, b, i):
        questions, interval = cls.get_info()
        b.l_say('%s Time interval: %d (%d minutes), %d questions listed.' %
                (cls.format, interval, interval/60, questions), i, 0)

    def repeat(l, b, i):
        global cls
        cls.print_question()

    def answer(l, b, i):
        global cls
        if i.args > 2:
            answer = cls.get_answers(' '.join(i.args[1:]))
        else:
            answer = cls.get_answers()
        b.l_say(answer, i, 0)

    def checktime(l, b, i):
        global cls
        time_rem = cls.get_time_remaining()
        b.l_say('%s Time remaining: %s%d%s seconds (~%s%d%s minutes).' %
            (cls.format, BOLD, time_rem, RESET, BOLD, time_rem/60, RESET), i, 0)

    def kickstart(l, b, i):
        global cls
        amount = cls.kickstart(i.nick)
        if amount is 0:
            b.l_say('%s Sorry! You can\'t kickstart multiple times per round.' % cls.format, i, 0)
        else:
            b.l_say('%s %s%s%s kickstarted the trivia! They knocked %s%d%s seconds off the clock.' %
                (cls.format, BOLD, i.nick, RESET, BOLD, amount, RESET), i, 1)

    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        info(l, b, i)
    return True

def a(l, b, i):
    """
    !d Answer a question
    !a <answer...>
    !r user
    """
    global cls
    correct, reward = cls.guess(i.args)
    if correct:
        b.l_say('%s %s%s%s %s %s+%d%s points' % (cls.format,
            BOLD, i.nick, RESET, misc._pick(winning_alts), BOLD, reward,
            RESET), i, 1)
        new_points = b.get_user(i.nick).add_points(reward)
        b.l_say('New score: %s' % format(new_points, ',d'), i, 0)
    elif cls.is_running():
        b.l_say('%s Incorrect!' % (cls.format), i, 0)
    else:
        b.l_say('%s There is no trivia question at the moment.' % (cls.format), i, 0)
    return True

'''
def t(l, b, i):
    """
    !d Alias command for trivia
    !r user
    """
    return trivia(l, b, i)
'''

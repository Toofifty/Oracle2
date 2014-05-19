# -*- coding: utf-8 -*-

import yaml
import random
import time
import traceback
from os import path
from threading import Thread

from format import PURPLE, WHITE, GREEN, BLUE

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
        self.bot = bot
        self.current = ''
        self.format = '%s[%sTrivia%s]' % (WHITE, PURPLE, WHITE)
        self.disabled = False
        self.dead = False
        print '\t\t%s thread started' % __name__
        
    def load_trivia(self):
        with open(path.join('..', 'files', 'trivia.yml')) as file:
            c = yaml.load(file)
        return c
        
    def get_question(self):
        return random.choice(self.questions.keys())
        
    def get_answer(self, question=None):
        if question is not None:
            for k, v in self.questions.iteritems():
                if k == question:
                    return str(v).capitalize()
        else:
            for k, v in self.questions.iteritems():
                if k == self.current:
                    return str(v).lower()
                    
    def guess(self, guess):
        if self.check(guess):
            self.current = ''
            return True, self.reward
        else:
            return False, None
            
    def check(self, guess):
        g = str(' '.join(guess))
        if g.lower() == self.get_answer():
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
            self.bot.say('%s %s (%d)' % (self.format, self.current, 
                                         len(self.get_answer().split(' '))), 'all')
            self.bot.say('%s Use .a [answer] to answer.' % self.format, 'all')
            return
        self.bot.say('%s There is no trivia question at the moment.' % self.format, 'all')
        
    def end_cycle(self):
        self.current = self.get_question()
        self.answer = self.get_answer()
        self.print_question()
        
    def kill(self):
        self.dead = True
        
    def is_running(self):
        return self.current != ''
        
    def run(self):
        while not self.dead:
            time.sleep(self.interval)
            if not self.disabled and self.current == '':
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
    
    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        b.l_say('Usage: .trivia info', i, 0)
    return True
    
def a(l, b, i):
    """
    !d Answer a question
    !a [answer...]
    !r user
    """
    global cls
    correct, reward = cls.guess(i.args)
    if correct:
        b.l_say('%s %s%s%s got the answer! %s+%d%s points' % (cls.format, 
            BLUE, i.nick, WHITE, GREEN, reward, WHITE), i, 1)
        new_points = b.get_user(i.nick).add_points(reward)
        b.l_say('New score: %s' % format(new_points, ',d'), i, 0)
    elif cls.is_running():
        b.l_say('%s Incorrect!' % (cls.format), i, 0)
    else:
        b.l_say('%s There is no trivia question at the moment.' % (cls.format), i, 0)
    return True
        
        
        
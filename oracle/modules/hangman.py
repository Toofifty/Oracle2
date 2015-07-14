# -*- coding: utf-8 -*-

import misc
import traceback
from math import sqrt
from format import PINK, BOLD, RESET

game = None

def _init(b):
    print '\t%s loaded' % __name__

def _delete():
    global game
    game = None

class Hangman(object):
    def __init__(self, bot, difficulty):
        lives = {
            'easy': 15,
            'medium': 10,
            'hard': 5,
            'boss': 1
        }

        self.format = '[%sHangman%s]' % (PINK, RESET)
        self.bot = bot
        self.diff = difficulty
        self.lives = lives[self.diff]
        self.phrases = self.load_phrases()
        self.complete_phrase = misc._pick(self.phrases)
        self.reward = (1500 / self.lives) / sqrt(len(self.complete_phrase))
        self.phrase = ''
        self.guessed_letters = ''

        for word in self.complete_phrase.split(' '):
            self.phrase = self.phrase + '_' * len(word) + ' '
        self.phrase = list(self.phrase)

        if self.diff == 'easy':
            self.guess_letter(misc._pick('aei'))
            self.guess_letter(misc._pick('ours'))

    def remove_life(self):
        self.lives -= 1
        self.reward *= 0.75
        if self.lives == 0:
            self.bot.say('%s Game over! Out of lives.' % self.format, 'all')
            _delete()

    def guess_letter(self, letter):
        letter = letter.lower()
        self.guessed_letters = self.guessed_letters + letter
        if not letter in self.complete_phrase:
            return False
        position = -1
        while True:
            position = self.complete_phrase.find(letter, position + 1)
            if position == -1:
                break
            self.phrase[position] = letter
        if not '_' in self.phrase:
            return 'winner'
        return True

    def guess_phrase(self, guess):
        if guess.lower() == self.complete_phrase.lower():
            self.phrase = list(self.complete_phrase)
            return True
        return False

    def load_phrases(self):
        with open('../files/hangman.txt') as f:
            phrases = f.read().strip().split('\n')
        return phrases

    def phrase_spaced(self):
        return ''.join([l + ' ' for l in self.phrase])

    def phrase_text(self):
        return ''.join(self.phrase)

    def print_phrase(self):
        self.bot.say(
            '%s %s | Guessed: %s | %d lives left | Prize: %d points' % (
                self.format, self.phrase_spaced(), self.guessed_letters,
                self.lives, self.reward
            ), 'all'
        )

def hangman(l, b, i):
    """!parent-command
    !c new
        !d Create a new game of hangman
        !a [easy|medium|hard]
        !r user
    !c guess
        !d Guess a letter or the entire phrase
        !a [letter/phrase]
        !r user
    !c info
        !d Get the current phrase as well as guess tally and used letters
        !r user
    """
    def new(l, b, i):
        global game
        if game is not None:
            b.l_say('There is already a hangman game running.', i, 0)
            return True
        diff = 'medium'
        if len(i.args) > 1:
            if i.args[1] not in ['easy', 'medium', 'hard', 'boss']:
                b.l_say('Please choose easy, medium or hard difficulty.', i, 0)
                return True
            diff = i.args[1]
        game = Hangman(b, diff)
        game.print_phrase()

    def guess(l, b, i):
        global game
        if game is None:
            b.l_say('There is no hangman game at the moment.', i, 0)
            b.l_say('Start one with %s.hangman new' % BOLD, i, 0)
            return True
        if len(i.args) > 1:
            if len(i.args[1]) > 1:
                if game.guess_phrase(' '.join(i.args[1:])):
                    game.print_phrase()
                    b.l_say('%s %s wins! +%d points.' % (game.format, i.nick, game.reward), i, 2)
                    i.user.add_points(game.reward)
                    b.l_say('You now have %d points.' % i.user.get_points(), i, 0)
                    game = None
                else:
                    game.remove_life()
                    b.l_say('%s %s guessed wrong! %d lives left.' % (game.format, i.nick, game.lives), i, 2)
            else:
                result = game.guess_letter(i.args[1])
                if result == 'winner':
                    game.print_phrase()
                    b.l_say('%s %s wins! +%d points.' % (game.format, i.nick, game.reward), i, 2)
                    i.user.add_points(game.reward)
                    b.l_say('You now have %d points.' % i.user.get_points(), i, 0)
                    game = None
                elif result:
                    game.print_phrase()
                else:
                    game.remove_life()
                    b.l_say('%s %s guessed wrong! %d lives left.' % (game.format, i.nick, game.lives), i, 2)

            return True
        b.l_say('You need to guess something...', i, 0)

    def info(l, b, i):
        global game
        if game is None:
            b.l_say('There is no hangman game at the moment.', i, 0)
            b.l_say('Start one with %s.hangman new' % BOLD, i, 0)
            return True
        game.print_phrase()

    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        info(l, b, i)
    return True

def hm(l, b, i):
    """
    !d Alias for .hangman
    !r user
    """
    return hangman(l, b, i)

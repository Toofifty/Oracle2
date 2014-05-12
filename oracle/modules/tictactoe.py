# -*- coding: utf-8 -*-

import traceback
from format import PURPLE, CYAN, WHITE, RED, UNDERLINE

GAMES = {}

def _init(bot):
    print '\t%s loaded' % __name__
    
def ttt(l, b, i):
    """!parent-command
    !c help
        !d Get the help guide on playing Tic Tac Toe
        !r user
    !c new
        !d Start a new game of Tic Tac Toe
        !a [user]
        !r user
    !c bot
        !d Play against Oracle
        !a [hard|medium|easy]
        !r user
    !c move
        !d Have your move
        !a [a|b|c][1|2|3]
        !r user
    !c cancel
        !d Cancel any current games running
        !r user
    """
    def c(str):
        b.l_say(str, i)
        
    def p(str):
        b.l_say(str, i, 0)
    
    def help(l, b, i):
        p('%s=== Tic Tac Toe Help Guide ===' % PURPLE)
        p('\tTo start a new game, use %s.ttt new [user] ' % CYAN)
        p('\tYour opponent will then be notified, and ')
        p('\thave their turn. To make your move, use  ')
        p('\t%s.ttt move a1 %sor %sa2 %sor %sb1... %swhere %sa%s, %sb%s, %sc' \
          % (CYAN, WHITE, CYAN, WHITE, CYAN, WHITE, CYAN, WHITE, CYAN, WHITE,
             CYAN))
        p('\tare the columns, and %s1%s, %s2%s, %s3%s are the rows' \
          % (CYAN, WHITE, CYAN, WHITE, CYAN, WHITE))
        p('\tCancel any games with %s.ttt cancel%s. You   ' \
          % (CYAN, WHITE))
        p('\tcan also use %s.ttt bot%s to play against an ' \
          % (CYAN, WHITE))
        p('\tAI opponent.')
        p('%s=== End help ===' % PURPLE)
        return True
        
    def new(l, b, i):
        if len(i.args) > 1:
            global GAMES
            game = Game(b, i.channel, i.nick, i.args[1])
            GAMES[i.nick.lower()] = game
            GAMES[i.args[1].lower()] = game
            return True
        else:
            p('You need someone to play against!')
            return True
            
    def move(l, b, i):
        def usage():
            p('Possible positions: a1, a2, a3, b1, b2, b3, c1, c2, c3')
            
        poss = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
        
        if len(i.args) > 1:
            if not i.args[1] in poss:
                usage()
                return True
        
            global GAMES
            if i.nick.lower() in GAMES:
                if not GAMES[i.nick.lower()].do_turn(i.args[1], i.nick):
                    p('It\'s not your turn!')
                return True
                
            p('You don\'t seem to be in a game at the moment.')
            
    #====================================================================#    
    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        b.l_say('Usage: %s.ttt [help|new|bot|cancel]' % CYAN, i, 0)
    return True
    #====================================================================#
    
def tictactoe(l, b, i):
    """
    !d Alias command for .ttt
    !a [help|new|bot|cancel] <user>
    !r user
    """
    return ttt(l, b, i)
    
class Game:
    
    def __init__(self, bot, channel, p1, p2=None):
        self.board = [0, 0, 0, 
                      0, 0, 0,
                      0, 0, 0]
        self.bot = bot
        self.channel = channel
        self.p1 = p1.lower()
        self.p2 = p2.lower()
        self.turn = 0
        
        self.alert_users(p1, p2)
        
    def c(self, str):
        self.bot.say(str, self.channel)
        
    def p(self, str, pl):
        self.bot.msg(pl, str)
        
    def alert_users(self, p1, p2):
        self.p('You have challenged %s to a game of Tic Tac Toe' % p2, p1)
        self.p('After they complete their turn, use .ttt move [pos]', p1)
        self.p('to make your move. Use .ttt help if you need help', p1)
        
        self.p('You have been challenged by %s to a game of Tic Tac Toe' % p1, p2)
        self.p('You are first, use .ttt move [pos] to make your move.', p2)
        self.p('Use .ttt help if you don\'t know what to do.', p2)
        
    def print_matrix(self):
        m = self.board
        c = 1
        out_line = ''
        for pos in m:
            if c == 1 or c == 4:
                out_line = UNDERLINE
            if pos == 0:
                out_line += ' '
            elif pos == 1:
                out_line += 'X'
            elif pos == 2:
                out_line += 'O'
            elif pos == 3:
                    out_line += RED+'X'+WHITE
            elif pos == 4:
                out_line += RED+'O'+WHITE
            if c == 3 or c == 6 or c == 9:
                self.c(out_line)
                out_line = ''
            else:
                out_line += '|'
            c += 1
        
    def do_turn(self, pos, pl):
        pl = pl.lower()
        # even, player 2
        if self.turn % 2 == 0:
            if not pl == self.p2:
                return False
            self.move(pos[0], pos[1], 2)
            return True
        # odd, player 1
        elif self.turn % 2 != 0:
            if not pl == self.p1:
                return False
            self.move(pos[0], pos[1], 1)
            return True
        
    def move(self, x, y, n):
    
        map = {
            'a': 0,
            'b': 1,
            'c': 2,
        }
            
        # x is in terms of a, b, c
        x = map[x.lower()]
            
        # Shift 1,2,3 to 0,1,2
        y = int(y) - 1
        
        pos = y * 3 + x
        
        self.turn += 1
        self.board[pos] = n
        print self.board
        self.check_win(n)
        return self.print_matrix()
        
    def check_win(self, n):
        def colour_row(row):
            for pos in row:
                self.board[pos] = n+2
    
        def check_row(row):
            for pos in row:
                if not self.board[pos] == n:
                    return False
            colour_row(row)
            return True
        
        return check_row([0,1,2]) or check_row([3,4,5]) \
            or check_row([6,7,8]) or check_row([0,4,8]) \
            or check_row([2,4,6]) or check_row([0,3,6]) \
            or check_row([1,4,7]) or check_row([2,5,8])
        
        
        
        
        
        
        
        
        
        
        
        
        
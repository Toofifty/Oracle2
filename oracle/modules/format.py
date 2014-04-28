# -*- coding: utf-8 -*-

import random

BOLD = '\x02'
ITALICS = '\x1D'
UNDERLINE = '\x1F'
BLACK = '\x0301'
DARKBLUE = '\x0302'
DARKGREEN = '\x0303'
RED = '\x0304'
DARKRED = '\x0305'
PURPLE = '\x0306'
ORANGE = '\x0307'
YELLOW = '\x0308'
GREEN = '\x0309'
CYAN = '\x0310'
LIGHTBLUE = '\x0311'
BLUE = '\x0312'
PINK = '\x0313'
DARKGREY = '\x0314'
GREY = '\x0315'
WHITE = '\x0300'

def _random():
    return '\x03%d' % random.randint(0, 15)

def _init(bot):
    print '\t%s loaded' % __name__
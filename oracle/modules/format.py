# -*- coding: utf-8 -*-

import random
from colorama import init, Fore, Back, Style
init(autoreset=True)

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

console = {
    BOLD: '',
    ITALICS: '',
    UNDERLINE: '',
    BLACK: Style.NORMAL + Fore.BLACK,
    DARKBLUE: Style.NORMAL + Fore.BLUE,
    DARKGREEN: Style.NORMAL + Fore.GREEN,
    RED: Style.BRIGHT + Fore.RED,
    DARKRED: Style.NORMAL + Fore.RED,
    PURPLE: Style.NORMAL + Fore.MAGENTA,
    ORANGE: Style.NORMAL + Fore.YELLOW,
    YELLOW: Style.BRIGHT + Fore.YELLOW,
    GREEN: Style.BRIGHT + Fore.GREEN,
    CYAN: Style.NORMAL + Fore.CYAN,
    LIGHTBLUE: Style.BRIGHT + Fore.CYAN,
    BLUE: Style.BRIGHT + Fore.BLUE,
    PINK: Style.BRIGHT + Fore.MAGENTA,
    DARKGREY: Style.BRIGHT + Fore.BLACK,
    GREY: Style.NORMAL + Fore.WHITE,
    WHITE: Style.BRIGHT + Fore.WHITE,
}

def _random():
    return '\x03%d' % random.randint(0, 15)

def _init(bot):
    print '\t%s loaded' % __name__

def _console_colours(text):
    text = unicode(' '.join(text))
    for colour in console:
        if colour in text:
            text = text.replace(colour, console[colour])
    return text

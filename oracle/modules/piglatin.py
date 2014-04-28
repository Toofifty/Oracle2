import re

def _init(bot):
    print '\t%s loaded' % __name__
    
def piglatin(l, b, i):
    """
    !d Translate the given phrase to Pig Latin (and back, using -)
    !a <-> [message...]
    !r user
    """
    if i.args[0] == '-':
        b.l_say('Sorry! This has not been implemented yet.', i, 0)
    else:
        out = ''
        vowel_pattern = re.compile(r'^[aeiouAEIOU]')    
        consonant_pattern = re.compile(r'^([^aeiouAEIOU]*)(.*)')    
        for word in i.args:
            print word
            c_v_match = vowel_pattern.match(word)
            if c_v_match is not None:
                out += word + 'ay '
                continue
            c_p_match = consonant_pattern.match(word)
            if c_p_match is not None:
                out += c_p_match.group(2) + c_p_match.group(1) + 'ay '
        b.l_say('%s: %s' % (i.nick, out), i, 1)
        return True
            
    
def opish(l, b, i):
    """
    !d Translate the given phrase to Opish (and back, using -)
    !a <-> [message...]
    !r user
    """
    if i.args[0] == '-':
        pass
    else:
        out = ''
        #consonant_pattern = re.compile(r'
    b.l_say('Sorry! This has not been implemented yet.', i, 0)

def turkeyirish(l, b, i):
    """
    !d Translate the given phrase to Turkey Irish (and back, using -)
    !a <-> [message...]
    !r user
    """
    b.l_say('Sorry! This has not been implemented yet.', i, 0)

def doubledutch(l, b, i):
    """
    !d Translate the given phrase to Double Dutch (and back, using -)
    !a <-> [message...]
    !r user
    """
    if i.args[0] == '-':
        b.l_say('Sorry! This has not been implemented yet.', i, 0)
    else:
        out = ''
        for word in i.args:
            for letter in word:
                ll = letter.lower()
                if ll == 'b': add = 'ub'
                elif ll == 'c': add = 'och'
                elif ll == 'd': add = 'ud'
                elif ll == 'f': add = 'uf'
                elif ll == 'g': add = 'ug'
                elif ll == 'h': add = 'ash'
                elif ll == 'j': add = 'ay'
                elif ll == 'k': add = 'uck'
                elif ll == 'l': add = 'ul'
                elif ll == 'm': add = 'um'
                elif ll == 'n': add = 'un'
                elif ll == 'p': add = 'up'
                elif ll == 'q': add = 'uack'
                elif ll == 'r': add = 'ur'
                elif ll == 's': add = 'us'
                elif ll == 't': add = 'ut'
                elif ll == 'v': add = 'uv'
                elif ll == 'w': add = 'ack'
                elif ll == 'x': add = 'ux'
                elif ll == 'y': add = 'ub'
                elif ll == 'z': add = 'ug'
                else: add = ''
                out += letter + add
            out += ' '
        b.l_say('%s: %s' % (i.nick, out), i, 1)
        return True
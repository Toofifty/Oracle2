import os
from format import GREY, _random, WHITE, CYAN
import traceback

def _init(bot):
    print '\t%s loaded' % __name__

def mail(l, b, i):
    """!parent-command
    !c check
        !d Check your mail
        !r user
    !c read
        !d Read the contents of a letter
        !a <mail>
        !r user
    !c delete
        !d Delete a letter
        !a <mail>
        !r user
    !c send
        !d Send mail to a player, who will be notified when they join
        !a <recipient> <title> <message...>
        !r user
    !c checko
        !d Check another user's mail
        !a <user>
        !r administrator
    !c reado
        !d Read another user's mail
        !a <user> <mail>
        !r administrator
    """
    def check(l, b, i):
        letters = []
        for f in os.listdir(os.path.join('..', 'files', 'mail')):
            if i.nick in f:
                try:
                    mail = _random() + f.split(i.nick + ' - ')[1]\
                                       .replace('.txt','')
                    letters.append(mail)
                except:
                    continue
        if letters == []:
            b.l_say('You have no mail :(', i, 0)
            return True
        b.l_say('Use %s.mail read <mail>%s: %s' %
                (GREY, WHITE, (WHITE+', ').join(letters)), i, 0)
        return True

    def read(l, b, i):
        path = os.path.join('..', 'files', 'mail', i.nick + ' - ' + i.args[1] + '.txt')
        if os.path.exists(path):
            with open(path,'r') as f:
                lines = f.read()
                lines = lines.split('\n')
                b.l_say('%s says: %s' % (lines[1], lines[0]), i, 0)
                return True
        b.l_say('No mail under that name.', i, 0)
        return True

    def delete(l, b, i):
        path = os.path.join('..', 'files', 'mail', i.nick + ' - ' + i.args[1] + '.txt')
        if os.path.exists(path):
            os.remove(path)
            b.l_say('Mail deleted.', i, 0)
            return True
        b.l_say('Mail failed to delete', i, 0)
        return True

    def send(l, b, i):
        path = os.path.join('..', 'files', 'mail', i.args[1] + ' - ' + i.args[2] + '.txt')
        if os.path.exists(path):
            b.l_say('Mail already exists under that name.', i, 0)
            return True
        with open(path, 'w') as f:
            f.write(' '.join(i.args[2:])+'\n'+i.nick)
        return True

    def checko(l, b, i):
        letters = []
        for f in os.listdir(os.path.join('..', 'files', 'mail')):
            if i.args[1] in f:
                try:
                    mail = _random() + f.split(i.args[0] + ' - ')[1]\
                                       .replace('.txt','')
                    letters.append(mail)
                except:
                    continue
        if letters == []:
            b.l_say('User has mail :(', i, 0)
            return True
        b.l_say('Use %s.mail read <mail>%s: %s' %
                (GREY, WHITE, (WHITE+', ').join(letters)), i, 0)
        return True

    def reado(l, b, i):
        path = os.path.join('..', 'files', 'mail', i.args[1] + ' - ' + i.args[2] + '.txt')
        if os.path.exists(path):
            with open(path,'r') as f:
                lines = f.read()
                lines = lines.split('\n')
                b.l_say('%s says: %s' % (lines[1], lines[0]), i, 0)
                return True
        b.l_say('No mail under that name.', i, 0)
        return True


    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        b.l_say('Usage: %s.mail check|read|delete|send' % CYAN, i, 0)
    return True

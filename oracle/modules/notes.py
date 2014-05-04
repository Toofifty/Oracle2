from os import path, listdir, remove
from format import CYAN, _random, WHITE
import traceback

def _init(bot):
    print '\t%s loaded' % __name__
    
def notes(l, b, i):
    """!parent-command
    !c new
        !d Create a new note
        !a [title] [message...]
        !r user
    !c list
        !d List all notes available
        !r user
    !c search
        !d Search for a phrase in a note's title
        !a [phrase...]
        !r user
    !c textsearch
        !d Search for a phrase within notes and titles
        !a [phrase...]
        !r user
    !c delete
        !d Delete a note
        !a [title]
        !r user
    !c edit
        !d Edit a note
        !a [title]
        !r user
    !c get
        !d Read a note
        !a [title]
        !r user
    """
    def new(l, b, i):
        text = ' '.join(i.args[2:])
        p = path.join('..','files','notes',i.args[1]+'.txt')
        if path.exists(p):
            b.l_say('Note already exists under that name.', i, 0)
            return True
        with open(p,'w') as f:
            f.write(text)
        b.l_say('Note successfully created.', i, 0)
        return True
        
    def list(l, b, i):
        notes = []
        for file in listdir(path.join('..','files','notes')):
            notes.append(_random()+file.replace('.txt','')+WHITE)
        b.l_say(', '.join(notes), i, 0)
        return True
        
    def search(l, b, i):
        results = []
        for note in listdir(path.join('..','files','notes')):
            if ' '.join(i.args[1:]) in note:
                results.append(_random()+note.replace('.txt','')+WHITE)
        if results == []:
            results.append('None')
        b.l_say('Notes that matched your query: %s' % ', '.join(results), i, 0)
        return True
        
    def textsearch(l, b, i):
        b.l_say('Feature not yet implemented.')
        
    def delete(l, b, i):
        p = path.join('..','files','notes',i.args[1]+'.txt')
        if path.exists(p):
            remove(p)
            b.l_say('Note deleted.', i, 0)
            return True
        b.l_say('Note does not exist.', i, 0)
        return True
        
    def edit(l, b, i):
        p = path.join('..','files','notes',i.args[1]+'.txt')
        if path.exists(p):
            with open(p,'w') as f:
                f.write(' '.join(i.args[2:]))
            return True
        b.l_say('Note does not exist.', i, 0)
        return True
        
    def get(l, b, i):
        p = path.join('..','files','notes',i.args[1]+'.txt')
        if path.exists(p):
            with open(p,'r') as f:
                b.l_say(f.read(), i, 0)
            return True
        b.l_say('Note does not exist.', i, 0)
        return True
    
    #====================================================================#    
    try:
        exec ('%s(l, b, i)' % i.args[0]) in globals(), locals()
    except Exception, e:
        traceback.print_exc()
        b.l_say('Usage: %s.notes [new|list|search|textsearch|delete|edit|get]' % CYAN, i, 0)
    return True
    #====================================================================#
    
def note(l, b, i):
    """
    !d Alias command for .notes
    !a [args]
    !r user
    """
    return notes(l, b, i)
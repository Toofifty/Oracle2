"""
Oracle 2.0 IRC Bot
input.py plugin module

http://toofifty.me/oracle
"""

import Tkinter
from threading import Thread
    
class Box(Tkinter.Tk, Thread):
    def __init__(self, parent, bot):
        Thread.__init__(self)
        Tkinter.Tk.__init__(self, parent)
        self.bot = bot
        self.parent = parent
        self.initialize()
        self.title('Oracle input')
        
    def initialize(self):
        self.grid()
        
        self.entry_variable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entry_variable)
        self.entry.grid(column=0, row=1, sticky='EW')
        self.entry.bind('<Return>', self.on_press_enter)
        
        button = Tkinter.Button(self, text=u'Send',
                                command=self.on_button_click)
        button.grid(column=1, row=1)
        
        self.label_variable = Tkinter.StringVar()
        
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def on_button_click(self):
        self.label_variable.set(self.entry_variable.get())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        _input(self.bot, self.entry_variable.get())
        self.entry_variable.set('')
        
    def on_press_enter(self, event):
        return self.on_button_click()
        
    def run(self):
        self.mainloop()
    
def _init(bot):
    app = Box(None, bot)
    app.start()
    print '\t%s loaded' % __name__
    
def _del(bot):
    print '\t%s unloaded' % __name__
    
def _input(bot, message):
    def get_level(char):
        """Gets the privacy level of char
        
        returns int -> 0-2, 0 being most private
        """
        
        if char == bot.config.char:
            return 1
        if char == bot.config.prchar:
            return 0
        if char == bot.config.puchar:
            return 2
        
    message = message.split(' ')
    input = bot.new_input(bot.config.nick, 'all', message)
    input.set_user(bot.try_create_user(bot.config.nick))
    
    char = bot.config.char
    for c in (bot.config.char, bot.config.prchar, bot.config.puchar):
        if message[0].startswith(c):
            message[0] = str(message[1:])
            char = c
    
    input.set_command(message[0])
    input.set_level(get_level(char))
    bot.plugins.event(bot, 'bot command', (input))
    return bot.plugins.process_command(bot, input)
    
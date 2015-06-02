from Tkinter import *

COLORS = {'white': '#fff',
          'darkgreen': '#006633',
          'green': '#009966',
          'lightgreen': '#00cc99',
          'lightred': '#ff9966',
          'red': '#ff6633',
          'darkred': '#ff3300'}
FONT = 'Courier'

class GUI:

    @staticmethod
    def create_button(button_name, event, root, x=0, y=0, color='green'):
        button = Button(root, text=button_name)
        gamma = {'light': '#00cc99', 'middle': '#009966', 'dark': '#006633'}
        if color == 'red':
            gamma = {'light': '#ff9966', 'middle': '#ff6633', 'dark': '#ff3300'}
        button.config(relief=FLAT,
                      bg=gamma['middle'],
                      fg=COLORS['white'],
                      activebackground=gamma['light'],
                      activeforeground=COLORS['white'],
                      height=1,
                      width=10,
                      font=FONT + ' 16 bold')
        button.config(highlightbackground=gamma['middle'])
        button.bind('<Button-1>', event)
        button.pack(padx=5, pady=5)
        button.place(x=x, y=y)

    @staticmethod
    def create_entry(root, x=0, y=0, show=''):
        entry = Entry(root, bd = 2)
        entry.config(relief=FLAT,
                     bg=COLORS['white'],
                     fg=COLORS['green'],
                     font=FONT +' 16',
                     show=show,
                     width=12,
                     selectbackground=COLORS['green'],
                     insertbackground=COLORS['green'])
        entry.config(highlightbackground=COLORS['green'],
                     highlightcolor=COLORS['green'])
        entry.pack()
        entry.place(x=x, y=y)

    def __init__(self, app):
        self.app = app
        self.setup_main_window()

    def setup_main_window(self):
        self.base = Tk()
        self.base.resizable(width=FALSE, height=FALSE)
        self.base.minsize(width=640, height=480)
        self.base.config(
            bg = COLORS['white']
        )
        self.make_all_frames()

    def make_all_frames(self):
        self.make_login_form()

    def make_login_form(self):
        self.create_entry(self.base, y=220, x=252)
        self.create_entry(self.base, show='*', y=260, x=252)
        self.create_button('Login', event=self.login_user, root=self.base, y=305, x=254)
        self.create_button('Register', event=self.register_user, root=self.base, y=350, x=254, color='red')

    def login_user(self, event):
        pass

    def register_user(self, event):
        pass

    def run(self):
        self.base.mainloop()
        self.app.quit()
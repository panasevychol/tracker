from Tkinter import *


class GUIFramework:

    COLORS = {'white': '#fff',
          'darkgreen': '#006633',
          'green': '#009966',
          'lightgreen': '#00cc99',
          'lightred': '#ff9966',
          'red': '#ff6633',
          'darkred': '#ff3300'}
    FONT = 'Courier'

    def create_button(self, button_name, command, root, x=0, y=0, color='green'):
        button = Button(root, text=button_name, command=command)
        gamma = {'light': '#00cc99', 'middle': '#009966', 'dark': '#006633'}
        if color == 'red':
            gamma = {'light': '#ff9966', 'middle': '#ff6633', 'dark': '#ff3300'}
        button.config(relief=FLAT,
                      bg=gamma['light'],
                      fg=self.COLORS['white'],
                      activebackground= gamma['middle'],
                      activeforeground = self.COLORS['white'],
                      height=1,
                      font=self.FONT + ' 16')
        button.config(highlightbackground=gamma['middle'],
                     highlightcolor=self.COLORS['lightgreen'],
                     highlightthickness=1)
        button.bind('<Button-1>')
        button.pack(padx=5, pady=5)
        button.place(x=x, y=y, width=200)

    def create_entry(self, root, x=0, y=0, show=''):
        entry = Entry(root, bd = 2)
        entry.config(relief=FLAT,
                     bg=self.COLORS['white'],
                     fg=self.COLORS['green'],
                     font=self.FONT +' 16',
                     show=show,
                     selectbackground=self.COLORS['green'],
                     insertbackground=self.COLORS['green'])
        entry.config(highlightbackground=self.COLORS['lightgreen'],
                     highlightcolor=self.COLORS['green'],
                     highlightthickness=1)
        entry.pack()
        entry.place(x=x, y=y, width=200)
        return entry

    def create_text_area(self, root, x=0, y=0):
        text_area = Text(root)
        text_area.config(relief=FLAT,
                     bg=self.COLORS['white'],
                     fg=self.COLORS['green'],
                     font=self.FONT +' 16',
                     height=10,
                     selectbackground=self.COLORS['green'],
                     insertbackground=self.COLORS['green'])
        text_area.config(highlightbackground=self.COLORS['lightgreen'],
                     highlightcolor=self.COLORS['green'],
                     highlightthickness=1)
        text_area.pack()
        text_area.place(x=x, y=y, width=540)
        return text_area


    def create_label(self, text, root, x=0, y=0, size=16, width=500):
        label = Label(root, text=text)
        label.config(font=self.FONT+ ' '+ str(size),
                     bg=self.COLORS['white'],
                     fg=self.COLORS['green'],)
        label.pack()
        label.place(x=x, y=y, width=width)
        return label

    def create_menu_button(self, button_name, root, x=0, y=0, color='green', labels_and_commands=None):
        if not labels_and_commands:
            labels_and_commands = {}
        gamma = {'light': '#00cc99', 'middle': '#009966', 'dark': '#006633'}
        if color == 'red':
            gamma = {'light': '#ff9966', 'middle': '#ff6633', 'dark': '#ff3300'}
        menu_button = Menubutton(root, text=button_name)
        menu_button.grid()
        menu_button.menu = Menu(menu_button, tearoff = 0)
        menu_button['menu']  =  menu_button.menu
        for label, command in labels_and_commands.iteritems():
            menu_button.menu.add_command(label=label, command=command)
        menu_button.config(relief=FLAT,
                      bg=self.COLORS['white'],
                      fg=gamma['light'],
                      borderwidth=0,
                      activebackground=gamma['light'],
                      activeforeground=self.COLORS['white'],
                      height=1,
                      font=self.FONT + ' 16')
        menu_button.config(highlightbackground=gamma['light'],
                     highlightcolor=gamma['middle'],
                     highlightthickness=1)
        menu_button.menu.config(relief=FLAT,
                      fg=gamma['light'],
                      bg=self.COLORS['white'],
                      borderwidth=0,
                      activebackground=gamma['light'],
                      activeforeground=self.COLORS['white'],
                      font=self.FONT + ' 16')
        menu_button.pack(padx=5, pady=5)
        menu_button.place(x=x, y=y, width=100)

    def clear_window(self, window):
        for widget in window.winfo_children():
            widget.destroy()

class GUI(GUIFramework):

    def __init__(self, app):
        self.app = app
        self.setup_main_window()

    def setup_main_window(self):
        self.base = Tk()
        self.base.resizable(width=FALSE, height=FALSE)
        self.base.minsize(width=640, height=480)
        self.base.config(
            bg = self.COLORS['white']
        )
        self.display_start_page()

    def display_start_page(self):
        if self.app.login_master.user:
            self.display_main_page()
        else:
            self.display_login_page()

    def display_main_page(self):
        self.clear_window(self.base)
        self.create_label('Welcome, ' + self.app.login_master.user + '!', self.base, size=32, x=70, y=80)
        self.create_menu_button('Options', self.base, x=20, y=20, labels_and_commands={'Logout': lambda: self.logout_user_command(), 'Quit': lambda: self.quit()})
        self.create_button('Create task', self.display_create_task_page, self.base, x=220, y=160)

    def logout_user_command(self):
        self.app.login_master.logout_user()
        self.display_start_page()

    def display_create_task_page(self):
        self.clear_window(self.base)
        self.create_label('Task name:', self.base, x=50, y=20, width=None)
        task_name_entry = self.create_entry(self.base, x=50, y=50)
        self.create_label('Assignee:', self.base, x=390, y=20, width=None)
        assignee_entry = self.create_entry(self.base, x=390, y=50)
        self.create_label('Task description:', self.base, x=50, y=90, width=None)
        text_entry = self.create_text_area(self.base, x=50, y=130)
        self.create_button('Return',
                           command=lambda: self.display_main_page(),
                           root=self.base,
                           y=400, x=50, color='green')
        self.create_button('Create task',
                           command=lambda: self.create_task_command(task_name_entry, assignee_entry, text_entry),
                           root=self.base,
                           y=400, x=390, color='red')

    def create_task_command(self, name_entry, assignee_entry, text_entry):
        name = name_entry.get()
        assignee = assignee_entry.get()
        print(assignee)
        text = text_entry.get("1.0", END)
        self.app.task_master.create_task(name, assignee, text)

    def display_login_page(self):
        self.clear_window(self.base)
        self.create_label('Welcome to Tracker!', self.base, size=28, x=70, y=50)
        self.create_label('Login:', self.base, x=220, y=165, width=None)
        login_entry = self.create_entry(self.base, y=195, x=220)
        self.create_label('Password:', self.base, x=220, y=230, width=None)
        password_entry = self.create_entry(self.base, show='*', y=260, x=220)
        self.create_button('Login', command=lambda: self.login_user_command(login_entry=login_entry, password_entry=password_entry), root=self.base, y=305, x=220)
        self.create_button('Register', command=lambda: self.display_register_page(), root=self.base, y=350, x=220, color='red')

    def login_user_command(self, login_entry, password_entry):
        login = login_entry.get()
        password = password_entry.get()
        if not login or not password:
            self.display_error_page('Required fields are empty', self.display_login_page)
            return
        error = self.app.login_master.login_user(login, password)
        if error:
            self.display_error_page(error, self.display_login_page)
        else:
            self.display_main_page()

    def register_user_command(self, login_entry, password_entry, confirm_password_entry):
        login = login_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        if not login or not password or not confirm_password:
            self.display_error_page('Required fields are empty', self.display_register_page)
        elif password != confirm_password:
            self.display_error_page('Passwords do not match', self.display_register_page)
        else:
            error = self.app.login_master.register_user(login, password)
            if error:
                self.display_error_page(error, self.display_register_page)
            else:
                self.display_start_page()

    def display_error_page(self, error_text, return_window_display_function):
        self.clear_window(self.base)
        self.create_label('Error!', self.base, size=24, y=120, x=70)
        self.create_label(error_text, self.base, size=16, y=180, x=70)
        self.create_button('Return',
                           command=lambda: return_window_display_function(),
                           root=self.base,
                           y=280, x=220, color='green')

    def display_register_page(self):
        self.clear_window(self.base)
        self.create_label('Login:', self.base, x=220, y=90, width=None)
        login_entry = self.create_entry(self.base, y=120, x=220)
        self.create_label('Password:', self.base, x=220, y=160, width=None)
        password_entry = self.create_entry(self.base, show='*', y=190, x=220)
        self.create_label('Confirm password:', self.base, x=220, y=230, width=None)
        confirm_password_entry = self.create_entry(self.base, show='*', y=260, x=220)
        self.create_button('Register',
                           command=lambda: self.register_user_command(login_entry, password_entry, confirm_password_entry),
                           root=self.base,
                           y=305, x=220, color='red')
        self.create_button('Return',
                           command=lambda: self.display_login_page(),
                           root=self.base,
                           y=350, x=220, color='green')

    def run(self):
        self.base.mainloop()

    def quit(self):
        self.base.destroy()
        self.app.quit()
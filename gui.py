from Tkinter import *

from gui_framework import GUIFramework

class GUI(GUIFramework):

    def __init__(self, app):
        self.app = app
        self.setup_main_window()

    def setup_main_window(self):
        self.base = Tk()
        self.base.wm_title('Tracker')
        self.base.option_add('*Dialog.msg.font', self.FONT)
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
        self.create_label('Welcome, ' + self.app.login_master.user + '!', self.base, size=24, x=70, y=20)
        self.create_menu_button('Options', self.base, x=20, y=20, labels_and_commands={'Logout': lambda: self.logout_user_command(), 'Quit': lambda: self.quit()})
        self.create_button('Create task', self.display_create_task_page, self.base, x=420, y=400, color='red')
        tasks = self.app.task_master.get_current_user_tasks()
        if tasks:
            self.create_label(self.app.login_master.user + "'s tasks:", self.base, x=20, y=90, width=None)
            task_listbox = self.create_listbox(self.base, x=20, y=130, width=600, options=tasks)
            self.create_button('Browse task', command=lambda : self.display_browse_task_page(task_listbox), root=self.base, x=20, y=400)
        else:
            self.create_label('No tasks for you\nYou can create some\nby clicking a button below', self.base, width=640, y=180)

    def display_browse_task_page(self, task_listbox):
        task_name = task_listbox.get(task_listbox.curselection())
        self.clear_window(self.base)
        self.create_label_frame(self.base, 'Task: ' + str(task_name), x=40, y=90)


    def logout_user_command(self):
        self.app.login_master.logout_user()
        self.display_start_page()

    def display_create_task_page(self):
        users = self.app.login_master.get_users_list()
        self.clear_window(self.base)
        self.create_label('Creating new task', self.base, y=40, size=24, width=640)
        self.create_label('Task name:', self.base, x=50, y=100, width=None)
        task_name_entry = self.create_entry(self.base, x=50, y=130)
        self.create_label('Assignee:', self.base, x=390, y=100, width=None)
        assignee_listbox = self.create_listbox(self.base, x=390, y=130, options=users, height=10)
        self.create_label('Task description:', self.base, x=50, y=175, width=None)
        text_entry = self.create_text_area(self.base, x=50, y=210, width=300, height=7)
        self.create_button('Return',
                           command=lambda: self.display_main_page(),
                           root=self.base,
                           y=400, x=50, color='green')
        self.create_button('Create task',
                           command=lambda: self.create_task_command(task_name_entry, assignee_listbox, text_entry),
                           root=self.base,
                           y=400, x=390, color='red')

    def create_task_command(self, name_entry, assignee_entry, text_entry):
        name = name_entry.get()
        assignee = assignee_entry.get(assignee_entry.curselection())[0]
        text = str(text_entry.get("1.0", END))
        if not assignee or not name or not text:
            self.display_error_page('Required fields are empty', self.display_create_task_page)
        else:
            error = self.app.task_master.create_task(name=name, text=text, owner=assignee)
            if error:
                self.display_error_page(error, self.display_create_task_page)
            else:
                self.display_message_page('New task for ' + assignee + ' created!', self.display_main_page)

    def display_login_page(self):
        self.clear_window(self.base)
        self.create_label('Welcome to Tracker!', self.base, size=28, x=70, y=50)
        self.create_label('Login:', self.base, x=220, y=165, width=None)
        login_entry = self.create_entry(self.base, y=195, x=220)
        self.create_label('Password:', self.base, x=220, y=230, width=None)
        password_entry = self.create_entry(self.base, show='*', y=260, x=220)
        self.create_button('Login', command=lambda: self.login_user_command(login_entry=login_entry, password_entry=password_entry), root=self.base, y=305, x=220)
        self.create_button('Register', command=lambda: self.display_register_page(), root=self.base, y=350, x=220, color='red')
        self.create_button('Quit', command=lambda: self.quit(), root=self.base, y=395, x=220)

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
        #error_window = self.create_top_window('Error!', self.base)
        self.create_label('Error!', self.base, size=24, y=100, x=70)
        self.create_label(error_text, self.base, size=16, y=200, x=70)
        self.create_button('Return',
                           command=lambda: return_window_display_function(),
                           root=self.base,
                           y=300, x=220, color='green')

    def display_message_page(self, message_text, continue_window_display_function):
        self.clear_window(self.base)
        self.create_label(message_text, self.base, size=16, y=180, x=70)
        self.create_button('Continue',
                           command=lambda : continue_window_display_function(),
                           root=self.base,
                           y=280, x=220, color='green')

    def display_register_page(self):
        self.clear_window(self.base)
        self.create_label('User registration', self.base, size=24, x=70, y=20)
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
        self.app.quit()

    def quit(self):
        self.base.destroy()
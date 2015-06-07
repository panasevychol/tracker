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

    def create_label_frame(self, root, title, x=0, y=0, width=None, height=None):
        label_frame = LabelFrame(root, text=title)
        label_frame.config(relief=FLAT,
                           font=self.FONT + ' 16',
                           bg=self.COLORS['white'],
                           fg=self.COLORS['lightgreen'],
                           bd=1,
                           width=width,
                           height=height)
        label_frame.config(highlightbackground=self.COLORS['lightgreen'],
                           highlightcolor=self.COLORS['green'],
                           highlightthickness=1)
        label_frame.pack(padx=x, pady=y, fill="both", expand="yes")
        return label_frame

    def create_top_window(self, name, root):
        top_window = Toplevel(root)
        top_window.resizable(width=FALSE, height=FALSE)
        top_window.minsize(width=400, height=200)
        top_window.config(
            bg = self.COLORS['white']
        )
        return top_window

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

    def create_text_area(self, root, x=0, y=0, width=540, height=10):
        text_area = Text(root)
        text_area.config(relief=FLAT,
                     bg=self.COLORS['white'],
                     fg=self.COLORS['green'],
                     font=self.FONT +' 16',
                     height=height,
                     selectbackground=self.COLORS['green'],
                     insertbackground=self.COLORS['green'])
        text_area.config(highlightbackground=self.COLORS['lightgreen'],
                     highlightcolor=self.COLORS['green'],
                     highlightthickness=1)
        text_area.pack()
        text_area.place(x=x, y=y, width=width)
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
                      bd=0,
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
                      bd=1,
                      activeborderwidth=0,
                      activebackground=gamma['light'],
                      activeforeground=self.COLORS['white'],
                      font=self.FONT + ' 16')
        menu_button.pack(padx=5, pady=5)
        menu_button.place(x=x, y=y, width=100)

    def create_listbox(self, root, x=0, y=0, options=None, height=10, width=200):
        if not options:
            options = ()
        listbox = Listbox(root)
        listbox.config(relief=FLAT,
                     bg=self.COLORS['white'],
                     fg=self.COLORS['green'],
                     font=self.FONT +' 16',
                     height=height,
                     selectbackground=self.COLORS['green'],
                     selectforeground=self.COLORS['white'],
                     selectborderwidth=0,
                     selectmode=SINGLE)
        listbox.config(highlightbackground=self.COLORS['lightgreen'],
                     highlightcolor=self.COLORS['green'],
                     highlightthickness=1)
        for number, option in enumerate(options):
            listbox.insert(number, option)
        listbox.pack()
        listbox.place(x=x, y=y, width=width)
        return listbox

    def clear_window(self, window):
        for widget in window.winfo_children():
            widget.destroy()

import pingpong
from tkinter import filedialog
import tkinter as tk
from tkinter import *
from tkinter import ttk


player_names = []
for player in pingpong.playerNames.find():
    player_names.append(player['name'])


class PingPongApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Ping Pong Game Stats Tracker')
        tk.Tk.wm_iconbitmap(self, default='pingpong.ico')
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (LoginPage, ReLoginPage, StartPage, EnterPage, GameStatsPage, PlayerStatsPage,
                  VersusStatsPage, GamesAddedPage, GameAddedPage, FailedLoginPage, FailedReLoginPage,
                  FileErrorPage, ErrorPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Enter Username, Password, and Database Name\n'
                                    'Then Click "Log in"')
        label.pack()
        label2 = tk.Label(self, text='Username')
        label2.pack()
        self.uname = StringVar()
        self.box1 = ttk.Entry(self, textvariable=self.uname)
        self.box1.pack()
        label3 = tk.Label(self, text='Password')
        label3.pack()
        self.pword = StringVar()
        self.box2 = ttk.Entry(self, textvariable=self.pword, show='*')
        self.box2.pack()
        label4 = tk.Label(self, text='Database Name')
        label4.pack()
        self.dbname = StringVar()
        self.dbname.set('')
        self.dd = OptionMenu(self, self.dbname, 'pingpongstats')
        self.dd.pack()

        button = ttk.Button(self, text='Log in', command=lambda: self.login())
        button.pack()

    def login(self):
        if self.uname.get().isalnum() and self.pword.get().isalnum() and self.dbname.get().isalnum():
            try:
                pingpong.reconnect(self.uname.get(), self.pword.get(), self.dbname.get())
                self.box1.delete(0, END)
                self.box2.delete(0, END)
                self.dbname.set('')
                self.controller.show_frame(StartPage)
            except:
                self.controller.show_frame(FailedLoginPage)
        else:
            pass


class ReLoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Enter Username, Password, and Database Name\n'
                                    'Then Click "Log in"')
        label.pack()
        label2 = tk.Label(self, text='Username')
        label2.pack()
        self.uname = StringVar()
        self.box1 = ttk.Entry(self, textvariable=self.uname)
        self.box1.pack()
        label3 = tk.Label(self, text='Password')
        label3.pack()
        self.pword = StringVar()
        self.box2 = ttk.Entry(self, textvariable=self.pword)
        self.box2.pack()
        label4 = tk.Label(self, text='Database Name')
        label4.pack()
        self.dbname = StringVar()
        self.dbname.set('')
        self.dd = OptionMenu(self, self.dbname, 'pingpongstats')
        self.dd.pack()

        button = ttk.Button(self, text='Log in', command=lambda: self.login())
        button.pack()

        button2 = ttk.Button(self, text='Cancel', command=lambda: controller.show_frame(StartPage))
        button2.pack()

    def login(self):
        if self.uname.get().isalnum() and self.pword.get().isalnum() and self.dbname.get().isalnum():
            try:
                pingpong.reconnect(self.uname.get(), self.pword.get(), self.dbname.get())
                self.box1.delete(0, END)
                self.box2.delete(0, END)
                self.dbname.set('')
                self.controller.show_frame(StartPage)
            except:
                self.controller.show_frame(FailedReLoginPage)
        else:
            pass


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Start Page')  # font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Enter Individual Games', command=lambda: controller.show_frame(EnterPage))
        button1.pack()

        button2 = ttk.Button(self, text='Import Games From File', command=lambda: self.select_file())
        button2.pack()

        button3 = ttk.Button(self, text='View Basic Game Stats', command=lambda: controller.show_frame(GameStatsPage))
        button3.pack()

        button4 = ttk.Button(self, text='View Individual Player Stats',
                             command=lambda: controller.show_frame(PlayerStatsPage))
        button4.pack()

        button5 = ttk.Button(self, text='View Versus Stats', command=lambda: controller.show_frame(VersusStatsPage))
        button5.pack()

        button6 = ttk.Button(self, text='Switch User or Database', command=lambda: controller.show_frame(ReLoginPage))
        button6.pack()

        button7 = ttk.Button(self, text='Log Out', command=lambda: controller.show_frame(LoginPage))
        button7.pack()

    def select_file(self):
        try:
            file = filedialog.askopenfilename()
        except:
            pass
        if file:
            try:
                pingpong.add_data(file)
                self.controller.show_frame(GamesAddedPage)
            except:
                self.controller.show_frame(FileErrorPage)


class EnterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Enter Game Info')
        label.pack(pady=10, padx=10)

        l1 = tk.Label(self, text='Player 1')
        l1.pack()
        self.player1 = StringVar()
        self.box1 = ttk.Entry(self, textvariable=self.player1)
        self.box1.pack()
        l2 = tk.Label(self, text='Player 1 Score')
        l2.pack()
        self.score1 = StringVar()
        self.box2 = ttk.Entry(self, textvariable=self.score1)
        self.box2.pack()
        l3 = tk.Label(self, text='Player 2')
        l3.pack()
        self.player2 = StringVar()
        self.box3 = ttk.Entry(self, textvariable=self.player2)
        self.box3.pack()
        l4 = tk.Label(self, text='Player 2 Score')
        l4.pack()
        self.score2 = StringVar()
        self.box4 = ttk.Entry(self, textvariable=self.score2)
        self.box4.pack()

        button1 = ttk.Button(self, text='Submit', command=lambda: self.add_game())
        button1.pack()

        button2 = ttk.Button(self, text='Clear Entries', command=lambda: self.clear())
        button2.pack()

        button3 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                            self.clear()])
        button3.pack()

    def clear(self):
        self.box1.delete(0, END)
        self.box2.delete(0, END)
        self.box3.delete(0, END)
        self.box4.delete(0, END)

    def add_game(self):
        if self.player1.get().isalnum() and self.player2.get().isalnum()\
                                        and self.score1.get().isnumeric() and self.score2.get().isnumeric():
            pingpong.add_data_obo(self.player1.get(), self.score1.get(), self.player2.get(), self.score2.get())
            self.controller.show_frame(GameAddedPage)
            self.box1.delete(0, END)
            self.box2.delete(0, END)
            self.box3.delete(0, END)
            self.box4.delete(0, END)
        else:
            self.controller.show_frame(ErrorPage)


class GamesAddedPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Games Added Successfully From File')
        label.pack()

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(StartPage))
        button.pack()


class GameAddedPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Game Added Successfully')
        label.pack()

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(EnterPage))
        button.pack()


class FailedLoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Failed to Connect to Server')
        label.pack()
        label2 = tk.Label(self, text='Check Username and Password and Try Again')
        label2.pack()

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(LoginPage))
        button.pack()


class FailedReLoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Failed to Connect to Server')
        label.pack()
        label2 = tk.Label(self, text='Check Username and Password and Try Again')
        label2.pack()

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(ReLoginPage))
        button.pack()


class FileErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Failed to Add Games From File')
        label.pack()
        label2 = tk.Label(self, text='Check Formatting of File')
        label2.pack()
        label3 = tk.Label(self, text='Format:\nplayer1 score1 player2 score2\n'
                                     'player1 score1 player2 score2\nplayer1 score1 player2 score2\nEtc...')
        label3.pack()

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(StartPage))
        button.pack()


class ErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Failed to Add Game')
        label.pack()
        label2 = tk.Label(self, text='Check Scores and Re-Submit')
        label2.pack()

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(EnterPage))
        button.pack()


class GameStatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Basic Game Stats')
        label.pack(pady=10, padx=10)
        self.table = ttk.Treeview(self, columns=('Value', 'Value2'))
        self.table.heading('#0', text='Stat')
        self.table.heading('#1', text='Value')
        self.table.heading('#2', text='Value2')

        button1 = ttk.Button(self, text='Show Stats', command=lambda: self.view_g_stats())
        button1.pack()

        button2 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                            self.clear()])
        button2.pack()

    def clear(self):
        self.table.delete(*self.table.get_children())

    def view_g_stats(self):
        for player in pingpong.playerNames.find():
            pingpong.update_pl_stats(player['name'])
        pingpong.update_g_stats()
        for document in pingpong.g_stats.find():
            for key in document:
                if key == '_id':
                    pass
                else:
                    try:
                        self.table.insert('', 'end', key, text=key, values=document[key])
                    except:
                        self.table.item(key, text=key, values=document[key])
        self.table.pack()


class PlayerStatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Select Player to Get Stats for\nThen Click "Show Stats"')
        label.grid(row=1, pady=10, padx=10)
        label2 = tk.Label(self, text='Note: if new players have been added this\n'
                                     'session, click "Update Player Names" to\n'
                                     'update the dropdown menus.')

        label2.grid(row=2)
        self.table = ttk.Treeview(self, columns='Value')
        self.table.heading('#0', text='Stat')
        self.table.heading('#1', text='Value')

        button = ttk.Button(self, text='Update Player Names', command=lambda: [self.clear(), self.update_names()])
        button.grid(row=3)

        self.player = StringVar()
        self.player.set('Select a Player')
        self.dd = OptionMenu(self, self.player, *player_names)
        self.dd.grid(row=4)

        button1 = ttk.Button(self, text='Show Stats', command=lambda: self.view_pl_stats())
        button1.grid(row=5)

        button2 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                            self.clear()])
        button2.grid(row=6)

    def update_names(self):
        self.dd.destroy()
        new_players = []
        for p in pingpong.playerNames.find():
            new_players.append(p['name'])
        self.dd = OptionMenu(self, self.player, *new_players)
        self.dd.grid(row=4)

    def clear(self):
        self.player.set('Select a Player')
        self.table.delete(*self.table.get_children())

    def view_pl_stats(self):
        pingpong.update_pl_stats(self.player.get())
        for document in pingpong.pl_stats.find({'name': self.player.get()}):
            for key in document:
                if key == 'name' or key == '_id':
                    pass
                else:
                    try:
                        self.table.insert('', 'end', key, text=key, values=str(document[key]))
                    except:
                        self.table.item(key, text=key, values=str(document[key]))
        self.table.grid(row=7)


class VersusStatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Select Two Players\nThen Click "Show Versus Stats"')
        label.grid(row=1, pady=10, padx=10)
        label2 = tk.Label(self, text='Note: if new players have been added this\n'
                                     'session, click "Update Player Names" to\n'
                                     'update the dropdown menus.')
        label2.grid(row=2)
        self.table = ttk.Treeview(self, columns='Value')
        self.table.heading('#0', text='Stat')
        self.table.heading('#1', text='Value')

        button = ttk.Button(self, text='Update Player Names', command=lambda: [self.clear(), self.update_names()])
        button.grid(row=3)

        self.player1 = StringVar()
        self.player1.set('Select Player 1')
        self.dd1 = OptionMenu(self, self.player1, *player_names)
        self.dd1.grid(row=4)
        self.player2 = StringVar()
        self.player2.set('Select Player 2')
        self.dd2 = OptionMenu(self, self.player2, *player_names)
        self.dd2.grid(row=5)

        button1 = ttk.Button(self, text='Show Versus Stats', command=lambda: self.view_vs_stats())
        button1.grid(row=6)

        button2 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                            self.clear()])
        button2.grid(row=7)

    def update_names(self):
        self.dd1.destroy()
        self.dd2.destroy()
        new_players = []
        for p in pingpong.playerNames.find():
            new_players.append(p['name'])
        self.dd1 = OptionMenu(self, self.player1, *new_players)
        self.dd2 = OptionMenu(self, self.player2, *new_players)
        self.dd1.grid(row=4)
        self.dd2.grid(row=5)

    def clear(self):
        self.player1.set('Select Player 1')
        self.player2.set('Select Player 2')
        self.table.delete(*self.table.get_children())

    def view_vs_stats(self):
        pingpong.update_vs_stats(self.player1.get(), self.player2.get())
        self.table.delete(*self.table.get_children())
        for document in pingpong.vs_stats.find({'name': self.player1.get()}):
            if 'wins against ' + self.player2.get() in document.keys():
                for key in document:
                    if key == 'name' or key == '_id':
                        pass
                    else:
                        try:
                            self.table.insert('', 'end', key, text=key, values=str(document[key]))
                        except:
                            self.table.item(key, text=key, values=str(document[key]))
            else:
                pass
        self.table.grid(row=8)


app = PingPongApp()
app.mainloop()

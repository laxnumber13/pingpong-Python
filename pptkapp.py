import pingpong
from tkinter import filedialog
import tkinter as tk
from tkinter import *
from tkinter import ttk


""" this app allows the user to connect to a mongodb database containing pingpong games and stats.
    once logged in, user can view a list of all games in the db, add games to the db, or check
    the overall stats, individual player stats, and player vs player stats."""


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
        for F in (LoginPage, ReLoginPage, StartPage, AllGamesPage, EnterPage, GameStatsPage, PlayerStatsPage,
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
        label = tk.Label(self, text='Enter Username and Password\n'
                                    'Select Database Name\n'
                                    'Then Click "Log in"', font=14)
        label.pack(pady=10)
        label2 = tk.Label(self, text='Username')
        label2.pack()
        self.uname = StringVar()
        self.box1 = ttk.Entry(self, textvariable=self.uname)
        self.box1.pack(pady=5)
        label3 = tk.Label(self, text='Password')
        label3.pack()
        self.pword = StringVar()
        self.box2 = ttk.Entry(self, textvariable=self.pword, show='*')
        self.box2.pack(pady=5)
        label4 = tk.Label(self, text='Database Name')
        label4.pack()
        self.dbname = StringVar()
        self.dbname.set('')
        self.dd = OptionMenu(self, self.dbname, 'pingpongstats')
        self.dd.pack(pady=5)

        button = ttk.Button(self, text='Log in', command=lambda: self.login())
        button.pack(pady=5)

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
        label = tk.Label(self, text='Enter Username and Password\n'
                                    'Select Database Name\n'
                                    'Then Click "Log in"', font=14)
        label.pack(pady=10)
        label2 = tk.Label(self, text='Username')
        label2.pack(pady=5)
        self.uname = StringVar()
        self.box1 = ttk.Entry(self, textvariable=self.uname)
        self.box1.pack(pady=5)
        label3 = tk.Label(self, text='Password')
        label3.pack(pady=5)
        self.pword = StringVar()
        self.box2 = ttk.Entry(self, textvariable=self.pword, show='*')
        self.box2.pack(pady=5)
        label4 = tk.Label(self, text='Database Name')
        label4.pack(pady=5)
        self.dbname = StringVar()
        self.dbname.set('')
        self.dd = OptionMenu(self, self.dbname, 'pingpongstats')
        self.dd.pack(pady=5)

        button = ttk.Button(self, text='Log in', command=lambda: self.login())
        button.pack(pady=5)

        button2 = ttk.Button(self, text='Cancel', command=lambda: [self.box1.delete(0, END),
                                                                   self.box2.delete(0, END),
                                                                   self.dbname.set(''),
                                                                   controller.show_frame(StartPage)])
        button2.pack(pady=5)

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
        label = tk.Label(self, text='Start Page', font=14)
        label.pack(pady=10, padx=10)

        label2 = tk.Label(self, text='Correct Format For Text File\n'
                                     'If Importing Games From a File:\n\nplayer1 score1 player2 score2\n'
                                     'player1 score1 player2 score2\nplayer1 score1 player2 score2\nEtc...')
        label2.pack(pady=10)

        button = ttk.Button(self, text='View All Games',
                            command=lambda: controller.show_frame(AllGamesPage))
        button.pack(pady=5)

        button1 = ttk.Button(self, text='Enter Individual Games',
                             command=lambda: controller.show_frame(EnterPage))
        button1.pack(pady=5)

        button2 = ttk.Button(self, text='Import Games From File',
                             command=lambda: self.select_file())
        button2.pack(pady=5)

        button3 = ttk.Button(self, text='View Basic Game Stats',
                             command=lambda: controller.show_frame(GameStatsPage))
        button3.pack(pady=5)

        button4 = ttk.Button(self, text='View Individual Player Stats',
                             command=lambda: controller.show_frame(PlayerStatsPage))
        button4.pack(pady=5)

        button5 = ttk.Button(self, text='View Versus Stats',
                             command=lambda: controller.show_frame(VersusStatsPage))
        button5.pack(pady=5)

        button6 = ttk.Button(self, text='Switch User or Database',
                             command=lambda: controller.show_frame(ReLoginPage))
        button6.pack(pady=5)

        button7 = ttk.Button(self, text='Log Out',
                             command=lambda: controller.show_frame(LoginPage))
        button7.pack(pady=5)

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


class AllGamesPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='All Games List', font=14)
        label.pack(pady=10, padx=10)
        self.table = ttk.Treeview(self, columns=('Game ID', 'Winner', 'Winning Score',
                                                 'Loser', 'Losing Score', 'Date Added'))

        self.table.heading('#0', text='Game ID')
        self.table.heading('#1', text='Winner')
        self.table.heading('#2', text='Winning Score')
        self.table.heading('#3', text='Loser')
        self.table.heading('#4', text='Losing Score')
        self.table.heading('#5', text='Date Added')

        button1 = ttk.Button(self, text='Show Games', command=lambda: self.view_games())
        button1.pack(pady=5)

        button2 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                            self.clear()])
        button2.pack(pady=5)

        button3 = ttk.Button(self, text='Delete Selected Game', command=lambda: self.delete_game())
        button3.pack(pady=5)

    def delete_game(self):
        selected_item = self.table.selection()
        self.table.delete(selected_item)
        for game in pingpong.games.find({'game_id': int(selected_item[0])}):
            p1 = game['winner']
            p2 = game['loser']
        pingpong.games.delete_one({'game_id': int(selected_item[0])})
        if pingpong.games.find({'$or': [{'winner': p1}, {'loser': p1}]}).count() == 0:
            pingpong.playerNames.delete_one({'name': p1})
            pingpong.pl_stats.delete_one({'name': p1})
        if pingpong.games.find({'$or': [{'winner': p2}, {'loser': p2}]}).count() == 0:
            pingpong.playerNames.delete_one({'name': p2})
            pingpong.pl_stats.delete_one({'name': p2})

    def clear(self):
        self.table.delete(*self.table.get_children())

    def view_games(self):
        i = pingpong.games.find().count()
        while i > 0:
            for game in pingpong.games.find({'game_id': i}):
                try:
                    self.table.insert('', 'end', game['game_id'], text=game['game_id'],
                                      values=(game['winner'], game['winningScore'],
                                              game['loser'], game['losingScore'],
                                              game['dateAdded']))
                except:
                    self.table.item(game['game_id'], text=game['game_id'],
                                    values=(game['winner'], game['winningScore'],
                                            game['loser'], game['losingScore'],
                                            game['dateAdded']))
                finally:
                    i -= 1
        self.table.pack(pady=5)


class EnterPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Enter Game Info', font=14)
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
        button1.pack(pady=5)

        button2 = ttk.Button(self, text='Clear Entries', command=lambda: self.clear())
        button2.pack(pady=5)

        button3 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                            self.clear()])
        button3.pack(pady=5)

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
        label = tk.Label(self, text='Games Added Successfully From File', font=14)
        label.pack(pady=10)

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(StartPage))
        button.pack(pady=5)

        button2 = ttk.Button(self, text='View All Games', command=lambda: controller.show_frame(AllGamesPage))
        button2.pack(pady=5)


class GameAddedPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Game Added Successfully', font=14)
        label.pack(pady=10)

        button = ttk.Button(self, text='Add Another Game', command=lambda: controller.show_frame(EnterPage))
        button.pack(pady=5)

        button2 = ttk.Button(self, text='View All Games', command=lambda: controller.show_frame(AllGamesPage))
        button2.pack(pady=5)

        button3 = ttk.Button(self, text='Return to Start', command=lambda: controller.show_frame(StartPage))
        button3.pack(pady=5)


class FailedLoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Failed to Connect to Server\n'
                                    'Check Username and Password and Try Again', font=14)
        label.pack(pady=10)

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(LoginPage))
        button.pack(pady=5)


class FailedReLoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Failed to Connect to Server\n'
                                    'Check Username and Password and Try Again', font=14)
        label.pack(pady=10)

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(ReLoginPage))
        button.pack(pady=5)


class FileErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Failed to Add Games From File\n'
                                    'Check Formatting of File', font=14)
        label.pack(pady=10)
        label3 = tk.Label(self, text='Correct Format:\n\nplayer1 score1 player2 score2\n'
                                     'player1 score1 player2 score2\nplayer1 score1 player2 score2\nEtc...', font=14)
        label3.pack(pady=10)

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(StartPage))
        button.pack(pady=5)


class ErrorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Failed to Add Game\n'
                                    'Check Scores and Re-Submit', font=14)
        label.pack(pady=10)

        button = ttk.Button(self, text='Continue', command=lambda: controller.show_frame(EnterPage))
        button.pack(pady=5)


class GameStatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Basic Game Stats', font=14)
        label.pack(pady=10, padx=10)
        self.table = ttk.Treeview(self, columns=('Value', 'Value2'))
        self.table.heading('#0', text='Stat')
        self.table.heading('#1', text='Value')
        self.table.heading('#2', text='Value2')

        button1 = ttk.Button(self, text='Show Stats', command=lambda: self.view_g_stats())
        button1.pack(pady=5)

        button2 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                            self.clear()])
        button2.pack(pady=5)

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
        self.table.pack(pady=5)


class PlayerStatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Select Player to Get Stats for\nThen Click "Show Stats"', font=14)
        label.pack(pady=10, padx=10)
        label2 = tk.Label(self, text='Note: if new players have been added this\n'
                                     'session, click "Update Player Names" to\n'
                                     'update the dropdown menu.', font=14)

        label2.pack(pady=5)
        self.table = ttk.Treeview(self, columns='Value')
        self.table.heading('#0', text='Stat')
        self.table.heading('#1', text='Value')

        button = ttk.Button(self, text='Update Player Names', command=lambda: [self.clear(), self.update_names()])
        button.pack(pady=5)

        self.player = StringVar()
        self.player.set('Select a Player')
        self.dd = OptionMenu(self, self.player, *player_names)
        self.dd.pack(pady=5)

        self.button1 = ttk.Button(self, text='Show Stats', command=lambda: self.view_pl_stats())
        self.button1.pack(pady=5)

        self.button2 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                                 self.clear()])
        self.button2.pack(pady=5)

    def update_names(self):
        self.dd.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.table.destroy()
        new_players = []
        for p in pingpong.playerNames.find():
            new_players.append(p['name'])
        self.dd = OptionMenu(self, self.player, *new_players)
        self.dd.pack(pady=5)
        self.button1 = ttk.Button(self, text='Show Stats', command=lambda: self.view_pl_stats())
        self.button1.pack(pady=5)
        self.button2 = ttk.Button(self, text='Return to Start', command=lambda: [self.controller.show_frame(StartPage),
                                                                                 self.clear()])
        self.button2.pack(pady=5)
        self.table = ttk.Treeview(self, columns='Value')
        self.table.heading('#0', text='Stat')
        self.table.heading('#1', text='Value')

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
        self.table.pack(pady=5)


class VersusStatsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Select Two Players\nThen Click "Show Versus Stats"', font=14)
        label.pack(pady=10, padx=10)
        label2 = tk.Label(self, text='Note: if new players have been added this\n'
                                     'session, click "Update Player Names" to\n'
                                     'update the dropdown menus.', font=14)
        label2.pack(pady=5)
        self.table = ttk.Treeview(self, columns='Value')
        self.table.heading('#0', text='Stat')
        self.table.heading('#1', text='Value')

        button = ttk.Button(self, text='Update Player Names', command=lambda: [self.clear(), self.update_names()])
        button.pack(pady=5)

        self.player1 = StringVar()
        self.player1.set('Select Player 1')
        self.dd1 = OptionMenu(self, self.player1, *player_names)
        self.dd1.pack(pady=5)
        self.player2 = StringVar()
        self.player2.set('Select Player 2')
        self.dd2 = OptionMenu(self, self.player2, *player_names)
        self.dd2.pack(pady=5)

        self.button1 = ttk.Button(self, text='Show Versus Stats', command=lambda: self.view_vs_stats())
        self.button1.pack(pady=5)

        self.button2 = ttk.Button(self, text='Return to Start', command=lambda: [controller.show_frame(StartPage),
                                                                                 self.clear()])
        self.button2.pack(pady=5)

    def update_names(self):
        self.dd1.destroy()
        self.dd2.destroy()
        self.button1.destroy()
        self.button2.destroy()
        self.table.destroy()
        new_players = []
        for p in pingpong.playerNames.find():
            new_players.append(p['name'])
        self.dd1 = OptionMenu(self, self.player1, *new_players)
        self.dd2 = OptionMenu(self, self.player2, *new_players)
        self.dd1.pack(pady=5)
        self.dd2.pack(pady=5)
        self.button1 = ttk.Button(self, text='Show Versus Stats', command=lambda: self.view_vs_stats())
        self.button1.pack(pady=5)
        self.button2 = ttk.Button(self, text='Return to Start', command=lambda: [self.controller.show_frame(StartPage),
                                                                                 self.clear()])
        self.button2.pack(pady=5)
        self.table = ttk.Treeview(self, columns='Value')
        self.table.heading('#0', text='Stat')
        self.table.heading('#1', text='Value')

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
        self.table.pack(pady=5)


app = PingPongApp()
app.mainloop()

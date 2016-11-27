from pymongo import MongoClient
import datetime


""" this module contains methods for connecting to a mongodb database server, adding individual games
    to the database, adding a group of games from a file, updating overall stats, updating
    individual player stats, and updating player vs player stats."""


client = MongoClient('mongodb://user:readonly@ds064748.mlab.com:64748/pingpongstats')
db = client.pingpongstats
games = db.games
playerNames = db.playerNames
g_stats = db.g_stats
pl_stats = db.pl_stats
vs_stats = db.vs_stats


def reconnect(uname, pword, dbname):
    global client, db, games, playerNames, g_stats, pl_stats, vs_stats
    client2 = MongoClient('mongodb://%s:%s@ds064748.mlab.com:64748/%s' % (uname, pword, dbname))
    if client2.server_info():
        client = client2
        db = client.pingpongstats
        games = db.games
        playerNames = db.playerNames
        g_stats = db.g_stats
        pl_stats = db.pl_stats
        vs_stats = db.vs_stats
    else:
        return False


def add_data_obo(player1, score1, player2, score2):
    p1data = {'name': player1}
    p2data = {'name': player2}
    playerNames.update({"name": player1}, p1data, upsert=True)
    playerNames.update({"name": player2}, p2data, upsert=True)
    if int(score1) > int(score2):
        games.insert_one({'winner': player1,
                          'loser': player2,
                          'winningScore': int(score1),
                          'losingScore': int(score2),
                          'dateAdded': datetime.datetime.now(),
                          'game_id': games.count() + 1})
    else:
        games.insert_one({'winner': player2,
                          'loser': player1,
                          'winningScore': int(score2),
                          'losingScore': int(score1),
                          'dateAdded': datetime.datetime.now(),
                          'game_id': games.count() + 1})


def add_data(file):
    # open score sheet file
    with open(file, 'r') as infile:
        for line in infile:
            player1, score1, player2, score2 = line.split()
            p1data = {'name': player1}
            p2data = {'name': player2}
            playerNames.update({"name": player1}, p1data, upsert=True)
            playerNames.update({"name": player2}, p2data, upsert=True)
            if int(score1) > int(score2):
                games.insert_one({'winner': player1,
                                  'loser': player2,
                                  'winningScore': int(score1),
                                  'losingScore': int(score2),
                                  'dateAdded': datetime.datetime.now(),
                                  'game_id': games.count()+1})
            else:
                games.insert_one({'winner': player2,
                                  'loser': player1,
                                  'winningScore': int(score2),
                                  'losingScore': int(score1),
                                  'dateAdded': datetime.datetime.now(),
                                  'game_id': games.count()+1})


def update_g_stats():
    # total games
    tot_games = games.find().count()
    # total overtime games
    ot_games = games.find({'winningScore': {'$gt': 21}}).count()
    # highest score
    high_score = 0
    high_scorer = ''
    for player in pl_stats.find():
        if player['Highest Score'] == high_score:
            high_scorer = high_scorer + ', ' + player['name']
        if player['Highest Score'] > high_score:
            high_score = player['Highest Score']
            high_scorer = player['name']
    # lowest score
    low_score = 99
    low_scorer = ''
    for player in pl_stats.find():
        if player['Lowest Score'] == low_score:
            low_scorer = low_scorer + ', ' + player['name']
        if player['Lowest Score'] < low_score:
            low_score = player['Lowest Score']
            low_scorer = player['name']
    # highest win percentage
    hi_win_pct = 0
    hi_win_pcter = ''
    for player in pl_stats.find({'Total Games': {'$gt': 4}}):
        if player['Overall Win %'] == hi_win_pct:
            hi_win_pcter = hi_win_pcter + ', ' + player['name']
        if player['Overall Win %'] > hi_win_pct:
            hi_win_pct = player['Overall Win %']
            hi_win_pcter = player['name']
    # lowest win percentage
    low_win_pct = 1
    low_win_pcter = ''
    for player in pl_stats.find({'Total Games': {'$gt': 4}}):
        if player['Overall Win %'] == low_win_pct:
            low_win_pcter = low_win_pcter + ', ' + player['name']
        if player['Overall Win %'] < low_win_pct:
            low_win_pct = player['Overall Win %']
            low_win_pcter = player['name']
    # longest win streak
    win_streak = 0
    win_streaker = ''
    for player in pl_stats.find():
        if player['Longest Win Streak'] == win_streak:
            win_streaker = win_streaker + ', ' + player['name']
        if player['Longest Win Streak'] > win_streak:
            win_streak = player['Longest Win Streak']
            win_streaker = player['name']
    # longest losing streak
    lose_streak = 0
    lose_streaker = ''
    for player in pl_stats.find():
        if player['Longest Losing Streak'] == lose_streak:
            lose_streaker = lose_streaker + ', ' + player['name']
        if player['Longest Losing Streak'] > lose_streak:
            lose_streak = player['Longest Losing Streak']
            lose_streaker = player['name']

    data = {'Total Games': tot_games,
            'Games to OT': ot_games,
            'Highest Score': (high_score, high_scorer),
            'Lowest Score': (low_score, low_scorer),
            'Highest Win % (>4 games)': (hi_win_pct, hi_win_pcter),
            'Lowest Win % (>4 games)': (low_win_pct, low_win_pcter),
            'Longest Win Streak': (win_streak, win_streaker),
            'Longest Losing Streak': (lose_streak, lose_streaker)}

    g_stats.update({'Total Games': tot_games,
                    'Games to OT': ot_games,
                    'Highest Score': (high_score, high_scorer),
                    'Lowest Score': (low_score, low_scorer),
                    'Highest Win % (>4 games)': (hi_win_pct, hi_win_pcter),
                    'Lowest Win % (>4 games)': (low_win_pct, low_win_pcter),
                    'Longest Win Streak': (win_streak, win_streaker),
                    'Longest Losing Streak': (lose_streak, lose_streaker)}, data, upsert=True)


def update_pl_stats(name):
    for player in playerNames.find({'name': name}):
        # count total games
        tot_games = games.find({'$or': [{'winner': player['name']}, {'loser': player['name']}]}).count()
        # count games where winner is player['name']
        wins = games.find({'winner': player['name']}).count()
        # losses
        losses = games.find({'loser': player['name']}).count()
        # wins / games played
        winpct = float('%.2f' % (wins / tot_games * 100))
        # average score
        # least points scored
        # most points scored
        scores = []
        for game in games.find({'winner': player['name']}):
            scores.append(game['winningScore'])
        for game in games.find({'loser': player['name']}):
            scores.append(game['losingScore'])
        avg = float('%.2f' % (sum(scores[:]) / tot_games))
        least = min(scores)
        most = max(scores)
        # average score of wins
        # average margin of victory
        scoresw = []
        marginsv = []
        for game in games.find({'winner': player['name']}):
            scoresw.append(game['winningScore'])
            marginsv.append(game['winningScore'] - game['losingScore'])
        if wins == 0:
            avg_scorew = 0
            avg_winby = 0
        else:
            avg_scorew = float('%.2f' % (sum(scoresw[:]) / wins))
            avg_winby = float('%.2f' % (sum(marginsv[:]) / wins))
        # average score of losses
        # average margin of defeat
        scoresl = []
        marginsd = []
        for game in games.find({'loser': player['name']}):
            marginsd.append(game['winningScore'] - game['losingScore'])
            scoresl.append(game['losingScore'])
        if losses == 0:
            avg_scorel = 0
            avg_loseby = 0
        else:
            avg_scorel = float('%.2f' % (sum(scoresl[:]) / losses))
            avg_loseby = float('%.2f' % (sum(marginsd[:]) / losses))
        # number of OT games played, winningScore over 21
        ot = games.find({'$or': [{'winner': player['name']}, {'loser': player['name']}],
                         'winningScore': {'$gt': 21}}).count()
        # number OT games won
        otw = games.find({'winner': player['name'], 'winningScore': {'$gt': 21}}).count()
        # number OT games lost
        otl = games.find({'loser': player['name'], 'winningScore': {'$gt': 21}}).count()
        # OT win percentage
        if otw == 0:
            ot_pct = 0
        else:
            ot_pct = float('%.2f' % (otw / ot * 100))
        # longest win streak
        wcount = 0
        wstreaks = []
        for game in games.find():
            if game['winner'] == player['name']:
                wcount += 1
            elif game['loser'] == player['name']:
                wstreaks.append(wcount)
                wcount = 0
            else:
                wstreaks.append(wcount)
        win_streak = max(wstreaks)
        # longest losing streak
        lcount = 0
        lstreaks = []
        for game in games.find():
            if game['loser'] == player['name']:
                lcount += 1
            elif game['winner'] == player['name']:
                lstreaks.append(lcount)
                lcount = 0
            else:
                lstreaks.append(lcount)
        loss_streak = max(lstreaks)

        data = {'name': player['name'],
                'Total Games': tot_games,
                'Total Wins': wins,
                'Total Losses': losses,
                'Overall Win %': winpct,
                'Average Score': avg,
                'Lowest Score': least,
                'Highest Score': most,
                'Average Margin of Victory': avg_winby,
                'Average Score of Win': avg_scorew,
                'Average Margin of Defeat': avg_loseby,
                'Average Score of Loss': avg_scorel,
                'Total Games to OT': ot,
                'Total OT Games Won': otw,
                'Total OT Games Lost': otl,
                'OT Win %': ot_pct,
                'Longest Win Streak': win_streak,
                'Longest Losing Streak': loss_streak}

        pl_stats.update({'name': player['name'],
                         'Total Games': tot_games,
                         'Total Wins': wins,
                         'Total Losses': losses,
                         'Overall Win %': winpct,
                         'Average Score': avg,
                         'Lowest Score': least,
                         'Highest Score': most,
                         'Average Margin of Victory': avg_winby,
                         'Average Score of Win': avg_scorew,
                         'Average Margin of Defeat': avg_loseby,
                         'Average Score of Loss': avg_scorel,
                         'Total Games to OT': ot,
                         'Total OT Games Won': otw,
                         'Total OT Games Lost': otl,
                         'OT Win %': ot_pct,
                         'Longest Win Streak': win_streak,
                         'Longest Losing Streak': loss_streak}, data, upsert=True)


def update_vs_stats(player1, player2):
    for player in playerNames.find({'name': player1}):
        # games against each player
        for player2 in playerNames.find({'name': player2}):
            # games against player2
            vs_games = games.find({'$or': [{'winner': player['name'], 'loser': player2['name']},
                                           {'winner': player2['name'], 'loser': player['name']}]}).count()
            # wins against player2
            vs_wins = games.find({'winner': player['name'], 'loser': player2['name']}).count()
            # losses against player2
            vs_losses = games.find({'loser': player['name'], 'winner': player2['name']}).count()
            # win percent against player2
            # average score against player2
            # lowest score against p2
            # highest score against p2
            scores = []
            for game in games.find({'winner': player['name'], 'loser': player2['name']}):
                scores.append(game['winningScore'])
            for game in games.find({'loser': player['name'], 'winner': player2['name']}):
                scores.append(game['losingScore'])
            if vs_games == 0:
                vs_winpct = 0
                vs_avg = 0
                vs_least = 0
                vs_most = 0
            else:
                vs_winpct = float('%.2f' % (vs_wins / vs_games * 100))
                vs_avg = float('%.2f' % (sum(scores[:]) / vs_games))
                vs_least = min(scores)
                vs_most = max(scores)
            # average score of wins
            # average margin of victory
            scoresw = []
            marginsv = []
            for game in games.find({'winner': player['name'], 'loser': player2['name']}):
                scoresw.append(game['winningScore'])
                marginsv.append(game['winningScore'] - game['losingScore'])
            if vs_wins == 0:
                vs_avg_scorew = 0
                vs_avg_winby = 0
            else:
                vs_avg_scorew = float('%.2f' % (sum(scoresw[:]) / vs_wins))
                vs_avg_winby = float('%.2f' % (sum(marginsv[:]) / vs_wins))
            # average score of losses
            # average margin of defeat
            scoresl = []
            marginsd = []
            for game in games.find({'loser': player['name'], 'winner': player2['name']}):
                scoresl.append(game['losingScore'])
                marginsd.append(game['winningScore'] - game['losingScore'])
            if vs_losses == 0:
                vs_avg_scorel = 0
                vs_avg_loseby = 0
            else:
                vs_avg_scorel = float('%.2f' % (sum(scoresl[:]) / vs_losses))
                vs_avg_loseby = float('%.2f' % (sum(marginsd[:]) / vs_losses))
            # number of OT games played vs player2, winningScore over 21
            vs_ot = games.find({'$or': [{'winner': player['name'], 'loser': player2['name']},
                                        {'loser': player['name'], 'winner': player2['name']}],
                                'winningScore': {'$gt': 21}}).count()
            # number OT games won
            vs_otw = games.find({'winner': player['name'], 'loser': player2['name'], 'winningScore': {'$gt': 21}}).count()
            # number OT games lost
            vs_otl = games.find({'loser': player['name'], 'winner': player2['name'], 'winningScore': {'$gt': 21}}).count()
            # OT win percentage
            if vs_otw == 0:
                vs_ot_pct = 0
            else:
                vs_ot_pct = float('%.2f' % (vs_otw / vs_ot * 100))
            # longest win streak against player2
            vs_wcount = 0
            vs_wstreaks = [0]
            for game in games.find({'$or': [{'winner': player['name'], 'loser': player2['name']},
                                            {'loser': player['name'], 'winner': player2['name']}]}):
                if game['winner'] == player['name']:
                    vs_wcount += 1
                    vs_wstreaks.append(vs_wcount)
                elif game['loser'] == player['name']:
                    vs_wstreaks.append(vs_wcount)
                    vs_wcount = 0
            vs_win_streak = max(vs_wstreaks)
            # longest losing streak against player2
            vs_lcount = 0
            vs_lstreaks = [0]
            for game in games.find({'$or': [{'winner': player['name'], 'loser': player2['name']},
                                            {'loser': player['name'], 'winner': player2['name']}]}):
                if game['loser'] == player['name']:
                    vs_lcount += 1
                    vs_lstreaks.append(vs_lcount)
                elif game['winner'] == player['name']:
                    vs_lstreaks.append(vs_lcount)
                    vs_lcount = 0
            vs_loss_streak = max(vs_lstreaks)

            data = {'name': player['name'],
                    'opponent': player2['name'],
                    'Games': vs_games,
                    'Wins': vs_wins,
                    'Losses': vs_losses,
                    'Win %': vs_winpct,
                    'Average Score': vs_avg,
                    'Lowest Score': vs_least,
                    'Highest Score': vs_most,
                    'Average Margin of Victory': vs_avg_winby,
                    'Average Score of Win': vs_avg_scorew,
                    'Average Margin of Defeat': vs_avg_loseby,
                    'Average Score of Loss': vs_avg_scorel,
                    'Games to OT': vs_ot,
                    'Games Won in OT': vs_otw,
                    'Games Lost in OT': vs_otl,
                    'OT Win %': vs_ot_pct,
                    'Longest Win Streak': vs_win_streak,
                    'Longest Losing Streak': vs_loss_streak}

            vs_stats.update({'name': player['name'],
                             'opponent': player2['name'],
                             'Games': vs_games,
                             'Wins': vs_wins,
                             'Losses': vs_losses,
                             'Win %': vs_winpct,
                             'Average Score': vs_avg,
                             'Lowest Score': vs_least,
                             'Highest Score': vs_most,
                             'Average Margin of Victory': vs_avg_winby,
                             'Average Score of Win': vs_avg_scorew,
                             'Average Margin of Defeat': vs_avg_loseby,
                             'Average Score of Loss': vs_avg_scorel,
                             'Games to OT': vs_ot,
                             'Games Won in OT': vs_otw,
                             'Games Lost in OT': vs_otl,
                             'OT Win %': vs_ot_pct,
                             'Longest Win Streak': vs_win_streak,
                             'Longest Losing Streak': vs_loss_streak}, data, upsert=True)

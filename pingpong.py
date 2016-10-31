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
        if player['highest score'] == high_score:
            high_scorer = high_scorer + ', ' + player['name']
        if player['highest score'] > high_score:
            high_score = player['highest score']
            high_scorer = player['name']
    # lowest score
    low_score = 99
    low_scorer = ''
    for player in pl_stats.find():
        if player['lowest score'] == low_score:
            low_scorer = low_scorer + ', ' + player['name']
        if player['lowest score'] < low_score:
            low_score = player['lowest score']
            low_scorer = player['name']
    # highest win percentage
    hi_win_pct = 0
    hi_win_pcter = ''
    for player in pl_stats.find({'total games': {'$gt': 4}}):
        if player['overall win percentage'] == hi_win_pct:
            hi_win_pcter = hi_win_pcter + ', ' + player['name']
        if player['overall win percentage'] > hi_win_pct:
            hi_win_pct = player['overall win percentage']
            hi_win_pcter = player['name']
    # lowest win percentage
    low_win_pct = 1
    low_win_pcter = ''
    for player in pl_stats.find({'total games': {'$gt': 4}}):
        if player['overall win percentage'] == low_win_pct:
            low_win_pcter = low_win_pcter + ', ' + player['name']
        if player['overall win percentage'] < low_win_pct:
            low_win_pct = player['overall win percentage']
            low_win_pcter = player['name']
    # longest win streak
    win_streak = 0
    win_streaker = ''
    for player in pl_stats.find():
        if player['longest win streak'] == win_streak:
            win_streaker = win_streaker + ', ' + player['name']
        if player['longest win streak'] > win_streak:
            win_streak = player['longest win streak']
            win_streaker = player['name']
    # longest losing streak
    lose_streak = 0
    lose_streaker = ''
    for player in pl_stats.find():
        if player['longest losing streak'] == lose_streak:
            lose_streaker = lose_streaker + ', ' + player['name']
        if player['longest losing streak'] > lose_streak:
            lose_streak = player['longest losing streak']
            lose_streaker = player['name']

    data = {'total games': tot_games,
            'games to OT': ot_games,
            'highest score': (high_scorer, high_score),
            'lowest score': (low_scorer, low_score),
            'highest win percentage (>4 games played)': (hi_win_pcter, hi_win_pct),
            'lowest win percentage (>4 games played)': (low_win_pcter, low_win_pct),
            'longest win streak': (win_streaker, win_streak),
            'longest losing streak': (lose_streaker, lose_streak)}

    g_stats.update({'total games': tot_games,
                    'games to OT': ot_games,
                    'highest score': (high_scorer, high_score),
                    'lowest score': (low_scorer, low_score),
                    'highest win percentage (>4 games played)': (hi_win_pcter, hi_win_pct),
                    'lowest win percentage (>4 games played)': (low_win_pcter, low_win_pct),
                    'longest win streak': (win_streaker, win_streak),
                    'longest losing streak': (lose_streaker, lose_streak)}, data, upsert=True)


def update_pl_stats(name):
    for player in playerNames.find({'name': name}):
        # count total games
        tot_games = games.find({'$or': [{'winner': player['name']}, {'loser': player['name']}]}).count()
        # count games where winner is player['name']
        wins = games.find({'winner': player['name']}).count()
        # losses
        losses = games.find({'loser': player['name']}).count()
        # wins / games played
        winpct = wins / tot_games
        # average score
        # least points scored
        # most points scored
        scores = []
        for game in games.find({'winner': player['name']}):
            scores.append(game['winningScore'])
        for game in games.find({'loser': player['name']}):
            scores.append(game['losingScore'])
        avg = sum(scores[:]) / tot_games
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
            avg_scorew = sum(scoresw[:]) / wins
            avg_winby = sum(marginsv[:]) / wins
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
            avg_scorel = sum(scoresl[:]) / losses
            avg_loseby = sum(marginsd[:]) / losses
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
            ot_pct = otw / ot
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
                'total games': tot_games,
                'total wins': wins,
                'total losses': losses,
                'overall win percentage': winpct,
                'average score': avg,
                'lowest score': least,
                'highest score': most,
                'average margin of victory': avg_winby,
                'average score of win': avg_scorew,
                'average margin of defeat': avg_loseby,
                'average score of loss': avg_scorel,
                'total games gone to OT': ot,
                'total OT games won': otw,
                'total OT games lost': otl,
                'OT win percentage': ot_pct,
                'longest win streak': win_streak,
                'longest losing streak': loss_streak}

        pl_stats.update({'name': player['name'],
                         'total games': tot_games,
                         'total wins': wins,
                         'total losses': losses,
                         'overall win percentage': winpct,
                         'average score': avg,
                         'lowest score': least,
                         'highest score': most,
                         'average margin of victory': avg_winby,
                         'average score of win': avg_scorew,
                         'average margin of defeat': avg_loseby,
                         'average score of loss': avg_scorel,
                         'total games gone to OT': ot,
                         'total OT games won': otw,
                         'total OT games lost': otl,
                         'OT win percentage': ot_pct,
                         'longest win streak': win_streak,
                         'longest losing streak': loss_streak}, data, upsert=True)


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
                vs_winpct = vs_wins / vs_games
                vs_avg = sum(scores[:]) / vs_games
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
                vs_avg_scorew = sum(scoresw[:]) / vs_wins
                vs_avg_winby = sum(marginsv[:]) / vs_wins
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
                vs_avg_scorel = sum(scoresl[:]) / vs_losses
                vs_avg_loseby = sum(marginsd[:]) / vs_losses
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
                vs_ot_pct = vs_otw / vs_ot
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
                    'games against ' + player2['name']: vs_games,
                    'wins against ' + player2['name']: vs_wins,
                    'losses against ' + player2['name']: vs_losses,
                    'win percentage against ' + player2['name']: vs_winpct,
                    'average score against ' + player2['name']: vs_avg,
                    'lowest score against ' + player2['name']: vs_least,
                    'highest score against ' + player2['name']: vs_most,
                    'average margin of victory against ' + player2['name']: vs_avg_winby,
                    'average score of win against ' + player2['name']: vs_avg_scorew,
                    'average margin of defeat against ' + player2['name']: vs_avg_loseby,
                    'average score of loss against ' + player2['name']: vs_avg_scorel,
                    'games to OT against ' + player2['name']: vs_ot,
                    'games won in OT against ' + player2['name']: vs_otw,
                    'games lost in OT against ' + player2['name']: vs_otl,
                    'OT win percentage against ' + player2['name']: vs_ot_pct,
                    'longest win streak against ' + player2['name']: vs_win_streak,
                    'longest losing streak against ' + player2['name']: vs_loss_streak}

            vs_stats.update({'name': player['name'],
                             'games against ' + player2['name']: vs_games,
                             'wins against ' + player2['name']: vs_wins,
                             'losses against ' + player2['name']: vs_losses,
                             'win percentage against ' + player2['name']: vs_winpct,
                             'average score against ' + player2['name']: vs_avg,
                             'lowest score against ' + player2['name']: vs_least,
                             'highest score against ' + player2['name']: vs_most,
                             'average margin of victory against ' + player2['name']: vs_avg_winby,
                             'average score of win against ' + player2['name']: vs_avg_scorew,
                             'average margin of defeat against ' + player2['name']: vs_avg_loseby,
                             'average score of loss against ' + player2['name']: vs_avg_scorel,
                             'games to OT against ' + player2['name']: vs_ot,
                             'games won in OT against ' + player2['name']: vs_otw,
                             'games lost in OT against ' + player2['name']: vs_otl,
                             'OT win percentage against ' + player2['name']: vs_ot_pct,
                             'longest win streak against ' + player2['name']: vs_win_streak,
                             'longest losing streak against ' + player2['name']: vs_loss_streak}, data, upsert=True)

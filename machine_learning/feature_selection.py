from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression

from database.config import TEAMS
from machine_learning.player_stats import find_runningbacks, \
    player_stats, convert_stats_to_points, runningback_stats, \
    gameplay_percentage
import nflgame as nfl
import pandas as pd
from pandas import DataFrame

FEATURES = ['RECENT PLAYER STATS',
            'SEASON PLAYER STATS',
            'TEAM STATS',
            '']

def recent_player_stats_FEATURE():

    year, current_week = nfl.live.current_year_and_week()
    games = nfl.games(year, current_week)
    players = {player.playerid: player.player
               for player in nfl.combine_max_stats(games)
               if player.player is not None}
    rbs = find_runningbacks(players)
    n = 5
    weeklystats = []
    #headers = []

    for player in rbs:
        for week in range(current_week-n, current_week):
            wstats = []
            stats = player.stats(year, week)
            game = nfl.one(year, week, home=player.team, away=player.team)
            if game != None:
                #add basic stats
                headers = ["Fantasy Points", "Position",
                           "Points Per Rush Attempt", "Points Per Target Att"]
                wstats = runningback_stats(stats, player)
                #wstats.append(  runningback_stats(stats, player))

                #add play percentage
                teamplay_percentage, play_percentage = gameplay_percentage(player, game)
                headers.append("Team Play Percentage")
                wstats.append(  teamplay_percentage)
                headers.append("Game Play Percentage")
                wstats.append(  play_percentage)

                # add player team and opponent
                if player.team == game.home:
                    opponent = game.away
                else:
                    opponent = game.home
                if opponent == "JAX":
                    opponent = "JAC"
                headers.append("Team")
                if player.team == "JAX":
                    wstats.append(TEAMS["JAC"])
                else:
                    wstats.append(TEAMS[player.team])
                headers.append("Opponent")
                wstats.append(  TEAMS[opponent])

                #add player name
                headers.append("Player Name")
                wstats.append(player.name)
                #add full list to weeklystats
                weeklystats.append(wstats)

    weeklystats = DataFrame(weeklystats)
    weeklystats.columns = headers
    #print(weeklystats)
    return weeklystats

def visualize_dataset(df):
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set(style='whitegrid', context='notebook')
    df.columns = ["FP", "Pos", "PR/A", "PT/A", "TPP", "GPP", "Team", "Opp", "Name"]
    sns.pairplot(data=df, size=2.5)
    plt.show()

if __name__ == "__main__":
    #TODO passing_yds doesn't work -- passing a stat player_stats(passing_yds, "Ben Roethlisberger", 2016)

    weeklystats = recent_player_stats_FEATURE()
    visualize_dataset(weeklystats)

    #X, y = weeklystats.iloc[:,1:-1], weeklystats.iloc[:,0]
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    '''
    print(X)
    print("---" *9)
    print(y)
    print(X_train)
    '''
    '''
    scaler = MinMaxScaler()
    #scaler = StandardScaler()
    X_train_std = scaler.fit_transform(X_train)
    X_test_std = scaler.transform(X_test)
    print(X_train_std)
    print(X_test_std)
    '''
    '''
    lr = LogisticRegression(penalty='l1', C=0.1)
    lr.fit(X_train, y_train)
    #lr.fit(X_train_std, y_train)
    print('Training Accuracy:', lr.score(X_train, y_train))
    print('Test Accuracy:', lr.score(X_test, y_test))
    print(lr.intercept_)
    print(lr.coef_)
    '''
    '''
    #Yearly Stats
    years = [2009, 2010, 2011, 2012, 2013, 2014, 2015]
    for player in rbs:
        for year in years:
            player.stats(year)
            pstats = []
            pstats.append(player.convert_stats_to_points)
    '''
    '''
    player = nfl.find('Ezekiel Elliott')[0]
    print(player)
    games = nfl.games(2016)
    for i,game in enumerate(games):
        if game.players.playerid(player.playerid):
            points = convert_stats_to_points(game.players.playerid(player.playerid))
            print('Game {:2}, Week {:2} - {:4}'.format(i + 1, game.schedule['week'], points))
    '''
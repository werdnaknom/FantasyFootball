import nflgame as nfl
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def find_runningbacks(players):
    '''Extracts running backs (RB) from a list of players'''
    runningbacks = {p : {'player' : players[p]}for p in players if players[p].position == 'RB'}
    return runningbacks

def yearly_stats(players, YEARS=None):
    if YEARS == None:
        YEARS = [2009, 2010, 2011, 2012, 2013, 2014, 2015]
    for p in players.keys():
        Y = []
        X = []

        for year in YEARS:
            try:
                players[p][year] = players[p]['player'].stats(year).stats
                #rush_att = players[p][year]['rushing_att']
                #rush_yds = players[p][year]['rushing_yds']
                #print(rush_att)
                #print(rush_yds)
                #print(float(rush_yds/rush_att))
                #X.append(float(rush_yds/rush_att))
                #Y.append(year)
                #plt.scatter(X, Y)
                #plt.show()
                #rint(dir(players[p].stats(2015)))
                #p[year] = players[p].stats(year).formatted_stats
                #players[p][year] = players[p].stats(year).stats
            except:
                pass
    for p in players.keys():

        plt.scatter(Y,X)
        plt.show()
        #print ('---' *6)


def rbs_prettyprint(rbs):
    fmt = "{:20} | {:4}"
    for rb in rbs.values():
        print(fmt.format(rb.name, rb.weight))

def team_stats(game):
    home = game.stats_home
    away = game.stats_away
    #Passing Yards Per Attempt (sacks and yards lost subtracted)
    pya = home.passing_yds / sum(game.data['home']['stats']['passing'][player]['att'] for player in game.data['home']['stats']['passing'])
    #Defensive Passing Yards Per Attempt (sacks and yards lost subtracted)
    dypa = away.passing_yds / sum(game.data['away']['stats']['passing'][player]['att'] for player in game.data['away']['stats']['passing'])
    #Rushing Yards per attempt
    rya = home.rushing_yds / sum(game.data['home']['stats']['rushing'][player]['att'] for player in game.data['home']['stats']['rushing'])
    #Defense Rushing Yards per attempt
    drya = away.rushing_yds / sum(game.data['away']['stats']['rushing'][player]['att'] for player in game.data['away']['stats']['rushing'])
    #Turnovers committed
    to = home.turnovers
    #Defensive Turnovers
    dto = away.turnovers
    #Differntial between penaties
    pendif = home.penalty_yds - away.penalty_yds
    #Return Touchdowns by opponent (includes TDs scored on fumbles, interceptions, kickoffs, and punts
    #ettd = sum(player.defense_tds for player in game.max_player_stats() if player.defense_tds > 0 and not player.home)
    rettd = 0
    '''
    int_td = 'defense_int_tds'
    d_td = 'defense_tds'
    kick_td = 'kickret_tds'
    fum_td = 'fumbles_rec_tds'
    misc_td = 'defense_misc_tds'
    '''
    scoring_margin = 3.17*rettd-0.6*pendif+61.67*pya+26.44*rya-2.77*to-67.5*dypa-22.79*drya+3.49*dto
    if scoring_margin >= 0 and game.score_home > game.score_away:
        winner = True
    elif scoring_margin >= 0 and game.score_home < game.score_away:
        winner = False
    elif scoring_margin <= 0 and game.score_home < game.score_away:
        winner = True
    else:
        winner = False
    return scoring_margin, game.score_home, game.score_away, winner

if __name__ == "__main__":
    '''
    players = nfl.players
    players = player_plays()
    #rbs = find_runningbacks(players)
    print(rbs)
    '''
    print("hello")
    #yearly_stats(rbs)
    #stats = set().union(*(players[player].stats(2016).stats for player in players))
    #print(stats)
    count = 0
    correct = 0
    fmt = "Score Difference {:9.4f} | {:4} | {:4} | {:10} "
    for game in nfl.games([2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]):
        ts = team_stats(game)
        print(fmt.format(*ts))
        count += 1
        if ts[3]:
            correct += 1

    print(correct/count)
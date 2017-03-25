from sklearn.model_selection import train_test_split
from machine_learning.player_stats import find_runningbacks, player_stats, convert_stats_to_points
import nflgame as nfl

if __name__ == "__main__":
    #TODO passing_yds doesn't work -- passing a stat player_stats(passing_yds, "Ben Roethlisberger", 2016)
    rbs = find_runningbacks(nfl.players)
    #print(rbs)
    player = nfl.find('Ezekiel Elliott')[0]
    print(player)
    games = nfl.games(2016)
    for i,game in enumerate(games):
        if game.players.playerid(player.playerid):
            points = convert_stats_to_points(game.players.playerid(player.playerid))
            print('Game {:2}, Week {:2} - {:4}'.format(i + 1, game.schedule['week'], points))
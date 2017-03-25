import unittest
import nflgame as nfl
import machine_learning.player_stats

class PlayerStatsTestCase(unittest.TestCase):
    def setUp(self):
        self.ps = machine_learning.player_stats
        self.games = nfl.games(2016)

    def _helper_points_to_stats(self, player, actual):

        count = 0
        games = nfl.games(2016)
        for game in games:
            if game.players.playerid(player.playerid):
                points = self.ps.convert_stats_to_points(game.players.playerid(player.playerid))
                self.assertEqual(points, actual[count])
                count += 1

    def test_convert_stats_to_points_QB_aRogers(self):
        arogers = nfl.find('Aaron Rodgers')[0]
        actual = [23.56, 18.42, 26.40, 17.86, 13.46, 23.74, 33.84, 27.18, 29.54, 29.34, 23.12, 15.96, 21.24, 11.98, 37.18, 34.20]
        self._helper_points_to_stats(arogers, actual)

    def test_convert_stats_to_points_QB_bigBen(self):
        bigben = nfl.find('Ben Roethlisberger')[0]
        actual = [22.80, 21.76, 7.98, 33.90, 29.20, 11.56, 19.86, 28.42, 8.68, 20.84, 18.56, 5.60, 14.94, 21.06]
        self._helper_points_to_stats(bigben, actual)

    def test_convert_stats_to_points_QB_aLuck(self):
        aluck = nfl.find('Andrew Luck')[0]
        actual = [35.50, 11.08, 14.24, 18.66, 22.18, 24.38, 27.82, 19.40, 14.74, 19.68, 29.72, 18.24, 18.80, 26.72, 19.54 ]
        self._helper_points_to_stats(aluck, actual)

    def test_convert_stats_to_points_RB_ezeElliot(self):
        eze = nfl.find('Ezekiel Elliott')[0]
        actual = [12.20, 14.70, 18.00, 22.70, 32.10, 19.40, 18.80, 22.70, 40.90, 16.70, 26.00, 20.50, 10.70, 27.80, 22.20]
        self._helper_points_to_stats(eze, actual)

    def test_convert_stats_to_points_WR_aBrown(self):
        abrown = nfl.find('Antonio Brown')[0]
        actual = [32.60, 7.90, 26.00, 22.40, 22.80, 8.50, 18.90, 21.50, 34.40, 15.60, 32.10, 17.40, 12.80, 8.80, 25.60]
        self._helper_points_to_stats(abrown, actual)

    def test_convert_stats_to_points_TE_rGronkowski(self):
        gronk = nfl.find('Rob Gronkowski')[0]
        actual = [2.10, 15.90, 29.20, 19.30, 21.90, 8.60]
        self._helper_points_to_stats(gronk, actual)
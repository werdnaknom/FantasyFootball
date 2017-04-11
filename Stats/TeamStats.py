from Stats.thinkbayes import Suite, MakeGaussianPmf
import Stats.thinkbayes as thinkbayes
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import poisson
import nflgame as nfl

class ProbabilityOfPass(Suite):

    def Likelihood(self, data, hypo):
        #Needs to be used with function UpdateSet
        #Data is of type tuple (# of pass plays, # of rush plays)
        x = hypo / 100.0
        passing, rushing = data
        like = x**passing * (1-x)**rushing
        return like


class Football(Suite):

    def __init__(self):
        pmf = MakeGaussianPmf(2.7, 0.3, 4)
        Suite.__init__(pmf)
        self.stats = []

    def EvalPoissonPmf(self, k, lam):
        #return np.random.poisson(lam)
        return (lam)**k * math.exp(-lam) / math.factorial(k)

    def Likelihood(self, data, hypo):
        '''
        :param data: Data is the observed number of goals, k
        :param hypo: Each hypothesis is a possible value of lamda
        :return: float probability that data is in hypothesis
        '''
        lam = hypo
        k = data
        like = self.EvalPoissonPmf(k, lam)
        return like

    def MakePoissonPmf(self, lam, high):
        pmf = thinkbayes.Pmf()
        for k in range(0, high+1):
            p = self.EvalPoissonPmf(k, lam)
            pmf.Set(k, p)
        pmf.Normalize()
        return pmf


class Team():

    def __init__(self, teamabbr, season=2016):
        self.teamabbr = teamabbr
        self.games = nfl.games(season, home=self.teamabbr, away=self.teamabbr)
        self.stats = []

    def getStats(self):
        if len(self.stats) == 0:
            for game in self.games:
                if game.home == self.teamabbr:
                    self.stats.append(game.stats_home)
                else:
                    self.stats.append(game.stats_away)
        return self.stats


    def teamPassing(self):
        stats = self.getStats()
        passing = [stat.passing_yds for stat in stats]
        return np.array(passing)

    def teamRushing(self):
        stats = self.getStats()
        rushing = [stat.rushing_yds for stat in stats]
        return np.array(rushing)

    def teamPenatly(self):
        stats = self.getStats()
        penalty = [stat.penalty_yds for stat in stats]
        return np.array(penalty)

    def teamTurnOver(self):
        stats = self.getStats()
        to = [stat.turnovers for stat in stats]
        return np.array(to)

    def teamTotalYds(self):
        stats = self.getStats()
        yds = [stat.total_yds for stat in stats]
        return np.array(yds)

    def teamRushAtt(self):
        games = self.games
        rush_att = []
        for game in games:
            rush_att.append(sum(player.rushing_att for player in game.max_player_stats().rushing()
                         if player.team == self.teamabbr))
        return np.array(rush_att)

    def teamPassAtt(self):
        games = self.games
        pass_att = []
        for game in games:
            pass_att.append(sum(player.passing_att for player in game.max_player_stats().passing()
                         if player.team == self.teamabbr))
        return np.array(pass_att)

    def teamReturnTD(self):
        games = self.games
        returnTD = []
        returnTD.append(1)
        #TODO:: Return TD
        return np.array(returnTD)

    def teamScoring(self, opponent):
        RET_TD = self.teamReturnTD()
        PENDIF = self.teamPenatly() - opponent.teamPenalty()
        PYA = self.teamPassing() / self.teamPassAtt()
        RYA = self.teamRushing() / self.teamRushAtt()
        TO = self.teamTurnOver()
        DPYA = opponent.teamPassing() / opponent.teamPassAtt()
        DRYA = opponent.teamRushing() / opponent.teamRushAtt()
        DTO = opponent.teamTurnOver()

        score = 3.17(RET_TD) - 0.06(PENDIF) + 61.67(PYA) + 26.44 (RYA) -2.77(TO)
        - 67.5(DPYA) - 22.79(DRYA) + 3.49(DTO)


    def teamPoints(self):
        '''
        :param season: season or list of seasons to evaluate
        :return: returns a list of all the team's scores throughout the season.
        '''
        scores = []
        for game in self.games:
            if self.teamabbr == game.home:
                scores.append(game.score_home)
            else:
                scores.append(game.score_away)
        return np.array(scores)

    def teamMeanPoints(self, points):
        return points.mean()

    def poisson(self, mu, range=None):
        if range == None:
            x = np.arange(poisson.ppf(0.01, mu), poisson.ppf(0.99, mu))
        else:
            x = range
        p = poisson.pmf(x, mu)
        return x, p

    def poissonPoints(self, season, home=False, range=None):
        '''
        
        :param season: season or list of seasons to evaluated
        :param range: the range to evaluate the poisson process over
        :return: returns a list of probabilities based on the distribution x
        '''

        points = self.teamPoints(season)
        mu = points.mean()
        if home:
            mu += 3
        x, prob =self.poisson(mu, range)
        return x, prob

    def graphPoisson(self, season, range=None):
        '''
        :param season: season or list of seasons to evaluated
        :return: None
        '''
        fig, ax = plt.subplots(1,1)

        points = self.teamPoints(season)
        mu = points.mean()

        if range == None:
            x = np.arange(poisson.ppf(0.01, mu), poisson.ppf(0.99, mu))
        else:
            x = range
        p = poisson.pmf(x, mu)
        ax.plot(x, p, 'bo', ms=8, label=self.teamabbr + ' poisson pmf')
        ax.vlines(x, 0, poisson.pmf(x, mu), colors='b', lw=5, alpha=1)

        rv = poisson(mu)
        ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1, label='frozen pmf')
        ax.legend(loc='best', frameon=False)
        plt.show()

        plt.show()

def graphedTeamsCompared(season=[2016]):

    for team in nfl.teams:
        try:
            t = Team(team[0])
            x, y = t.poissonPoints(season, range=range(0, 50))
            plt.plot(x, y, label=team[0])

        except TypeError:
            print(team)

    plt.xlabel("Points Scored")
    plt.ylabel("Probability")
    plt.legend(loc='best', frameon=True)
    plt.show()

def individual_teams():
    # seasons = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
    '''
    seasons = [2016]
    graphedTeamsCompared(seasons)

    t = Team("KC")

    a, b = t.poissonPoints(seasons)
    for i, x in enumerate(a):
        print(x, b[i])
    '''
    t1 = Team('NE')
    t2 = Team('CAR')

    x1, prob1 = t1.poissonPoints(2016, range=range(0, 50))
    x2, prob2 = t2.poissonPoints(2016, range=range(0, 50))
    team1 = {x : prob1[x] for x in x1}
    team2 = {x: prob2[x] for x in x2}

    diff = dict()
    for v1, p1 in team1.items():
        for v2, p2 in team2.items():
            x = v1-v2
            diff[x] = diff.get(x, 0) + p1*p2

    # print(pmf1)
    # print(pmf2)

    # diff.ProbGreater(0)
    p_win = [prob for (x, prob) in diff.items() if x > 0]
    print(p_win)
    print(sum(p_win))
    p_lose = [prob for (x, prob) in diff.items() if x < 0]
    print(p_lose)
    print(sum(p_lose))
    # print(diff)
    '''
    pop = ProbabilityOfPass(range(0,101))
    rushing = 30
    passing = 10
    pop.Update((passing, rushing))
    pop.Print()
    '''
    # poisson.ppf()
    # poisson.pmf()



    '''
    for team in nfl.teams:
        t = Team(team[0])
        t.graphPoisson([2015,2016], range=range(0,50))
    '''

def season_stats(season):
    fmt = "{:3} vs {:3} | {:2}({:4}) -- {:2}({:4}) | {:5} "
    count = 0
    correct = 0
    for game in nfl.games(season):
        try:
            home = game.home
            away = game.away

            t1 = Team(home)
            t2 = Team(away)

            x1, prob1 = t1.poissonPoints(season, range=range(0, 50), home=True)
            x2, prob2 = t2.poissonPoints(season, range=range(0, 50))
            team1 = {x: prob1[x] for x in x1}
            team2 = {x: prob2[x] for x in x2}

            diff = dict()
            for v1, p1 in team1.items():
                for v2, p2 in team2.items():
                    x = v1 - v2
                    diff[x] = diff.get(x, 0) + p1 * p2

            p_win = sum(prob for (x, prob) in diff.items() if x > 0)
            p_lose = sum(prob for (x, prob) in diff.items() if x < 0)


            home_score = game.score_home
            away_score = game.score_away

            result = ""

            if p_win > p_lose and home_score > away_score:
                result = True
            elif p_win < p_lose and home_score < away_score:
                result = True
            elif p_win == p_lose:
                result = "Unknown"
            elif p_win > p_lose and home_score < away_score:
                result = False
            elif p_win < p_lose and home_score > away_score:
                result = False
            elif home_score == away_score:
                result = "Tie"
            else:
                result = "Failure"

            if result == True:
                correct += 1
            count += 1


            #print(fmt.format(home, away, home_score, round(p_win,2), away_score, round(p_lose,2), result))
        except TypeError:
            print(home, away)
    print(season, ":", correct/count)

def mathletics_distri(season):
    t1 = Team('GB')
    t1_to = t1.poisson(t1.teamTurnOver().mean())
    t1_rushatt = t1.poisson(t1.teamRushAtt().mean())
    t1_rushyds = t1.poisson(t1.teamRushing().mean())
    t1_passatt = t1.poisson(t1.teamPassAtt().mean())
    t1_passyd = t1.poisson(t1.teamPassing().mean())
    t1_penalty = t1.poisson(t1.teamPenatly().mean())
    t1_rettd = t1.poisson(t1.teamReturnTD().mean())

    t2 = Team('KC')
    t2_to = t2.poisson(t2.teamTurnOver().mean(), range=t1_to[0])
    t2_rushatt = t2.poisson(t2.teamRushAtt().mean(), range=t1_rushatt[0])
    t2_rushyds = t2.poisson(t2.teamRushing().mean(), range=t1_rushyds[0])
    t2_passatt = t2.poisson(t2.teamPassAtt().mean(), range=t1_passatt[0])
    t2_passyd = t2.poisson(t2.teamPassing().mean(), range=t1_passyd[0])
    t2_penalty = t2.poisson(t2.teamPenatly().mean(), range=t1_penalty[0])
    t2_rettd = t2.poisson(t2.teamReturnTD().mean(), range=t1_rettd[0])

    print(t1_rushyds[1])
    print(t2_rushyds[1])
    print(t1_rushyds[1] - t2_rushyds[1])





if __name__ == "__main__":
    #individual_teams()
    '''
    for season in [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]:
        season_stats(season=season)
    '''
    mathletics_distri(2016)

"""

class TeamScoring(Suite):
    '''Represents a hypothesis about the scoring rate for a team'''

    def __init__(self, name=''):
        '''
        Initializes the Football Scoring Object
        :param name: string
        '''
        self.name = name
        mu = self.teamPoints(2016).mean()
        sigma = 6

        pmf = thinkbayes.MakeGaussianPmf(mu, sigma, 4)
        Suite.__init__(self, pmf, name=name)

    def Likelihood(self, data, hypo):
        '''Computes the likelihood of the data under the hypothesis.

        Evaluates the Poisson PMF for lambda and k.

        hypo: goal scoring rate in goals per game
        data: goals scored in one period
        '''
        lam = hypo
        k = data
        like = thinkbayes.EvalPoissonPmf(k, lam)
        return like

    def teamPoints(self, season):
        '''
        :param season: season or list of seasons to evaluate
        :return: returns a list of all the team's scores throughout the season.
        '''
        games = nfl.games(season, home=self.name, away=self.name)
        scores = []
        for game in games:
            if self.name == game.home:
                scores.append(game.score_home)
            else:
                scores.append(game.score_away)
        return np.array(scores)
        #return scores

def MakeGoalPmf(suite, high=100):
    '''Makes the distribution of goals scored, given distribution of lam.

    suite: distribution of goal-scoring rate
    high: upper bound

    returns: Pmf of goals per game
    '''
    metapmf = thinkbayes.Pmf()

    for lam, prob in suite.Items():
        pmf = thinkbayes.MakePoissonPmf(lam, high)
        metapmf.Set(pmf, prob)

    mix = thinkbayes.MakeMixture(metapmf, name=suite.name)
    return mix


def MakeGoalTimePmf(suite):
    '''Makes the distribution of time til first goal.

    suite: distribution of goal-scoring rate

    returns: Pmf of goals per game
    '''
    metapmf = thinkbayes.Pmf()

    for lam, prob in suite.Items():
        pmf = thinkbayes.MakeExponentialPmf(lam, high=2, n=2001)
        metapmf.Set(pmf, prob)

    mix = thinkbayes.MakeMixture(metapmf, name=suite.name)
    return mix

def TestTest123():
    suite1 = TeamScoring("DEN")
    suite2 = TeamScoring("CAR")

    suite1.UpdateSet(suite1.teamPoints(2016))
    suite2.UpdateSet(suite2.teamPoints(2016))

    goal_dist1 = MakeGoalPmf(suite1)
    goal_dist2 = MakeGoalPmf(suite2)

    time_dist1 = MakeGoalTimePmf(suite1)
    time_dist2 = MakeGoalTimePmf(suite2)

    print("NE", suite1.MaximumLikelihood())
    print("ARI", suite2.MaximumLikelihood())

    diff = goal_dist1 - goal_dist2
    print("Diff", diff)
    p_win = diff.ProbGreater(0)
    print("Win:", p_win)
    p_loss = diff.ProbLess(0)
    print("Lose:", p_loss)
    p_tie = diff.Prob(0)
    print("Tie:", p_tie)

    p_overtime = thinkbayes.PmfProbLess(time_dist1, time_dist2)
    p_adjust = thinkbayes.PmfProbEqual(time_dist1, time_dist2)
    p_overtime += p_adjust / 2
    print('p_overtime', p_overtime)

    print(p_overtime * p_tie)
    p_win += p_overtime * p_tie
    print('p_win', p_win)

    # win the next two
    p_series = p_win ** 2

    # split the next two, win the third
    p_series += 2 * p_win * (1 - p_win) * p_win

    print('p_series', p_series)

def predictSeason():
    #print("Game | %Win | %Lose | Home Score | Away Score |")
    fmt = "{:3} vs {:3} | {:2}({:4}) -- {:2}({:4}) |"
    for game in nfl.games(2016):
        home = game.home
        away = game.away

        suite1 = TeamScoring(home)
        suite2 = TeamScoring(away)

        suite1.UpdateSet(suite1.teamPoints(2016))
        suite2.UpdateSet(suite2.teamPoints(2016))

        goal_dist1 = MakeGoalPmf(suite1)
        goal_dist2 = MakeGoalPmf(suite2)

        diff = goal_dist1 - goal_dist2

        p_win = diff.ProbGreater(0)

        p_loss = diff.ProbLess(0)


        home_score = game.score_home
        away_score = game.score_away

        print(fmt.format(home, away, home_score, p_win, away_score, p_loss))

if __name__ == "__main__":
    TestTest123()
    predictSeason()

"""
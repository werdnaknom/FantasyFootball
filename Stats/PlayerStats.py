from Stats.thinkbayes import Pdf
from scipy import stats
import nflgame as nfl
import numpy as np
import csv
import matplotlib.pyplot as plt

class EstimatePlayerPointsPdf(Pdf):
    """creates a probability density function based on a players points

       Attributes:
           points: list fantasy points
           kde: A gaussian Kernal Density Function
           
    """
    def __init__(self, points, name=""):
        self.name = name
        self.points = np.asarray(points)
        self.kde = stats.gaussian_kde(self.points)

    def createLinearRange(self, mu, sigma, num_sigmas, n=101):
        """Makes an equally-spaced list of values.

            mu: mean
            sigma: standard deviation
            num_sigma: number of standard deviations above and below the mean
            n: number of equally spaced values
            
            Returns: list of equally spaced values between low and high, including both
        """

        low = mu - num_sigmas*sigma
        high = mu + num_sigmas*sigma

        return np.linspace(low, high, n)

    def MakePmf(self, xs, name=''):
        """Makes a discrete version of this Pdf, evaluated at xs.

        xs: equally-spaced sequence of values

        Returns: new Pmf
        """
        pmf = self.kde.evaluate(xs)
        return pmf

    def GraphPmf(self, xs):
        """Makes a discrete version of this Pdf, evaluated at xs.

            xs: equally-spaced sequence of values

            Returns: displays a graph of the PDF evaluated at xs.
        """
        pmf = self.MakePmf(xs)


        plt.scatter(xs, pmf)
        plt.xlabel("Fantasy Points")
        plt.ylabel("Probability")
        plt.title(self.name + "'s " +"Fantasy Points Probabilities")
        plt.show()


if __name__ == "__main__":
    arodgers = [23.56, 18.42, 26.40, 17.86, 13.46, 23.74, 33.84, 27.18, 29.54, 29.34, 23.12, 15.96, 21.24, 11.98, 37.18,
              34.20]
    bigben = [22.80, 21.76, 7.98, 33.90, 29.20, 11.56, 19.86, 28.42, 8.68, 20.84, 18.56, 5.60, 14.94, 21.06]
    aluck = [35.50, 11.08, 14.24, 18.66, 22.18, 24.38, 27.82, 19.40, 14.74, 19.68, 29.72, 18.24, 18.80, 26.72, 19.54]
    ezekiel = [12.20, 14.70, 18.00, 22.70, 32.10, 19.40, 18.80, 22.70, 40.90, 16.70, 26.00, 20.50, 10.70, 27.80, 22.20]
    abrown = [32.60, 7.90, 26.00, 22.40, 22.80, 8.50, 18.90, 21.50, 34.40, 15.60, 32.10, 17.40, 12.80, 8.80, 25.60]
    gronk = [2.10, 15.90, 29.20, 19.30, 21.90, 8.60]

    players = [arodgers, bigben, aluck, ezekiel, abrown, gronk]
    for player in players:
        eppp = EstimatePlayerPointsPdf(player, "big ben")
        low, high = 0, 50
        n = 50
        xs = np.linspace(low, high, n)
        eppp.GraphPmf(xs)

    '''
    kernel = stats.gaussian_kde(arodgers)
    low, high = 0, 50
    n = 101
    xs = np.linspace(low, high, n)
    kernel.evaluate(xs)
    pdf = kernel.pdf(xs)
    print(pdf)
    '''
    '''
    #pdf = EstimatedPdf(values)
    pdf = EstimatedPdf(arodgers)
    
    low, high = 0, 4
    
    
    pmf = pdf.MakePmf(xs)
    pmf.Print()
    '''
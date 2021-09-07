import scipy.stats
import numpy as np
import scipy.optimize
import math

class MEASUREMENTS:
    def __init__(self, data):
        self.length = len(data)
        self.min = min(data)
        self.max = max(data)
        self.mean = np.mean(data)
        self.variance = np.var(data, ddof=1)
        self.std = math.sqrt(np.var(data, ddof=1))
        self.skewness = scipy.stats.moment(data, 3) / pow(np.std(data, ddof=1),3)
        self.kurtosis = scipy.stats.moment(data, 4) / pow(np.std(data, ddof=1),4)
        self.median = np.median(data)
        self.mode = self.calculate_mode(data)
        self.data = data
        self.num_bins = self.danoes_formula()

    def calculate_mode(self, data):
        def calc_fmin_mode(data, distribution):
            objective = lambda x: -distribution.pdf(x)[0]
            solution = scipy.optimize.fmin(objective, self.mean, disp=False)
            return solution[0]
        
        ## KDE
        distribution = scipy.stats.gaussian_kde(data)
        mode = calc_fmin_mode(data, distribution)
        return(mode)

    def danoes_formula(self):
        """
        DANOE'S FORMULA
        https://en.wikipedia.org/wiki/Histogram#Doane's_formula
        
        Parameters
        ----------
        data : iterable 
            data set
        Returns
        -------
        num_bins : int
            Cumulative distribution function evaluated at x
        """
        N = self.length
        skewness = scipy.stats.skew(data)
        sigma_g1 = math.sqrt((6*(N-2))/((N+1)*(N+3)))
        num_bins = 1 + math.log(N,2) + math.log(1+abs(skewness)/sigma_g1,2)
        num_bins = round(num_bins)
        return num_bins

if __name__ == "__main__":
    ## Import function to get measurements
    def get_data(direction):
        file  = open(direction,'r')
        data = [float(x.replace(",",".")) for x in file.read().splitlines()]
        return data
    
    ## Distribution class
    path = "./data/data_normal.txt"
    data = get_data(path) 

    measurements = MEASUREMENTS(data)
    print(measurements.max-measurements.min)

    print("Length: ", measurements.length)
    print("Min: ", measurements.min)
    print("Max: ", measurements.max)
    print("Mean: ", measurements.mean)
    print("Variance: ", measurements.variance)
    print("Skewness: ", measurements.skewness)
    print("Kurtosis: ", measurements.kurtosis)
    print("Median: ", measurements.median)
    print("Mode: ", measurements.mode)
    print("num_bins: ", measurements.num_bins)